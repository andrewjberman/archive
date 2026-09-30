# AMGT_CORPUS round 15 -- never-widen pair for the Hitachi 6501 JP registration and crosswalk put (cell CRPS-q-2)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Ruling it implements: round-14 analysis s.2 ruling 4 and s.4 cell 2
(`ledger/ROUND_ANALYSIS.round14.md`); input msg 26708 (AMGT_RESAPP `ROUND_ANALYSIS.round48.md` s.2 ruling 3).

## THE ACT -- ONE RUN, NO BUILD
`python -m lib.research.identity.add_security --folder "Hitachi 6501 JP" --bloomberg "6501 JP" --as-of <today UTC> --write-pool`,
from CLOUD HEAD, then commit `lib/research/identity/registrations.json`. A change entry opens before the run and closes with
content proof. No code changes: the registration tool exists and already landed 70 rows this way.

**The identity choice, stated for the CTO half to grade (it is a judgment, not a mechanical read):** `--folder` alone reads the
Bloomberg id from a `*ONE PAGER*.xlsx` workbook; Hitachi's folder has none (one memo docx), so that route returns UNRESOLVED
with 0 calls (dry-run 21:43:19Z). The id `6501 JP` is taken from the folder's own name, which follows the library's
`<Name> <ROOT> <CC>` convention (for example `Adobe ADBE US` and `Air Liquide AI FP`). It is then MEASURED by the call, not
assumed: the dry-run at 21:44:16Z (one scripted `reference_data` call) returned `MEASURED: security_key 6501_JP_Equity
bloomberg '6501 JP' name 'HITACHI LTD' lei '549300T6IPOCDWLKC615' cik 47710 composite_figi 'BBG000C2QRN8' AGREES: id token 'JP'
== Bloomberg EXCH_CODE 'JP'`. The returned name matches the folder's name.

**Vendor authority:** Andrew R-21 (`b390c36444`, 2026-09-23: egress to all vendors, every call through a script).
`add_security.py` is that script; the act makes ONE Bloomberg call.

## WRITER CENSUS -- three surfaces, one writer each in this act
- `bloomberg/harvest/bronze/identity/security_key=6501_JP_Equity/<stamp>.json` -- a conditional put, a fresh stamp.
- `lib/research/identity/registrations.json` -- appended by `add_security._persist_registration_and_pool`, committed by this seat.
- `s3://opal-data-harvest/crosswalk/v1/<today>.json` -- `crosswalk.write_pool` (the one function every crosswalk write passes
  through: `crosswalk --write-pool`, `add_security`, `build_universe` union). N = 1 rule read for the served object:
  `write_pool` (create with IfNoneMatch when absent; overwrite with IfMatch when the digest differs; no-op when equal).

## BEFORE-STATE (measured 2026-09-29T21:45:04Z; `evidence/r15_q2_before.txt`)
- `crosswalk/v1/`: 5 objects, latest `2026-09-25.json` (596,029 bytes, 23:48:58Z). No `2026-09-29.json`.
- bronze identity for `6501_JP_Equity`: 0 objects. `registrations.json`: 70 rows, 0 for Hitachi.
- The in-memory build from HEAD inputs today equals the pool object record for record (`checks/round15/q2_census.py` at base:
  `added 0 removed 0 changed 0`), and `backlog` reads `folders 96 resolved 95 unresolved 1 ambiguous 0 hitachi UNRESOLVED`.

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE -- both branches
- **Branch 1 -- no `<today>.json` exists (today):** one create. The served latest key moves 2026-09-25 -> `<today>`. Records:
  **added 1 (`6501_JP_Equity`), removed 0, changed 0**; the six existing `_JP_Equity` records unmoved. Every `resolve()`
  reader (corpus, backlog, the scoped API's identity reads) resolves Hitachi; every other resolution is unchanged.
- **Branch 2 -- another writer created `<today>.json` before the run:** `write_pool` OVERWRITES it (IfMatch) with this build,
  which is that writer's inputs plus Hitachi only if both builds read the same HEAD inputs. STOP limb 1 reads the key's absence
  immediately before the run; if present, stop and re-measure rather than overwrite a peer's object.
- The `as_of` date must be today UTC (`--write-pool` refuses any other); a run after 24:00Z uses the next date, same shape.

## AFTER-STATE THE VERIFY READS (content, not rc)
1. `crosswalk/v1/`: 6 objects, latest `<today>.json`; bronze identity `6501_JP_Equity`: 1 object; `registrations.json` 71 rows.
2. `checks/round15/q2_census.py` against the POOL (after the put, the in-memory build equals it): `q2 folders 96 resolved 96
   unresolved 0 ambiguous 0 hitachi 6501_JP_Equity`.
3. A record diff `<today>.json` vs `2026-09-25.json`: `added 1 removed 0 changed 0`, other JP moved 0 of 6.
4. `induction_request.run()` (FWD-4's organic arm): Hitachi is no longer a candidate (resolved), population 0 of 96.

## BLAST RADIUS AND ROLLBACK
- **Touches:** one new pool key (the served latest), one bronze raw object, one appended registration row. No delete; the
  five existing pool keys are untouched.
- **Rollback, same UTC day, by write:** revert the registration row and run `crosswalk --as-of <today> --write-pool`; the
  digest differs, so `write_pool` overwrites `<today>.json` (IfMatch) with the 09-25 record set. **Rollback on a later day:**
  the same run under that day's date writes a newer latest without Hitachi. Neither needs a delete. The bronze raw object stays
  (write-once evidence of the call).

## STOP LIMBS
1. `<today>.json` exists immediately before the run -> stop, re-measure, re-sign.
2. The run prints anything but `MEASURED ... 6501_JP_Equity ... AGREES` or `bloomberg_calls` != 1 -> stop; nothing is committed.
3. After-state 2 or 3 differs (any record changed or removed) -> roll back by write the same day.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against CLOUD HEAD at signing. The act runs from CLOUD HEAD; this half
travels with any HEAD whose `lib/research/identity/` and `registrations.json` equal the signing HEAD's.
