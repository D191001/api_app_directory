from typing import List, Optional

from pydantic import BaseModel


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
