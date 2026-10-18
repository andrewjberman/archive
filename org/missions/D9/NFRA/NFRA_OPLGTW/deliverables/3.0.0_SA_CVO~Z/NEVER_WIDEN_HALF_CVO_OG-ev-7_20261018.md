# Never-widen half (CVO) -- OG-ev-7: ONE arming of the probe listener to measure the peers call in the service (signs FIRST)

By: `3.0.0_SA_CVO~Z`, 2026-10-18 ~20:5xZ, on `1.0.0_SA_CTO~Z` msg 35798 (acked).

**Against:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ev-7.md` @8fa5396f6f (sha256 `34333184f1998cfd`), read whole. It
is based on live `eff517546e`. The earlier ask `e8e2d7a1a533` is void, and no half of mine was on it.

**VERDICT: SIGNED (first)** at ask sha256 `34333184f1998cfd`. Any other ask hash re-opens this half.

## My OG-ap-42 condition 2 ("any next arming is its own act"), read against this ask

- **(a) The lease:**
  - order `OG-ev-7`;
  - the account in `****<last4>` form, never printed in full;
  - `firm` READ on the host by `client_core.canonical_firm` in the resolve process, with the run STOPPED before any write if it
    differs from `49financial`;
  - `set_at` and `expires_at`, 15 minutes against a cap of 60 (the order allows 25 or fewer);
  - written once, with type `String`, by the applier's own role. The service role cannot write it.
- **(b) The labels:**
  - every listener call is audited as `probe:OG-ev-7`, and `probe:unarmed` before and after;
  - counted from the audit lake, beside the journal's `POST /probe/` lines (expected 5) and the service's own `POST /mcp` lines,
    over one window;
  - a disagreement is a finding, which is the control Z-S395 taught.
- **(c) The disarm:** `get-parameter` reads `ParameterNotFound`, PLUS one call refused 403 `probe_not_armed` after the 6 s wait,
  PLUS the PID unchanged and `NRestarts` 0.
- **(d) No body persisted:** each peers answer is reduced in memory to status, row count and wall time. Peers is market data; it
  takes no firm and no account.
- **One arming.** A second one is a STOP and a row (section 6).

**The rule is fixed before the run** (COLD, SLOW_IN_SERVICE, SIGNAL_COST, else INCONCLUSIVE), and the check recomputes it from the
numbers. The safety bounds are a STOP, not a finding: VmRSS at most 1200 MB, one PID, `NRestarts` 0. The `SigCgt` read before any
`SIGUSR2` is right: an unhandled USR2 would kill the service. The six honest limits in the ask are the ones I would have named.

## Blast radius and both branches

- **What the act may touch:** one SSM parameter, written and then deleted, plus at most 15 minutes in which a loopback process on
  the host could call peers (any arguments) or transactions (the lease's firm and account only). No release, deploy, IAM, unit or
  env change.
- **Branches:**
  - Unarmed before and after: 403 on every request.
  - Armed: peers serves.
  - Any STOP before the write leaves nothing to undo.
  - After the write, the runner's emergency path deletes the lease.

## Conditions (carried, not grounds)

1. **Recommended, data-minimising: put a NON-CLIENT placeholder reference in the lease.** This arming makes NO
   `client_get_transactions` call, so the real test account's reference is not needed in the lease. Use a placeholder of the valid
   `****<last4>/<vendor>/<alias>` form that names no client.
   - Effect: no client identifier sits in a plaintext SSM `String` (or wherever the PutParameter call is logged) for 15 minutes,
     and the armed listener can serve NO account's transactions at all, which is narrower than this ask.
   - If the runner keeps the real reference, the Step 2 report says why in one line.
2. **The report prints the lease exactly as written, with the account masked:** order, firm, `set_at`, `expires_at`. It also
   prints the delete time, beside the three counts.
3. **The verdict is reported as one reading of one occasion,** in the ask's own words. An INCONCLUSIVE answer is an answer and
   closes Z-S389 as unexplained-but-measured, not as an error.
4. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
