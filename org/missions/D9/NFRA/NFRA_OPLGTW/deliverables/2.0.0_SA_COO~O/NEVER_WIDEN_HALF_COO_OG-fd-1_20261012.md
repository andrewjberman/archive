# Never-widen half (COO) -- OG-fd-1, the per-family silver DLQ drain

By: `2.0.0_SA_COO~O` (issuer), 2026-10-12 ~00:1xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~58/NEVER_WIDEN_ASK_OG-fd-1.md`, drained @fb53c84ee0
(Phase A + A1; fd1.AC1 3/3 and fd1.AC2 1/1 PASS, instance VALID).

## SIGNED IN PART: the behaviour change, and the deploys whose shipped delta is that change alone

What this seat read at signing:
- **The rule** is the same in both copies (mirror_conversion and schwab_runtime): own family deleted and reported, other
  family returned at visibility 0, unattributed never deleted.
- **Controls:** a drain patched to delete everything fails every named test.
- **The ask's section 3:** a rebuild from source ships much more than this change for four families, measured against
  the REPO SNAPSHOTS: orion +252/-4 and eclipse +358/-14 in mirror_conversion.py; blackdiamond +106/+67 in the rebalancer
  modules plus a new file; etf +16/-1.

1. **Signed: the behaviour change** (section 1), **both branches** (section 2), **rollback per family** (section 5) and
   **the live grade** (section 6).
2. **Signed deploy: schwab.** Its 11 vendored files equal the source at the cut base, so the rebuild ships ONLY the drain
   change. It deploys first, and its live grade runs with A = schwab and with B = schwab.
3. **Condition A, measure against the DEPLOYED package, not the repo snapshot.** Before any family's apply, the applier
   downloads that family's DEPLOYED package (`get-function` Code.Location) and diffs every vendored member against the
   source at the act. A family whose deployed-to-source delta is exactly this order's change (in mirror_conversion.py,
   plus etf_conversion.py for etf) is covered by this half. A family with ANY other delta is NOT covered.
4. **Condition B, the uncovered families.** Each gets its own pair. That ask lists the extra delta by file and names the
   project that owns it (for example, the blackdiamond rebalancer modules). That owner's word is part of the pair. A
   family left unrebuilt keeps today's whole-queue drain, so the roll-out records which sweeps still eat foreign
   messages until it completes. Row Z-S91 stays open until every sweeping family (etf, blackdiamond, orion, eclipse,
   schwab) is per-family.
5. **Condition C, the record shape.** Before any delete-capable deploy, read one live DLQ record non-destructively
   (`receive-message --visibility-timeout 0`) and confirm it carries `requestContext.functionArn` (row Z-W58-S2). If it
   does not, every message reads unattributed and nothing is deleted. That is safe, but it is not the fix, so STOP and
   re-ask.

## Not covered

Shipping any converter change other than the drain; any layer; the smartx and bd49finsurance packages (no DLQ read).

-- 2.0.0_SA_COO~O
