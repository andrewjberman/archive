# L10 SLUG -- NFRA_OPLGTW round 47 (DRAFT, 2.0.0_SA_COO~O, started 2026-10-20 ~13:5xZ; NOT SENT)

**To `1.0.0_SA_CTO~Z`, only after every task order of the round is terminal and `python .tools/round-close-check.py --project NFRA_OPLGTW --round 47` reads `MAY-CLOSE`.** Sections marked OPEN are not yet measured; nothing below is a claim until it is filled from the order files, my own check runs or the seats' committed records.

## 1. The round, by order (state at the draft)

| order | what | state |
|---|---|---|
| `OG-fc-1`, `OG-ix-1`, `OG-sx-1`, `OG-rt-1`, `OG-nf-1`, `OG-sz-1`, `OG-mg-3` + `OG-tp-1`, `OG-sz-2` | the build cells (workers `~166` to `~173`) | complete, drained (`6c747e7e50`, `d1c30de58b`, `77834d2acb`, `fd69a7cb77`, `fb46590b00`, `0dad6e544b`, `2d2a56cb04`, `8a201cfdc4`) |
| `OG-ls-1` | ListBucket narrowing | complete (ledger `nfra-oplgtw-grants-ls1` CLOSED 11:02:38Z) |
| `OG-mg-4` | the in-flight cap 4 to 26 (the CTO's C1 ruling, msg 36195) | complete (worker `~174`, drained `c0a0ee2e9c2`; my `mg4.AC1` and `mg4.AC2` PASS) |
| `OG-gc-1` | `client_*` tools for Alyssa and Menachem: facts first | complete on Phase A facts (row Z-S432: no `person_access` record can admit the tools; the cell is round 48, the CTO's msg 36202) |
| `OG-gm-1` | Menachem's Schwab grant | SUPERSEDED for round 47 (row Z-S433: no verified identity record, gate G-E) |
| `OG-gv-1` | Andrew's Schwab grant to `accounts ["*"]` | OPEN: Phase A done, three halves SIGNED at ask `637db69736ab`; Phase B only after `OG-rl-18` AND the `/callback` exemption release are live |
| `OG-ed-1` | master-admin exemption on the legacy `/callback` consent branch (the CTO half of `OG-gv-1`, option 2) | complete (worker `~175`, drained `17c53cdd2cb`; my `ed1.AC1`, `AC2`, `AC3` PASS on the merged tree; rows Z-S437) |
| `OG-rl-17` | batch16 release | OPEN: re-cut at the cap 26 (release `8e3eddf959`, ask `291ffc35747a`), all three halves SIGNED, Phase B GO sent for window 2026-10-21 06:00Z |
| `OG-mp-1` | mount `admin_people_access.routes` in `app/admin_api.py` (the CTO's ferry 17:30Z, NFRA_MCPORTAL v0.10) | complete (worker `~176`, drained `a4197b93aed`; my `mp1.AC1`, `AC2`, `AC3` PASS on the merged tree; no rows) |
| `OG-rl-18` | batch17 release (master-wide scope plus the `/callback` exemption plus the mount: ten files) | OPEN: staged, not before 2026-10-22 06:00Z |

## 2. What the round delivered against the endpoint -- OPEN

To fill from the live read-backs after `OG-rl-17` and `OG-rl-18` close.

## 3. Rows

- **Rulings this round (mine):** `Z-S429`, `Z-S430`, `Z-S434` (adjudicates `Z-S431`, `Z-S432`, `Z-S433`), `Z-S435` (worker rows `W174-S1`, `W174-S2`), `Z-S437` (`W175-S1`). Filed, not ruled: `Z-S436` (relayed, see section 4).
- **Carried ARMED:** `Z-W169-S2` (Teams-poll cursor tie at a page cut), `Z-S420`, `Z-S410` (disarm on the live proofs if `OG-rl-17` closes).

## 4. The enrichment list this seat proposes for round 48

- **The per-firm client grant shape (CTO msg 36202):** a grant names the (vendor, firm) pairs a principal may read through the `client_*` tools; `decide()` admits a `client_*` call only inside those pairs; proof: one granted pair PASS, one ungranted pair refused, master admin unchanged; its own release and never-widen ask naming Alyssa's and Menachem's pairs as the first grants.
- **Menachem's identity (gate G-E)** and then `OG-gm-1` re-cut.
- **A call start or duration field in the audit record** (the CTO's C1 ruling): without it true overlap is not computable.
- **Alyssa's grant to `accounts ["*"]`** (the CVO's note, msg 36209), after `OG-gv-1` reads back.
- **`portal_get_security_scan` AccessDenied on an absent-universe request** (row Z-S436, relayed by `2.0.0_SA_COO~MI`, round 24 case K2-31; NOT reproduced by this seat; test first whether `OG-ls-1`'s ListBucket narrowing removed the portal prefix's listing).
- **The gateway edit for the Schwab move to `schwab/49financial/` (Andrew-direct ~17:0xZ via the laptop; the CTO~Z ferry 17:13Z names this seat owner, `~NFRA1` applies it under its own never-widen pair in the cutover window):** the contract's `data_prefixes` and `completion_prefixes` in both copies, `app/refs/DATA_CATALOG.yaml`, `client_adapter_schwab.py`, the reader IAM `.tf`, tests; master-level fencing inside the firm folder must hold; read back Alyssa's 0840 grant and `OG-gv-1`'s `["*"]` resolution after the cutover. ANSWERED 17:22Z by ferry (laptop CTO as PRD owner, msg 109948, and COO~SB, msg 109949; relayed by `0.0.0_AB_MSTR~Z`, not measured by me): silver, meta and `_ops` move for `08403355` ONLY (PRD v0.9 C-TIERS @3941c46886); `08242234` and `08335338` stay at `schwab/<master>/`; silver key `schwab/49financial/silver/<table>/date=YYYY-MM-DD/08403355.parquet` replacing `data.parquet` (18 tables); fixed-name meta objects take the `08403355` prefix the same way; FENCE BY FILE NAME, not column (the reader IAM statement per master: `schwab/49financial/silver/*/date=*/08403355.*`). UPDATE 17:47Z (COO~SB msg 109971 via the laptop MSTR, relayed, not measured by me; PRD v1.0 C-TIERS and the CTO's ruling on rolling objects): meta and `_ops` become the builder's STATE tier in the FIRM bucket `s3://opal-data-49financial/schwab/49financial/state/<table>/date=D/<master>.<name>` (tables: complete, conversions, pulls, backfill_status, daily_pull), so the contract's `completion_prefixes` and every meta reader point at `opal-data-49financial` (a bucket the gateway reader role does not read today as far as this seat knows: the reader IAM gains a per-master, file-name-fenced read on it, a widening for the never-widen pair); silver stays in `opal-data-assets`; rolling objects (`{master}.last_run.json`, `{master}.backfill-status.json`) take date = the UTC date of the write and readers take the NEWEST partition at or before today (`family_depth.py`'s backfill-status read is in the edit set). THE CTO~Z's CONDITION on that grant (ferry 17:49Z): the gateway's FIRST grant on `opal-data-49financial`, a widening under the cell's never-widen pair: `s3:GetObject` only, on `arn:aws:s3:::opal-data-49financial/schwab/49financial/state/*/date=*/08403355.*`; `s3:ListBucket` conditioned on the prefix `schwab/49financial/state/`; no bucket-wide read and no write; each master added later is one more resource line in its own ask; the cross-firm guard's enumeration (`.tools/ds-precommit-check.py` `_CROSS_FIRM_FOREIGN_BUCKETS` / `_KEY_PREFIXES`) must accept the gateway as a multi-firm reader of that bucket, or the gate edit goes in the same cell. STILL OPEN: the DATE (none yet; COO~SB's round-4 cells first, then the CloudOps lane). The CTO~Z's condition (ferry 17:22Z): from day one the gateway's reads under `schwab/49financial/` match the master's file name (`<master>.parquet`), never the folder alone; the cell's proof PLANTS a second master's file in a test tree and the reader must ignore it for a 0840-only grant, so a later landing of 0824 or 0833 widens no grant and changes no code. The gateway cell is cut when the date and names arrive; its Phase A is a read-only census of every code path that builds a Schwab prefix from the master.
- **FWD-29 (NFRA_MCPORTAL v0.10): `person_access` and the data grant admit through ONE rule** (changes `decide()`; joins the per-firm client-grant cell above).
- **Advisor tables per vendor (the CTO's ruling `CTO_RULING_ADVISOR_TABLES_PER_VENDOR_ROUTING_20261020_Z.md` on CRO~Y's brief @1ce8848c4b; ferry 18:03Z), seven code items:** #3 Orion `custodianName`; #4 the Cottonwood `--` strategy; #5 Eclipse `modelId` on the account path; #6 Schwab resolve by LAST FOUR DIGITS (never the title; `master_admin` only until the per-firm grant; under never-widen); #7 Commonwealth fees derived from transactions; #9 Orion fees as separate charges, credits, adjustments and net lines; #10 the `TypedOverCap` envelope. The proof for each is a live call compared with the newest partition. (#1 rides `OG-rl-17`'s read-back: `W/rl17_deployed_vs_head.json`.)
- The CVO's test that the hand-typed IAM source list equals the silver families; the Teams-poll cursor tie (`Z-W169-S2`); the extra S3 read cost of `news_for_security`.

## 5. For other seats -- OPEN

Push state: LOCAL on `box/sitez` (not pushed by me; origin head not re-measured).
