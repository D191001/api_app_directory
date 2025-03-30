import math
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from app import models, schemas


def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Activity).offset(skip).limit(limit).all()


def get_activity(db: Session, activity_id: int):
    return (
        db.query(models.Activity)
        .filter(models.Activity.id == activity_id)
        .first()
    )


def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


def get_buildings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Building).offset(skip).limit(limit).all()


def get_building(db: Session, building_id: int):
    return (
        db.query(models.Building)
        .filter(models.Building.id == building_id)
        .first()
    )


def create_building(db: Session, building: schemas.BuildingCreate):
    db_building = models.Building(**building.model_dump())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organization).offset(skip).limit(limit).all()


def get_organization(db: Session, organization_id: int):
    return (
        db.query(models.Organization)
        .filter(models.Organization.id == organization_id)
        .first()
    )


def create_organization(db: Session, organization: schemas.OrganizationCreate):
    db_organization = models.Organization(**organization.model_dump())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization


def get_organizations_by_building(db: Session, building_id: int):
    return (
        db.query(models.Organization)
        .filter(models.Organization.building_id == building_id)
        .all()
    )


def get_organizations_by_coordinates(
    db: Session, latitude: float, longitude: float, radius: float
) -> List[models.Organization]:
    if any(v is None for v in [latitude, longitude, radius]) or radius <= 0:
        return []

    # Используем формулу гаверсинусов для поиска в радиусе
    organizations = (
        db.query(models.Organization)
        .join(models.Building)
        .filter(
            func.acos(
                func.sin(func.radians(latitude))
                * func.sin(func.radians(models.Building.latitude))
                + func.cos(func.radians(latitude))
                * func.cos(func.radians(models.Building.latitude))
                * func.cos(func.radians(models.Building.longitude - longitude))
            )
            * 6371
            <= radius  # 6371 - радиус Земли в км
        )
        .all()
    )
    return organizations


def get_organizations_by_name(
    db: Session, name: str
) -> List[models.Organization]:
    if not name:
        return []
    return (
        db.query(models.Organization)
        .filter(models.Organization.name.ilike(f"%{name}%"))
        .all()
    )


def get_organizations_by_activity(db: Session, activity_name: str):
    # Получаем активность по имени
    activity = (
        db.query(models.Activity)
        .filter(models.Activity.name.ilike(f"%{activity_name}%"))
        .first()
    )

    if not activity:
        return []

    # Получаем все дочерние активности (до 3 уровня)
    child_activities = set()

    def add_children(parent_id, level=0):
        if level >= 3:
            return
        children = (
            db.query(models.Activity)
            .filter(models.Activity.parent_id == parent_id)
            .all()
        )
        for child in children:
            child_activities.add(child.id)
            add_children(child.id, level + 1)

    child_activities.add(activity.id)
    add_children(activity.id)

    # Получаем все организации с найденными активностями
    return (
        db.query(models.Organization)
        .filter(
            models.Organization.activities.any(
                models.Activity.id.in_(child_activities)
            )
        )
        .all()
    )
