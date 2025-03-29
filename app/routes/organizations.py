from typing import List

from fastapi import APIRouter, Depends, HTTPException
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
