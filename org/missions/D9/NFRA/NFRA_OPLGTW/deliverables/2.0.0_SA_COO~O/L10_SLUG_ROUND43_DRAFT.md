# L10 SLUG -- NFRA_OPLGTW round 43 -- DRAFT (2.0.0_SA_COO~O, 2026-10-18 ~15:0xZ), NOT SENT

Status: three of nine orders are open (`OG-ap-42`, `OG-ev-7`, `OG-ap-43`), so the round is not terminal and nothing is sent. This file is the skeleton the slug is finished from; the round-close check (`python .tools/round-close-check.py --project NFRA_OPLGTW --round 43`) must read MAY-CLOSE first.

## 1. The round, by order (state at the writing)

| order | what | state |
|---|---|---|
| `OG-pr-4` | the probe lease pins the firm; the listener refuses a mismatched firm (403 `probe_firm_refused`) before the tool runs, and a lease without a valid firm as malformed; drained `01c182170a`; my runs AC1 12 of 12, AC3 30 both orders, proof VALID | complete |
| `OG-en-31` | `test_ogpr1_ac13`: every refusal pulls the whole body before `http.response.start`; the mutant check FAILED/PASSED/restored byte-equal; drained `30e0cfc889` | complete |
| `OG-sec-2` | `graph.call` refuses a non-https, non-`graph.microsoft.com`, user-info or odd-port absolute URL before any client; my AC3 file set was the issuer's error (row `Z-W152-S1`, ruled `Z-S390`), amended; drained `ff2c1969f8` | complete |
| `OG-sec-3` | SSRF audit over six modules, 21 sites, 0 controllable, CLEAN; drained `c26cd96d5f` | complete |
| `OG-ev-8` | inline audit-write table: 81 sites, 68 on the loop, 1 off, 12 unknown; every timeout botocore's default; frequency ABSENT (the lake key names no tool); drained `273fd63f3d` | complete |
| `OG-ev-9` | limiter trace: 120 per 60 s, keyed on the validated principal key, Retry-After set, fail-open; 1 refusal row in 24 hours; recommendation no change; drained `fb6d78084b` | complete |
| `OG-ap-42` | ninth release (the four take-list files) on dell1's `ck-3` base `922ee425fe`; Phase A with the applier (release `a0c83303ee` cut; the four files are blob-equal to trunk) | open |
| `OG-ev-7` | the peers call in the service under one firm-pinned lease; after `OG-ap-42` CLOSED | open |
| `OG-ap-43` | the landing of `922ee425fe` (carrying `6575999df5` and `3b94a83e05`) on `box/sitez`; GO sent | open |

## 2. What the round delivered against the endpoint

(To write at the close from the CLOSED ledger and the served record.)

## 3. Rows

Rulings: `Z-S388` (earlier), `Z-S390`, `Z-S392`. CVO: `Z-S375` and `Z-S338` DISARMED. Carried ARMED: `Z-W94-S2`, `Z-S177` (traced), `Z-W155-S1`. Observations carried to round 44: `Z-S391`, `Z-W153-S2`; items for the CTO and MSTR: the audit-lake registry row, the device's missing hashed account-id list.

## 4. The enrichment list this seat proposes for round 44

Full text and source rows: `deliverables/2.0.0_SA_COO~O/ROUND44_CANDIDATES_DRAFT_20261018.md`.
