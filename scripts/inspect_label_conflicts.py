
from pathlib import Path
from collections import defaultdict

import pandas as pd

RAW_PATH = Path("data/raw/cicids2017_cleaned.csv")
TARGET = "Attack Type"
CHUNK_SIZE = 50000

# Each hash maps to the labels and their occurrence counts.
hash_labels = defaultdict(lambda: defaultdict(int))

columns = pd.read_csv(RAW_PATH, nrows=0).columns.tolist()
features = [col for col in columns if col != TARGET]

print("Scanning original dataset...")

for chunk in pd.read_csv(RAW_PATH, chunksize=CHUNK_SIZE):
    hashes = pd.util.hash_pandas_object(
        chunk[features], index=False
    )

    pairs = pd.DataFrame({
        "hash": hashes.to_numpy(),
        "label": chunk[TARGET].to_numpy(),
    })

    counts = pairs.groupby(["hash", "label"]).size()

    for (feature_hash, label), count in counts.items():
        hash_labels[int(feature_hash)][label] += int(count)

conflicts = {
    feature_hash: labels
    for feature_hash, labels in hash_labels.items()
    if len(labels) > 1
}

print("\nRESULTS")
print("Conflicting feature hashes:", len(conflicts))

pair_counts = defaultdict(int)

for labels in conflicts.values():
    categories = sorted(labels.keys())

    for i in range(len(categories)):
        for j in range(i + 1, len(categories)):
            pair_counts[
                (categories[i], categories[j])
            ] += 1

print("\nConflicting label combinations:")

for pair, count in sorted(
    pair_counts.items(),
    key=lambda item: item[1],
    reverse=True,
):
    print(f"{pair[0]} vs {pair[1]}: {count}")


print("\nVERIFYING ACTUAL FEATURE VALUES")

conflict_hashes = set(conflicts)
matched_chunks = []

for chunk in pd.read_csv(RAW_PATH, chunksize=CHUNK_SIZE):
    hashes = pd.util.hash_pandas_object(
        chunk[features], index=False
    )

    matching = chunk.loc[hashes.isin(conflict_hashes)].copy()

    if not matching.empty:
        matching["_feature_hash"] = hashes.loc[
            matching.index
        ].to_numpy()
        matched_chunks.append(matching)

matched = pd.concat(matched_chunks, ignore_index=True)

# Group by all actual feature values, not hashes.
actual_conflicts = (
    matched.groupby(features, dropna=False)[TARGET]
    .nunique()
)

actual_conflicts = int((actual_conflicts > 1).sum())

print("Hash-based conflicts:", len(conflicts))
print("Verified full-feature conflicts:", actual_conflicts)
print("Records involved:", len(matched))
