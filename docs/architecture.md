# Architecture

## Overview
A shared risk engine feeding three defense-only modules:
1. Fraud-spike detector (LightGBM + Isolation Forest on transaction velocity/anomaly features)
2. Return-risk scorer (LightGBM on order-level features)
3. Chargeback evidence responder (template-based evidence packet generator)

All three read from a shared SQLite feature store and log every score/decision
to an audit trail table (timestamp, model version, threshold used).

## Modules
- src/feature_store.py — shared feature engineering + SQLite read/write
- src/fraud_model.py — fraud-spike detection model
- src/return_model.py — return-risk scoring model
- src/chargeback_responder.py — evidence packet generator
- src/decision_layer.py — cost-aware threshold logic
- src/dashboard.py — Streamlit UI