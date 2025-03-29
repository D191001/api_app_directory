from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import Base

organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        primary_key=True,
    ),
    Column(
        "activity_id", Integer, ForeignKey("activities.id"), primary_key=True
    ),
)


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_numbers = Column(String)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    activities = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations",
    )
    building = relationship("Building", back_populates="organizations")

    def to_schema(self):
        from app.schemas import OrganizationWithRelations

        return OrganizationWithRelations(
            id=self.id,
            name=self.name,
            phone_numbers=self.phone_numbers,
            building_id=self.building_id,
            activities=self.activities,
            building=self.building,
        )


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    organizations = relationship("Organization", back_populates="building")

    def to_schema(self):
        from app.schemas import BuildingWithRelations

        return BuildingWithRelations(
            id=self.id,
            address=self.address,
            latitude=self.latitude,
            longitude=self.longitude,
            organizations=self.organizations,
        )


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"))
    organizations = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities",
    )

    def to_schema(self):
        from app.schemas import ActivityWithRelations

        return ActivityWithRelations(
            id=self.id,
            name=self.name,
            parent_id=self.parent_id,
            organizations=self.organizations,
        )
