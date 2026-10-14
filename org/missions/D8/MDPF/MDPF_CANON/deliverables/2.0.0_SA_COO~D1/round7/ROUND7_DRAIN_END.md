# MDPF_CANON round 7 -- drain-end packet (2.0.0_SA_COO~D1), 2026-10-14 ~15:4xZ

To `3.0.0_SA_CVO` (L8/L9). Input: the CTO's round-6 analysis `ledger/ROUND_ANALYSIS.round6.md` @65bf603a7a section 4 (msg 5589). Decomposition v7 and eight orders: issuance `879feb7e99`, merged `7df957722b`.
`round-close-check.py --project MDPF_CANON --round 7` reads: 8 of 8 orders complete, proofs 8 of 8 valid, 5 JUDGMENT criteria ungraded, verdict REFUSED (the five below are the only reason).

## 1. Orders, merges and evidence (MEASURED at the merged tree, 2026-10-14 ~15:3xZ)

| order | worker | merge | mechanical result | judgment owed |
|---|---|---|---|---|
| CN-h-1 frontier counts read the newest A4 distribution (WORLD) | ~17 | `9592daf75c` | reader 8 of 8, seams 6 of 6, comparator 5 of 5; pytest 7 passed; the loader prefix is the `legacy_addresses` row `mdpf-portal-gold-account-distribution` (registry `81453d51cf`) and `build_package.py` ships that row's file | AC4 |
| CN-i-1 AUA Trend grouping (portal) | ~18 | outer `0da4e7a7df`; portal candidate `4f100451` on `wk-MDPF_CANON-18-portal`, NOT landed | module 9 of 9, page 8 of 8, data 5 of 5; portal typecheck rc 0, provenance guard OK | AC4 |
| CN-j-1 category-views history leaf (WORLD) | ~23 | `1c8ebf3e5d` | unit 6 of 6, seam 8 of 8, real 6 of 6 over 95 dated objects; publisher tests 19 passed | AC4 |
| CN-k-1 repairs D1-S23 and D1-S24 (direct-act) | ~22 | `be1fb86ee4` | tool 6 of 6, card 5 of 5, pytest 3 passed, guard 5 of 5 | none |
| CN-l-1 Other Models dated carry (WORLD) | ~19 | `72ef4f8a3a` | unit 8 of 8, seams 5 of 5, real 6 of 6 | none |
| CN-l-2 its card text (portal) | ~18 | outer `cb9836f2c1`; portal candidate `34cd12d2` on `4f100451`, NOT landed | helper 7 of 7, page 8 of 8; typecheck rc 0 | AC3 |
| CN-m-1 staged-copy reader census | ~20 | `6ad2e97350` | record 7 of 7, verify 5 of 5; READERS-FOUND, 14 readers, two PARTNER-FACING-CANDIDATE; trail does not cover the bucket, so a zero could not have been proven | AC3 |
| CN-n-1 refusal arm DRIVEN (direct-act) | ~21 (four seats) | `edd4f4f2f6` | grade 6 of 6, served 4 of 4, guard 5 of 5; the run: Global refused whole with the `GLOBAL MIN-FIRMS FOLD REFUSED:` prefix, `errors=['global']`, writes 0, blocked-calls 0, 2886 served object-versions identical before and after | none |

Hygiene once at the drain: gold and canon suites 163 passed, 3 failed; the three are the carry-forward tests of row D1-S1 and read the same 3 failures on a detached checkout of `7df957722b` (before any round-7 merge).

## 2. The real run of the portal cells (the issuer looked at the page)

`/ui-walk` on the candidate build (`wk-MDPF_CANON-18-portal` @34cd12d2, port 5174), Global (All), Snapshot and Trend. Local screenshots only (the ui-walk rule: never committed).
- Total Holdings reads 8,430 (the CTO's corrected figure; my round-6 packet's 8,607 was a wrong-date read, row D1-S24, repaired by CN-k-1).
- Trend legend: the five archetypes, Custom Models, Other AUA, Client Supervised, Client Unsupervised, ETF Strategies, ALT Strategies. Client chips appear on the latest period only, as designed. Before about 2026-05-19 per-model history collapses into one grey Other AUA band.
- Colours: Client Unsupervised and Ultra Short-Term are both orange, and ALT Strategies red sits close to Ultra Long-Term (worker row D1-W18-S7). That is a design judgment for AC4.
- The Other Models "as of" stamp was NOT exercised: the pool is present today, so no value is carried.

## 3. ARMED rows and how each stands (the CVO dispositions)

| row | standing | the issuer's reading |
|---|---|---|
| D1-W21-S1 (CN-n-1 first drive RAISED) | disarm act done; the CVO records it | the cause was my instrument's plant (in-place edits; then a plant inside the builder tripping its own gates), fixed in three amendments; the fourth run refuses Global without a raise |
| D1-W20-S1 (face leak) | ruled | the pre-read sat in the order's RECORD FACE, which the extraction excluded; the worker saw it only by opening the order file to flip its status (the order's `<paths>` names that file). Its counts differ from the pre-read (8,812 files and five code readers against 8,831 and four), so the census is independent. Grade AC3 on the record, not on that row |
| D1-W16-S5 (staged copy unfolded, readers unknown) | open | CN-m-1 found 14 readers, two candidates for a partner-facing surface (`build_portal_gold_accrual.py`, schedule `mdpf-accrual-bridge-daily`); the re-point is NOT in this round and is a pair-owed act; the row stays armed until it is ruled |
| D1-W16-S2, D1-W16-S4 (Other Models carry) | open until the deploy | CN-l-1 is merged and green; the rows disarm on the first scheduled fire after its deploy |
| D1-W17-S3 (naming gate; BLOCKING, INERT) | answered | registry row `81453d51cf`; CN-h-1 committed with the gate passing |

## 4. What waits, and on what

- AC4 of CN-h-1 and CN-j-1 and AC3 of CN-l-2 need served or landed evidence the issuer cannot yet give: the CloudOps deploys (gold package for CN-h-1 and CN-l-1 together; publisher for CN-j-1), each under a never-widen pair (CTO half owed), then the first scheduled fire after each (2026-10-15 13:30Z at the earliest).
- The portal candidate (`4f100451` and `34cd12d2`) is client-facing: landing is `portal-merge-forward.sh` on an approved row with Andrew as approver (CLAUDE.md Portal, fcdfc34843). The issuer asks the CTO to carry the card.
- Gradable now: CN-m-1 AC3 (the record is merged) and CN-i-1 AC4 (on section 2, with the colour notes). The rest follow the deploys.

## 5. What this packet asks

CVO: grade CN-m-1 AC3 and CN-i-1 AC4 on the artifacts named above; disposition the rows in section 3; acknowledge receipt (the L8 packet is unread until you do).
