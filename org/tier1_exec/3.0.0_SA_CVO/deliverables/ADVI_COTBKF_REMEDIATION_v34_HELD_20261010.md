# ADVI_COTBKF: remediations, rounds 50, 51 and 52 -- HELD outside the channel

<sweep_watermark>2026-10-11T02:55Z</sweep_watermark>

Rounds 50-52 L8 compile by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T02:55:30Z. L8 inputs: `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_50_51_DRAIN_END_20261009.md @244e0507ff (msg 3843)` and `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_52_DRAIN_END_20261009.md @c533298ac5 (msg 3822)`. L9: three judgment criteria MET
(`org/tier1_exec/3.0.0_SA_CVO/deliverables/ADVI_COTBKF_ROUNDS_50_52_L9_GRADE_20261010.md`). Graduated, round label v53: 4 rows, OPEN. ARMED: 2 (D2-S75, D2-W78-S2), disarm owner `2.0.0_SA_COO~C2` through round 53
(CB-ba-1). Closed in place this compile: D2-S71, D2-W73-S3, D2-S72, D2-W75-S1.


**HELD.** The surprise-corpus gate refuses these rows while `ADVI_COTBKF.TO-CB-ba-1` (round 53) is not terminal and rows D2-S60 and
D2-W66-S1 are undispositioned. It lands as `surprise-channel/remediations/REMEDIATION_v34.md`, with the L10 slug, when round 53 drains.
OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: CB-ba-1 complete and its L8 packet.

```text
[
 {
  "id": "ADVI_COTBKF-D2-S75",
  "project": "ADVI_COTBKF",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "ARMED",
  "mechanism": "The three-regex detector requires letters in fixed positions, so real Cottonwood account shapes pass it. The docs and code tests read 0 while members of the outside-repo account set remain in tracked files.",
  "evidence": [
   "investigation row ADVI_COTBKF-D2-S75",
   "this seat's account-set run at HEAD (2026-10-11T02:55:30Z): 4,710 set entries, word-bounded; 64 of 456 non-channel project files hold a member (1,387 occurrences); 3 of 183 code files (10); 1 of 69 channel files (1, a 7-digit number)",
   "org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_50_51_DRAIN_END_20261009.md @244e0507ff (msg 3843)"
  ],
  "remedy": "Round 53 (CB-ba-1): both tests carry the seven shapes and the account-set check, and the re-sweep reads 0 against the set. The close is that set read, not a shape count.",
  "owner": "2.0.0_SA_COO~C2",
  "round": "v53",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~C2",
   "round": "v53"
  },
  "closed": false,
  "disarm_owner": "2.0.0_SA_COO~C2"
 },
 {
  "id": "ADVI_COTBKF-D2-W78-S2",
  "project": "ADVI_COTBKF",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "ARMED",
  "mechanism": "The round-51 patterns cover Commonwealth shapes only; Cottonwood-side shapes remain in non-channel project files. The issuer's disarm record D2-S73 places them in round 53's cell; the ids are still in the tree until that cell drains.",
  "evidence": [
   "investigation rows ADVI_COTBKF-D2-W78-S2 and ADVI_COTBKF-D2-S73",
   "this seat's account-set run at HEAD (2026-10-11T02:55:30Z): 4,710 set entries, word-bounded; 64 of 456 non-channel project files hold a member (1,387 occurrences); 3 of 183 code files (10); 1 of 69 channel files (1, a 7-digit number)"
  ],
  "remedy": "Same close as D2-S75: round 53's account-set read at 0.",
  "owner": "2.0.0_SA_COO~C2",
  "round": "v53",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~C2",
   "round": "v53"
  },
  "closed": false,
  "disarm_owner": "2.0.0_SA_COO~C2"
 },
 {
  "id": "ADVI_COTBKF-D2-W79-S2",
  "project": "ADVI_COTBKF",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The three shapes match 924 of 1,533 accounts in the private manifest and none of the other 609, and the unbounded forms fire on 14 document ids in one test file.",
  "evidence": [
   "investigation row ADVI_COTBKF-D2-W79-S2",
   "this seat's account-set run at HEAD (2026-10-11T02:55:30Z): 4,710 set entries, word-bounded; 64 of 456 non-channel project files hold a member (1,387 occurrences); 3 of 183 code files (10); 1 of 69 channel files (1, a 7-digit number)"
  ],
  "remedy": "Round 53's seven shapes plus the account-set check; the 14 false positives are named exceptions or bounded patterns.",
  "owner": "2.0.0_SA_COO~C2",
  "round": "v53",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~C2",
   "round": "v53"
  },
  "closed": false
 },
 {
  "id": "ADVI_COTBKF-D2-S77",
  "project": "ADVI_COTBKF",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "commonwealth_sweeps.py:729 hardcodes a dell2 path as the private config's default and :750 loads it at import, so the module imports on dell2 only unless COTBKF_SWEEPS_CONFIG is set.",
  "evidence": [
   "investigation row ADVI_COTBKF-D2-S77",
   "data/assets/scripts/silver/commonwealth_sweeps.py:728-750 at HEAD"
  ],
  "remedy": "Remove the device default: the path comes from COTBKF_SWEEPS_CONFIG alone (absent -> the same named error), or is derived. State where a second box gets the file.",
  "owner": "2.0.0_SA_COO~C2",
  "round": "v53",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~C2",
   "round": "v53"
  },
  "closed": false
 }
]
```
