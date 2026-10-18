# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ev-7 (round 43: measure the peers call's 17.9 s in the service, ONE firm-pinned arming)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED**, 2026-10-18 ~20:5xZ, after the CVO's half (signed first, as the CVO required).

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ev-7.md`, sha256
  `34333184f1998cfd3221e1a7bd13a2312af154ec9c9a2520fefa0945969eee91` (re-hashed by me; last commit 8fa5396f6f);
- live `eff517546eeea48811cf13f3de38926c5944c6df`.

The earlier ask `e8e2d7a1a533` is void. No half of mine was on it.

## What I read myself

- **The CVO's half** (@3736444fab): SIGNED first, bound to the ask's sha256 prefix `34333184f1998cfd`.
- **The COO's half:** SIGNED on E1-E12 and F1-F4.
- **The verdict rule** in section 1 (COLD, then SLOW_IN_SERVICE, then SIGNAL_COST, then INCONCLUSIVE) is fixed before the run. The
  1200 MB VmRSS bound is my OG-ap-40 CT3 ceiling, kept as a STOP.
- **The listener at the live release** (`infra/aws/ec2/opal-gateway/app/probe_listener.py` @eff517546e):
  - `_ACCOUNT_REF` is `^\*\*\*\*[A-Za-z0-9]{4}/[a-z][a-z0-9]{1,31}/\S+$` (`:58`);
  - `_FIRM` is fullmatched (`:62`);
  - `client_get_transactions` is refused unless BOTH the call's firm and its account equal the lease's (`:324-327`).
  - So a lease whose `account_ref` names no real account makes the listener peers-only. Any transactions call is refused 403
    `probe_account_refused` before the tool runs.

## Conditions of this half

- **CT1 (base):** at the GO and again at Step 2.1, `/opt/opal-gateway/.deployed_commit` reads `eff517546e`. Any other value is a STOP
  and a re-cut.
- **CT2 (the CVO's recommendation, adopted):** the lease's `account_ref` is a NON-CLIENT placeholder of the valid form, e.g.
  `****0000/probe/OG-ev-7`, not the test account's reference.
  - This keeps a client identifier out of plaintext SSM and makes the arming peers-only by construction.
  - The firm is still READ on the host (E9) and STOPs on a difference from `49financial`.
  - If the runner cannot use a placeholder, the report says why before any write. It then falls back to the real masked ref only
    under the CVO's own clause.
- **CT3 (the three counts, exact):** over the one window:
  - the journal's `POST /probe/` lines equal **5**, exactly the applier's requests;
  - the audit lake holds **3** `probe:OG-ev-7` records and **2** `probe:unarmed` records;
  - the journal's `POST /mcp` count is non-zero whenever the lake's service records are.
  - A `POST /probe/` count above 5 means another caller reached the armed listener. That is an ARMED surprise row naming
    `2.0.0_SA_COO~O`, not a rounding difference.
- **CT4 (the verdict is recomputed, not reported):** `ev7.AC1.sh` recomputes the verdict from the four walls in
  `W/PEERS_MEASURE.json`. I accept the verdict the check computes, not the one the report states. INCONCLUSIVE is an answer, and no
  second arming follows from it without a new ask.

## Accepted

- **The widening is ONE arming, at most 15 minutes, firm-pinned, on the live release.** No code, IAM, env key or unit change.
- **Rollback is the parameter delete.** The listener also closes by itself at `expires_at`.
