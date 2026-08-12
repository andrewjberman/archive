# P3 re-point: PREPARED edit surface (NOT APPLIED — AE's IAM leg lands first)

**Prepared:** 2026-08-12 ~13:57Z · `0.4.0_DS_ClientPlatform`
**Authority:** Andrew-direct 2026-08-12 "all recs approved" (P3) via COO 132630Z; option (a) ruled
COO 135005Z. **Status: PREPARED, NOTHING FIRED.**

## ⛔ THE BOOBY TRAP — read this before touching anything

COO's dispatch says "three edits: K1 `OUT_ROOT` · K2 `a00_runner.SCOPE`'s gold derivation · K3 the
literal." **The middle one is precisely worded and easy to mis-apply.** `a00_runner.SCOPE` is NOT a
gold root — it is the **firm/master scope**, and it also derives **TEN silver and meta read paths**:

| MUST NOT MOVE (silver/meta, 10 lines) |
|---|
| `a00_runner.py:43` ACC_PREFIX `{SCOPE}/silver/fact_acc/` · `:44` CONV_PREFIX `{SCOPE}/meta/conversions/` · `:50` FAM_PREFIX `{SCOPE}/silver/fact_fam/` |
| `c00_runner.py:46` TXN · `:47` POS (silver) |
| `c02_runner.py:40` POS · `:41` TXN (silver) |
| `c03_runner.py:44` TXN · `:45` POS · `:46` CONV |

**Re-pointing `SCOPE` itself would silently move every one of those reads to a root that contains no
silver.** The runners would then read nothing — and the failure would present as *"no input data,"*
not as *"wrong root,"* which is the expensive kind of wrong.

## THE REAL EDIT SURFACE — 1 + 10, not 3

**K1 — genuinely ONE line** (`runner_common.py` already separates the tiers):
`SCOPE = "schwab/08335338"` · `SILVER = f"{SCOPE}/silver"` · **`OUT_ROOT = f"{SCOPE}/gold"` <- the only edit.**

**K2 — one NEW constant + 10 gold-derived re-derivations across 6 files** (`SCOPE` untouched):
add `GOLD_ROOT` beside `SCOPE` in `a00_runner.py`, export it the same way, then:

| file | line | constant | current |
|---|---|---|---|
| a00_runner.py | 51 | OUT_PREFIX | `{SCOPE}/gold/dimensions/dim_account/` |
| a01_runner.py | 30 | OUT_PREFIX | `'schwab/08335338/gold/dimensions/dim_relationship/'` **(K3 literal)** |
| c00_runner.py | 48 | DIM_PREFIX | `{SCOPE}/gold/dimensions/dim_account/` |
| c00_runner.py | 49 | OUT_PREFIX | `{SCOPE}/gold/canonical/account_gains/` |
| c01_runner.py | 42 | C00_PREFIX | `{SCOPE}/gold/canonical/account_gains/` |
| c01_runner.py | 43 | OUT_PREFIX | `{SCOPE}/gold/canonical/account_performance/` |
| c02_runner.py | 38 | C01_PREFIX | `{SCOPE}/gold/canonical/account_performance/` |
| c02_runner.py | 39 | DIMR_PREFIX | `{SCOPE}/gold/dimensions/dim_relationship/` |
| c02_runner.py | 42 | OUT_PREFIX | `{SCOPE}/gold/canonical/client_performance/` |
| c03_runner.py | 47 | OUT_PREFIX | `{SCOPE}/gold/canonical/nna_atomic/` |

**K3 is absorbed by the K2 edit** (the literal becomes `GOLD_ROOT`-derived). Sibling audit: COMPLETE
over 47 files, exactly this 1 rogue literal, no others.

## PRECONDITION (hard, not advisory)

**AE's IAM leg must land first.** Applied-verified: `consolidation-gold-runner-role` `PutObject` at
`portal/gold/advi/49financial/...` = **implicitDeny**; at the current root = **allowed** (isolated
calls, separate positive control, Rule 22a). Needed grants at the new root: **GetObject + PutObject +
prefix-conditioned ListBucket** — the read/list halves matter regardless of knob 2's fate because
K1's own D-family reads `canonical/*`.

## VERIFICATION AT FIRE TIME (CVO parity bar §8, three legs)

1. **VALUES** — the existing harness/pin batteries.
2. **WRITE-side location** — live `head-object` at the NEW root; re-read, never the write rc.
3. **READ-side location** — assert consumers resolve to the new root.
> ⚠ **Corollary, binding:** on a cutover-window grade an **UNCHANGED vintage is a QUESTION, never a
> pass** — a stranded re-point and a quiet day are byte-identical from presence alone.

## NOT IN THIS ACT
- The `dim_relationship` two-writer defect (FILED @c127712198, bundled to P5 with the knob-2
  superseded-vs-stopped question). A cutover changes WHERE, not WHAT.
- P4 (the platinum read/serve side) — that is where NEVER#3 binds; gold is not served.
