
from src.preprocessing.artifacts import load_schema


def test_schema_has_no_identifier_columns():
    schema = load_schema()

    names = [feature["name"] for feature in schema["features"]]

    forbidden = {
        "Flow ID",
        "Source IP",
        "Destination IP",
        "Source Port",
        "Timestamp",
        "Attack Type",
        "label",
    }

    assert len(names) == 52
    assert len(names) == len(set(names))
    assert not forbidden.intersection(names)
