# IRPT_DASHBD round 148, workstream B-CW (Cottonwood) -- drain-end packet (2.0.0_SA_COO~C2, 2026-10-16)

FWD-10 cell (a) closed out: the page mirror takes on series contract 0.3.1, and the real Cottonwood publish is read through the page. Issuance `1797e63a16`; merges `c2f31e3f1e` (worker ~418: DB-c-26) and `f3f033ac05` (worker ~419: DB-c-27). Amendment 1 (`356404f569`) added DB-c-28, the PROD promote. Decomposition `org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_B-CW.md` section 17. `python .tools/round-close-check.py --project IRPT_DASHBD --round 148 --workstream B-CW`: `verdict=MAY-CLOSE` (2 orders, 0 judgment). `DBC148-1-AC1` and `-AC2`, `DBC149-1-AC1` and `-AC2` PASS, re-run by this seat (AC1 of the test read made its own fresh S3 read). Push: integrator-only; the workspace merges and this commit are LOCAL.

## What happened this round

- **DB-c-26 (portal, 1 file):** `SERIES_OPTIONAL` is the contract's six names, `SeriesDocument` gains `income_claim?`, `ManifestDocument` gains `calendar_source?`; `iv-e-124` green. Class: **opal-internal**, on the measured built bytes (88 of 88 dist files and 63 of 63 chunks identical, positive control moved 44): `deliverables/2.0.0_SA_COO~C2/prod_promote/DB_C26_BUILD_BYTES_R148.md`. Candidate `cand/dell2/irpt-series-mirror-contract-031` @`a020da0bff`, row `8ddd` approved by the CTO, merged forward: **portal origin/DEV = `34a6baf865`** (MSTR push; my ls-remote read). The PROD-based branch carried seven commits into DEV, not one: the four 92c0 commits, DB-c-26 and the two 40fa commits, all Andrew-approved and already on PROD (disclosed to MSTR).
- **PROD promote of the round 147 sentence (DB-c-28, to the DT):** Andrew's "approve 92c0"; **PROD `8012cd1afbaa` (portal-v2.1.230)**, run `38862904307` success (my own reads: `gh run view` conclusion and head sha, origin/PROD, the peeled tag). The DT's receipt U1 to U4 and ledger CLOSED are theirs; the page read was FIXTURE-ONLY, the sentence is in the served bundle.
- **DB-c-27 (the labelled TEST READ, counts only, read 2026-10-16T06:06:50Z):** 939 series and 939 manifests under `irpt/cottonwood/platinum/reporting/`; all 939 documents read by the page's reader, none refused or threw; **917 accounts print exactly one sentence** (the other 22 carry an empty list), every printed count equals its list's length, longest list 3 days, 2,529 listed days; income is null on every entry of every document and never read as 0; `income_claim` absent on all; history scope `PARTIAL_HISTORY` on all 939; `calendar_source` absent on all 939 manifests. No identifier, key or value is recorded. The 22 accounts and the 917 are the publisher's count; whether the promoted PROD page shows them is for the Act 4 and the daily schedule (CTO msg 9022 condition 1).

## What the CTO's half decides

1. **Every Cottonwood screen will carry "Returns from <date>."** (round 146's note) because all 939 are `PARTIAL_HISTORY`. That is what the rule produces; whether a note on every account is the wanted reading is yours. No change is made.
2. **The next B-CW cell.** By your order of work (msg 8741) it is the 49 Financial FWD-10 coverage census (read-only, like round 145's Cottonwood one); I cut it as round 149 on your word, or on your next analysis for this workstream.
3. Nothing is held for Andrew from this round: the 92c0 PROD promote and the 8ddd DEV merge are closed.

## Standing notes (no cell cut)

- **Income words.** Where a surface first prints the series' income, the sentence is "Income is not broken out for this account's returns." (CTO msg 9159; the old "not reported by the source" words are dropped). No portal surface prints series income today (measured round 147), so there is nothing to word yet.
- **The parked first scheduled Cottonwood report-run read** waits to 2026-10-16T16:00Z (owner this seat; `~D2`'s report build and the publish pair's Act 4).

## Rows

`D2-S111` (this commit) dispositions worker 418's `W418-S1` to `S3` and worker 419's `W419-S1` and `S2` (all INERT, accepted). Nothing ARMED or BLOCKING of this round remains.

## Issuer's own defects this round

1. My orders named the proof instance as `IRPT_DASHBD.TO-DB-c-26.proof_of_spec.json` (shortened after round 147's path-length trouble), but `round-close-check` looks for the instance under the order's full file stem; it read `REFUSED` (proof_bad 2). My first fix, renaming the two instances inside the workers' folders, was refused by the lane gate (`TREE_DELIVERABLES`: a worker folder is not the COO's lane); I took no override, restored the worker folders to their original names, and committed a COPY of each instance under the order stem in my own folder (`deliverables/2.0.0_SA_COO~C2/`, commit `34fa16a248`), which the check reads (one folder level below `deliverables/`). The copies are byte-identical to the workers' instances. Next time the order names the stem the check expects and the slug is short from the start.
2. Round 147's order slug was too long (disclosed in `R147_BCW_DRAIN_END.md`).
3. In dry-running the build-bytes comparison I created scratch worktrees under `C:/dev/g-bld*` and `C:/dev/g-cand148`; each node_modules junction was removed with a non-recursive `rmdir` first, the main `node_modules` was verified intact each time, and the folders are gone.
