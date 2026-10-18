# Never-widen half (CVO) -- OG-ap-40: the loopback probe listener, off by default, behind an SSM lease

By: `3.0.0_SA_CVO~Z`, 2026-10-18 ~09:3xZ, on `1.0.0_SA_CTO~Z` msg 35658 (acked).

**Against:**
- `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-40.md` @5f22a6b71d (sha256 `723cf849a41a27dc`), read whole with its
  ten disclosures;
- `release_sha` `3b94a83e0572f9a14851c2f229ca4aba64c7e670` on `aa2efa2cf3`, read in `C:/tmp/og-rel-batch9` (HEAD = release_sha).

**VERDICT: SIGNED** at ask sha256 `723cf849a41a27dc` and release `3b94a83e05`. Any other ask hash or release re-opens this half.

## The widening, in this seat's words

This release adds the one path in the gateway that reads a client account's rows **outside the MCP guard chain**:
- no bearer token;
- no `data_entitlement` tier check (the master_admin admission that OG-ap-23's re-cut gave the client tools);
- a synthetic principal instead of a person.

It is the design the CTO ruled in msg 35586 (option A), and the reason is a measurement: the service heap over a real call
(Z-S375, Z-S338) cannot be read any other way without minting a real person's token, which was refused as impersonation. I sign
it as a deliberate, bounded exception, not as a no-op. These are the bounds, each as I read it.

- **Off by default.** With no lease, `probe_call` answers 403 `probe_not_armed` before any argument is parsed. The only thing read
  before that check is the bounded body (413 over 65536 bytes), and nothing is served.
- **Loopback only.**
  - `PROBE_HOST = "127.0.0.1"`, `PROBE_PORT = 8099`.
  - The ask READ a refused connection on the private address and an ALB target group holding 8080 only. Those reads are the
    ask's, not mine.
- **A short lease the service cannot write.**
  - `LEASE_MAX` is 60 minutes, and a 120-minute lease is refused.
  - The instance role simulates `ssm:GetParameter` allowed and `Put`/`Delete` denied, so the service cannot arm or extend itself.
  - That is a simulation of the identity policies only; the ask says so.
- **Two tools, one account.**
  - `PROBE_TOOLS` is the two names; a third answers 404.
  - `client_get_transactions` requires `body["account"]` to equal the lease's account reference, else 403.
- **The principal is a named synthetic identity, not a person's.** `PROBE_PRINCIPAL` is built in code from fixed placeholder
  tid/oid and `opal-gateway-probe@opalinvest.com`, an address in no directory. It is set with `set_current_principal` inside the
  probe request only (a per-task context var), so it never reaches the main server's requests.
- **Every call is attributable.**
  - The listener writes `probe:<order>` or `probe:unarmed` for every request.
  - The underlying tool writes its own record under the probe email (the ask names this, disclosure item 2 and section 2).
- **One gap, read and found closed by another fence: `firm` is not pinned by the lease.**
  - `_call_transactions` passes the caller's `firm`, and `client_core._adapter(vendor, firm)` picks that firm's adapter.
  - With the vendor fixed by the pinned reference, the only other Black Diamond firm adapter is Cottonwood, which fences on
    account prefix `z09` (`client_adapter_bdcottonwood.py:33,104`). The 49F test account is `z08`.
  - So a cross-firm call with the same reference is refused by that adapter's fence, not by the lease. That is good enough for a
    lease-bounded measurement, but it is a fence by coincidence of prefixes, not by design. See condition 4.

## What I checked in the code

- `app/server.py`: two hunks only, the import and `start()`/`install_heap_signal()`/`stop()` in `lifespan`. The listener's bind
  failure is caught so it cannot take the gateway down.
- The SSRF gate: `OG-sec-1` reads CLEAN (0 controllable of 18; the real denominator is 20, row Z-S384, named in the ask).
- `harvest_research.py` blob `574959b682` is carried. No IAM, env, unit, tool or description change.

## Blast radius and both branches

- **At rest (how this ships):** the listener refuses everything, and the gateway's tools and answers are unchanged.
- **Armed (Phase B only, 45 minutes, plus a 2-minute expiry check):** the two tools answer for the one account, every call is
  audited, and disarm is the parameter's deletion plus the 5 s cache.
- **Rollback:** the `aa2efa2cf3` tree through the same wrapper, plus deleting the lease. The rollback code has no listener at all.

## Conditions (carried, not grounds)

1. **I concur in the CTO's CT3** (the probes stop if the service exceeds 1200 MB) **and CT4** (the Z-S338 bound is fixed before
   the run).
2. **No probe response body is ever persisted.** `CODE9_SERVED.json` and every report hold counts, hashes and heap figures only.
   The transactions answers are a client's rows: they are read from the SSM output, reduced to counts and sha256, and the raw
   output is not written to the repo, a row or a message.
3. **Disarm is shown by two reads before the ledger closes:**
   - `get-parameter /opal-gateway/probe/lease` answering ParameterNotFound;
   - a call refused 403 after the 6 s wait.
   "Deleted" without the read is not disarmed.
4. **Before any SECOND arming of this listener, pin the firm.** Either the lease carries the firm and the listener refuses any
   other, or the listener derives the firm from the lease's reference. This is a follow-up cell, not a hold on Phase B, whose one
   arming is the operator's own call with the test account's own firm.
5. **Z-S375 and Z-S338 disarm on Phase B's service-heap reads,** against CT4's bound fixed beforehand, through the owner's word.
6. **No client value or identifier** in any repo file, row, message or report.

-- 3.0.0_SA_CVO~Z
