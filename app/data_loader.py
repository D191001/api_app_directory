import traceback

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Activity, Building, Organization


def create_activities(db: Session):
    main_activities = {
        "Финансовые услуги": Activity(name="Финансовые услуги"),
        "Торговля": Activity(name="Торговля"),
        "Развлечения": Activity(name="Развлечения"),
        "Бизнес": Activity(name="Бизнес"),
    }
    for activity in main_activities.values():
        db.add(activity)
    db.commit()

    sub_activities = {
        "Финансовые услуги": [
            "Микрофинансовые организации",
            "Потребительское кредитование",
            "Займы до зарплаты",
        ],
        "Торговля": ["Торговые центры", "Продуктовые магазины", "Бутики"],
        "Развлечения": ["Кинотеатры", "Рестораны", "Кафе"],
        "Бизнес": ["Бизнес-центры", "Коворкинги", "Офисы"],
    }

    activity_map = {}
    for main_name, sub_list in sub_activities.items():
        main_activity = db.query(Activity).filter_by(name=main_name).first()
        activity_map[main_name] = main_activity.id

        for sub_name in sub_list:
            sub_activity = Activity(name=sub_name, parent_id=main_activity.id)
            db.add(sub_activity)
            db.flush()
            activity_map[sub_name] = sub_activity.id
    db.commit()
    return activity_map


def create_buildings_and_organizations(db: Session, test_data, activity_map):
    for location in test_data:
        # В PostGIS для ST_MakePoint первым идет longitude (X), затем latitude (Y)
        building = Building(
            address=location["address"],
            location=func.ST_SetSRID(
                func.ST_MakePoint(
                    location["coords"][1],  # longitude (X)
                    location["coords"][0],  # latitude (Y)
                ),
                4326,
            ),
        )
        db.add(building)
        db.flush()

        for org_name, activity_type, phone in location["organizations"]:
            org = Organization(
                name=org_name, phone_numbers=phone, building_id=building.id
            )
            if activity_type in activity_map:
                activity = db.query(Activity).get(activity_map[activity_type])
                if activity:
                    org.activities.append(activity)
            db.add(org)
    db.commit()


def load_test_data(db: Session):
    if db.query(Organization).first():
        print("Data already exists. Skipping...")
        return

    try:
        activity_map = create_activities(db)

        # Объединяем тестовые данные с данными МФО
        test_data = [
            # Москва, Центр
            {
                "address": "ул. Тверская, 22",
                "coords": (55.7648, 37.6059),
                "organizations": [
                    (
                        "МигКредит",
                        "Микрофинансовые организации",
                        "+7 (495) 545-45-45",
                    ),
                    (
                        "Быстроденьги",
                        "Займы до зарплаты",
                        "+7 (495) 647-65-65",
                    ),
                ],
            },
            # Екатеринбург, Центр
            {
                "address": "ул. Ленина, 50",
                "coords": (56.8386, 60.5950),
                "organizations": [
                    (
                        "ДоброЗайм",
                        "Потребительское кредитование",
                        "+7 (343) 311-21-21",
                    ),
                    (
                        "МФО Центр",
                        "Микрофинансовые организации",
                        "+7 (343) 311-22-22",
                    ),
                ],
            },
            # Екатеринбург, ТЦ Гринвич
            {
                "address": "ул. 8 Марта, 46",
                "coords": (56.8304, 60.5951),
                "organizations": [
                    (
                        "Деньги Сразу",
                        "Займы до зарплаты",
                        "+7 (343) 222-72-22",
                    ),
                    (
                        "Быстрые Займы",
                        "Микрофинансовые организации",
                        "+7 (343) 222-72-23",
                    ),
                ],
            },
        ]

        create_buildings_and_organizations(db, test_data, activity_map)
        print("Test data loaded successfully!")
    except Exception as e:
        print(f"Error loading test data: {e}")
        traceback.print_exc()
        db.rollback()


def load_mfo_data(db: Session):
    if db.query(Organization).first():
        print("Data already exists. Skipping...")
        return

    try:
        activity_map = create_activities(db)

        # Данные МФО по городам России
        mfo_data = [
            # Москва
            {
                "address": "ул. Тверская, 22",
                "coords": (55.7648, 37.6059),
                "organizations": [
                    (
                        "МигКредит",
                        "Микрофинансовые организации",
                        "+7 (495) 545-45-45",
                    ),
                    (
                        "Быстроденьги",
                        "Займы до зарплаты",
                        "+7 (495) 647-65-65",
                    ),
                ],
            },
            {
                "address": "пр. Мира, 119",
                "coords": (55.8321, 37.6297),
                "organizations": [
                    (
                        "MoneyMan",
                        "Микрофинансовые организации",
                        "+7 (495) 981-91-91",
                    ),
                ],
            },
            # Санкт-Петербург
            {
                "address": "Невский проспект, 100",
                "coords": (59.9311, 30.3795),
                "organizations": [
                    (
                        "Деньги Сразу",
                        "Займы до зарплаты",
                        "+7 (812) 309-38-38",
                    ),
                    (
                        "Е капуста",
                        "Микрофинансовые организации",
                        "+7 (812) 425-31-31",
                    ),
                ],
            },
            # Екатеринбург
            {
                "address": "ул. Ленина, 50",
                "coords": (56.8386, 60.5950),
                "organizations": [
                    (
                        "ДоброЗайм",
                        "Потребительское кредитование",
                        "+7 (343) 311-21-21",
                    ),
                ],
            },
            # Новосибирск
            {
                "address": "Красный проспект, 65",
                "coords": (55.0415, 82.9346),
                "organizations": [
                    (
                        "Займер",
                        "Микрофинансовые организации",
                        "+7 (383) 207-98-89",
                    ),
                ],
            },
        ]

        create_buildings_and_organizations(db, mfo_data, activity_map)
        print("MFO data loaded successfully!")
    except Exception as e:
        print(f"Error loading MFO data: {e}")
        db.rollback()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        load_test_data(db)
        load_mfo_data(db)
    finally:
        db.close()
