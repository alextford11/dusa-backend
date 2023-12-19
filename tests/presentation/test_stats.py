from datetime import datetime, timedelta

from src.dusa_backend.domain.models import Category
from tests.factories.categories import CategoryFactory
from tests.factories.category_items import CategoryItemFactory
from tests.factories.records import RecordFactory


def test_stats_endpoint_single_record(client, db):
    record = RecordFactory()
    r = client.get("/stats")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": record.category_item.category.name,
                "category_items": [{"name": record.category_item.name, "records_value_sum": record.value}],
            }
        ]
    }


def test_stats_endpoint_multiple_records(client, db):
    category_item = CategoryItemFactory()
    records = [
        RecordFactory(category_item=category_item),
        RecordFactory(category_item=category_item),
        RecordFactory(category_item=category_item),
    ]
    r = client.get("/stats")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category_item.category.name,
                "category_items": [
                    {"name": category_item.name, "records_value_sum": sum(record.value for record in records)}
                ],
            }
        ]
    }


def test_stats_endpoint_multiple_records_multiple_category_items(client, db):
    category = CategoryFactory()
    category_item1 = CategoryItemFactory(category=category)
    category_item2 = CategoryItemFactory(category=category)
    category_item3 = CategoryItemFactory(category=category)
    category_item1_records = [
        RecordFactory(category_item=category_item1),
        RecordFactory(category_item=category_item1),
        RecordFactory(category_item=category_item1),
    ]
    category_item2_records = [
        RecordFactory(category_item=category_item2),
        RecordFactory(category_item=category_item2),
        RecordFactory(category_item=category_item2),
    ]
    category_item3_records = [
        RecordFactory(category_item=category_item3),
        RecordFactory(category_item=category_item3),
        RecordFactory(category_item=category_item3),
    ]
    r = client.get("/stats")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category.name,
                "category_items": [
                    {
                        "name": category_item1.name,
                        "records_value_sum": sum(record.value for record in category_item1_records),
                    },
                    {
                        "name": category_item2.name,
                        "records_value_sum": sum(record.value for record in category_item2_records),
                    },
                    {
                        "name": category_item3.name,
                        "records_value_sum": sum(record.value for record in category_item3_records),
                    },
                ],
            }
        ]
    }


def test_stats_endpoint_multiple_records_multiple_category_items_multiple_categories(client, db):
    category1 = CategoryFactory()
    category1_category_item1 = CategoryItemFactory(category=category1)
    category1_category_item2 = CategoryItemFactory(category=category1)
    category1_category_item3 = CategoryItemFactory(category=category1)
    category1_category_item1_records = [
        RecordFactory(category_item=category1_category_item1),
        RecordFactory(category_item=category1_category_item1),
        RecordFactory(category_item=category1_category_item1),
    ]
    category1_category_item2_records = [
        RecordFactory(category_item=category1_category_item2),
        RecordFactory(category_item=category1_category_item2),
        RecordFactory(category_item=category1_category_item2),
    ]
    category1_category_item3_records = [
        RecordFactory(category_item=category1_category_item3),
        RecordFactory(category_item=category1_category_item3),
        RecordFactory(category_item=category1_category_item3),
    ]
    category2 = CategoryFactory()
    category2_category_item1 = CategoryItemFactory(category=category2)
    category2_category_item2 = CategoryItemFactory(category=category2)
    category2_category_item3 = CategoryItemFactory(category=category2)
    category2_category_item1_records = [
        RecordFactory(category_item=category2_category_item1),
        RecordFactory(category_item=category2_category_item1),
        RecordFactory(category_item=category2_category_item1),
    ]
    category2_category_item2_records = [
        RecordFactory(category_item=category2_category_item2),
        RecordFactory(category_item=category2_category_item2),
        RecordFactory(category_item=category2_category_item2),
    ]
    category2_category_item3_records = [
        RecordFactory(category_item=category2_category_item3),
        RecordFactory(category_item=category2_category_item3),
        RecordFactory(category_item=category2_category_item3),
    ]
    r = client.get("/stats")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category1.name,
                "category_items": [
                    {
                        "name": category1_category_item1.name,
                        "records_value_sum": sum(record.value for record in category1_category_item1_records),
                    },
                    {
                        "name": category1_category_item2.name,
                        "records_value_sum": sum(record.value for record in category1_category_item2_records),
                    },
                    {
                        "name": category1_category_item3.name,
                        "records_value_sum": sum(record.value for record in category1_category_item3_records),
                    },
                ],
            },
            {
                "name": category2.name,
                "category_items": [
                    {
                        "name": category2_category_item1.name,
                        "records_value_sum": sum(record.value for record in category2_category_item1_records),
                    },
                    {
                        "name": category2_category_item2.name,
                        "records_value_sum": sum(record.value for record in category2_category_item2_records),
                    },
                    {
                        "name": category2_category_item3.name,
                        "records_value_sum": sum(record.value for record in category2_category_item3_records),
                    },
                ],
            },
        ]
    }


def test_stats_endpoint_time_range_filter(client, db):
    category_item1 = CategoryItemFactory()
    category_item1_today_record = RecordFactory(category_item=category_item1)
    category_item1_yesterday_record = RecordFactory(
        created=datetime.now() - timedelta(days=1), category_item=category_item1
    )
    category_item2 = CategoryItemFactory()
    category_item2_yesterday_record = RecordFactory(
        created=datetime.now() - timedelta(days=1), category_item=category_item2
    )
    r = client.get("/stats?time_range=today")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category_item1.category.name,
                "category_items": [
                    {"name": category_item1.name, "records_value_sum": category_item1_today_record.value}
                ],
            }
        ]
    }

    r = client.get("/stats?time_range=yesterday")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category_item1.category.name,
                "category_items": [
                    {"name": category_item1.name, "records_value_sum": category_item1_yesterday_record.value}
                ],
            },
            {
                "name": category_item2.category.name,
                "category_items": [
                    {"name": category_item2.name, "records_value_sum": category_item2_yesterday_record.value}
                ],
            },
        ]
    }

    r = client.get("/stats?time_range=all_time")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category_item1.category.name,
                "category_items": [
                    {
                        "name": category_item1.name,
                        "records_value_sum": category_item1_today_record.value + category_item1_yesterday_record.value,
                    }
                ],
            },
            {
                "name": category_item2.category.name,
                "category_items": [
                    {"name": category_item2.name, "records_value_sum": category_item2_yesterday_record.value}
                ],
            },
        ]
    }


def test_stats_endpoint_time_range_filter_with_nsfw(client, db):
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
    r = client.get("/stats?time_range=today&nsfw=true")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category1.name,
                "category_items": [
                    {
                        "name": category1_category_item.name,
                        "records_value_sum": category1_category_item_today_record.value,
                    }
                ],
            }
        ]
    }

    r = client.get("/stats?time_range=today&nsfw=false")
    assert r.status_code == 200
    assert r.json() == {"stats": []}

    r = client.get("/stats?time_range=yesterday&nsfw=true")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
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
        ]
    }

    r = client.get("/stats?time_range=yesterday&nsfw=false")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category3.name,
                "category_items": [
                    {
                        "name": category3_category_item.name,
                        "records_value_sum": category3_category_item_yesterday_record.value,
                    }
                ],
            },
        ]
    }

    r = client.get("/stats?time_range=all_time&nsfw=true")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category1.name,
                "category_items": [
                    {
                        "name": category1_category_item.name,
                        "records_value_sum": (
                            category1_category_item_today_record.value + category1_category_item_yesterday_record.value
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
        ]
    }

    r = client.get("/stats?time_range=all_time&nsfw=false")
    assert r.status_code == 200
    assert r.json() == {
        "stats": [
            {
                "name": category3.name,
                "category_items": [
                    {
                        "name": category3_category_item.name,
                        "records_value_sum": category3_category_item_yesterday_record.value,
                    }
                ],
            },
        ]
    }
