from typing import List, Optional, Tuple

from pydantic import BaseModel, Field, validator


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int

    class Config:
        from_attributes = True


class BuildingBase(BaseModel):
    address: str


class BuildingCreate(BaseModel):
    address: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class Building(BuildingBase):
    id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


class BuildingWithRelations(Building):
    organizations: List['OrganizationWithoutBuilding'] = []


class BuildingWithDistance(BuildingBase):
    id: int
    latitude: float
    longitude: float
    distance: float  # расстояние в километрах

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    name: str
    phone_numbers: Optional[str] = None
    building_id: int


class OrganizationCreate(OrganizationBase):
    pass


class ActivityWithRelations(Activity):
    organizations: List['OrganizationWithoutActivities'] = []


class OrganizationWithRelations(OrganizationBase):
    id: int
    activities: List[Activity] = []
    building: Building

    class Config:
        from_attributes = True


class OrganizationWithoutActivities(OrganizationBase):
    id: int
    building: Building

    class Config:
        from_attributes = True


class OrganizationWithoutBuilding(OrganizationBase):
    id: int
    activities: List[Activity] = []

    class Config:
        from_attributes = True


class OrganizationSearch(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius: Optional[float] = Field(None, gt=0)
    activity_name: Optional[str] = Field(None, min_length=1)
