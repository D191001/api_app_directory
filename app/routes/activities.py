from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Activity])
def read_activities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    activities = crud.get_activities(db, skip=skip, limit=limit)
    return activities


@router.get("/{activity_id}", response_model=schemas.ActivityWithRelations)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = crud.get_activity(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.get(
    "/{activity_id}/organizations",
    response_model=List[schemas.OrganizationWithoutActivities],
)
def read_activity_organizations(
    activity_id: int, db: Session = Depends(get_db)
):
    activity = crud.get_activity(db, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity.organizations


@router.post("/", response_model=schemas.Activity)
def create_activity(
    activity: schemas.ActivityCreate, db: Session = Depends(get_db)
):
    return crud.create_activity(db, activity)
