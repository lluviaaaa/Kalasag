
from pathlib import Path
import gc

import pandas as pd

RAW_PATH = Path("data/raw/cicids2017_cleaned.csv")
TARGET = "Attack Type"
REMOVED_FEATURES = [
    "Active Mean", "Active Max", "Active Min",
    "Idle Mean", "Idle Max", "Idle Min",
]

if not RAW_PATH.exists():
    raise FileNotFoundError(RAW_PATH)

header = pd.read_csv(RAW_PATH, nrows=0).columns.tolist()
features_52 = [c for c in header if c != TARGET]
features_46 = [c for c in features_52 if c not in REMOVED_FEATURES]

assert len(features_52) == 52
assert len(features_46) == 46

def inspect_conflicts(features):
    # Store compact hashes and numeric label IDs, not all feature columns.
    label_ids = {}
    hashes = []
    labels = []
    rows = 0

    for chunk in pd.read_csv(RAW_PATH, chunksize=50000, low_memory=False):
        chunk = chunk.drop_duplicates()
        rows += len(chunk)

        for label in chunk[TARGET].unique():
            if label not in label_ids:
                label_ids[label] = len(label_ids)

        h = pd.util.hash_pandas_object(
            chunk[features], index=False
        ).to_numpy()

        hashes.extend(h)
        labels.extend(chunk[TARGET].map(label_ids).to_numpy())

        del chunk, h
        gc.collect()

    compact = pd.DataFrame({
        "hash": hashes,
        "label": labels,
    })

    conflicts = (
        compact.groupby("hash")["label"].nunique() > 1
    ).sum()

    print(f"Feature count: {len(features)}")
    print(f"Rows scanned: {rows:,}")
    print(f"Conflicting feature hashes: {conflicts:,}")

    del compact, hashes, labels
    gc.collect()

print("Checking original 52 features...")
inspect_conflicts(features_52)

print("\nChecking selected 46 features...")
inspect_conflicts(features_46)
