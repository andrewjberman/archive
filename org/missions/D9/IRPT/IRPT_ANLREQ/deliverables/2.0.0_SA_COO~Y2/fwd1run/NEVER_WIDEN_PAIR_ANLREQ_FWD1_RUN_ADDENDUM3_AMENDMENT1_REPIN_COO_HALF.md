# IRPT_ANLREQ FWD-1 run, ADDENDUM 3 AMENDMENT 1 -- re-pin two start-state reads (R0d, R0e) to the releases that now stand in front of the window: the r35L status Lambda and the resident r34C -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No run-3 order is cut until the CTO half of addendum 3 (signed, blob `64884b3338965c79a962c3f40cdb5cde44ad5811`, `@bf5eb93047`) AND the CTO half of THIS amendment are signed on this file's blob, and both releases below have closed.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-16. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Amends: `fwd1run/NEVER_WIDEN_PAIR_ANLREQ_FWD1_RUN_ADDENDUM3_THIRD_WINDOW_COO_HALF.md` section 5, reads R0d and R0e ONLY. Nothing else of addendum 3 changes: W7 (the driver, sha256 `455f6609...`, 67 selftest cases), W8 (the probe, its five candidates and the selection rule), the address `fwd1-staff-r41b@opal.invalid`, the STOP conditions the CTO set (msg 9089), sections 6 to 8.

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record this seat opened (named); RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read.

## 1. Why the pins moved (RECORD)

Addendum 3 was written against the first signed form of the r34 packet (R34B) and the r33 `irpt-status`. Since then `~G2` has changed what the window will stand on, and each change alters a digest the window reads at step 0:
- **`irpt-status` becomes r35L** (RECORD, `NEVER_WIDEN_PACKET_R35L_STATUS_20261016.md`, ledger `irpt-status-r35l-20261016`, AQ2 order `AR-g-117`): one Lambda code release carrying the closed hop-failure code and words (C-HOP-FAILURE, PRD v0.20/v0.21). Pin `90b69dcb12cdfedc786966ab33d034bf14229396`; zip sha256 `f937190d69b013bbafdec530a2cdbe8e7d656cac908a42bed779cd0730faab80`; **CodeSha256 `+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A=`**, 368309 bytes, 49 members, 3 changed against the r33 build (`durable_job.py`, `owned_status.py`, `status.py`).
- **The resident r34 is rebuilt a third time (r34C)** (RECORD, `NEVER_WIDEN_PACKET_RESIDENT_R34C_20261016.md`, COO half git blob **`db596c0725c73bcecce2ec0d08027c23e4f10ca5`**, commit `1c2288f8a5`): 314 members, 10 changed against r32 and 4 added (the door's yfinance checker, the swap pass, the dated pool, `yahoo_history_days.py`, and the resident writers of `hop_failure` in `durable_job.py` and `resident_worker.py`); pin `c43f8fc13a950dd031f2c5c79a7ab0e11d730fd0`; tar `irpt-resident-0485393f3a-r34.tar.gz` sha256 **`56410a26bafe530b8765f4fe50de1ac076000f90478b1c55c4ccd66034b1f725`**, 1,119,934 bytes (the earlier R34B tar `861e6900...` and COO blob `f787a4eabc...` are superseded: the first install of that form was rolled back at V2). Its apply protocol, step 1, requires the library delivery closed first: `yfinance` 1.2.0 and its Linux cp312 closure installed in the host's `pydeps` under its own pair (CTO msgs 9066, 9070, 9075).

## 2. The two reads, restated (these replace R0d and R0e of addendum 3 section 5)

- **R0d:** `irpt-ycharts-generate` CodeSha256 `kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=` (release 33, unchanged) AND `irpt-status` CodeSha256 **`+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A=`** (r35L), the applier reading both with `get-function` and the status key's latest S3 version hashing to the zip sha256 above. Any other `irpt-status` digest (the r33 value `OOez8YSm...` above all: r35L not applied) ABORTS. **Status of the pin at this writing: MEASURED live-equal** (this seat read AQ2's after-record `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r35l/A_AFTER_R35L.txt`, commit `7e022fc37d`: `irpt-status` live CodeSha256 `+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A=`, 3 of 49 members differ from r33, ledger `irpt-status-r35l-20261016` CLOSED); the applier re-reads it at R0.
- **R0e:** the resident root is `0485393f3a-r34` installed from the r34C tar (sha256 `56410a26bafe530b8765f4fe50de1ac076000f90478b1c55c4ccd66034b1f725` read from the install record and from the host), the applier's record of the re-apply (R34C) reads V1 green AND **V2 SPY KEPT through the door's checker**, the library delivery's record reads CLOSED with `yfinance` importable by the resident's interpreter, `opal_pricing` false, the producer list `andrew@opalinvest.com` and `fwd1-staff-r41b@opal.invalid`, the queues readable (depths printed; the DLQ message of window 2 may remain and is not touched). A record that names the R34B tar or any V2 other than KEPT ABORTS.

## 3. What this adds to the blast radius (the delta over addendum 3 section 4)

Nothing is added to what the window moves: the window still mints one internal viewer for the probe, one staff row for the run, drives the page and reads. Two things change in what the window MEETS:
1. The ticket page can now show a failed hop as the step and what happens next (C-HOP-FAILURE; the page read is `~V2`'s portal cell, and whether it is in this window's DEV build is INFERRED not read); the status route returns the closed code and its words for a failed job.
2. The resident writes `hop_failure` on the failure paths of the packager and the ready-signal send; a failure in the window is therefore recorded on the job and returned by `irpt-status`. The run's record names it; no retry in the window.

## 4. Limits named

- NOT read: whether r35L and the library delivery and R34C have closed (they are gates, read at R0); the hop-failure words on a live failed job (no failure is driven in this window).
- The classifier is still not in r34 (CTO addendum 6).

## 5. Owed before any run order is released

1. The CTO half on this file's blob (the two restated reads), and the CTO's re-sign of the R34C packet on its own blob (`db596c07...`) as `~G2`'s ledger requires.
2. r35L closed; the library delivery closed; the R34C re-apply closed with V2 SPY KEPT.
3. The run order to `0.7.0_AE_CloudOps~AQ2`, carrying a `# pipeline-override:` line, cut by this seat only after (1) and (2).
