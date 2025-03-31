from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.get("/bounds", response_model=List[schemas.BuildingWithRelations])
def get_buildings_in_bounds(
    min_lat: float = Query(
        ..., ge=-90, le=90, description="Минимальная широта"
    ),
    max_lat: float = Query(
        ..., ge=-90, le=90, description="Максимальная широта"
    ),
    min_lon: float = Query(
        ..., ge=-180, le=180, description="Минимальная долгота"
    ),
    max_lon: float = Query(
        ..., ge=-180, le=180, description="Максимальная долгота"
    ),
    db: Session = Depends(get_db),
):
    """Получение зданий в заданных географических границах"""
    return crud.get_buildings_in_bounds(db, min_lat, max_lat, min_lon, max_lon)


@router.get("/nearest", response_model=List[schemas.BuildingWithDistance])
def get_nearest_buildings(
    latitude: float = Query(..., ge=-90, le=90, description="Широта"),
    longitude: float = Query(..., ge=-180, le=180, description="Долгота"),
    limit: int = Query(5, ge=1, le=50, description="Количество результатов"),
    db: Session = Depends(get_db),
):
    """Получение ближайших зданий с расстоянием"""
    buildings_with_distance = crud.get_nearest_buildings(
        db, latitude, longitude, limit
    )
    return [
        schemas.BuildingWithDistance(
            id=building.id,
            address=building.address,
            latitude=building.latitude,
            longitude=building.longitude,
            distance=distance,
        )
        for building, distance in buildings_with_distance
    ]


@router.get(
    "/search/radius", response_model=List[schemas.BuildingWithRelations]
)
def search_buildings_in_radius(
    latitude: float = Query(..., ge=-90, le=90, description="Широта"),
    longitude: float = Query(..., ge=-180, le=180, description="Долгота"),
    radius: float = Query(..., gt=0, description="Радиус поиска в километрах"),
    limit: int = Query(
        10, ge=1, le=100, description="Максимальное количество результатов"
    ),
    db: Session = Depends(get_db),
):
    """Поиск зданий в радиусе от точки"""
    print(
        f"Received search request: lat={latitude}, lon={longitude}, radius={radius}km"
    )

    # Проверяем работу PostGIS
    test_query = "SELECT PostGIS_Version(), PostGIS_Full_Version();"
    result = db.execute(text(test_query)).first()
    print(f"PostGIS version: {result[0]}")

    return crud.get_buildings_in_radius(db, latitude, longitude, radius, limit)


@router.get("/{building_id}", response_model=schemas.BuildingWithRelations)
def read_building(building_id: int, db: Session = Depends(get_db)):
    building = crud.get_building(db, building_id)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.get("/", response_model=List[schemas.BuildingWithRelations])
def read_buildings(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    buildings = crud.get_buildings(db, skip=skip, limit=limit)
    return buildings


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
