from typing import List, Optional

from pydantic import BaseModel, Field


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
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int

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


class BuildingWithRelations(Building):
    organizations: List['OrganizationWithoutBuilding'] = []


class OrganizationWithRelations(OrganizationBase):
    id: int
    activities: List[Activity] = []
    building: Building


class OrganizationWithoutActivities(OrganizationBase):
    id: int
    building: Building


class OrganizationWithoutBuilding(OrganizationBase):
    id: int
    activities: List[Activity] = []


class OrganizationSearch(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius: Optional[float] = Field(None, gt=0)
    activity_name: Optional[str] = Field(None, min_length=1)
