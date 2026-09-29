# TO-IB-er-401 — step 0 delivered, Cottonwood blocked on a registry row

**Seat:** `0.4.0_DS_ClientPlatform~E` | **Issuer:** `2.0.0_SA_COO~P` | **2026-09-29 ~10:2xZ**
**Status:** `E4-AC3` **PASS**. `E4-AC1` and `E4-AC2` **NOT CLAIMED** — the channel cannot be
declared. Nothing was weakened to pass. TO stays `pending`.

---

## 1. Step 0 is done — this is the part the adapter switch was waiting on

PRD v0.21 ruling 18 is implemented and both golds are re-emitted.

```
E4-AC3 PASS
  49financial: IMPLAUSIBLE-RETURN rows 2 | follow-day OK violations 0
  inflection:  IMPLAUSIBLE-RETURN rows 0 | follow-day OK violations 0
    ..0090 1Y chain  0.1020 over 249 OK days
    ..4714 1Y chain -0.6535 over 226 OK days
```

| Leg | Result |
|---|---|
| 49F re-emit | 557 of 557 days, 3,188,339 rows, 0 not computed |
| INF re-emit | 1,609 of 1,609 computable days, 1,420,782 rows, 4 ABSENT and named |
| Rows flipped | exactly 2, both 49F (2025-12-15, 2025-12-18) — the count the ruling predicted |

`FOLLOWS-DISCONTINUITY` is a sixth status. It does **not** cascade (only an `IMPLAUSIBLE-RETURN`
day triggers it) and it never overwrites a row that already carries its own named reason. The
mechanism is `ImplausibleIndex`, a memoised `(source, day) -> accounts` lookup; recursion
terminates because `_frame_for()` grades ruling 16 only. Commits `bf1683f172`, `e79dd684bf`.

**One thing to carry into the switch:** ..0090 is fixed (−91.5% → +10.2%), but ..4714 is still
−65.4% over **226** OK days against ..0090's 249. Ruling 18 removed the reversion; it did not make
that account's series complete, and a 1Y figure built from 226 of ~250 days is partial in the
sense ruling 16 already names.

## 2. Why Cottonwood cannot be declared

Two laws with no common satisfying move for this firm:

- **PRD v0.19 ruling 1** — "A new firm channel is a new entry here, never a code branch."
- **LGIC_ENFORCE DEC-6** (the naming limb) — refuses any new string in an authored file carrying a
  registered firm token; its remedy on every one is *"read it through `lookup('cottonwood')`"*, and
  `lookup()` is a permitted context **only in the Python syntax tree** — i.e. in code.

**Four candidate carriers built and graded with `python .tools/naming-gate.py --diff`. All four REFUSE.**

| # | Candidate | Verdict |
|---|---|---|
| 1 | entry key `blackdiamond_cottonwood` | REFUSE — hand-kept carrier of `cottonwood` |
| 2 | `registry_key: "cottonwood"` | REFUSE — same |
| 3 | `scope_bucket: "opal-data-cottonwood"` (the registry's own bucket for the firm) | REFUSE — *"CONFORMANT as S3_BUCKET, but a NEW hand-kept carrier"* |
| 4 | `registry_key: "F-COT"` (the tenant code the registry publishes; `lookup('F-COT')` → `key=cottonwood`) | REFUSE — hand-kept carrier of `F-COT` |

**Why 49F and INF escaped and COT cannot.** 49financial is reachable by its custody masters
`['08242234','08335338']`, neither a registered token. Inflection is reachable because its monolith
`orion` carries exactly **1** registry scope, so `firm_scope()` derives it without naming it.
Measured: `orion` → 1, `eclipse` → 1, `blackdiamond` → **2** (49financial, cottonwood). Cottonwood
carries `masters: null`. Neither route exists.

**Not the bucket fence:** `opal-data-cottonwood` was probed with `head_bucket` and **exists and is
reachable**. The registry's own alias note on that firm — *"opal-data-cottonwood does not exist
yet"* — is **stale**, and is a separate, smaller correction someone should make.

## 3. A clean key exists, the gate accepts it, and only the registry row is missing

Black Diamond issues a firm-instance prefix on every account id:

| Firm | Measured | Prefix |
|---|---|---|
| Cottonwood | 19,784 of 19,784 `AccountID` (984 distinct accounts) at `date=2026-09-24` | `z09` — 100% |
| 49 Financial | 6,202 of 6,202 `bd_account_id` in `dim_account_xref` | `z08` — 100% |

Zero overlap. A trial entry declaring `registry_key: "z09"` grades **`NAMING-GATE: PASS, 1 graded,
0 REFUSE`**. What is missing is only the row that makes `lookup('z09')` resolve — it raises
`KeyError` today — and `infra/logic/registry/` is outside this order's `<paths>` grant.

**Recommended remedy, in preference order:**

1. **`1.0.0_SA_CTO` adds a registry row keyed `z09` with firm `cottonwood`**, exactly parallel to
   `08335338 → 49financial`. Measured, vendor-issued, gate-clean. Unblocks this cell today: the
   entry is then about six declared fields and the run is one command.
2. **LGIC_ENFORCE admits the declaration's `registry_key` field as a permitted `lookup()`
   context.** Fixes the class rather than the instance — otherwise this recurs at the next firm
   that shares a monolith and has no master.

## 4. What IS built, tested and committed

Everything in the cell that does not depend on the key:

- **Price by derivation** (ruling 4's *"COT price = Market Value / Units"*). `price_of()` reads a
  declared `price_column` when there is one and otherwise derives value/quantity. The choice is
  **structural** — an entry declaring no `price_column` has no price — so it is a declaration
  shape, never a firm branch.
- **The zero-`Units` trap.** An absent *or zero* quantity yields a NULL price, which is ruling 4's
  price-missing. Measured: **1,605 of 19,784** rows carry `Units == 0` at `date=2026-09-24`; a bare
  division would have handed each an infinity.
- **The text cash flag.** `Cash Equivalent` arrives as the strings `'true'`/`'false'`, and
  `astype(bool)` on `'false'` is **True** — every holding would have become cash, every account
  would have read 0.00%, and nothing would have raised. `_flag()` is a token test that REFUSES an
  unparseable value rather than defaulting to either side. Measured: 1,522 of 19,784 are true.
- `validate_entry()` now requires one of `price_column` or `quantity_column`.

**45 tests pass** (was 41). The 49F and INF paths are untouched — all 41 prior tests pass unchanged.

## 5. Ledger — deliberately RED, and why

`irpt-holdings-gold-v021-cot-e-20260929`: **L1, L2, L3 closed with proof. L4 and L5 OPEN.**

L4 (the Cottonwood mint) was **never started** — no write was attempted. Measured, with a positive
control:

```
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_daily/     -> 0 object(s)
s3://opal-data-cottonwood/irpt/cottonwood/gold/holdings_performance_manifest/  -> 0 object(s)
POSITIVE CONTROL  .../49financial/gold/holdings_performance_daily/             -> 557 object(s)
```

So nothing is half-landed. `deploy_ledger.py hold` was **refused** — *"a half-landed deploy cannot
be HELD"* while an apply leg is open — so this record is the loud escalation NEVER-2 asks for
instead. The entry should be read as BLOCKED-NOT-STARTED, not as a forgotten open deploy.

## 6. Pointers

- Surprise row **`IRPT_BCKEND-S203`** (class BLOCKING, INERT, `disarm_owner 1.0.0_SA_CTO`)
  `@b88b92c57b` — carries all four graded candidates and the `z09` measurement.
- Commits `bf1683f172` (ruling 18), `e79dd684bf` (the COT rules), `b88b92c57b` (the row),
  merged `7e8a32fe21`. Push state **LOCAL** — `git ls-remote origin CLOUD` read `15655f4a25`.
