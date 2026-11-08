"""Live feature mapper output must match data/schema/feature_schema.json (Step 26)."""
import pytest

def test_live_columns_match_schema():
    pytest.skip("Implement after Step 8/26: compare mapper output columns/order to the schema.")


def test_final_feature_list_has_46_features_without_active_idle():
    import json
    from pathlib import Path

    schema_path = Path(__file__).resolve().parents[1] / "data/schema/feature_schema.json"

    if not schema_path.exists():
        import pytest
        pytest.skip("feature_schema.json not found")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    names = [feature["name"] for feature in schema["features"]]

    dropped = [
        "Active Mean",
        "Active Max",
        "Active Min",
        "Idle Mean",
        "Idle Max",
        "Idle Min",
    ]

    assert len(names) == 46
    assert not any(name in names for name in dropped)
