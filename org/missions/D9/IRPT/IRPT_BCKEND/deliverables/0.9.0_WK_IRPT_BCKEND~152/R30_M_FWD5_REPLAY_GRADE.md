# R30 M FWD-5 replay grade (0.9.0_WK_IRPT_BCKEND~152, TO-IB-m30-301)

Read: delivered file, 2026-10-05 publications; no AWS called.

## c1 (rc=0)
```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R30M_FWD5_REPLAY_READ_2.json@8b83fd1d6f sha256 afa19a65eb338c6adc72be8684e81c51f9f4c2347fea7d5584e78b3cbe884c52 (pinned afa19a65eb338c6adc72be8684e81c51f9f4c2347fea7d5584e78b3cbe884c52)
c1: account acc_015d15b45d7a8ac71f951a67 value 779002.51, 2 partitions, 0 unbalanced, 0 faults
C1-TIES
```

## c2 (rc=0)
```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R30M_FWD5_REPLAY_READ_2.json@8b83fd1d6f sha256 afa19a65eb338c6adc72be8684e81c51f9f4c2347fea7d5584e78b3cbe884c52 (pinned afa19a65eb338c6adc72be8684e81c51f9f4c2347fea7d5584e78b3cbe884c52)
c2: 29 of 29 Cottonwood accounts holding SPYI or PSLV tie; per symbol {'SPYI': 20, 'PSLV': 9}
C2-TIES
```

## c3 (rc=0)
```
FILE org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_MVP_M/R30M_FWD5_REPLAY_READ_2.json@8b83fd1d6f sha256 afa19a65eb338c6adc72be8684e81c51f9f4c2347fea7d5584e78b3cbe884c52 (pinned afa19a65eb338c6adc72be8684e81c51f9f4c2347fea7d5584e78b3cbe884c52)
c3 49financial: arms {'partitions_balance': 'PASS', 'account_sum_equals_custody_total': 'PASS', 'served_reconcile_reads_reconciled': 'PASS'}; account sum 1825384091.11 vs served custody total 1825384091.11; 15187 partitions, 0 unbalanced
c3 inflection: arms {'partitions_balance': 'PASS', 'account_sum_equals_custody_total': 'PASS', 'served_reconcile_reads_reconciled': 'PASS'}; account sum 208044040.13 vs served custody total 208044040.13; 2343 partitions, 0 unbalanced
c3 cottonwood: arms {'partitions_balance': 'PASS', 'account_sum_equals_custody_total': 'PASS', 'served_reconcile_reads_reconciled': 'PASS'}; account sum 545819721.23 vs served custody total 545819721.23; 2389 partitions, 0 unbalanced
c3: firms denominator 3
C3-RECONCILES
```
