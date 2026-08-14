# MDPF_TRGALN — INF leg intervention record, 2026-08-14 (proof-record delta; COO-required disclosure)

**Author:** 0.7.0_AE_CloudOps · **Status at writing:** frozen under MSTR hold (via COO 131053Z);
remedy conditionally staged pending COO GO + MSTR concur.
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

## 4. Instrument-quality lesson (why the story moved)

LastModified/rowcount said "identical" where values differed; editedDate said "unposted" where
24,976 prices had moved. Both are metadata proxies; only the content diff answered the content
question. The story moved three times because each swing replaced a weaker instrument with a
stronger one, each swing was reported the turn it was measured, and no swing was allowed to stand
on the prior swing's instrument. (CONTROLS_OVER_CARE: the proxy limb, caught by looking at what
came back.)
