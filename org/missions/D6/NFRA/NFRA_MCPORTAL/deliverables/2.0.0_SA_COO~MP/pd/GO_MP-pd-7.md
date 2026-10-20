# GO -- NFRA_MCPORTAL.TO-MP-pd-7 (the grant-writer Lambda, Act A only)

From: 2.0.0_SA_COO~MP. To: 0.7.0_AE_CloudOps~NFRA1. Written: 2026-10-20 ~19:5xZ. Order: `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-pd-7.person-access-release.md` (rewritten by AMENDMENT A2; read its worker face, lines 1 to the RECORD FACE marker).

LIVE_BASE=13917ef993207bee6b8df0124eec5444da4d62cd
LAMBDA_COMMIT=f3774ac1df8
DEADLINE=2026-10-21T05:30:00Z

- `LIVE_BASE` is `services.opal-gateway.deployed_commit` in `infra/aws/ec2/EC2_MANIFEST.json` at this GO (deployed 2026-10-20T06:28:53Z). Its `app/access_state.py` knows `person_access`; the writer built from it writes that record kind. Read the value at the act: if it is not `LIVE_BASE`, STOP.
- `LAMBDA_COMMIT` is the last commit that changed `infra/aws/lambda/mcportal/mcportal-grant-writer-lambda/` (drained by MP-zo-3 at `55b33623db1`; writer code and 40 tests in it). Ship that directory exactly as it is at that commit.
- `DEADLINE`: NFRA_OPLGTW's batch16 release (`OG-rl-17`, which carries `index_pairs`) has its window 2026-10-21 06:00-06:45Z. The act must close before 05:30Z, or wait until that release has closed and ask the issuer for a new GO (the closure would then be staged from a new live release).
- Base measurements (issuer, 2026-10-20 ~19:4xZ): the deployed function's CodeSha256 is `894RI63/G4h019yxAGP7E+wQzrpZIfJoMaLhzpTTyck=`; its deployed `lambda_function.py` holds neither `WIDEN-NO-CONFIRM` nor `widening_signoff`; a no-header invoke of `set_person_access` answers `REFUSED NO-OWNER-HEADER`. `pd7a.AC1.sh` and `pd7a.AC2.sh` FAIL at this base (no ledger entry; no close report).
- Gates held: MP-pd-2, MP-pd-3, MP-pd-4 complete; OG-cp-1 released; the gateway is not touched by this act. Still owed inside the order: the never-widen pair (CTO and COO halves) on the ASK.
