from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.BuildingWithRelations])
def read_buildings(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    buildings = crud.get_buildings(db, skip=skip, limit=limit)
    return buildings


@router.get("/{building_id}", response_model=schemas.BuildingWithRelations)
def read_building(building_id: int, db: Session = Depends(get_db)):
    building = crud.get_building(db, building_id)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.get(
    "/{building_id}/organizations",
    response_model=List[schemas.OrganizationWithRelations],
)
def read_building_organizations(
    building_id: int, db: Session = Depends(get_db)
):
    building = crud.get_building(db, building_id)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return crud.get_organizations_by_building(db, building_id)


@router.post("/", response_model=schemas.BuildingWithRelations)
def create_building(
    building: schemas.BuildingCreate, db: Session = Depends(get_db)
):
    return crud.create_building(db, building)
