'''Kalasag dashboard. Run from the Kalasag folder:  streamlit run dashboard/app.py
Practice mode:  KALASAG_DIR=~/kalasag-dummy streamlit run dashboard/app.py'''
import os
import sys
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.response.simulated_block import simulate_block  # noqa: E402

BASE = Path(os.environ.get('KALASAG_DIR', str(ROOT))).expanduser()
PRACTICE = 'KALASAG_DIR' in os.environ
RUN = BASE / 'runtime'
NORMAL = 'Normal Traffic'

st.set_page_config(page_title='Kalasag', layout='wide')
st.title('Kalasag: network attack detection')
st.caption('Detect, flag, and simulated block. Blocking is only written to a log; no firewall command is ever run.')
if PRACTICE:
    st.warning('PRACTICE DATA: fake model and fake records. Results mean nothing.')


@st.cache_resource
def load_artifacts(model_file):
    scaler = joblib.load(BASE / 'models' / 'scaler.pkl')
    le = joblib.load(BASE / 'models' / 'label_encoder.pkl')
    model = joblib.load(model_file)
    if hasattr(model, 'get_xgb_params'):
        model.set_params(device='cpu')        # a model trained on a GPU must also run on this laptop
    return scaler, le, model


@st.cache_data
def load_records():
    return pd.read_parquet(BASE / 'data' / 'interim' / 'split_test_unscaled.parquet')


def show_log(name, title, mode=None):
    st.subheader(title)
    path = RUN / name
    if not path.exists():
        st.info('Nothing logged yet.')
        return
    df = pd.read_csv(path)
    if mode and 'mode' in df.columns:
        df = df[df['mode'] == mode]
    st.dataframe(df.tail(20))


model_files = sorted((BASE / 'models' / 'local').glob('*.joblib'))
if not model_files:
    st.error('No model found. Put a .joblib file in ' + str(BASE / 'models' / 'local'))
    st.stop()
model_file = st.sidebar.selectbox('Model', model_files, format_func=lambda p: p.name)
scaler, le, model = load_artifacts(model_file)
names = list(le.classes_)
cols = list(scaler.feature_names_in_)

tab_off, tab_live = st.tabs(['Offline demo', 'Live lab demo'])

with tab_off:
    records = load_records()
    kind = st.selectbox('Type of traffic to try', names, index=names.index(NORMAL))
    ids = records.index[records['label'] == names.index(kind)]
    if len(ids) == 0:
        st.warning('No demo records of this type.')
        st.stop()
    if st.button('Pick a random one'):
        st.session_state['pick'] = int(np.random.randint(len(ids)))
    if st.session_state.get('pick', 0) > len(ids) - 1:
        st.session_state['pick'] = 0
    pick = int(st.number_input('Record number', min_value=0, max_value=len(ids) - 1, step=1, key='pick'))
    row = records.loc[ids[pick]]
    X = pd.DataFrame([row[cols].astype('float64').values], columns=cols)
    st.subheader('Flow record (before scaling)')
    st.dataframe(X.T.rename(columns={0: 'value'}), height=300)

    if st.button('Classify this flow', type='primary'):
        t0 = time.perf_counter()
        proba = model.predict_proba(pd.DataFrame(scaler.transform(X), columns=cols))[0]
        ms = (time.perf_counter() - t0) * 1000
        predicted = names[int(model.classes_[int(np.argmax(proba))])]
        confidence = float(proba.max())
        c1, c2, c3 = st.columns(3)
        c1.metric('Prediction', predicted)
        c2.metric('Confidence', f'{confidence:.1%}')
        c3.metric('Time for this record', f'{ms:.1f} ms')
        st.bar_chart(pd.Series(proba, index=[names[int(c)] for c in model.classes_]))
        actual = names[int(row['label'])]
        st.caption('Actual label (demo only): ' + actual)
        if predicted == NORMAL:
            st.success('Normal traffic: no action.')
        else:
            st.error(f'ATTACK DETECTED: {predicted}')
            fake_ip = f'192.0.2.{int(ids[pick]) % 254 + 1}'          # documentation address, not a real host
            res = simulate_block(fake_ip, predicted, confidence, mode='offline', runtime=RUN)
            st.write('Simulated block of source ' + res['src_ip'] + ' (practice address). This command is shown but NOT executed:')
            st.code(res['command'], language='bash')
    show_log('alerts.csv', 'Alert log (offline)', 'offline')
    show_log('blocklist.csv', 'Blocklist (simulated)')

with tab_live:
    st.write('Alerts written by the live lab pipeline (victim VM). Press Refresh to reload.')
    st.button('Refresh')
    show_log('alerts.csv', 'Alert log (live lab)', 'live')
