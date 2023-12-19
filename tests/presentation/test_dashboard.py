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
                    "name": category1.name,
                    "category_items": [
                        {
                            "name": category1_category_item.name,
                            "records_value_sum": category1_category_item_record.value,
                        },
                    ],
                },
                {
                    "name": category2.name,
                    "category_items": [
                        {
                            "name": category2_category_item.name,
                            "records_value_sum": category2_category_item_record.value,
                        },
                    ],
                },
                {
                    "name": category3.name,
                    "category_items": [
                        {
                            "name": category3_category_item.name,
                            "records_value_sum": category3_category_item_record.value,
                        },
                    ],
                },
                {
                    "name": category4.name,
                    "category_items": [
                        {
                            "name": category4_category_item.name,
                            "records_value_sum": category4_category_item_record.value,
                        },
                    ],
                },
                {
                    "name": category5.name,
                    "category_items": [
                        {
                            "name": category5_category_item.name,
                            "records_value_sum": category5_category_item_record.value,
                        },
                    ],
                },
            ],
            "yesterday": [
                {
                    "name": category7.name,
                    "category_items": [
                        {
                            "name": category7_category_item.name,
                            "records_value_sum": sum(record.value for record in category7_category_item_records),
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
                    "name": category3.name,
                    "category_items": [
                        {
                            "name": category3_category_item.name,
                            "records_value_sum": category3_category_item_yesterday_record.value,
                        }
                    ],
                },
            ],
            "all_time": [
                {
                    "name": category3.name,
                    "category_items": [
                        {
                            "name": category3_category_item.name,
                            "records_value_sum": category3_category_item_yesterday_record.value,
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
                    "name": category1.name,
                    "category_items": [
                        {
                            "name": category1_category_item.name,
                            "records_value_sum": category1_category_item_today_record.value,
                        }
                    ],
                }
            ],
            "yesterday": [
                {
                    "name": category1.name,
                    "category_items": [
                        {
                            "name": category1_category_item.name,
                            "records_value_sum": category1_category_item_yesterday_record.value,
                        }
                    ],
                },
                {
                    "name": category2.name,
                    "category_items": [
                        {
                            "name": category2_category_item.name,
                            "records_value_sum": category2_category_item_yesterday_record.value,
                        }
                    ],
                },
                {
                    "name": category3.name,
                    "category_items": [
                        {
                            "name": category3_category_item.name,
                            "records_value_sum": category3_category_item_yesterday_record.value,
                        }
                    ],
                },
            ],
            "all_time": [
                {
                    "name": category1.name,
                    "category_items": [
                        {
                            "name": category1_category_item.name,
                            "records_value_sum": (
                                category1_category_item_today_record.value
                                + category1_category_item_yesterday_record.value
                            ),
                        }
                    ],
                },
                {
                    "name": category2.name,
                    "category_items": [
                        {
                            "name": category2_category_item.name,
                            "records_value_sum": category2_category_item_yesterday_record.value,
                        }
                    ],
                },
                {
                    "name": category3.name,
                    "category_items": [
                        {
                            "name": category3_category_item.name,
                            "records_value_sum": category3_category_item_yesterday_record.value,
                        }
                    ],
                },
            ],
        }
    }
