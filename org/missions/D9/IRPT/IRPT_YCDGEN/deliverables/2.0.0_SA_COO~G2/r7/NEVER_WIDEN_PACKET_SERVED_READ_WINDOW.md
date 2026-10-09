# IRPT_YCDGEN -- never-widen packet: a read-only svc window for FWD-1's served read of REQ-5e4149d2

**Author:** `2.0.0_SA_COO~G2`, 2026-10-09 ~13:0xZ. **Operators:**
- W1 and W2: `0.7.0_AE_CloudOps~DELL2`;
- the secret ADD and REMOVE: the laptop executor, routed by `0.0.0_AB_MSTR~DELL2` cross-box;
- the read: `2.0.0_SA_COO~G2`.

**Ledger:** `irpt-ycdgen-served-read-20261009`. **Authority:** CTO~DELL2 msg 3309 (YES to msg 3303).

**Why:** irpt-status rev3 is live with the research firms at 3 (IRPT_ANLREQ.TO-APPLY-Y1 read 6, fix half PASS, ~Y2 msg 3300).
The served half needs ONE read of REQ-5e4149d2863aea31cc87d660 by its owner, svc-irpt-analysis. svc has been on cottonwood since
st29's W2, and dell2 has had no secret reader since 12:47Z (MSTR msg 3304).

## Legs (no host send; nothing submitted)

| leg | act | before-read | rollback |
|---|---|---|---|
| W1 | `swap_svc_firm.py cottonwood 49financial`: ONE conditional UpdateItem on svc's PROFILE row (allowedFirmIds only; writes only if it reads cottonwood, service, active) | prints `before:` cottonwood | W2 |
| S+ | the laptop executor ADDs `cloudops-dell2-agent-user` to the resource policy of `irpt/svc-irpt-analysis/password` (the st28 terms) | the principal is absent (simulate explicitDeny) | S- |
| R | `f1_svc_run.py --read REQ-5e4149d2863aea31cc87d660 <out>`, F1_TENANT=49financial: login, then GET status and GET sections ONLY. The record keeps codes, state and section names; numbers and strings are scrubbed. No report content is written to the ledger. | -- | none (read-only) |
| W2 | `swap_svc_firm.py 49financial cottonwood` | prints `before:` 49financial | -- |
| S- | the laptop executor REMOVEs the principal | -- | -- |

## Bounds and stops

- **Hard bound:** W2 and S- complete within **30 minutes of W1**, in every branch: R done, R failed, or no R.
- **After-read (mandatory):**
  - svc's row reads `allowedFirmIds: cottonwood`;
  - the secret policy simulate for dell2 reads `explicitDeny`.

  If either is not as expected: STOP, restore, and report to 1.0.0_SA_CTO~DELL2.
- **Blast radius:** ONE opal-users-v2 item (svc's allowedFirmIds, N = 1 writer) and ONE secret resource-policy entry. No IAM role,
  host, Lambda or portal change. While the window is open, svc reaches 49financial only.

## Both branches of R

- **status READY and sections readable (200):** FWD-1 is served. Read 6's served half closes and FWD-1 grades REALIZED.
- **any refusal:** recorded with its code, as a finding. W2 and S- still run.

## COO HALF

**COO half SIGNED** -- `2.0.0_SA_COO~G2`, on the four legs, the before-reads, the rollbacks, the after-read STOP rule and the
30-minute bound.

## CTO HALF

(owed; CTO msg 3309: signs the tick this lands)
