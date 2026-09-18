# IB-rtc-1 -- RT5-AC2 repaired from the sibling cell's host reading

**Worker:** `0.9.0_WK_IRPT_BCKEND~1`  **Branch:** `wk-irpt_bckend-3-1`  **Worktree HEAD at hand-off:** `e9dc18f3021be6e8f93e933ed3ad48778d27daf4`
**Deliverable:** an APPEND to `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/IRPT_BCKEND.TO-IB-rt-5.the-gold-first-mint-bundle-declared-and-minted.proof_of_spec.json`, criterion `RT5-AC2`, `output_evidence` field.

## R31-AC1 and R31-AC2 (mechanical)

Both PASS BY OUTPUT. See `IB-rtc-1_R31-AC1_output.txt` in this same folder for the verbatim invocations and their deciding lines (`VALID (rc=0)` and `SIBLING-CITED`).

## R31-AC3 (judgment -- recorded for `3.0.0_SA_CVO`, no verdict set here)

**Which of RT5-AC2's three sub-questions the sibling's record answers as a FACT, and which it does not:**

1. **THE HOST -- ANSWERED AS A FACT.** Row `IRPT_BCKEND-W2-S49` measured, directly on the host via SSM command `fb070815-519e-4699-9a6b-193267476d25` (`Status Success rc=0`), the caller identity `arn:aws:sts::313476888478:assumed-role/mdpf-daily-runner-ec2-role/i-02448edb624a7a7cf`. That is the same host `IB-rt-6`'s deployed dispatch targets in production (`battery_ib_rt_6.result.md` arm (a): three real SSM command ids dispatched to this mechanism; arm (d) runs the import check on it). RT5-AC2's "which host will execute them" is no longer undetermined.

2. **PANDAS -- ANSWERED AS A FACT, TWICE.** Row `IRPT_BCKEND-W2-S44`'s on-host stdout: `boto3 1.42.97, pandas 2.3.3 and jsonschema 3.2.0 ALL RESOLVE`. A later on-host read in `battery_ib_rt_6.result.md` (run at HEAD `5d71d45442`, after amendment H's `ids.py` distribution landed) reprints `dep pandas 2.3.3` alongside `dep boto3 1.42.97`, `dep pyarrow 21.0.0`, `dep jsonschema 3.2.0` and `IMPORT-OK first-party modules resolved: trading_calendar, ids, contract`. Pandas resolving on this host is measured, not inferred, on both reads.

3. **THE SILVER REGISTRY -- ANSWERED AS A FACT, AND THE FACT IS MIXED, NOT A CLEAN YES.** Row `IRPT_BCKEND-W2-S49` measured six named silver source prefixes plus three firm destination prefixes from the host's own identity: 2 of 6 source prefixes read `READ-OK` (`opal-data-inf/silver/api_dims/accounts_v2/`, `opal-data-assets/blackdiamond/cottonwood/silver/fact_allocations/`), 4 of 6 read `READ-DENY` (`AccessDenied`), and 0 of 3 firm destination prefixes are writable. So "does the host's tree already carry the silver registry" is measured, and the measured answer is NO as a whole -- the host carries a partial slice, not the registry the runner needs to complete a build. This is consistent with `battery_ib_rt_6.result.md` arm (b), which reads `0 of 3` firms with a landed directory artifact, BLOCKED on this same row.

**Nothing in the three sub-questions is left as "not measured by any sibling cell."** All three are answered as facts by rows `IRPT_BCKEND-W2-S49` and `IRPT_BCKEND-W2-S44`, cross-read against `battery_ib_rt_6.result.md`.

**Whether anything in IB-rt-5's own record contradicts the sibling's reading:**

No measurement disagrees -- but one thing has moved between the two records and is worth the CVO holding it. IB-rt-5's own `RT5-AC1` evidence certifies a **two-member** bundle (`directory_runner.py`, `holdings_snapshot.py`; ETag `cd188f6edb7270300a7409d66f9a3432`) and its own `RT5-AC2` text (unchanged by this append) states "the bundle carries 2 files and zero dependencies." The sibling's record shows that scope was **since amended twice by a different cell** under the CTO's own H3 distribution-vs-definition ruling (row `IRPT_BCKEND-S49`): `IRPT_BCKEND-W2-S49` reads a **3-member** tarball (`ids.py` added) and `battery_ib_rt_6.result.md` reads a **4-member** bundle (`trading_calendar.py` also added; bundle sha256 `d949b7881c...`), which is what the deployed function currently dispatches and what closes the `ModuleNotFoundError` this same cell's original read left open. So: IB-rt-5's `RT5-AC1` PASS describes the object AS MINTED AT THAT TIME, correctly; it does not describe the object currently exercised in production, and the sibling's host reading is a reading of the LATER, amended object, not of IB-rt-5's own two-member artifact. Neither record is wrong at its own vintage; the scope moved between them. This is not a fact this cell adjudicates -- it is named here because R31-AC3 asks whether IB-rt-5's own record contradicts the sibling's, and the honest answer is "not a contradiction, a supersession," which the CVO may want to weigh alongside the PASS status of `RT5-AC1`.

No verdict is set by this row or this file; `status_reason` in the appended `RT5-AC2` row already names `3.0.0_SA_CVO` as grader at L9, unchanged by this append.
