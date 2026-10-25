# Kalasag

Supervised Learning-Based Classification of Network Traffic for Real-Time Cyberattack Detection.
Undergraduate thesis project (3-member team). Dataset: CICIDS2017 Cleaned & Preprocessed (Kaggle).

## Safety rule (read first)
Live capture runs ONLY on our own isolated VirtualBox lab network. Blocking is SIMULATED inside
the lab VM. Never capture on, or run attacks against, a shared home/school network or anyone else's traffic.

## Roles
| Member | Role | Owns |
|---|---|---|
| Member 1 (name) | Data & Preprocessing Lead | data/, src/preprocessing/, notebooks 01-03 |
| Member 2 (name) | Model Development Lead | src/modeling/, models/, notebooks 04-07 |
| Member 3 (name) | Systems & Demo Lead | lab/, src/capture/, src/response/, dashboard/ |
| All | Shared | docs/, tests/, code review |

## Quick start
```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Dataset: download CICIDS2017 Cleaned & Preprocessed from Kaggle
(ericanacletoribeiro/cicids2017-cleaned-and-preprocessed) into data/raw/.

## Team rules
1. Split BEFORE resampling. Scale with training-set statistics only (see tests/).
2. `models/scaler.pkl` and `data/schema/feature_schema.json` are the cross-team contract. Never re-fit the scaler elsewhere.
3. Branch per member, pull request into main, one teammate reviews every PR.
4. Every handoff gets a note in docs/handoffs/ (use TEMPLATE.md).
5. Clear notebook outputs before committing.
