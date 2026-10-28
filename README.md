# Kalasag

**Supervised Learning-Based Classification of Network Traffic for Real-Time Cyberattack Detection**

*Kalasag* is Filipino for "shield." It is a machine-learning system that looks at network traffic and decides whether each piece of it is **normal** or **an attack**. It is an undergraduate thesis project built by a 3-member team, using the CICIDS2017 (Cleaned & Preprocessed) dataset from Kaggle.

> **Safety rule (read this first):** Live capture runs **only** on our own isolated VirtualBox lab network. Blocking is **simulated** inside the lab VM and never touches a real network. Never capture on, or run attacks against, a shared home or school network, or anyone else's traffic.

---

## Table of Contents

1. [What Kalasag Does](#what-kalasag-does)
2. [Success Targets](#success-targets)
3. [How It Works](#how-it-works)
4. [Scope](#scope)
5. [Tech Stack](#tech-stack)
6. [Repository Structure](#repository-structure)
7. [Team and Roles](#team-and-roles)
8. [Getting Started](#getting-started)
9. [Team Workflow](#team-workflow)
10. [Ground Rules](#ground-rules)
11. [Lab and Hardware Setup](#lab-and-hardware-setup)
12. [Roadmap](#roadmap)
13. [References](#references)

---

## What Kalasag Does

Think of Kalasag as a security guard that has studied thousands of examples of well-behaved visitors and known troublemakers, and learned to tell them apart by how they behave.

- **Input:** a *flow record*, which is a summary of one conversation between two devices (duration, packets and bytes in each direction, timing, flags).
- **Output:** a prediction of **normal vs. attack**, plus the attack type (for example DoS, PortScan, brute-force) and a confidence score.
- **Response (simulated):** when an attack is detected, Kalasag logs an alert and *pretends* to block the source. Think of a smoke detector that also pretends to call the fire department.
- **Demo:** a Streamlit dashboard with two modes: an **offline demo** on test records, and a **live lab demo** on real packets captured between two VMs we own.

**Why recall matters most:** attacks are rare compared to normal traffic, so a lazy model that always says "normal" could look about 99% accurate while catching nothing. Missing a real attack is the costliest mistake, so we optimize for **high recall** while keeping false alarms low enough that whoever watches the dashboard doesn't start ignoring it (alert fatigue).

---

## Success Targets

| Metric | Target | In plain terms |
|---|---|---|
| Recall (attack classes, macro-avg) | at least 90% | Catch at least 90 of every 100 real attacks |
| False Positive Rate | at most 5% | Wrongly flag no more than 5 of every 100 normal flows |
| F1-score (macro-avg) | at least 0.85 | Balance between catching attacks and not crying wolf |
| Inference latency | under 100 ms per flow | Fast enough to feel near real-time |
| Demo pipeline | 100% of steps working | Capture, classify, flag, and simulated block all run end to end |

We claim **near real-time**, and we back it with the latency we actually measure.

---

## How It Works

```text
                  OFFLINE (training)                        LIVE (demo, our lab only)

   CICIDS2017 dataset                               Attacker VM ----> Victim VM
          |                                                  \         /
          v                                                   Packet capture
   Clean, encode, split                                       (Zeek / CICFlowMeter)
   (split BEFORE resampling)                                          |
          |                                                           v
          v                                              Map to the training feature schema
   Resample TRAIN only, scale                            and apply the SAVED scaler
          |                                                           |
          v                                                           |
   Train and compare models                                           |
          |                                                           |
          +-----------------> Trained model <-------------------------+
                                    |
                                    v
                       Prediction + confidence score
                                    |
                     Attack? ----> Log alert + SIMULATED block
                                    |
                                    v
                          Streamlit dashboard
```

The key link between the two halves is the **feature schema** and the **saved scaler**. Live traffic has to be converted into exactly the same shape of data the model was trained on.

---

## Scope

| In scope | Out of scope (future work) |
|---|---|
| Training and evaluating several algorithms on CICIDS2017 | Deployment on production infrastructure or any network we don't own or have permission to monitor |
| Offline and batch classification | Integration with a real firewall or router |
| A demo dashboard simulating detection and response | Any real blocking against real users' traffic |
| Live capture and classification on our own isolated VM lab, using real (not replayed) packets | |

---

## Tech Stack

Everything is free or free-tier.

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| Data handling | pandas, numpy |
| Class imbalance | imbalanced-learn (SMOTE, ADASYN) |
| Classical ML | scikit-learn (Logistic Regression, Random Forest, SVM, Decision Tree) |
| Gradient boosting | XGBoost, LightGBM |
| Deep learning (optional) | TensorFlow/Keras or PyTorch (MLP comparison) |
| Explainability | SHAP, scikit-learn `feature_importances_` |
| Visualization | matplotlib, seaborn, plotly |
| Dashboard | Streamlit |
| Live capture (lab only) | Zeek or CICFlowMeter, Scapy (optional traffic generation) |
| Simulated blocking (lab only) | Python `subprocess` with iptables/netsh, inside an isolated VM |
| Lab | VirtualBox (internal network), AWS/Azure free tier for any extra VM |
| Training environment | Google Colab, Kaggle Notebooks |
| Version control | Git and GitHub |

---

## Repository Structure

```text
Kalasag/
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/                  Project documents
│   ├── handoffs/          One note per handoff between members (see TEMPLATE.md)
│   ├── methodology_notes/ Cleaning and modeling decision logs for the thesis
│   └── manuscript/        Thesis chapter drafts
│
├── data/
│   ├── raw/               Original dataset files (NOT in Git)
│   ├── interim/           Partially cleaned data (NOT in Git)
│   ├── processed/         Final train/val/test splits (NOT in Git)
│   └── schema/            feature_schema.json, class distribution notes
│
├── notebooks/             Cleaning, EDA, modeling, and evaluation notebooks
│
├── src/
│   ├── preprocessing/     Cleaning, stratified split, resampling, scaling
│   ├── modeling/          Training, tuning, evaluation, explainability
│   ├── capture/           Live feature mapper (capture output -> training schema)
│   ├── response/          Simulated detect -> flag/block logic
│   └── utils/             Shared helpers
│
├── models/                Trained models, scaler, label encoder (large files NOT in Git)
│   └── metrics/           Comparison sheets and plots (these are committed)
│
├── dashboard/             Streamlit app (offline and live demo pages)
├── lab/                   VM setup notes, network config, capture tool configs
│   ├── virtualbox/
│   ├── network/
│   ├── capture_tooling/
│   └── cloud/
│
└── tests/                 Guards against data leakage and schema/scaler mismatches
```

Some folders only contain a `.gitkeep` placeholder for now. They fill up as the project moves through its phases.

**Never commit:** dataset files, VM images (`.ova`, `.vdi`, `.vmdk`), packet captures (`.pcap`), or large model files. The `.gitignore` blocks these. Share large files through a Drive or Kaggle link and record the link in the relevant `docs/handoffs/` note.

---

## Team and Roles

| Member | Role | Owns |
|---|---|---|
| Member 1 (name TBD) | Data & Preprocessing Lead | Phases 0 to 3: `data/`, `src/preprocessing/`, notebooks 01 to 03 |
| Aleah | Model Development Lead | Phases 4 to 5: `src/modeling/`, `models/`, notebooks 04 to 07 |
| Pou | Systems & Demo Lead | Phases 6 to 7: `lab/`, `src/capture/`, `src/response/`, `dashboard/` |
| All | Shared | Phase 8 (documentation), `docs/`, `tests/`, and code review |

Every member should be able to explain and defend any part of the system at the oral defense, not just the part they built.

---

## Getting Started

### Prerequisites

- Python **3.10 or newer** (check with `python --version`)
- Git
- A Google account (Colab) and a Kaggle account with a verified phone number (needed for free GPU notebooks)

### 1. Clone the repository

```bash
git clone https://github.com/lluviaaaa/Kalasag.git
cd Kalasag
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Once everyone's install works, one person runs `pip freeze > requirements.lock.txt` and commits it, so all three laptops use identical versions.

### 4. Get the dataset

Download **CICIDS2017 - Cleaned & Preprocessed** from Kaggle (`ericanacletoribeiro/cicids2017-cleaned-and-preprocessed`) and place the files in `data/raw/`. Do not commit them.

### 5. Run the tests

```bash
pytest
```

Early on, most tests are placeholders that skip. They are filled in as each pipeline step is built.

---

## Team Workflow

1. **Branch per member.** Work on your own branch, for example `member1-data`, `aleah-models`, `pou-systems`. Never commit straight to `main`.
2. **Pull request into `main`.** At least one teammate reviews every PR. This is how we make sure each of us understands the whole pipeline.
3. **Handoffs get a written note.** When you pass work to the next person, copy `docs/handoffs/TEMPLATE.md`, fill it in (what changed, exact file locations, large-file links, known issues, how to verify), and commit it.
4. **Clear notebook outputs before committing**, so diffs stay readable.
5. **Weekly check-in** for the whole team, with decisions logged in `docs/`.

**How work flows between members:** everyone pushes to and pulls from this repo. Member 1 publishes the cleaned data, the fitted scaler, and the feature schema. Aleah pulls those to train, then publishes the trained model and metrics. Pou pulls the model **and** Member 1's scaler and schema to build the live pipeline and dashboard.

---

## Ground Rules

These protect the correctness of our results. Breaking them can make a model look great while being quietly wrong.

1. **Split before you resample.** Do the stratified train/validation/test split first, then apply SMOTE/ADASYN to the **training set only**. Resampling before the split leaks near-duplicate records into the test set (data leakage) and inflates our scores.
2. **Scale with training-set statistics only.** Fit the scaler on the training set, then reuse it unchanged for validation, test, and live data.
3. **The cross-team contract.** `models/scaler.pkl` and `data/schema/feature_schema.json` are shared by everyone. **Never re-fit the scaler elsewhere**, and treat any change to either file as a big deal that needs a handoff note.
4. **Don't chase accuracy alone.** Always report recall, false-positive rate, F1, and **per-class** metrics, not just overall accuracy.
5. **The test set is touched once.** Use it only for final evaluation. Cross-validation uses the training set only.
6. **Simulated means simulated.** Any block or firewall command runs only inside the isolated lab VM, never on a host laptop or a real network device.

---

## Lab and Hardware Setup

The live demo uses two machines on an isolated VirtualBox internal network.

| | Laptop 1 | Laptop 2 |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Free storage | about 90 GB | about 40 GB |
| Role | Attacker VM (lean Kali install). One VM at a time. | Victim VM (lean Ubuntu Server) plus the live capture and feature-extraction tooling |

Notes:

- Keep to **one VM per laptop**. Running two VMs on the 8 GB laptop will be painfully slow.
- Rough VM sizes: lean Ubuntu Server 15 to 25 GB, Kali 40 to 80 GB (less if you skip the full tool suite), VirtualBox plus ISOs 5 to 10 GB. Delete old snapshots regularly, since they eat storage quietly.
- Model training happens on Google Colab and Kaggle Notebooks, so no powerful local hardware is needed for that part.
- If an extra VM is ever needed, use an AWS or Azure free-tier instance rather than overloading a laptop. These are still machines we control, so they stay within scope as long as capture is never pointed at someone else's traffic.
- Confirm virtualization (VT-x / AMD-V) is enabled in BIOS on both machines before building VMs.

---

## Roadmap

We follow the six-step **CRISP-DM** process from *Data Analytics Made Accessible* (Maheshwari, 2020, Ch. 4): Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, and Dissemination.

| Weeks | Milestone | Status |
|---|---|---|
| 1-2 | Setup: repo, environment, cloud accounts, dataset, schema documentation | [ ] |
| 3-4 | Data cleaning and EDA, documented | [ ] |
| 5-7 | Stratified split, imbalance handling, scaling, baseline models | [ ] |
| 8-9 | Model comparison, hyperparameter tuning, cross-validation | [ ] |
| 10 | Adviser review of interim results | [ ] |
| 11-12 | Live capture lab, simulated detect/flag/block, Streamlit dashboard | [ ] |
| 13 | End-to-end integration testing | [ ] |
| 14 | Full manuscript draft | [ ] |
| 15 | Adviser review and revisions | [ ] |
| 16 | Defense preparation and demo rehearsal | [ ] |

Tick the boxes as each milestone is finished.

---

## References

- Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization.* ICISSP.
- Engelen, G., Rimmer, V., & Joosen, W. (2021). *Troubleshooting an Intrusion Detection Dataset: The CICIDS2017 Case Study.* IEEE S&P Workshops.
- Maheshwari, A. (2020). *Data Analytics Made Accessible.* Chapter 4: Data Mining.
- CICIDS2017 official page: https://www.unb.ca/cic/datasets/ids-2017.html
- Dataset used: https://www.kaggle.com/datasets/ericanacletoribeiro/cicids2017-cleaned-and-preprocessed


## Python Development Environment

Kalasag uses Python 3.13.3 as the initial development environment.

### Requirements
- Python 3.13.3
- Git
- pip
- VS Code (recommended)

### Windows Setup

1. Clone the repository and open the Kalasag folder.
2. Create a virtual environment:

   python -m venv .venv

3. Activate the environment in PowerShell:

   .\.venv\Scripts\Activate.ps1

4. Install the pinned dependencies:

   python -m pip install -r requirements.lock.txt

5. Verify dependency compatibility:

   python -m pip check

6. Run the project tests:

   python -m pytest

### Dependency Management

- `requirements.txt` lists the project's direct dependencies.
- `requirements.lock.txt` records the exact installed package versions.
- Use the lock file for consistent installations.
- Do not commit the `.venv` directory.
- Test dependency changes before updating the lock file.

### Reproducibility

The initial environment was prepared using Python 3.13.3 on Windows. The dependency lock file is intended to support reproducible setup across team members. Compatibility on other machines and platforms must be verified separately.

