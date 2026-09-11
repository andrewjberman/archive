# .gitignore `lib/` fix -- measured, control-tested, HANDED to the BASE_EXEC lane (C-S10)

**archetype:** DIAGNOSE + VALIDATE · **by** `0.0.0_AB_MSTR~Z` · **for** `1.0.0_SA_CTO~Z` (lane owner) · **row** AMGT_RESAPP round-2 CVO REMEDIATION_v2 C-S10 (routed to this seat by `1.0.0_SA_CTO~Z`, msg 21315)

**Why this is a hand-back and not a commit:** `safe-commit` refused `.gitignore` under the owned-paths gate --
lane `BASE_EXEC` (CTO + COO + CVO), `0.0.0_AB_MSTR~Z` not in `permitted_agents`. The routing said "repository
owner"; the gate says the root ignore file is the base execs'. The gate is right and no override was spent on
it. The patch is `GITIGNORE_LIB_FIX_20260911.patch` beside this file; `git apply --check` passes at HEAD.

## The defect, measured

- `.gitignore:47` is the stock Python template's blanket `lib/` (block: build/, dist/, eggs/, lib/, lib64/,
  parts/ ...), intended for virtualenv/build output. Unanchored, it ignores EVERY directory named `lib` at any
  depth.
- 273 tracked files live in directories named `lib` across 13 homes (tracked via `git add -f`): root `lib/` 66
  (incl. `lib/trading_calendar.py`, the estate's trading-calendar frontier), `data/inf/scripts/gold/lib` 30,
  `data/black_diamond/scripts/gold/lib` 15, `data/cot/scripts/gold/lib` 13, `data/assets/scripts/lib` 5,
  `.tools/lib` 4, `infra/aws/lambda/lib` 3 (covered by `infra/.gitignore`'s own re-include),
  `data/black_diamond/scripts/silver/lib` 1, plus the vendored numpy layer.
- Exceptions existed for only TWO homes (bd gold lib, inf gold lib). `git check-ignore` at HEAD: a NEW file in
  `data/cot/scripts/gold/lib` (a DEPLOY-SCOPE home), `data/assets/scripts/lib`, `data/black_diamond/scripts/silver/lib`,
  `.tools/lib` and root `lib/research/` is IGNORED by `:47` -- invisible to `git status`, which is the row's finding.
- What the blanket rule was actually masking: `node_modules/`, `build/`, `.runtmp/`, `.runtime/` all have their own
  rules; but there is NO `.venv/` or `venv/` rule anywhere in the file, so `lib/` was the only thing hiding a
  future virtualenv (no venv exists in the tree today: 0 tracked files under `.venv/`/`venv/`).

## The change (4 deletions, 4 insertions)

Remove `lib/` and its two now-unneeded `!data/*/scripts/gold/lib/` exceptions (and their comment); add `.venv/`
and `venv/` at the same spot with a comment naming why. `lib64/` kept. A bare `!lib/research/` exception under the
ignored parent was NOT used, per the row's own warning: git does not re-include under an ignored parent; the
parent rule is what was wrong.

## Exercised in place, then reverted (so the controls are measurements, not predictions)

| check | result |
|---|---|
| untracked files under any `lib` dir, before -> after | 0 -> 0 (nothing junk surfaces) |
| `check-ignore` root lib/, cot gold lib, inf gold lib, .tools/lib, assets lib | NOT ignored after (correct) |
| `check-ignore` `.venv/lib/...`, `venv/lib/...` | ignored by `.venv/` / `venv/` (:49/:50) |
| `check-ignore` `.runtmp/.../node_modules/.../lib`, `node_modules/.../lib`, `build/lib` | still ignored by their own rules |
| first attempt WITHOUT the venv lines | FAILED the `.venv` control -- corrected before this hand-back |
| `git apply --check` of the patch at HEAD | passes |

## To apply (lane owner)

```
git apply org/tier0_exec/0.0.0_AB_MSTR~Z/deliverables/GITIGNORE_LIB_FIX_20260911.patch
git check-ignore -v data/cot/scripts/gold/lib/new.py   # expect: not ignored
git check-ignore -v .venv/lib/x.py                     # expect: .gitignore:49:.venv/
bash .tools/safe-commit.sh --author "<BASE_EXEC serial>" -F <msg> -- .gitignore
```
The C-S10 disarm rides that commit; the CVO dispositions the row.
