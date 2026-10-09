# LGIC_BLANKFIX -- round 10 drain end (2.0.0_SA_COO~B1, dell1, 2026-10-09)

**Issuance:** @46f6d8a447, `decompositions/LGIC_BLANKFIX_DECOMP.round10.md`, cut on `ledger/ROUND_ANALYSIS.round9.md` @1bd6fcf3dd
with ADDENDUM 1. The two override cells follow the laptop CTO's XA-...-3003 (a) (msg 2050).

**Switch:** `org/mcp/naming-place.enforce` has been ON since @4d2bfc6dfd. The FWD-6 live read is @8bff90628c.

**Orders:** 3 of 3 complete. Each was re-proved by the issuer in its slot's worktree before the chain-end merge. Worktrees and
slot branches are removed.

| cell | serves | merge | proof re-run by the issuer |
|---|---|---|---|
| `BF-y-1`: the audit row is committed in the commit it permits | FWD-6 | @ee10dc4c3e | `AUDIT-IN-COMMIT ok=True arms=11 held=11`; `NAMING-GATE-SELF-TEST: PASS` |
| `BF-y-2`: the override is bound to the commit message | FWD-6 | @ee10dc4c3e | `OVERRIDE-BOUND ok=True arms=14 held=14`, with the forged-row arm refused; **BY2-AC3 judgment, ungraded** |
| `BF-y-3`: the nine held entries | FWD-2, FWD-7 | @dcfb18066a | `HELD-ENTRIES ok=True entries=7 land=7 refused=0 retired=2 mapped_before=78 mapped_after=85 hole_before=0 hole_after=6`; `ROOTMAP-TEST ok=True assertions=46` |

**Hygiene at the merges:**
- Every gate exercise passes:
  - `SWITCH-ON ok=True arms=11 held=11`;
  - `OVERRIDE-ARMS ok=True arms=12 held=12` (the copy in `~1`'s folder);
  - both gate self-tests.
- `bash -n` and `py_compile` pass.
- `pytest lib/tests` reads 193 passed, 1 skipped, the same as the base.
- On the trunk, the switch is present and no real audit row exists.
- **The FWD-6 refusal was re-read on the merged scripts.** In a probe tree, safe-commit refused an unplaceable name with rc=1 and printed its owed text. Nothing landed.

## The real run at the close

`ALL_ROOTS_round10.txt` beside this file, base dcfb18066a:

`ALL-ROOTS ok=True roots_total=88 mapped=78 unmapped=10 ... hole=0 ... uncounted=1 counted_at_caller=17`

**What the figures mean:**
- **Holes:** hole=0 holds on the 78 mapped roots with the placement switch ON.
- **The nine held entries:** they are drafted, not written. Only `4.0.0_SA_CRO` writes the registry. Merged on a registry copy, the drafts give mapped 78 -> 85, with `roots_total` 88 -> 86 after the two retirements. That leaves `unmapped=1`: `advi/billing-read`, a root that is new since round 9 and named in no ruling (row D1-W2-S3).
- **The 48 holes the seven newly mapped roots open:** 41 drafted rows fill 42 of them. The 6 left are owned:
  - 4 to `1.0.0_SA_CTO`: a `bucket_of` defect (row D1-W2-S4).
  - 2 to `4.0.0_SA_CRO`: a `declared_in` on `gold/meta/pipeline-complete.json`, and the vocabulary of the word `restricted`.

## Rows

| row | kind | state |
|---|---|---|
| `D1-W1-S2` | worker | The round-9 override exercise in `~2`'s folder reads the live switch and fails O12. A corrected copy is in `~1`'s folder. |
| `D1-W1-S3` | worker, BLIND | `.tools/git-hooks/mstr-ledger-check.sh` does not name `org/audit/naming-place-override-audit.jsonl` as record-only. A real override commit may be refused there; it would fail closed. Unexercised. Owner: `0.0.0_AB_MSTR`'s hook lane. |
| `D1-W1-S4` | worker | A refusal after the naming stage can leave the row on disk to ride a later commit. This over-records and never under-records. |
| `D1-W1-S5` | worker | The hash covers the message as passed to safe-commit, not git's cleaned bytes. `-F -` (stdin) has no override reader. The trust base is unchanged. |
| `D1-W2-S3` | worker | The base has 88 roots: `advi/billing-read` is new and in no ruling. |
| `D1-W2-S4` | worker | `bucket_of` names the wrong bucket, so 4 correct rows drop. Owner: `1.0.0_SA_CTO`. |
| `D1-W2-S5` | worker | Measured exceptions: harvest 13 and mdpf-pipeline 1, where the ruling says 11 and 0. No verdict moves. |

## Open for the round-10 analysis

- **BY2-AC3 (judgment, `3.0.0_SA_CVO`).** The question: is an override now visible fabric-wide in git, and is it impossible to admit with a row written for another commit?
  - Artifacts in `deliverables/0.9.0_WK_LGIC_BLANKFIX~1/`: `exercise_audit_in_commit.py` and `exercise_override_bound.py`.
  - The two scripts: `.tools/safe-commit.sh` and `.tools/naming-gate.py`.
  - Rows D1-W1-S3 to S5.
  - `round-close-check` reads REFUSED on this one judgment, so `dep_stage` stays `EXECUTING` until it is graded.
- **To `4.0.0_SA_CRO`:** write `MAP_ENTRIES_round10.json` and `REGISTRY_ROWS_round10.json` (both in `~2`'s folder), and retire the two empty roots.
- **Not yet ruled:**
  - `advi/billing-read` (D1-W2-S3);
  - `bucket_of` (D1-W2-S4);
  - the `mstr-ledger-check` naming of the audit file (D1-W1-S3).
