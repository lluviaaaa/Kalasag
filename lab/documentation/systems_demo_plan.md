
# Kalasag Systems Demo Plan

## Purpose
Demonstrate the network traffic classification system and its simulated response to detected attacks.

## Demo Modes

### 1. Offline Demo
Use prepared sample flow records to demonstrate traffic classification without capturing live network traffic.

### 2. Live Lab Demo
Capture traffic only within the isolated VirtualBox lab network, once the capture module and trained model are ready.

## Detection Output
The demo should display:
- Predicted traffic class
- Predicted attack type, if supported by the trained model
- Prediction confidence, if available

## Simulated Response
When traffic is classified as an attack, record an alert and display a simulated blocking message. Do not apply real firewall rules to the host computer or shared networks.

## Dependencies
- Trained model and scaler from the team
- Agreed feature schema
- Working capture module for the live demo
- Sample flow records for the offline demo

## Current Status

### Implemented
- Offline dashboard for prepared sample flow classification.
- Live feature conversion from CICFlowMeter output to the agreed 46-feature training schema.
- CSV-based flow classification using the trained model, scaler, and label encoder.
- Simulated response that records alerts and simulated blocks without executing firewall commands.
- CICFlowMeter 0.4.2 setup and feature patch validation.

### Pending Validation
- Continuous packet capture within the isolated VirtualBox lab network.
- End-to-end processing of browser-generated traffic from the Victim VM.
- Verification that live predictions and alerts appear in the dashboard.
- Controlled attack traffic testing and detection verification.

### Safety
All live testing must remain within the isolated lab network. Simulated blocking must not execute real firewall commands.
