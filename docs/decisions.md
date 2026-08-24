## 2026-08-24 - Hardware upgrade, scope revised
- Switched primary dev machine from i3 to i7 + 1TB NVMe
- Revised scope: all four modules (fraud-spike, return-risk, chargeback
  responder, abuse-ring sentinel) will be built at full depth instead of
  1 flagship + 2 lightweight modules
- Will use IEEE-CIS Fraud Detection dataset (590k+ rows, 400+ features)
  instead of the smaller Credit Card Fraud dataset, given available compute
- Added abuse-ring sentinel (graph-based, networkx) — previously cut for
  compute reasons on i3