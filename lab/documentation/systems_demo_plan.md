
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
The dashboard and capture module still need implementation. The live demo depends on the team's model and feature schema being ready.
