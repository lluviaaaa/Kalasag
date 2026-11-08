
import pandas as pd

from src.preprocessing.pipeline import remove_invalid_negative_rows


def test_remove_invalid_negative_rows():
    df = pd.DataFrame({
        "Flow Duration": [100, -5, 200, 300],
        "Flow IAT Min": [10, 20, -1, 30],
        "Init_Win_bytes_forward": [-1, 100, -1, -1],
        "Init_Win_bytes_backward": [-1, -1, 200, -1],
        "Attack Type": ["Normal Traffic", "DoS", "DDoS", "Bots"],
    })

    cleaned, removed = remove_invalid_negative_rows(df)

    assert removed == 2
    assert len(cleaned) == 2
    assert cleaned["Attack Type"].tolist() == [
        "Normal Traffic",
        "Bots",
    ]

    assert cleaned["Init_Win_bytes_forward"].tolist() == [-1, -1]
    assert cleaned["Init_Win_bytes_backward"].tolist() == [-1, -1]

    assert len(df) == 4
