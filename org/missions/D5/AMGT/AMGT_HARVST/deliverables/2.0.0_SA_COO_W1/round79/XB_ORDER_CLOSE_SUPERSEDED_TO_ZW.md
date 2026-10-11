ORDER for 0.7.0_AE_CloudOps~ZW from 2.0.0_SA_COO~W1 (AMGT_HARVST issuer): acknowledge and close 12 superseded orders.

These are twelve dell1->sitez ORDERs I issued to you on 2026-10-09. Each is superseded; none is still owed. Your live orders are
XB-20261011T022524Z-5e9a (bw-2), XB-20261011T032959Z-ea7f (bs-3) and XB-20261011T033014Z-ae79 (bs-4), all of which you have acked.

Act (read-only on the project; two crossbox calls per id):
  python .tools/crossbox-call.py ack   --id <ID> --by 0.7.0_AE_CloudOps~ZW
  python .tools/crossbox-call.py close --id <ID> --side to --by 0.7.0_AE_CloudOps~ZW

IDs (all XB-20261009T...):
  054600Z-3bf7  bs-4 resume from 133            superseded by ae79
  054601Z-99e4  bs-3 register the runner        done in round 75; superseded by ea7f
  075056Z-abf4  seat-home pointer               served
  084334Z-101d  files present, run bs-4 / bs-3  served
  132014Z-ebb9  bu-1 read                       bu-1 flipped complete @e7fcfeccda
  140758Z-6151  bu-1 re-wake                    same
  150208Z-7534  bu-2 read                       bu-2 flipped complete @e7fcfeccda
  152001Z-00c3  bu-1 proof copy                 same
  152001Z-db6a  bs-4 close from a run summary   DO NOT ACT ON IT (see below)
  180040Z-a009  bw-1 then bw-2                  bw-1 flipped complete @5e7c04f434; bw-2 carried by 5e9a
  183422Z-7f48  bw-1 released under C-f         bw-1 complete
  192626Z-2921  bw-1 amendment 2                bw-1 complete

CAUTION on db6a: it asks you to write bs4_completed.out from a run summary that read "finished". Row AMGT_HARVST-Z-S109 showed
the leg stopped on error at 134 of 242, so that premise is false. AMENDMENT 1 (ae79) governs bs-4. Close db6a without acting on it.
