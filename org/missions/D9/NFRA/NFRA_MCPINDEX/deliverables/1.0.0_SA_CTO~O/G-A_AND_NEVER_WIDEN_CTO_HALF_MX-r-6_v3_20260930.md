# MX-r-6 v3 -- G-A and the CTO never-widen half SIGNED (the Schwab enable release, on live ref 4ce7946426)

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-30 ~17:4xZ.
**Ask:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-6_v3_20260930.md`
@20599c0c29 (msg 27287).
**Supersedes** this seat's v1 half (VOID @9e7a0e72f0) and v2 half (VOID by its base clause after the 14:41Z overwrite;
row Z-S68).
**Grounds:**
- rulings B1, B2, B4 and B7 (@4e598ab7be);
- Andrew-direct "agreed" (@29bc46d827) for ONE new Schwab grant to Alyssa: two masters, four dims;
- this seat's base-guard rulings (msgs 27210 and 27230).

**Pin:**

| part | hash |
|---|---|
| release | `a5e73b6e72` |
| deploy-only | `42c52ed4d9` |
| gateway tree | `a3893da22ad839edb26e9537ac13d7347b02396d` |
| live ref | `4ce7946426` (tree `29b25ad640`) |

**Verdict: G-A PASSES, and the CTO half is SIGNED on this pin only.**

## Measured by this seat

- **Live ref, read at 17:3xZ:**
  - S3 `opal-gateway-latest.tar.gz` ETag `da7b3c9d...` equals `opal-gateway-4ce7946426.tar.gz` (15:22Z), and no key is
    newer.
  - This is ~RV's Plan A restore, which its read-back shows as host == ref, 80 of 80 files (msg 27229).
  - The guard's fallback read resolves exactly one SHA-keyed object, so it reads `4ce7946426`.
- **Tree:** `a3893da22a` is equal at `a5e73b6e72` and `42c52ed4d9`.
- **Diff against the live ref:** 22 files, +1268 -45. It is the v2 Schwab/MX-q-3 set plus the guard: `deploy-to-ec2.sh`
  +90 lines and `tests/test_deploy_base_guard.py`, which is new.
- **Preserved, byte-equal to live:**
  - `app/tenant_registry.py` (6876b359) and `app/firm_role.py` (0ff54e33), which are MCPMSP's;
  - `app/rivalfunds_view.py` (2a8be974), which is ETFS_RIVALS';
  - `server.py`, which still carries 7 `rivalfunds` references.
  - The `.env` printf keeps `FIRM_ROLE_ARNS` and adds `schwab`.
- **The base guard,** read in the diff:
  - `DEPLOY_BASE_REF` is required, and an absent value refuses with no upload.
  - The live ref is read at upload time from `git-ref` object metadata, falling back to the single SHA-keyed object
    sharing `-latest`'s ETag.
  - An unreadable ref refuses. It compares by REF, not by ETag, as ruled.
- **The IAM leg** is terraform-only and targeted. The half is CONDITIONAL on the re-plan at the GO reading
  0 add, 1 change, 0 destroy, with only the 8 `dim_transaction` elements.

## What this half covers

- The IAM change and the host deploy from `42c52ed4d9`, run with `DEPLOY_BASE_REF=4ce7946426`. The rollback deploy
  also runs with the guard (CVO H1).
- The `.env` going from 28 to 33 keys, with MCPMSP's line kept, and tools moving from 52 to 58.
- ONE new Schwab grant to Alyssa (masters 08242234 and 08335338; `dim_position`, `dim_balance`, `dim_asset`,
  `dim_transaction`), through the grant admin tool, recorded before and after.
- **Both branches of every leg:**
  - the guard refuses: no act;
  - the plan is not 0/1/0: no apply, and a BLOCKING row;
  - the apply fails: no deploy, and the IAM rollback;
  - the deploy or read-back fails: a guarded redeploy of the live-ref rollback tree, plus the IAM rollback, and the
    ledger closes ROLLED-BACK;
  - the grant tool refuses: no grant, and the A2 refusal stands;
  - never half-landed (NEVER-2).

## Not covered

- An untargeted apply, or another IAM resource.
- A changed pin, or a live ref other than `4ce7946426` at the GO (the guard enforces this).
- Any other grant or identity.
- The ETF and BD tools.

**GO guards:**
- NEVER-2 ledger opened first.
- 3.0.0_SA_CVO~O's half is SIGNED (@5c54630648, H1-H3).
- The GO waits for 2.0.0_SA_COO~O's Part D sitting read-back, so the host does not move during Andrew's sitting.
