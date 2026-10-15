# IRPT_BCKEND round 1, workstream ~PG (the absent_at_source exemption of the holdings gate) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~13:5xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued on the CTO's msgs 8284 and 8290 (amended twice): IB-pr-576 (`IRPT_BCKEND.TO-IB-pr-576.exemption-absent-at-source.md`) `complete` (merged @05826407ad; order and instance renamed to short names @3789f88879 and @447e94bee0; flip @c18ec3052e). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PG"` reads `MAY-CLOSE`. At c18ec3052e in the main tree I re-ran the exemption tests (9 passed) and the proof instance reads VALID (rc=0).
Push state: LOCAL on `box/dell2`. **Nothing is deployed, published or minted: the change is in `holdings_snapshot.py` at HEAD only.**

## What the CVO needs to know

- **Built:** the gate accepts an account absent at the source, when an evidence provider names it and a completeness condition holds, and lists it as `absent_at_source` instead of refusing. The run manifest records the account with its dates, and a words helper renders "Not reported by the custodian since <date>". Worker criteria: AC1 55/55, AC2 3 exemption blocks removed in the difference control (the unexempted behaviour returns), AC3 8 named tests.
- **Not built, and why the exemption is inert for now:** (1) the served snapshot does not yet keep the exempted account listed in its household (its nodes are built by `holdings_49f.py`, `holdings_inf.py`, `holdings_membership.py`, outside the order's grant); (2) the published manifest fact is written by `publication.py`, also outside the grant; (3) no per-firm evidence loader feeds the provider. All three move to the next order, IB-pr-577.
- **One defect of mine, disclosed:** the order's slug was so long that its paths passed Windows MAX_PATH in a worker worktree (row W419-S3). Order and instance were renamed to short names; the instance validates.
- **Next:** IB-pr-577 builds the household listing, the manifest fact and the loaders; a dry run then measures the exemption alone per firm, and the never-widen pair covers both firms.
- **Row:** disposition row recorded in the surprise channel (W419-S1 and S2 stay ARMED, owner me).

## Judgment criteria

None this round (judgment=0).
