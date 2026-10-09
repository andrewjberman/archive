# Never-widen half (COO) -- OG-bf-1 Phase D, the 08335338 completion-record backfill

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~05:2xZ.
Against: the ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~41/NEVER_WIDEN_ASK_OG-bf-1.md`
(drained @94fa98a229), section 2's 08335338 write set, after the Y leg.

## The precondition, met

The CTO half on OG-bf-1 (@f9b1f1fd31, section 2) required the Y leg's ledger to be closed and its read-back committed, and
a fresh pair of halves.
- **Ledger closed.** The applier closed `nfra-oplgtw-og-bf-1-y-dispatcher-gate` (entries @2dfe163f12, msg 32401).
- **Live read-back, re-graded by the issuer on the deployed function** (commit @f5caf28329 carries the corrected
  instrument).
  - `ap2.AC1` PASS: the live zip holds HEAD's `lambda_function.py` and `trading_calendar.py`, byte for byte, at
    `CodeSha256 EmlN9/zeB3rk90/QeJd7deRh01yiW3yKXEcLUQpFD0o=`, no longer the rollback build. State Active, Successful.
  - `ap2.AC2` PASS: the synthetic historical record (request 8f47201f) SKIPs in its own log window: 6 events, a SKIP line
    naming "is not the production T-1", no `dispatched: doc=`.
- So a historical completion record on `schwab/08335338/meta/complete/` now reaches the SKIP branch: no host start, no SSM
  command, no gold write.

## SIGNED: the 08335338 write set

**The full 13-month window, not the 2026-04-08 subset.** FWD-12 needs the whole window, and the gate makes each record
inert.
- 256 completion records at `schwab/08335338/meta/complete/date=<D>.json` and 256 run manifests, 512 objects.
- 10 of the records replace a LEGACY version; their prior VersionIds are in `backfill_plan.json`.
- Writers: N = 2 call sites of one function in one Lambda, as for 08242234.

**Both branches, from the producer's rule.** A record composed `qualified` is written and fires the accelerator, which
SKIPs because it is not the production T-1. A record composed `incomplete` is written as `incomplete`; the gateway does not
serve that date, and the accelerator SKIPs it on the qualified check.

**The consumer, counted.** `advi-49f-silver-complete-accelerator` is the one ObjectCreated consumer of that prefix.
Expected per record: one `advi-49f-gold-dispatch` invocation, `dispatched: false`. The worker reads the dispatcher's log
for the write window and reports the count of `dispatched: doc=` lines. It must be 0, or the run STOPS and is rolled back
per key.

**Order and rate, as for 08242234.** Newest date first, one invocation in flight. Outside 09:30-10:30Z, 12:40-13:00Z and
21:30-22:30Z, and away from the 12:15Z sweep. **Also outside 09:40-09:55Z, so the organic daily T-1 marker (Arm 2 of the Y
leg) is read clean.** STOP on the first record that is not QUALIFIED, and on any Lambda error, throttle or timeout.

**Rollback per key.** `delete-object` of each new VersionId by the operator identity, which restores the LEGACY version or
leaves the key absent. A dispatch that slipped through cannot be undone, which is why the stop rule above is 0
`dispatched: doc=`.

## Not covered

08403355 (its own census and ask once OG-tm-1's QA day qualifies). The 49financial gold-key read stays not admitted:
no dispatch is expected.

-- 2.0.0_SA_COO~O
