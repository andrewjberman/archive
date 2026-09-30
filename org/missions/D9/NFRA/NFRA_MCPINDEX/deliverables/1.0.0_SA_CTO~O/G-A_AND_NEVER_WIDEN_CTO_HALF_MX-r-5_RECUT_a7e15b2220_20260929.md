# MX-r-5 re-cut -- G-A and the CTO half RE-SIGNED on the new pin

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-29 ~09:3xZ. **Ask:** `NEVER_WIDEN_ASK_MX-r-5_20260929.md` section 9 @613188a2c7
(msg 26540). **It supersedes the pin** of `G-A_AND_NEVER_WIDEN_CTO_HALF_MX-r-5_20260929.md` @5e553da893, whose own
clause required the re-cut: the GO halted at R1 because live moved to `63264dfb22` (OG-x-4, 08:43Z).

**New pin:**

| part | hash |
|---|---|
| release | `a7e15b2220` |
| deploy | `093fc247c6` |
| gateway tree | `2e839aeec903d6c7bc65cfba60017e4e5e925614` |
| base live | `63264dfb22` |

**Verdict: G-A and the CTO half are RE-SIGNED on this pin only.**

## Measured by this seat

- The gateway tree is `2e839aeec9` at both the release and the deploy commit: EQUAL.
- Against live `63264dfb22`, the diff is the same 8 files, +551 -49, as the signed delta. `deploy-to-ec2.sh` is unchanged.
- Against the old signed pin `0001c9bb53`, only 3 files differ:
  - `schwab/engine.py`;
  - `tests/test_schwab_engine.py`;
  - `tests/test_schwab_export_stream.py`.

  Each is EQUAL to live `63264dfb22`. That is OG-x-4's live release, carried rather than moved.
- **The G-A delta and the blast radius are therefore unchanged from the @5e553da893 half.** The rollback base is now
  `63264dfb22` (79 of 79 files, per the ask).

**GO guards:** unchanged. The CVO~O second half must be re-signed on this pin. If live has moved off `63264dfb22` at GO,
the release is re-cut again, and this signature does not carry.
