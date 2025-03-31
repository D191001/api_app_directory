import math
from typing import List, Optional

from geoalchemy2.functions import (
    ST_Distance,
    ST_DWithin,
    ST_MakePoint,
    ST_SetSRID,
    ST_Transform,
)
from sqlalchemy import func, or_
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


def get_buildings_in_radius(
    db: Session,
    latitude: float,
    longitude: float,
    radius: float,
    limit: int = 10,
) -> List[models.Building]:
    try:
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
        radius_meters = radius * 1000

        return (
            db.query(models.Building)
            .filter(
                func.ST_DWithin(
                    func.Geography(models.Building.location),
                    func.Geography(point),
                    radius_meters,
                )
            )
            .order_by(
                func.ST_Distance(
                    func.Geography(models.Building.location),
                    func.Geography(point),
                )
            )
            .limit(limit)
            .all()
        )
    except Exception as e:
        print(f"Error in get_buildings_in_radius: {e}")
        return []


def get_nearest_buildings(
    db: Session, latitude: float, longitude: float, limit: int = 5
) -> List[tuple[models.Building, float]]:
    try:
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)

        query = (
            db.query(
                models.Building,
                func.ST_Distance(
                    func.Geography(models.Building.location),
                    func.Geography(point),
                ).label('distance'),
            )
            .order_by('distance')
            .limit(limit)
        )

        results = query.all()
        return [
            (building, float(distance) / 1000)
            for building, distance in results
        ]
    except Exception as e:
        print(f"Error in get_nearest_buildings: {e}")
        return []


def get_buildings_in_bounds(
    db: Session, min_lat: float, max_lat: float, min_lon: float, max_lon: float
) -> List[models.Building]:
    try:
        if min_lat > max_lat or min_lon > max_lon:
            print("Invalid bounds: min values greater than max values")
            return []

        bounds_wkt = f'SRID=4326;POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, {max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))'
        search_area = func.ST_GeomFromEWKT(bounds_wkt)

        print(
            f"Searching in bounds: lat [{min_lat}, {max_lat}], lon [{min_lon}, {max_lon}]"
        )

        buildings = (
            db.query(models.Building)
            .filter(func.ST_Within(models.Building.location, search_area))
            .all()
        )

        print(f"Found {len(buildings)} buildings")
        for building in buildings:
            print(
                f"Building at: {building.address} ({building.latitude}, {building.longitude})"
            )

        return buildings

    except Exception as e:
        print(f"Error in get_buildings_in_bounds: {e}")
        return []


def create_building(db: Session, building: schemas.BuildingCreate):
    location = func.ST_SetSRID(
        func.ST_MakePoint(building.longitude, building.latitude), 4326
    )
    db_building = models.Building(address=building.address, location=location)
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
    try:
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
        radius_meters = radius * 1000

        return (
            db.query(models.Organization)
            .join(models.Building)
            .filter(
                func.ST_DWithin(
                    func.Geography(models.Building.location),
                    func.Geography(point),
                    radius_meters,
                )
            )
            .order_by(
                func.ST_Distance(
                    func.Geography(models.Building.location),
                    func.Geography(point),
                )
            )
            .all()
        )
    except Exception as e:
        print(f"Error in get_organizations_by_coordinates: {e}")
        return []


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
    activity = (
        db.query(models.Activity)
        .filter(models.Activity.name.ilike(f"%{activity_name}%"))
        .first()
    )

    if not activity:
        return []

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

    return (
        db.query(models.Organization)
        .filter(
            models.Organization.activities.any(
                models.Activity.id.in_(child_activities)
            )
        )
        .all()
    )
