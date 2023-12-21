from datetime import datetime, timedelta

from tests.factories.categories import CategoryFactory
from tests.factories.category_items import CategoryItemFactory
from tests.factories.records import RecordFactory


def test_dashboard_stats_endpoint_multiple_everything(client, db):
    category1 = CategoryFactory()
    category2 = CategoryFactory()
    category3 = CategoryFactory()
    category4 = CategoryFactory()
    category5 = CategoryFactory()
    category6 = CategoryFactory()

    category1_category_item = CategoryItemFactory(category=category1)
    category2_category_item = CategoryItemFactory(category=category2)
    category3_category_item = CategoryItemFactory(category=category3)
    category4_category_item = CategoryItemFactory(category=category4)
    category5_category_item = CategoryItemFactory(category=category5)
    category6_category_item = CategoryItemFactory(category=category6)

    category1_category_item_record = RecordFactory(category_item=category1_category_item)
    category2_category_item_record = RecordFactory(category_item=category2_category_item)
    category3_category_item_record = RecordFactory(category_item=category3_category_item)
    category4_category_item_record = RecordFactory(category_item=category4_category_item)
    category5_category_item_record = RecordFactory(category_item=category5_category_item)
    RecordFactory(category_item=category6_category_item)

    yesterday = datetime.utcnow() - timedelta(days=1)
    category7 = CategoryFactory()
    category7_category_item = CategoryItemFactory(category=category7)
    category7_category_item_records = [
        RecordFactory(category_item=category7_category_item, created=yesterday),
        RecordFactory(category_item=category7_category_item, created=yesterday),
        RecordFactory(category_item=category7_category_item, created=yesterday),
    ]
    r = client.get("/dashboard")
    assert r.status_code == 200

    response = {
        "stats": {
            "today": [
                {
                    "id": str(category1.id),
                    "name": category1.name,
                    "category_items": [
                        {
                            "id": str(category1_category_item.id),
                            "name": category1_category_item.name,
                            "records_value_sum": str(category1_category_item_record.value),
                        },
                    ],
                },
                {
                    "id": str(category2.id),
                    "name": category2.name,
                    "category_items": [
                        {
                            "id": str(category2_category_item.id),
                            "name": category2_category_item.name,
                            "records_value_sum": str(category2_category_item_record.value),
                        },
                    ],
                },
                {
                    "id": str(category3.id),
                    "name": category3.name,
                    "category_items": [
                        {
                            "id": str(category3_category_item.id),
                            "name": category3_category_item.name,
                            "records_value_sum": str(category3_category_item_record.value),
                        },
                    ],
                },
                {
                    "id": str(category4.id),
                    "name": category4.name,
                    "category_items": [
                        {
                            "id": str(category4_category_item.id),
                            "name": category4_category_item.name,
                            "records_value_sum": str(category4_category_item_record.value),
                        },
                    ],
                },
                {
                    "id": str(category5.id),
                    "name": category5.name,
                    "category_items": [
                        {
                            "id": str(category5_category_item.id),
                            "name": category5_category_item.name,
                            "records_value_sum": str(category5_category_item_record.value),
                        },
                    ],
                },
            ],
            "yesterday": [
                {
                    "id": str(category7.id),
                    "name": category7.name,
                    "category_items": [
                        {
                            "id": str(category7_category_item.id),
                            "name": category7_category_item.name,
                            "records_value_sum": str(sum(record.value for record in category7_category_item_records)),
                        },
                    ],
                },
            ],
        }
    }
    response["stats"]["all_time"] = response["stats"]["today"]
    assert r.json() == response


def test_dashboard_stats_endpoint_multiple_everything_with_nsfw(client, db):
    category1 = CategoryFactory(nsfw=True)
    category1_category_item = CategoryItemFactory(category=category1)
    category1_category_item_today_record = RecordFactory(category_item=category1_category_item)
    category1_category_item_yesterday_record = RecordFactory(
        created=datetime.now() - timedelta(days=1), category_item=category1_category_item
    )
    category2 = CategoryFactory(nsfw=True)
    category2_category_item = CategoryItemFactory(category=category2)
    category2_category_item_yesterday_record = RecordFactory(
        created=datetime.now() - timedelta(days=1), category_item=category2_category_item
    )
    category3 = CategoryFactory(nsfw=False)
    category3_category_item = CategoryItemFactory(category=category3)
    category3_category_item_yesterday_record = RecordFactory(
        created=datetime.now() - timedelta(days=1), category_item=category3_category_item
    )
    r = client.get("/dashboard?nsfw=false")
    assert r.status_code == 200
    assert r.json() == {
        "stats": {
            "today": [],
            "yesterday": [
                {
                    "id": str(category3.id),
                    "name": category3.name,
                    "category_items": [
                        {
                            "id": str(category3_category_item.id),
                            "name": category3_category_item.name,
                            "records_value_sum": str(category3_category_item_yesterday_record.value),
                        }
                    ],
                },
            ],
            "all_time": [
                {
                    "id": str(category3.id),
                    "name": category3.name,
                    "category_items": [
                        {
                            "id": str(category3_category_item.id),
                            "name": category3_category_item.name,
                            "records_value_sum": str(category3_category_item_yesterday_record.value),
                        }
                    ],
                },
            ],
        }
    }

    r = client.get("/dashboard?nsfw=true")
    assert r.status_code == 200
    assert r.json() == {
        "stats": {
            "today": [
                {
                    "id": str(category1.id),
                    "name": category1.name,
                    "category_items": [
                        {
                            "id": str(category1_category_item.id),
                            "name": category1_category_item.name,
                            "records_value_sum": str(category1_category_item_today_record.value),
                        }
                    ],
                }
            ],
            "yesterday": [
                {
                    "id": str(category1.id),
                    "name": category1.name,
                    "category_items": [
                        {
                            "id": str(category1_category_item.id),
                            "name": category1_category_item.name,
                            "records_value_sum": str(category1_category_item_yesterday_record.value),
                        }
                    ],
                },
                {
                    "id": str(category2.id),
                    "name": category2.name,
                    "category_items": [
                        {
                            "id": str(category2_category_item.id),
                            "name": category2_category_item.name,
                            "records_value_sum": str(category2_category_item_yesterday_record.value),
                        }
                    ],
                },
                {
                    "id": str(category3.id),
                    "name": category3.name,
                    "category_items": [
                        {
                            "id": str(category3_category_item.id),
                            "name": category3_category_item.name,
                            "records_value_sum": str(category3_category_item_yesterday_record.value),
                        }
                    ],
                },
            ],
            "all_time": [
                {
                    "id": str(category1.id),
                    "name": category1.name,
                    "category_items": [
                        {
                            "id": str(category1_category_item.id),
                            "name": category1_category_item.name,
                            "records_value_sum": str(
                                category1_category_item_today_record.value
                                + category1_category_item_yesterday_record.value
                            ),
                        }
                    ],
                },
                {
                    "id": str(category2.id),
                    "name": category2.name,
                    "category_items": [
                        {
                            "id": str(category2_category_item.id),
                            "name": category2_category_item.name,
                            "records_value_sum": str(category2_category_item_yesterday_record.value),
                        }
                    ],
                },
                {
                    "id": str(category3.id),
                    "name": category3.name,
                    "category_items": [
                        {
                            "id": str(category3_category_item.id),
                            "name": category3_category_item.name,
                            "records_value_sum": str(category3_category_item_yesterday_record.value),
                        }
                    ],
                },
            ],
        }
    }
