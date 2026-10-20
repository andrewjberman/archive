# MP-pd-7 CLOSE REPORT -- the grant-writer Lambda's code, deployed from source (Act A only)

Applier `0.7.0_AE_CloudOps~NFRA1`. Order `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pd-7.person-access-release.md` (A2); GO LIVE_BASE `13917ef993`, LAMBDA_COMMIT `f3774ac1df8`. Ask sha256 prefix `f0098d2b67ab`, both halves SIGNED (CTO @392b19649f, COO~MP at HEAD). Ledger `nfra-mcportal-pd-release` CLOSED (all three legs proven). Push state: LOCAL (box/sitez), not pushed.

GW_LAMBDA_SHA256=RUGwtI9t8UKV8VpyCeArffZFwHeuUm4QhOIJU+nAJjg=

## The act
- Plan: `Plan: 0 to add, 1 to change, 0 to destroy.`, exactly `aws_lambda_function.mcportal_grant_writer` updated in place (source_code_hash `894RI63/G4h019yxAGP7E+wQzrpZIfJoMaLhzpTTyck=` -> `RUGwtI9t8UKV8VpyCeArffZFwHeuUm4QhOIJU+nAJjg=`). The live release was `13917ef993` at all three reads (measure, gate, plan).
- Apply (one `safe-apply` of the saved plan): `Apply complete! Resources: 0 added, 1 changed, 0 destroyed`, started 2026-10-20T20:18:31Z, finished 2026-10-20T20:22:28Z, 237.4 s.
- Code hash before / after: `894RI63/G4h019yxAGP7E+wQzrpZIfJoMaLhzpTTyck=` / `RUGwtI9t8UKV8VpyCeArffZFwHeuUm4QhOIJU+nAJjg=`.

## The two no-header invokes, before and after
| action | before (2026-10-20T20:04:11Z) | after (2026-10-20T20:22:57Z) |
|---|---|---|
| `narrow` | REFUSED NO-OWNER-HEADER | REFUSED NO-OWNER-HEADER |
| `set_person_access` | REFUSED NO-OWNER-HEADER | REFUSED NO-OWNER-HEADER |
Each refused invoke wrote one append-only changes-table record (`record: PUT`), the function's existing behaviour: four in all.

## The deployed-bytes read (AC2's subject)
The served code zip (the presigned URL `get-function` returns): 65 members; every member's md5 equals the package built here (differing members: 0); `lambda_function.py` holds `WIDEN-NO-CONFIRM` (True) and `widening_signoff` (True).

## Rollback
Not executed (no trigger fired). Proven as far as the ask's departure allows: the old handler `30d9b99758d` on the current closure (the previous behaviour, not the previous bytes), command `python mp_pd7_act.py rollback`. Its time: MEASURED as the forward apply of this act (237.4 s for the one in-place code update; a rollback is the same operation in the other direction) plus the plan/build step; the rollback itself was not run, so the figure is the forward apply's, not a rollback's. The deployed package's own bytes are held in `MP-pd-7_deployed_before_894RI63.zip` (sha256 prefix `f3de1123adff1b88`, 57,638 bytes) until 2026-10-27 (7 days after the close; the CTO half's condition).

## Not touched
The function's role, environment, owner key, layer (version 1), changes table (other than the four refusal records above), the gateway (no release, no restart) and every other resource. No `person_access` record written. Nothing reaches `set_person_access` until a route mounts it (not this order).
