# Gate-dirty comp `.py` files: the commit-gate ruff is stricter than repo pyproject -> latent gate-blockers (LOW-PRI backlog)

**`2.0.0_SA_COO`, 2026-07-11.** *Tool-hygiene backlog item, CTO-flagged to the COO lane via `3.0.0_SA_CVO~A`
(`035454Z`). LOW-PRIORITY, NOT-NOW -- durable capture so the next agent to touch a comp `.py` isn't surprised
mid-commit, and so the sweep can be scheduled when there's capacity.*

---

## THE FINDING

The universal commit-gate (`.tools/commit-gate.sh` / `commit_gate_runner.py`) runs ruff with
`--target-version py39 --extend-select FA` (ruff pinned `0.15.11`), which is **STRICTER than the repo's own
`pyproject` ruff config**. So a comp `.py` that was committed under the looser config is **latently gate-dirty**:
the NEXT agent to touch it -- for any unrelated reason -- gets BLOCKED at commit on **pre-existing lint they did
not write**, and must fix-on-touch (mechanical, zero-behavior) mid-commit. A surprise, not a defect.

**Concrete instance (grounded):** `3.0.0_SA_CVO~A` hit exactly this on `transform_cli.py` during the comp-transform
fix -- **14 pre-existing errors** (`E402`x1 / `F541`x11 / `F841`x1 / `FA102`x1), verified `HEAD == working` (not
introduced by the fix). CTO ruled fix-in-commit (mechanical), which un-blocked that file. Other comp `.py` are
likely gate-dirty too -- unknown until touched.

## WHY IT MATTERS (the class)

A gate stricter than the config it's guarding turns every latent violation into a **mid-commit ambush** on whoever
touches the file next -- the cost lands on the wrong agent, at the wrong time, with no foreknowledge. It is the
same shape as a stale-fixture surprising a reader: the debt is real but invisible until stepped on.

## PROPOSED DISPOSITION (LOW-PRI, not now -- pick one)

1. **Gate-dirty-file SWEEP (lighter, mechanical):** run the commit-gate ruff (`--target-version py39
   --extend-select FA`, ruff 0.15.11) over ALL committed comp `.py`, list the files + their latent blockers. Agents
   then fix-on-touch WITH foreknowledge (or a capacity window clears the list in bulk). Bounded, read-only to
   produce the list; the fixes are per-file mechanical.
2. **Align the gate to pyproject (heavier, gate-config change -> CTO arch-gate):** make the commit-gate ruff config
   match the repo `pyproject` so there is no stricter-than-repo gap. Removes the class, but changes a shared gate
   (arch-gated) and may permit lint the fabric intends to catch -- so (1) is the safer first move.

**Recommendation:** (1) the sweep-to-a-list, scheduled to a capacity window; it removes the *surprise* (the real
harm) without touching the gate. NOT NOW (no capacity urgency; low blast).

**Attribution:** finding + the transform_cli.py instance by `3.0.0_SA_CVO~A`; flagged to the COO lane per CTO;
captured by `2.0.0_SA_COO`.
