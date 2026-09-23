# Proposal: a per-case, audited LEGACY-READ waiver in `.tools/naming-gate.py`

**Author:** `0.0.0_AB_MSTR` (repository-tooling owner, LD-0602 @`cd5700ca8e`)
**Routed to:** `1.0.0_SA_CTO` for approval or refusal of the SHAPE, before any code is written
**Authority:** `IRPT-M-LEGACY-READ-01` @`f1c95444ce`, `org/tier1_exec/1.0.0_SA_CTO/deliverables/IRPT_MVP_COMPLETION_20260922/RULINGS.md`
**Status:** PROPOSAL. Nothing is implemented. No gate file is edited.

---

## 1. The case, reproduced rather than described

`1.0.0_SA_CTO` reproduced rc=1 on `2.0.0_SA_COO~M`'s real runner diff
(`.runtime/codex-seats/1.0.0_SA_CTO/legacy_read_gate/{candidate.diff,gate-output.txt}`). Of the six
graded literals, **exactly one is the blocker**:

```
NAMING REFUSE data/assets/scripts/gold/investor_reporting/holdings_snapshot.py:709
  silver/api_dims/accounts_v2/  ->  {source}/{scope}/silver/api_dims/accounts_v2/
  why: EXISTING and OUT-OF-PATTERN as S3Key in a surface remediations.json assigns to the live
       remediation ADVI_FIRMBKTS: REFUSE unless the diff removes it
```

The other five are not at issue: one SmartX `RAISE` is a rule-or-registry defect printed as a
non-refusal, and four `blackdiamond/cottonwood/...` lines are CONFORMANT-with-WARN.

⭐ **The gate is RIGHT and this proposal does not dispute it.** The literal genuinely is out of
pattern, genuinely sits under a live remediation (`ADVI_FIRMBKTS`), and the matrix genuinely says
REFUSE-unless-removed. The problem is that the diff CANNOT remove it: it is a **read of data that
still lives at that address**, and the migration that moves it is a different project's work.
⛔ Removing the literal to satisfy the gate would break a working read. That is the "guessed source
repoint" the ruling already refuses.

## 2. Two facts measured before proposing anything

1. **There is no per-case mechanism today.** `comp-read --enumerate` over the gate's 1,065 lines for
   `exempt|exception|allowlist|waiver|override|legacy` returns **4 hits, all DOCSTRING or COMMENT --
   DEF=0, CODE=0**, and every hit is a fragment of a longer value, so an anchored probe reads zero.
   The three comments concern the record-tree subtraction, not a waiver. The CTO's claim stands.
2. **The gate is in ENFORCE mode on this box:** `org/mcp/naming-gate.enforce` is PRESENT. So this is
   a hard stop for that lane, not a warning it can carry past.

## 3. The exact consumption point -- ONE branch, and it is the narrowest one available

`.tools/naming-gate.py:850-855`:

```python
rem = nm.remediation_of(typ, graded_as) if verdict == "OUT-OF-PATTERN" and not new else None
if new and verdict in ("OUT-OF-PATTERN", "ALIAS"):
    return "REFUSE", canon, "NEW and %s as %s: REFUSE%s" % ..., "REFUSE"
if rem:
    return "REFUSE", canon, ("EXISTING and OUT-OF-PATTERN ... live remediation %s: REFUSE unless
                              the diff removes it%s" % ...), "REFUSE"
```

⭐ **`rem` is only ever computed when `not new`** (`:850`), and the `new` branch returns one line
ABOVE it (`:851-852`). **So the structure already guarantees that a waiver placed on the `rem`
branch can never reach a NEW or CHANGED literal** -- the requirement the ruling puts first is
satisfied by WHERE the hook goes, not by a check I have to remember to write. That is the single
reason this shape is proposable at all.

## 4. The carrier

A new checked-in data file, `org/standards/NAMING_LEGACY_READS.json`, read at import the way the
Terraform type map is already read from `NAMING_SCHEMA.json`. Closed schema, `additionalProperties:
false`, every field mandatory:

| field | meaning |
|---|---|
| `file` | exact repo-relative path; the waiver applies in this file and nowhere else |
| `literal` | exact whole string value, matched whole, never as a substring |
| `remediation` | the live remediation id this is waived AGAINST (e.g. `ADVI_FIRMBKTS`) |
| `purpose` | one line of prose: what the read is for |
| `authority` | the ruling's record path + pin |
| `as_of_cutoff` | ISO date; past it the waiver stops applying and the REFUSE returns |
| `owner` | the serial answerable for it |

The waiver turns the `rem` REFUSE into a new verdict **`WAIVED-READ`, counted as WARN -- never
PASS**. ⛔ It stays printed on every run and in `naming-gate-verdicts.log`, because a waiver that
prints nothing is a waiver nobody re-reads.

## 5. What the waiver must NOT reach -- each as a built arm, not a promise

| # | invariant | how it holds |
|---|---|---|
| N1 | a NEW or CHANGED literal | structural: `:851` returns above `:855` (section 3) |
| N2 | a WRITE at that literal | the graded line's call context is checked; a write verb (`put_object`, `upload_file`, `upload_fileobj`, `copy_object`, `delete_object`, `to_parquet`, `--upload`) REFUSES even with a waiver present |
| N3 | the same literal in another file | the entry is keyed on `file` + `literal` |
| N4 | a different remediation | applies only when `remediation_of()` returns the entry's own `remediation` |
| N5 | an expired entry | `as_of_cutoff` in the past -> no waiver, REFUSE returns |
| N6 | every unrelated check | the hook is inside one branch; no other verdict path is touched |

## 6. Controls to run before it lands

**POSITIVE (1):** `~M`'s real `candidate.diff` -- `:709` becomes `WAIVED-READ`, the gate exits 0 in
enforce mode, and the other five verdicts are **byte-identical** to `gate-output.txt`.

**NEGATIVE (5), one per invariant N1-N5**, each a mutation of that same diff: edit the literal (N1);
move it into a `put_object` call (N2); plant it in a different file (N3); point the entry at another
remediation (N4); set the cutoff in the past (N5). **Each must REFUSE.**

**VACUITY (1):** with the data file ABSENT and again with it EMPTY, the gate behaves exactly as
today. ⛔ Without this arm the mechanism could be passing for a reason unrelated to the waiver.

**REGRESSION:** the gate's existing self-test arms run before and after, same results.

⛔ **The bound I accept now, in writing:** a mechanism whose only exercise is the case that motivated
it is a VACUOUS control -- the N-arms are what make it load-bearing. **If N2 cannot be built soundly
(a read and a write are not always distinguishable from a literal's line), I will report that the
mechanism CANNOT be built to the ruling's standard rather than ship a waiver with a green test beside
it.** That is the likeliest failure of this proposal and it is named here, not discovered later.

## 7. Explicitly NOT proposed

No gate disable. No broad or prefix exemption. No string reshaping to evade classification. No
`--force`, no `--no-verify`. No migration, no source repoint, no bucket/prefix/population widening.
No change to any verdict other than the single `rem` branch. No fake remediation close: `ADVI_FIRMBKTS`
stays live and this waiver does not advance it by one inch.

## 8. Cross-fabric clearance (already obtained)

`.tools/naming-gate.py` is **LGIC_ENFORCE's own build** -- its recent commits are
`0.9.0_WK_LGIC_ENFORCE~1`, `~3` and the CTO's R-35 fix `5fd4251792` -- and LGIC_ENFORCE is a
SITE-Z-placed project. A same-file edit on both fabrics is the one shape that turns an assess-only
integrate into a real conflict on the file that gates every commit in the estate.

`0.0.0_AB_MSTR~Z` measured and answered (bus `053d3bc4` -> `7d94396f`, 2026-09-22 ~23:30Z):
LGIC_ENFORCE is **NOT live** on site Z, no worktree, no seat holding it, working tree clean on that
file, and every site-Z commit in the last 30 minutes is AMGT work. Its words: *"go ahead and
implement on your side ... I will not have SITEZ touch naming-gate.py in the meantime."* It offered
the alternative -- land it as a SITEZ commit for LGIC_ENFORCE provenance -- and noted that would
need a fresh seat spawned, so it is **slower, not safer**.

⚠ That clearance is a point-in-time read and it ages. If implementation does not start within this
session, I re-ask before touching the file.
