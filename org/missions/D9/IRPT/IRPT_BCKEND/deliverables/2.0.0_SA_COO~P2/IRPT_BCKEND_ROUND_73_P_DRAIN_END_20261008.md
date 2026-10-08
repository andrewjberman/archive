# L8 drain end -- IRPT_BCKEND round 73, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~00:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** LOCAL (portal)

**Cut from:** CTO review msg 1113 of IB-pr-356 (portal b3fedfea). It passed for DEV on two conditions:
- W165-S2 disarmed before the DEV push;
- W165-S1 closed before PROD.

Issuance @bed4381aca, decomposition section 66. **Judgment criteria:** 0.

## The order

**IB-pr-359, slot ~167.**
- **Drains:** workspace @c77e7c86ea; portal commit 63b9382a on `wk-IRPT_BCKEND-167-portal`, stacked on b3fedfea.
- **W165-S2:** only `iv-e-26.wire-regen.test.ts` ran `generate()`. `gen-wire.ts` `generate()` now takes an optional out directory, and
  the test generates into a per-run `os.tmpdir()` and compares against the committed files. 0 of 25 tracked contracts/wire files
  are written. IB73-1-AC1 PASS.
- **W165-S1:** `parseIrEnvelope` cannot carry `custody-report-read`, which is not in the generated `RESPONSE_OPERATIONS`. So a named
  `validateCustodyReport` in `contracts/envelope.ts` is called by the custody read. An invalid body is refused with EnvelopeMismatch
  and mounts no document. IB73-1-AC2 PASS (14/14).
- **tsc -b:** rc 0.
- **Proof:** VALID.

## Row and the issuer's follow-up

**W167-S1.** The IB-pr-355 route row in routes.json carried no `response_schema`, and `gen-wire.ts` skips only an explicit null. So
`generate()` threw before comparing anything. This was the issuer's own regression from round 72.
- **Fixed @60f7d8f4c8:** the row now states `"response_schema": null`.
- **Re-run in worktree ~167:** IB73-1-AC1 PASS (0 tracked files written).
- **What this exposes:** with the generator running, its comparison tests now report the pre-existing drift between generated
  output and 4 committed AnalysisReport-related wire files (3 of 7 fail). That drift was measured at base before round 73 and is
  outside this cell; it is recorded for its owner.

## Still open

- **The portal DEV candidate:** `wk-IRPT_BCKEND-167-portal` @63b9382a (IB-pr-356 + IB-pr-359). Conditions met, CTO confirmation
  asked; DEV lands on Andrew's word.
- **Push state:** LOCAL at the time of writing.
