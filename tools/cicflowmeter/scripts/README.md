# CICFlowMeter One-Off Scripts

This folder contains diagnostic and maintenance scripts used during the
Kalasag CICFlowMeter v0.4.2 feature-validation and patching work.

These scripts are not part of the normal live-classification workflow.

## Diagnostic scripts

The following scripts inspect CICFlowMeter output and compare it with
the training dataset.

| Script | Purpose |
|---|---|
| `check_iat_truth.py` | Compares packet inter-arrival time values from a PCAP with CICFlowMeter output and training statistics. |
| `check_udp_hdr.py` | Compares UDP-related header and segment-size values between training data and CICFlowMeter output. |
| `check_win.py` | Inspects TCP window-size values by protocol and packet direction. |
| `compare_values.py` | Compares selected feature medians and 90th percentiles between training data and CICFlowMeter output. Writes `value_check.csv` to `~/cfm-work/`. |

These scripts expect previously prepared files under `~/cfm-work/`,
including `test.pcap`, `flows.csv`, and `cleaned.parquet`, depending
on the script.

## Maintenance and historical patch scripts

| Script | Purpose |
|---|---|
| `fix_padding.py` | Historical one-off correction for Ethernet padding affecting packet payload calculations. |
| `patch2.py` | Historical fixes for initial TCP window values and packet header/payload calculations. |
| `patch5.py` | Historical correction for duplicate counting of the first packet. |
| `patch6.py` | Historical correction for single-gap inter-arrival time calculations. |

These scripts modify files inside a locally installed CICFlowMeter
package. They are not intended to be run as ordinary project scripts.

## Important: Use the unified patch

The official consolidated patch is:

`tools/cicflowmeter/cicflowmeter-0.4.2-kalasag.patch`

Use the unified patch for the documented CICFlowMeter v0.4.2 setup.

Do not separately execute `patch2.py`, `patch5.py`, or `patch6.py`.
Their fixes are included in the consolidated patch.

Do not execute `fix_padding.py` as an additional patch step when
using the unified patch. The Ethernet padding correction is already
included in the consolidated patch.

## Safety and reproducibility notes

- These are one-off development and diagnostic scripts.
- Some scripts use hard-coded paths under `~/cfm-work/`.
- Maintenance scripts can modify the installed Python package.
- Review the target environment before running any maintenance script.
- Keep the unified patch as the single documented patch source.
- Do not treat diagnostic output as proof of full lab validation.
