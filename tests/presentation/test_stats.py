from tests.factories.records import RecordFactory


def test_correct_result(client, db):
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
