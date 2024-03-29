from datetime import datetime, timedelta

import pytz

from dusa_backend.domain.categories.repository import CategoryRepository
from dusa_backend.domain.category_items.repository import CategoryItemRepository
from dusa_backend.domain.records.repository import RecordRepository
from dusa_backend.infrastructure.database.session import SessionLocal
from dusa_backend.infrastructure.database.tables import RecordTable


NSW_TZ = "Australia/Sydney"
QLD_TZ = "Australia/Brisbane"
NZ_TZ = "Pacific/Auckland"

CORRECT_RECORD_IDS = [
    "ae214406-1be6-40a1-9ae5-04e0d1719194",
    "1b2e3037-c0a5-4b27-afba-8a58e6362bf2",
    "923c42fa-f133-4c87-a42e-b5df5492c0b5",
    "af43aa3d-ff91-454d-9835-a82bcef2f150",
    "aaf751f4-008f-4532-ba6f-05a747beb9a6",
    "eb025261-0d75-499e-ae4d-d5c9c078dac6",
    "f0d8877c-1dd8-444e-b4c7-f3088b082fd4",
    "c450f2e4-6091-4f28-8a9f-f62f4bedce3c",
    "162dcbae-2368-4cbe-b18e-198e9fb1d004",
    "14f4962b-803d-4ab9-bd21-880fcd5466d6",
    "c93c3b09-1fca-4777-8cd6-7e13016af9c2",
    "7d64370a-726f-442c-9409-63fc8c127492",
    "6f59e55d-fb26-4076-b90e-455d98e76597",
    "c18d39cc-9f1e-4b20-831a-ffd52c09e01d",
    "1d2b21a5-b4f8-40b3-9498-8defecd75f7c",
    "3c1b4806-8a63-40a4-8439-825e47bbd488",
    "5cc4ac41-df02-457b-9a13-1967bf28b94a",
    "8f1ee4a9-37d4-4924-b0fd-d87435b35641",
    "abfeb145-3374-430a-8c26-1ec030e006f6",
    "39506353-7018-439c-9c41-491651ef7190",
    "c285e165-91dc-44fe-ba04-c6766030e8d0",
    "9f959ea7-8131-4e2d-a348-79a58f3cc692",
    "ef44bbed-1904-40ed-b782-e01dd2faf3c4",
    "a716e146-dc2b-4a99-9f22-107eff7c5252",
    "ae4a538b-9c3a-48a1-9d29-ad166ef16614",
    "5b881ae3-afd1-43bc-82c6-557bad0ecb11",
    "38ab542f-3445-412e-87b1-08907f1e3f0d",
    "e7758a87-e687-4e26-b1e4-b47ec2534fc5",
    "4d88cf43-a164-4655-a3bb-de17c977db6f",
    "088e2b12-a2b1-4388-ba2c-18e8c6067a10",
    "36117810-fe39-45c5-9134-0f37b0586672",
    "a355ee93-901f-4bda-bcaf-d572fbd7b77c",
    "0944fbe0-5b2c-448e-a8aa-73cadb103140",
    "74eaa84b-f172-41cc-af53-75450eb7b609",
    "94f578ef-9525-45a0-8dec-c767a58d4dc9",
    "a6028a50-f739-451f-a684-d87daefd9931",
    "bc9a32b2-9ac8-43c3-a5d2-c8f285c50250",
    "ae8d9f60-b5ab-439d-a114-9b5d58ede669",
    "b56bac03-4427-45bc-8a6b-d94c7c9f91ea",
    "e3ba19cf-e662-477f-8394-c8affeeecec4",
    "b2e89639-f9a3-4ce0-963b-fc4946c835e5",
    "76660282-a82b-4d7c-987a-83ae881702f8",
    "0aac59db-55e2-4d21-b36f-6316a254e7f5",
    "b6977878-04de-4936-95a2-bf577969e361",
    "e29bd6fc-d4f3-4a99-92ce-7bca33567a51",
    "6e47cd9b-50e3-4058-9e0e-8917912cfb13",
    "6530f25e-ac3e-49a0-895d-0f1c516e9c16",
    "ccbaac28-64dc-42be-be48-409f8e5a0a75",
    "c0db5942-e327-46ac-a1b2-7a8a74c79907",
    "fc2657c2-f092-4b3f-9c5e-bf3af7b5b037",
    "e79cb9c7-43c5-4d16-98e9-cd958175d7ce",
    "cfaa6d79-9a86-4230-a061-cef9dfc60d20",
    "371bbe32-4110-409a-b93d-e908c2b53109",
    "265303c4-fe18-4afc-bdf4-01106632e070",
    "97d3f3cf-2b50-4ec5-94cb-a70052bb179f",
    "7bc429d1-15b6-4f28-b430-4b069fa0281b",
    "bf9d43a1-34f9-45b2-a59b-86a3198cdd95",
    "77623fd1-7426-4ac0-862a-cf3e4ed3717a",
    "e61105d2-3301-4cee-9c43-0b5161e6549d",
    "a450df16-03b1-4e16-9a59-5f21451cdac5",
    "44b29482-fee9-421f-8f4d-648b20db9eb7",
    "ccfb2788-ef88-45e7-a79a-8c8e8c51c132",
    "caf79faa-d7f9-4fa4-9a54-9f4b81481c95",
    "32c8e319-254c-41d8-b743-380f7d130722",
    "6ccbf6a2-7bdb-47cf-91a1-84d954542e3f",
    "7d5712c3-ee44-4667-88e4-8fea65f1721c",
    "a98ef6cd-99e1-43da-a0b1-b7c995d1cba5",
    "676f2d32-37c1-4f16-85f3-4bd30bf53e2f",
    "d2e733a5-35d7-4ebc-970d-d5010fa8a171",
    "c2ba3ed1-b48b-465c-8a09-28db535a35fc",
    "bed3c38a-2364-4ab7-9570-4b372220be8a",
    "06e2da33-59d9-46ad-ad13-5f5a50748d1d",
    "8cedbd73-e73d-42ff-9911-fd78423fc394",
    "bef95a70-8bb7-4491-a1d1-5c594ce5b7af",
    "dad30166-8cea-4e74-a21e-356e1eb828a9",
    "872c4190-7d04-4fb9-a1d4-26fe7d86373a",
    "7cdebdb5-b70a-486e-9b4b-78555371408f",
    "ed90db53-f93c-44e6-ab96-9f39d4d85dd3",
    "282771b9-b660-435f-848e-379dc831956b",
    "35e60056-6377-4521-8978-5ae96c738514",
    "6e10c2e2-eecf-465b-b06c-0f010eddd3c2",
    "3a708f66-dc2a-4d74-96f3-db23d5e742ce",
]


def get_created_tz(created):
    tz = NSW_TZ
    if datetime(2024, 2, 4) <= created < datetime(2024, 2, 24):
        tz = QLD_TZ
    elif datetime(2024, 2, 24) <= created < datetime(2024, 2, 26):
        tz = NSW_TZ
    elif datetime(2024, 2, 26) <= created < datetime(2024, 3, 17):
        tz = NZ_TZ
    return created.astimezone(pytz.timezone(tz))


def drinks_fix_matcher():
    correct_drink_ids = []

    def print_days_purchases(records, day):
        for record in records:
            if record.created.date() == day:
                print(record.category_item.name, get_created_tz(record.created), record.value)

    with SessionLocal() as db_session:
        category_repo = CategoryRepository(db_session)
        category_item_repo = CategoryItemRepository(db_session)

        drinks_category = category_repo.get(name="Drinks")
        drinks_category_item = category_item_repo.get(name="Drinks/Nights Out")
        food_category_item = category_item_repo.get(name="Food and/or drink")
        money_spent_records = (
            db_session.query(RecordTable)
            .join(RecordTable.category_item)
            .filter(RecordTable.category_item_id.in_([drinks_category_item.id, food_category_item.id]))
            .order_by(RecordTable.created.asc())
        )
        drinks_records = (
            db_session.query(RecordTable)
            .join(RecordTable.category_item)
            .filter(RecordTable.category_item_id.in_([dc_item.id for dc_item in drinks_category.category_items]))
            .order_by(RecordTable.created.asc())
        )

        created_drinks_mapper = {}
        for dr in drinks_records:
            if dr.created.date() in created_drinks_mapper:
                created_drinks_mapper[dr.created.date()].append(dr)
            else:
                created_drinks_mapper[dr.created.date()] = [dr]

        for created_date, d_records in created_drinks_mapper.items():
            print(created_date)
            print_days_purchases(money_spent_records, created_date)
            print()
            for index, d_record in enumerate(d_records):
                print(f"({index}): ", d_record.category_item.name, get_created_tz(d_record.created))

            for index, d_record in enumerate(d_records):
                correct = input(f"Is ({index}) correct? y/n: ")
                if correct.lower() == "y":
                    correct_drink_ids.append(str(d_record.id))
            print()
            print("So far: ", correct_drink_ids)
            print("===================================================================================================")


def change_drinks_created():
    with SessionLocal() as db_session:
        record_repo = RecordRepository(db_session)
        category_repo = CategoryRepository(db_session)

        drinks_category = category_repo.get(name="Drinks")
        drinks_records = (
            db_session.query(RecordTable)
            .join(RecordTable.category_item)
            .filter(
                RecordTable.id.notin_(CORRECT_RECORD_IDS),
                RecordTable.category_item_id.in_([dc_item.id for dc_item in drinks_category.category_items]),
            )
            .order_by(RecordTable.created.asc())
        )
        for dr in drinks_records:
            assert str(dr.id) not in CORRECT_RECORD_IDS, dr.id

            dr.created = (dr.created - timedelta(days=1)).replace(hour=22, minute=0, second=0, microsecond=0)
            record_repo.update(dr)
        print(f"Updated {len(list(drinks_records))} records")
