# `HVST-v-2` session log -- `0.9.0_WK_AMGT_HARVST~22`

**Worktree:** `C:/tmp/wk-hvst-v2`, branch `wk-harvst-7-22`, base `3af3761b0c`.
**Placeholder:** the order declares `<placeholders>MAIN_TREE</placeholders>`; every invocation below carries it
EXPANDED to `C:/Users/Opal Bloomberg/Desktop/ajb_workspace`, which is the expansion the spawn face gave.
**Bound:** every invocation run under `timeout 900`. No invocation timed out; no invocation was retried.

---

## 0. FIRST ACT -- the bar, and `HVST-v-1`'s fix

- `git rev-parse --abbrev-ref HEAD` -> `wk-harvst-7-22`; `git rev-parse HEAD` -> `3af3761b0c465335ea3590656d7bd8f1939b6dbf`; `test -d org && test -d .tools` -> `TREE-OK`.
- **`HVST-v-1`'s fix is present, and here is how that was confirmed** (three reads, not one): (a) `grep -n "_null_empty_mappings" lib/opal_data_harvest/silver_from_bronze.py` prints it DEFINED at `:292` and APPLIED at `:314`, `:316`, `:323`, `:357` -- the applied line is `rows.append({key: _null_empty_mappings(value) for key, value in row.items()})` inside `listing_hit_rows`; (b) `git merge-base --is-ancestor 3dba19e7cb HEAD` -> rc 0 (`ANCESTOR-YES`), so the drain commit named in the cell is in this branch's history; (c) `git show --stat 3dba19e7cb` names `lib/opal_data_harvest/silver_from_bronze.py | 33 ++-`. **The module path in the cell's text is `lib/research/harvest/silver_from_bronze.py`, which does not exist; the file is `lib/opal_data_harvest/silver_from_bronze.py`.** That is a path detail inside the same repo, resolved by reading the drain commit's own stat rather than by hunting, so it is recorded here and not as a row.
- Section 3 paths: `surprise-channel/investigations/INVESTIGATION_v1.md` and the task order EXISTED; the deliverables folder `deliverables/0.9.0_WK_AMGT_HARVST~22/` and the ledger file `ledger/VENDOR_CALLS_0.9.0_WK_AMGT_HARVST_22.md` DID NOT and were created by this cell, as the order instructs ("create it").
- The runtime root `C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest` exists and holds `secrets/`, `progress.sqlite3`, `harvest_listing/`. It was READ, never copied into the repo, and nothing under it is committed.

## 1. WHAT WAS HELD, measured before anything ran

`progress.sqlite3` (opened `mode=ro`) held ONE pending `harvest_listing_outbox` row, not twenty:
`(3, 'sa', 'LNVGY', 1, '2026-09-26T02:18:20.056214+00:00', 'ArrowNotImplementedError', attempts 1, retry_at 1790389501.22)`.
That ONE page yields TWENTY `listing_hit` rows (`page[size]=20`), which is the cell's "20 sa listing rows"; the
COO's ledger says the same ("The 20 listing rows remain `pending` in the outbox"). `retry_at` was already in the
past at run time (now 1790412967), so the row was DUE and no clock had to be moved.

## 2. AC1 -- the held rows reach silver, with NO vendor call

Invocation: `cd "$(git rev-parse --show-toplevel)" && python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~22/scripts/ac1.py`
(full output: `ac1_output.txt`; machine-readable: `ac1_before_after.json`).

| instrument | BEFORE | AFTER | delta |
|---|---|---|---|
| silver `listing_hit` rows, sa | 0 | 20 | **+20** |
| silver `listing_hit` rows, wsj | 20 | 20 | +0 |
| silver `listing_hit` rows, barrons / bbg / ft | 0 / 0 / 0 | 0 / 0 / 0 | +0 each |
| bronze `news_listing` objects, sa | 1 | 1 | +0 |
| silver `listing_hit` part files, sa | 0 | 1 | +1 |
| outbox pending listing rows | 1 (`sa`) | 0 | -1 |

Producer output, VERBATIM (one line, rc 0):

```
{"results": [{"listing_id": 3, "status": "uploaded", "bronze": {"skipped": true, "existing": ["seeking-alpha/harvest/bronze/news_listing/date=2026-09-26/25e5656d4c2adc9c7ff40aeae172d70684824255288810e16f8a219ebc00b384_p1_20260926T021820Z.json"]}, "silver": {"written_rows": 20, "skipped_unchanged": 0, "parts": ["s3://opal-data-harvest/seeking-alpha/harvest/silver/listing_hit/date=2026-09-26/part-20260926T021820Z.parquet"]}}], "remaining_pending": 0}
```

**`HVST-v-1`'s fix works on REAL sa bytes.** The same call raised `ArrowNotImplementedError` at 02:1xZ on these
exact bytes (row `AMGT_HARVST-Z-S28`); it now writes 20 of 20 rows. The bronze delta is +0 BY DESIGN -- the bronze
object was already put in round 6 before the parquet raise, so `put_listing_bronze` returned
`{"skipped": true, "existing": [...]}` on its own dedupe check. **No vendor request was made:** `upload-harvest`
reads the local outbox and writes S3 only (`__main__.py:195-211`), and the event log gained no `http` row.

## 3. AC2 -- the bounded capture, its CEILING, and the ledger

### 3a. The ceiling, MEASURED BEFORE the call (zero network)

`scripts/ac2_ceiling.py` (output `ac2_ceiling_output.txt`, `ac2_ceiling.json`) reads `universe(config)` and two
local JSON files only:

```
--all-securities resolves: 89 securities
  carry a usable sa_symbol : 25 of 89
  no sa_symbol, has ticker : 19 of 89
  carry NEITHER            : 45 of 89
  SUBTRACTION CHECK: 25 + 19 + 45 = 89 (must equal 89)
  carry a usable ticker, WHOLE POPULATION (the amendment's 32): 32 of 89
  of which also carry an sa_symbol: 13 -- so ticker-only = 19
```

The amendment's 89 / 25 / 32 / 45 ALL reproduce. Its "32 carry a ticker" is the whole-population count; the
disjoint ticker-only slice is 19, and both are printed so the two numbers are not read as a discrepancy.

**AND A CEILING THE AMENDMENT DOES NOT NAME:** `--max-jobs` caps JOBS, and `jobs = securities x publishers`
(`worker.py:332`, `:341`). With one publisher, `--max-jobs 8` executes **8 of 89** jobs from a persistent
per-plan cursor (cursor 0 here), so ONE invocation can attempt at most 8 names -- filed as
`AMGT_HARVST-Z-W22-S1`. The 8 the cursor selected were ASML, Adobe, Air Liquide, Alibaba, America Movil,
AstraZeneca, BB Seguridade, BNP Paribas -- **8 of 8 carrying a usable `sa_symbol`, 0 not.**

### 3b. The capture

Invocation, LITERAL, with `MAIN_TREE` expanded:

```
cd "$(git rev-parse --show-toplevel)" && python -m lib.opal_data_harvest run --publishers sa --harvest-grammar --runtime-root "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest" --all-securities --max-jobs 8 2>&1 | tail -40
```

Its whole stdout was 8 lines (`ac2_run_output.txt`), so `tail -40` truncated nothing. VERBATIM, first and second:

```
{"event": "job_finished", "publisher": "sa", "security_key": "security-81a74ed057551e58", "status": "error", "accepted": 2, "result": "C:\\Users\\Opal Bloomberg\\Desktop\\ajb_workspace\\.runtime\\opal-data-harvest\\runs\\20260926T094447Z-sa-ee1fa71c16.json", "at": "2026-09-26T09:47:18.904603+00:00"}
{"event": "job_finished", "publisher": "sa", "security_key": "security-37dddff4d4357038", "status": "cooldown", "accepted": 0, "result": "...20260926T094718Z-sa-fb53f6e8d2.json", "at": "2026-09-26T09:47:18.906144+00:00"}
```

**THE SPLIT, each with its denominator:**

| quantity | value |
|---|---|
| resolved by `--all-securities` | 89 |
| carrying a usable `sa_symbol` (the population ceiling) | 25 of 89 |
| ATTEMPTED by this invocation (the job cap) | 8 of 89 |
| SKIPPED for a missing symbol | **0 of 8** (all 8 carried one) |
| actually QUERIED against the vendor | **1 of 8** |
| suppressed by the publisher cooldown | **7 of 8** |
| RETURNED rows | **1 of 8** -- 20 listing rows + 2 article bodies |

A count below 25 was the expected outcome and **its cause is measured, not guessed:** job 1 (ASML) accepted 2
article bodies and then raised `Timeout` on the third (`articles_per_security` is 5), which set a
PUBLISHER-LEVEL cooldown; jobs 2-8 then finished `cooldown / accepted 0` inside 30 ms with no request. Filed as
`AMGT_HARVST-Z-W22-S2`. The vendor plane shows exactly 4 requests, all 200:
`/api/v3/account/1btfwdu/info` 5,149 B; `/api/v3/symbols/asml/news` 154,875 B; `/api/v3/articles/4640871`
10,354 B; `/api/v3/articles/4640637` 9,868 B.

**CLAUSE 4 -- NO RE-AUTHENTICATION, measured three ways:** the run receipt reads `"auth_refreshes": 0,
"verification_repairs": 0`; `events.jsonl` carries NO `reauth_started` or `verification_started` row in the
window (12 events, all listed in the row's grounding); no browser process was launched. The hard stop was never
reached, so this cell did not have to take it.

### 3c. The second `upload-harvest` -- the captured pages reach S3

Output `ac2_upload_output.txt`, rc 0, and the deltas on the SAME instrument AC1 used:
sa `listing_hit` **+20 (20 -> 40)**, bronze `news_listing` **+1 (1 -> 2)**, silver `article` parts **+2 (33 -> 35)**,
outbox pending 3 -> 0. The put receipts name the keys:
`seeking-alpha/harvest/bronze/news_listing/date=2026-09-26/c908d13f...ROW_p1_20260926T094516Z.json`
(`put_performed: true`, 154,875 B) and
`s3://opal-data-harvest/seeking-alpha/harvest/silver/listing_hit/date=2026-09-26/part-20260926T094516Z.parquet`
(`written_rows: 20`).

### 3d. The ledger

`org/missions/D5/AMGT/AMGT_HARVST/ledger/VENDOR_CALLS_0.9.0_WK_AMGT_HARVST_22.md`, created this cell, CALL 1,
in this commit. It states the authorization **live at 09:44Z when the call ran** -- the session-wide
Andrew-direct of 2026-09-26 ~03:xxZ, verified by printing the cited bytes:
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260926_03xxZ_SELF_DRIVE_SITEZ_DIRECTIVES_AS_A_WHOLE.md:16`
reads `> - Egress is permitted for API calls this session -- no per-use word per vendor call, but every call is
ledgered by the seat that makes it. Spend, contracts, entitlements and hold-lifts are NOT covered.` -- NOT the
earlier per-use word of 02:1xZ that covered the COO's own call.

## 4. AC3 -- the grade change, PURE and IN MEMORY

Invocation: `... python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~22/scripts/ac3.py`
(output `ac3_output.txt`, `ac3_summary.json`). `write_gold` is never imported; the only traffic is READS (silver
`listing_hit`, and the newest `article_security_mention` gold snapshot -- 263 rows -- which is the same mention
input `build_daily` reads). BEFORE and AFTER are ONE read split by the pre-cell record keys AC1 recorded.

`as_of` 2026-09-26, start `BACKFILL_FLOOR` 2026-01-01, 269 days. `ENABLED_PUBLISHERS` = 5
(barrons, bbg, ft, sa, wsj) -- **NOT narrowed** (clause 5).

| population | sa spans AFTER | data_status BEFORE | data_status AFTER | moved DENIED -> PARTIAL | COMPLETE in a moved row |
|---|---|---|---|---|---|
| **A**: the 6 gold-builder securities | **0 of 6** | `{DENIED: 1613, PARTIAL: 1}` | `{DENIED: 1613, PARTIAL: 1}` | **0 of 1614** | 0 |
| **B**: the 89-name `--all-securities` universe (`security_key` DERIVED from `key`, in memory only) | **1 of 89** -- `security-81a74ed057551e58`, span (2026-07-15, 2026-09-26) | `{DENIED: 23940, PARTIAL: 1}` | `{DENIED: 23866, PARTIAL: 75}` | **74 of 23941** | 0 |

Sample moved row (population B): `security_key=security-81a74ed057551e58 day=2026-07-15 data_status=PARTIAL
publishers_covered=1 publishers_enabled=5`; last moved row: same key, `day=2026-09-26`, same 1 of 5. **The string
`COMPLETE` appears 0 times in any moved row, in both populations** -- consistent with clause 5, since 1 of 5
enabled publishers can only ever grade PARTIAL.

**POPULATION A'S ZERO IS REPORTED AS THE OUTCOME, AND ITS CAUSE IS NAMED, NOT EXPLAINED AWAY:**
`publication_gold._listing_hit_security_match` (`:476-481`) word-bounds a security's ALIASES against the row's
`search_query`, and sa is queried by VENDOR SYMBOL. `992_HK_Equity`'s alias set is `['Lenovo']`, which cannot
match `'LNVGY'`; all 20 drained rows therefore file under NO security in the population the gold builder
actually uses. ASML's 20 rows file 20 of 20 only because that company's NAME equals its `sa_symbol`. Filed as
`AMGT_HARVST-Z-W22-S3` (ARMED, `disarm_owner 2.0.0_SA_COO~Y`) -- it is a false negative in a served grade and
the code is outside this cell's write grant.

## 5. AC4 -- JUDGMENT, PRESENTED AND NOT GRADED

`scripts/ac4_evidence.py` (output `ac4_output.txt`, `ac4_evidence.json`). **Sample: EVERY sa `listing_hit` row
now in silver, n = 40 of 40** -- 20 from the held LNVGY page (AC1) and 20 from the ASML page (AC2). A census,
chosen so there is no selection to argue about; the two source pages are labelled per row.

What a reader needs and where it is: per row, the vendor symbol the row came from (`search_query`), the symbols
linked inside the row's OWN content (an independent read of "which company is this about"), the article title,
and the `security_key`(s) the matcher files the row under, for both populations. Headline counts:
**population A files 0 of 40 rows under any key; population B files 20 of 40 (every ASML row, no LNVGY row).**
The corroboration arm: the queried symbol appears in the row's own content links for **36 of 40** rows; the 4
that do not are three rows whose `content` carries no symbol anchor at all (LNVGY r14, ASML r17, ASML r18) and
one that lowercases it (ASML r14, `asml`).

Two things a grader will want to weigh, presented without a verdict: (a) EIGHT of the 20 LNVGY titles literally
name "Lenovo" and still file under nothing, because the matcher reads the query string and not the title;
(b) several ASML-filed rows are only tangentially about ASML -- e.g. "Notable tech headlines for the week: IBM,
Meta, TSMC in focus" and "Semiconductor stocks face more downside..." -- which is a question about what a
SYMBOL-page listing means, not about the plumbing. **No grade is asserted here; AC4 is `3.0.0_SA_CVO`'s at L9.**

## 6. CONTROLS

- **Negative control (the BEFORE arm), and it discriminates:** the identical AC3 instrument over the pre-cell
  row set reads 0 of 6 and 0 of 89 sa spans and `{DENIED: 23940, PARTIAL: 1}`. So population B's 74 moved rows
  cannot be an artifact of the instrument, and population A's zero is not the instrument being blind -- the same
  code returns 1 span on the same read when an alias does match.
- **Determinism:** `ac2_ceiling.py` was run twice on the same inputs and printed the same 89 / 25 / 19 / 45 / 32
  / 13 both times. The S3 census was run at three points and chains exactly: AC1's AFTER (sa 20) IS AC2's
  BEFORE (sa 20), and AC3 read 60 rows total = 20 wsj + 40 sa.
- **No mutant was named by the order and none was planted:** this cell's acts are live producer runs against a
  live vendor and live S3; a planted defect would mean a second vendor act or a write nothing would read.

## 7. WHAT WAS NOT DONE

No gold write. No second capture, no retry of the timed-out job, no re-authentication, no `lib/` edit, no
publisher other than sa, no S3 delete of any kind, no portal / Terraform / deploy / schedule / notifier. Nothing
outside `<paths>` plus this worker's own deliverables folder was written; the runtime root was read only.

## 8. ROWS FILED

`AMGT_HARVST-Z-W22-S1` (OBSERVATION / INERT) -- the 8-job cap makes the 25-name ceiling unreachable in one call.
`AMGT_HARVST-Z-W22-S2` (OBSERVATION / ARMED, `2.0.0_SA_COO~Y`) -- one Timeout cooled the publisher down and cost 7 of 8 jobs.
`AMGT_HARVST-Z-W22-S3` (OBSERVATION / ARMED, `2.0.0_SA_COO~Y`) -- the listing join reads the query string, so a symbol-queried page cannot become coverage.
`AMGT_HARVST-Z-W22-S4` (OBSERVATION / INERT) -- the order on disk and the worker face name different script paths; the face was followed.
`AMGT_HARVST-Z-W22-S5` (BLOCKING / ARMED, `2.0.0_SA_COO~Y`) -- that path divergence makes the gate refuse AC1's row, and AC1 cannot be re-run inside the BOUNDS.
`AMGT_HARVST-Z-W22-S6` (BLOCKING / ARMED, `2.0.0_SA_COO~Y`) -- the alignment limb's `(\S+)` cannot match a MAIN_TREE expansion containing a space, so AC2's faithful record is refused too.

## 9. THE PROOF INSTANCE, AND WHY THE ORDER IS LEFT OPEN

`python .tools/proof-of-spec-check.py org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~22/AMGT_HARVST.TO-HVST-v-2.drain-what-is-held-then-capture.proof_of_spec.json AC1,AC2,AC3,AC4`
-> **rc=1, INVALID, with EXACTLY TWO violations, both on the same limb** (full output: `proof_of_spec_check_output.txt`):

```
VIOLATION: invocation-alignment[AC1]: the RECORDED invocation is NOT the criterion's invocation modulo the placeholder(s) ['MAIN_TREE'].
VIOLATION: invocation-alignment[AC2]: the RECORDED invocation is NOT the criterion's invocation modulo the placeholder(s) ['MAIN_TREE'].
```

Every other limb is clean: structural `jsonschema`, 4 acceptance rows, alignment 4/4 forward and 1/1 backward,
artifact-resolution 11 pending-on-worktree + 5 `s3_object` skipped with 1 CONTENT-resolved row, and
`surprises-frame: 6 entries; 6 open with a row id; 6 resolve to a channel row`.

**AC1's divergence is the face-vs-file script path** and it cannot be discharged from this side: AC1's act is a
one-shot drain, the outbox is empty, and re-running the literal `.scratch/r2/ac1.py` would make a SECOND
`upload-harvest` invocation (the BOUNDS forbid exactly that), print `sa +0` where the criterion asks for `+20`,
and overwrite the pre-cell record keys AC3's BEFORE arm reads. **AC3's half of the SAME divergence WAS
discharged** -- the script was copied to `.scratch/r2/ac3.py` (`cmp` byte-identical), the literal invocation was
run, and the two outputs `diff` IDENTICAL -- which is how we know the path is the whole cause.

**AC2's divergence is an instrument limit, measured with a positive control:** the limb builds `(\S+)` per
declared placeholder (`.tools/proof-of-spec-check.py:1355-1372`), and this device's MAIN_TREE expansion carries
ONE SPACE. Against the checker's own `_invocation_pattern`: the string as run -> `fullmatch False`; the identical
string with that single space removed -> `True`.

**THEREFORE THE `<status>` WAS NOT FLIPPED and the task-order file was not touched.** All three mechanical
criteria PASS BY OUTPUT; the flip needs rc 0, and criterion amendment is the ISSUER's act under rule 27, never
the graded worker's. Rows `-S5` and `-S6` carry the disarm options, cheapest first.
