'''Classify one CICFlowMeter CSV with the saved scaler and a saved model.
Run from the Kalasag folder:
  python -m src.live.classify_csv flows.csv --model models/local/final_model.joblib
'''
import argparse
from collections import Counter
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.live.convert import to_scaled
from src.response.simulated_block import simulate_block

ROOT = Path(__file__).resolve().parents[2]
NORMAL = 'Normal Traffic'


def classify(raw, scaler, le, model):
    '''One row per usable flow: predicted class and confidence. Also returns the skipped count.'''
    X, ok = to_scaled(raw, scaler)
    proba = model.predict_proba(X)
    ids = np.asarray(model.classes_)[proba.argmax(axis=1)].astype(int)
    out = pd.DataFrame({'predicted': le.inverse_transform(ids),
                        'confidence': proba.max(axis=1)}, index=X.index)
    return out, int((~ok).sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('--model', required=True)
    ap.add_argument('--mode', default='live')
    ap.add_argument('--runtime', default=None, help='folder for alerts.csv and blocklist.csv')
    a = ap.parse_args()

    raw = pd.read_csv(a.csv)
    scaler = joblib.load(ROOT / 'models' / 'scaler.pkl')
    le = joblib.load(ROOT / 'models' / 'label_encoder.pkl')
    model = joblib.load(a.model)
    if hasattr(model, 'get_xgb_params'):
        model.set_params(device='cpu')
    res, skipped = classify(raw, scaler, le, model)
    print('flows:', len(raw), '| classified:', len(res), '| skipped (NaN/inf):', skipped)
    print(dict(Counter(res['predicted'])))
    refused = 0
    for i, r in res[res['predicted'] != NORMAL].iterrows():
        try:
            simulate_block(raw.loc[i, 'src_ip'], r['predicted'], r['confidence'], a.mode, a.runtime)
        except ValueError:
            refused += 1          # public address: the block module refuses it by design
    print('attack flows:', int((res['predicted'] != NORMAL).sum()), '| refused (public IP):', refused)


if __name__ == '__main__':
    main()
