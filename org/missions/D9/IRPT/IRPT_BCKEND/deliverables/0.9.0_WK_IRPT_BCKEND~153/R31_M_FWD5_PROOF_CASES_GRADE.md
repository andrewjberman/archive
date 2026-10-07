# R31 M FWD-5 proof cases grade (0.9.0_WK_IRPT_BCKEND~153, IB-mr-311)

Printed lines copied verbatim; each invocation rc=0. Judgment: none.

## e1: python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R31_CHECKS/r31_delivered_reads.py e1
```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R31M_FWD5_PROOF_CASES_READ.json@471da6f0b0 sha256 2b61c5a833c761e60b581f4f983f4c2795bc84624494df3a063d45571865f3e5 (pinned 2b61c5a833c761e60b581f4f983f4c2795bc84624494df3a063d45571865f3e5)
FILE org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R31M_UNASSIGNED_RECHECK_20261007.json@6458a5a9d3 sha256 9eb9cff78f7721a07653606eb9624ad33ed46b86688ac04641e6c09bde64498e (pinned 9eb9cff78f7721a07653606eb9624ad33ed46b86688ac04641e6c09bde64498e)
e1 unassigned: FOUND at 49financial, instance acc_8edbf9b2d53df56d206d2717, 1876 instance(s) in total
e1 unmatched_join: FOUND at 49financial, instance firm, 3 instance(s) in total
e1 blended_model: FOUND at cottonwood, instance acc_000c147a49a4d234b37dab66, 366 instance(s) in total
e1 multi_membership: FOUND at 49financial, instance acc_1c312e69da7efca76d0f17d3, 1487 instance(s) in total
E1-CASES-NAMED
rc=0
```

## e2: python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R31_CHECKS/r31_delivered_reads.py e2
```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R31M_FWD5_PROOF_CASES_READ.json@471da6f0b0 sha256 2b61c5a833c761e60b581f4f983f4c2795bc84624494df3a063d45571865f3e5 (pinned 2b61c5a833c761e60b581f4f983f4c2795bc84624494df3a063d45571865f3e5)
FILE org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R31M_UNASSIGNED_RECHECK_20261007.json@6458a5a9d3 sha256 9eb9cff78f7721a07653606eb9624ad33ed46b86688ac04641e6c09bde64498e (pinned 9eb9cff78f7721a07653606eb9624ad33ed46b86688ac04641e6c09bde64498e)
e2 unassigned (re-check, every instance): PASS, 1876 of 1876 pass, publications {'49financial': '2026-10-05', 'inflection': '2026-10-05'}, same date as the cases read: True
e2 unassigned 49financial: 1645 of 1645 (zero-value 888, tie 1645, no model node 1645)
e2 unassigned inflection: 231 of 231 (zero-value 56, tie 231, no model node 231)
e2 unmatched_join at 49financial: reconciles {'arms': {'partitions_balance': 'PASS', 'account_sum_equals_custody_total': 'PASS', 'served_reconcile_reads_reconciled': 'PASS'}, 'remainder': {'amount': 168525497.37, 'reason': '1645 of 7597 custody account(s) carried in Client with membership unattributed', 'units': 'USD'}}
e2 blended_model at cottonwood: reconciles {'account_value': 187724.63, 'partitions': 3}
e2 multi_membership at 49financial: reconciles {'account_value': 2855280.7, 'partitions': 2}
E2-CASES-RECONCILE
rc=0
```

## e3: python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R31_CHECKS/r31_delivered_reads.py e3
```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R31M_FWD5_PROOF_CASES_READ.json@471da6f0b0 sha256 2b61c5a833c761e60b581f4f983f4c2795bc84624494df3a063d45571865f3e5 (pinned 2b61c5a833c761e60b581f4f983f4c2795bc84624494df3a063d45571865f3e5)
FILE org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R31M_UNASSIGNED_RECHECK_20261007.json@6458a5a9d3 sha256 9eb9cff78f7721a07653606eb9624ad33ed46b86688ac04641e6c09bde64498e (pinned 9eb9cff78f7721a07653606eb9624ad33ed46b86688ac04641e6c09bde64498e)
e3 49financial: coverage 5952 resolved of 7597 attempted (1645 unmatched), remainder 168525497.37; assigned_without_custody 19 (17 SmartX-mapped and 2 Tax-traded account(s) absent from custody)
e3 inflection: coverage 627 resolved of 858 attempted (231 unmatched), remainder 40952571.87; assigned_without_custody 35 (35 Eclipse-mapped account(s) absent from accounts_v2)
e3 cottonwood: coverage 475 resolved of 860 attempted (385 unmatched), remainder 352662621.54; assigned_without_custody 0 (0 of 860 overlay account(s) absent from custody)
E3-COVERAGE-DENOMINATED
rc=0
```
