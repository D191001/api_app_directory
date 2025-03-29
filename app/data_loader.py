from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Activity, Building, Organization


def load_test_data(db: Session):
    if db.query(Organization).first():
        print("Data already exists. Skipping...")
        return

    try:
        building1 = Building(
            address="123 Main St", latitude=40.7128, longitude=-74.0060
        )
        building2 = Building(
            address="456 Elm St", latitude=34.0522, longitude=-118.2437
        )
        db.add_all([building1, building2])
        db.commit()

        activity1 = Activity(name="IT Services")
        activity2 = Activity(name="Consulting")
        activity3 = Activity(
            name="Software Development", parent_id=activity1.id
        )
        db.add_all([activity1, activity2])
        db.commit()
        db.add(
            activity3
        db.commit()

        organization1 = Organization(
            name="Tech Corp",
            phone_numbers="123-456-7890",
            building_id=building1.id,
            activities=[activity1, activity3],
        )
        organization2 = Organization(
            name="Consulting Group",
            phone_numbers="987-654-3210",
            building_id=building2.id,
            activities=[activity2],
        )
        db.add_all([organization1, organization2])
        db.commit()

        print("Test data loaded successfully!")
    except Exception as e:
        print(f"Error loading test data: {e}")
        db.rollback()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        load_test_data(db)
    finally:
        db.close()
