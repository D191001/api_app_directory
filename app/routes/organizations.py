from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.OrganizationWithRelations])
def read_organizations(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    organizations = crud.get_organizations(db, skip=skip, limit=limit)
    return organizations


@router.get("/search", response_model=List[schemas.OrganizationWithRelations])
def search_organizations(
    name: Optional[str] = Query(None, description="Название организации"),
    latitude: Optional[float] = Query(
        None, ge=-90, le=90, description="Широта"
    ),
    longitude: Optional[float] = Query(
        None, ge=-180, le=180, description="Долгота"
    ),
    radius: Optional[float] = Query(
        None, gt=0, description="Радиус поиска в км"
    ),
    activity_name: Optional[str] = Query(
        None, description="Название вида деятельности"
    ),
    db: Session = Depends(get_db),
):
    if name:
        return crud.get_organizations_by_name(db, name)
    if all(v is not None for v in [latitude, longitude, radius]):
        return crud.get_organizations_by_coordinates(
            db, latitude, longitude, radius
        )
    if activity_name:
        return crud.get_organizations_by_activity(db, activity_name)
    raise HTTPException(
        status_code=400,
        detail="Укажите параметры поиска: name, coordinates (latitude+longitude+radius), или activity_name",
    )


@router.get(
    "/{organization_id}", response_model=schemas.OrganizationWithRelations
)
def read_organization(organization_id: int, db: Session = Depends(get_db)):
    organization = crud.get_organization(db, organization_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.post("/", response_model=schemas.OrganizationWithRelations)
def create_organization(
    organization: schemas.OrganizationCreate, db: Session = Depends(get_db)
):
    return crud.create_organization(db, organization)
