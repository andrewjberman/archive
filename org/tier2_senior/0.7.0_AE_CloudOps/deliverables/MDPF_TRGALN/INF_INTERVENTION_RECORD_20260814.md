# MDPF_TRGALN — INF leg intervention record, 2026-08-14 (proof-record delta; COO-required disclosure)

**Author:** 0.7.0_AE_CloudOps · **Status: CLOSED at the authorized boundary 14:20:43Z** (COO
stand-down concur; completion staged one-word-away for Andrew). §5 carries the end-state.
**Why this file exists:** COO 132308Z — *"the full three-swing sequence goes in verbatim with each
instrument named, so the record shows WHY the story moved (instrument quality, not indecision)."*

## 1. The authorized-delete sequence (timeline, all stamps UTC)

| t | act | authority |
|---|---|---|
| 06:12:00 / 06:13:33 | tonight-refresh QA pulls land bronze/assets + positions 2026-08-14 keys (pre-roll content) | v1.1 §8.1 (ad-hoc QA, run-and-read) |
| 11:17:23 | scheduled inf-api-assets-v2 logs `RESUME: s3://opal-data-inf/bronze/assets/2026-08-14.parquet exists — skipping date 2026-08-14` | — (the collision, verbatim) |
| 13:03:09 | AE decision package to COO: option (A) delete-and-repull vs (B) accept 08-12 | AE report |
| 13:04:16 | COO **GO (A) AMENDED** — backup-first, hard stop 13:27Z, disclosure non-negotiable | COO |
| 13:04:41–13:05:2x | backups to scratchpad, distinct-named after catching a basename collision; hashes: assets parquet 1,232,444B sha256=bc5dea17a23c4c14 · assets jsonl.gz 2,204,686B sha256=c179f0b4c39c854b · positions parquet 1,233,031B sha256=97439122b43733fe | COO GO binding 1 |
| 13:05:36 | deletes: the 3 authorized keys, exactly | COO GO binding 2 |
| 13:05:40 → 13:09:45 | re-pull assets COMPLETED (1,232,398B fresh) | COO GO binding 2 |
| ~13:10 → 13:13:02 | re-pull positions COMPLETED (1,233,238B) | COO GO binding 2 |
| 13:10:53 | **[STOP] MSTR HOLD** delivered (S3-delete is Andrew-reserved; the GO crossed the gate — COO owns the crossing on the record, AE acted exactly as bound). Read 13:13Z mid-positions-invoke. | MSTR via COO |
| 13:13+ | mirror {"firm":"inf"} **NEVER FIRED**; floor untouched; freeze per COO state-dependent ruling ("re-pulls completed → leave everything exactly as it is") | MSTR hold |
| 13:14:55 | step-state + hash-verified recoverability reported | COO STOP items 2–3 |

## 2. The three-swing mechanism narrative — each swing named by its instrument

**Swing 1 (13:03Z): "collision-material."** Instrument: the producer's own log (`RESUME … skipping`)
+ key LastModified. Claim: my pre-roll QA pull claimed the production date key; the scheduled
post-roll pull skipped; INF would serve 08-12 for a self-inflicted reason. *Correct mechanism,
correct instrument — but its materiality assumed the vendor had rolled.*

**Swing 2 (13:17Z): "vendor-late day, collision immaterial, fork (b) not live."** Instrument:
`editedDate` max/pattern across 08-12/08-13/08-14 pulls. Claim: Orion posts overnight (~03:35–04:15
CT historical), had not posted today by 09:09 ET, so even an unskipped pull would have carried
08-12. **WRONG — instrument failure:** editedDate is a position-record edit stamp, not a valuation
clock (distribution dominated by a 2025-07-21 bulk stamp on 19,239 of 35,285 rows; the mid-day
"posting" edits were 17 position INSERTS, 0 matched existing rows).

**Swing 3 (13:21Z): retraction + "collision material again."** Instrument: matched-row VALUE-DIFF
(accountNumber+ticker join): backup(02:12 ET) vs re-pull(09:09 ET) = 24,976/35,285 currentPrice
changed, portfolio total 210,128,341.20 → 210,313,542.25. Orion HAD posted between 02:12 and
09:09 ET; the 11:17Z scheduled pull would have caught fresh values but for the skip. Open caveat,
honestly held: close-marks vs live-quotes not determinable from bronze alone — the discriminator is
what the gold builder keys from a fresh copy (staged read).

**Swing 4 (13:25Z): staging correction.** Instrument: mirror source (`_is_raw` Ruling-16 refusal +
size-compare idempotent skip at the copy loop) + key-state reads. The staged mirror+trio remedy
would NO-OP: the mirror carries RAW only, and the raw `bronze/assets/2026-08-14.jsonl.gz` twin is
ABSENT since the authorized delete — its producer is the EC2 runner leg (two-producer evidence:
prior-day parquet/jsonl stamps minutes apart; runner assets marker 06:08:43Z before the 06:12:00Z
dual landing; the Lambda-only re-pull produced parquet only). Working remedy re-sequenced:
runner → raw lands → mirror → trio → discriminator read.

## 3. Standing facts for the TO-4 / Part-B adjudication

- COT leg: unattended-clean and GREEN — 11:31:44Z session, all 5 tables, holdings as_of=2026-08-13,
  monolith fact_holdings date=2026-08-13 @11:46:04Z. **B1 CONFIRMED PASS at the 07:30 ET slot.**
- 49F leg: unattended-clean, rides its normal morning pulls.
- INF leg: carries this disclosed intervention; unattended acceptance formally rides tomorrow's
  cycle unless CTO rules today's disclosed read sufficient (COO routing).
- B2: fresh valuations measured PRESENT by 09:09 ET (< the 11:17Z scheduled slot) — pending the
  close-vs-quote discriminator; today is unadjudicable for B2 at the slot itself because of the skip.
- Visibility fact (named, no checker proposed — moratorium): an Orion late/stale pull succeeds
  GREEN with stale content; nothing in the chain distinguishes it. Same class as the vendor-side
  facts that only content reads exposed today.
- Banked for CTO: deployed handler lacks `--no-resume` passthrough; QA key-hygiene lesson (a
  pre-roll QA pull that claims a production date key collides with resume logic); raw-vs-coerced
  two-producer asymmetry on bronze/assets (Lambda writes parquet, EC2 leg writes the raw twin);
  bronze/assets/2026-08-14.jsonl.gz remains a raw-set hole unless the runner re-fires.

## 5. END-STATE (appended 14:3xZ — the remedy's full arc and terminal state)

Clearance chain: COO GO 132711Z + re-delivery/ACK 133910Z (MSTR concur 132624Z + corrected-spec
concur 132803Z; CTO no-objection 132639Z). Executed: runner fired 13:54:29Z → raw
`bronze/assets/2026-08-14.jsonl.gz` re-landed 14:01:19Z (2,201,746B) → mirror 14:02:19Z carried it
(monolith raw 14:02:17Z, 1 written/verified). **Blocked one layer up:** the silver converter
invoked (RequestId aa57254f, 518ms) and SKIPPED-IDEMPOTENT on the existing stale partition
(`mirror_conversion.py:421 partition_exists`); the deployed entry (`lambda_entry` :876-898) has NO
force path (library carries force :415/:707 — unreachable; sweep = misses-only). Only remaining
lever = deleting the stale silver partition = **Andrew-reserved**; COO stand-down 142043Z: legs 3–4
NOT fired (byte-identical re-serve serves nobody), the delete "NOT authorized and will not be"
tonight. Terminal state: **raw layers healed; silver/gold/served on the 02:12 ET marks; the served
08-13 label correct as a label; the $185,201.05 / 0.088% understatement permanent for the historical
08-13 INF point absent Andrew's word** (staged completion: delete stale partition → converter
re-fires on healed raw → trio → tie-out). Scheduled-cycle meta-fact: the mid-cycle scheduled fires
(11:02–13:50Z) all ran untouched; the labels served 3/3 at 08-13. CTO ruling (v1.4 §9.5, relayed
142243Z): INF TO-4 leg = PASS_WITH_DISCLOSURE, closing read = tomorrow's clean cycle, failure
REOPENS. Both conditions written into proof_TO-4 verbatim.

## 6. ANDREW-AUTHORIZED COMPLETION RUN (appended ~15:25Z) — his word, the legs, guard #4, and the (a) ruling

**ANDREW-DIRECT, VERBATIM: "go ahead"** — 2026-08-14 ~15:14Z at the 0.7.0_AE_CloudOps terminal, in
direct response to the /open-calls card CALL 1 of 1 ("Authorize the one-delete INF completion?").
Recorded + broadcast to COO/CTO/MSTR 15:15:04-13Z same turn. Scope read narrowly: the carded
sequence only; COO 152434Z confirmed that reading ("the carded sequence named ONE delete").

Execution legs (each verified before the next):
1. Pre-mutation live-state verify 15:15:36Z: stale partition 06:16:21Z/1,216,778B; healed raws
   14:01:19Z (inf) / 14:02:17Z (monolith), 2,201,746B both.
2. Backup: `stale_fact_assets_date-2026-08-14.parquet` 1,216,778B sha256=2e8141d01f58f885
   (scratchpad qa-bronze-backup/; first cp attempt to an absolute /cygdrive dest silently
   mis-landed — aws-shim path class, banked; relative-path pattern verified byte-exact).
3. DELETE `orion/inflection/silver/fact_assets/date=2026-08-14/data.parquet` 15:17:50Z,
   absence verified.
4. Sweep-heal: opal-assets-silver-orion {"mode":"sweep"} run 20260814T151816Z-46eb25be —
   set-identity PASS (4,762/4,762, 0 holes), converted=1; partition REBUILT 15:18:23Z
   (1,217,482B) from the healed raw.
5. Floor re-run 15:18-15:19Z green: fresh values COMPUTED — then **GUARD #4**:
   `mdpf_gold_consolidator.py conditional_put` (:455-517) recorded-not-overwrote the
   business-different content at the existing dated keys (verbatim: "CONFLICT (recorded, not
   overwritten): portal/gold/mdpf/inflection/aggregate-aua-timeseries/2026-08-13.json -- 9
   business path(s)"; + inflection aum-metrics 12 paths incl. total.aum; + global x2). NO
   override exists BY DESIGN ("NEVER silently overwritten"). Accrual/publisher NOT fired.
6. Mechanism finding that re-priced the call: the builder recomputes the whole 445-date series
   every run — tomorrow's NEW frontier key (2026-08-14.json) carries the corrected 08-13 point
   and platinum serves it. THE SERVED UNDERSTATEMENT SELF-HEALS IN ~20h; permanence attaches
   only to the 4 frozen dated gold snapshots (inflection+global × aggregate-aua-timeseries +
   aum-metrics @ 2026-08-13.json).
7. **COO DECISION 152434Z: (a) STOP** — the 4 gold keys are a NEW reserved-category delete set
   outside the carded word; no widening on inference (4th hold of the day); ~20h of a 0.088%
   self-healing served understatement does not price another reserved act. Conflict records
   LEFT IN PLACE (the guard's evidence). Option (b) rides Andrew's card until tomorrow's cycle
   moots it. Tomorrow's closing read reverts to the ORIGINAL form: served-point tie-out at the
   fresh total (== CTO precision (a)).

Terminal state after the authorized run: silver layer FULLY HEALED (durable); gold/served
self-heal at tomorrow's cycle; the 4 dated gold snapshots keep the stale point unless Andrew
spends one more word before tomorrow moots it.

## 4. Instrument-quality lesson (why the story moved)

LastModified/rowcount said "identical" where values differed; editedDate said "unposted" where
24,976 prices had moved. Both are metadata proxies; only the content diff answered the content
question. The story moved three times because each swing replaced a weaker instrument with a
stronger one, each swing was reported the turn it was measured, and no swing was allowed to stand
on the prior swing's instrument. (CONTROLS_OVER_CARE: the proxy limb, caught by looking at what
came back.)
