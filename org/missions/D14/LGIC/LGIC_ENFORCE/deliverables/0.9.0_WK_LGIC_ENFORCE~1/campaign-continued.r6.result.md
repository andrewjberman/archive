# LGIC_ENFORCE.TO-EN-c-33-r6 -- result

Commit: `7604292b33f9668258f8faf9f792b0eba5abd9d7` (artifacts) and the flip commit alongside this file,
both LOCAL on branch `wk-lgic-enforce-6-2`, base `a981b05ee8`. Push state: LOCAL, not pushed by this worker.

## Both denominators, instrument named

| Figure | Value | Instrument |
|---|---|---|
| `population_at_start` | **1370** | a fresh read of `PLACEHOLDER_CAMPAIGN_R5.json`'s `delta_riding_next_round.count`, re-read at WRITE time by `r6_campaign_resolve.py`, never quoted from the task order |
| `population_at_close` | **1370** | the same population re-derived AFTER the write as `len(resolved) + len(carded) + len(deferred)` over this record's own three lists |

`denominator_delta_note`: the delta is **ZERO, and that is a measurement rather than a default.** Round 5's
denominator genuinely MOVED (1411 -> 1370) because its own resolutions removed rows from the census
population it was counting. This round's population is not a census re-parse -- it is the **HANDED SET**, a
fixed list of 1370 rows, so resolving a row moves it between lists and *cannot* move the denominator. The
two figures are equal BY CONSTRUCTION of the population. A later census over `NAMING_CENSUS_REPORT` will
report a smaller brace-carrying population than 1370; that is a different denominator over a different
instrument and is not this one.

## The three inherited classes, by name

| Class | Count | Carried as |
|---|---|---|
| `TIMEBOXED_R33` | **1134** | 41 census rows resolved, 1093 DEFERRED (owner + reason each) |
| `NON_SYSTEM_PLACEHOLDER_TOKEN` | **235** | CARDED, dispositioned PER TOKEN, never deferred |
| `TYPE_MISMATCH_NEEDS_CONFIRMATION` | **1** | CARDED (owner + reason) |

Derivation: a fresh `Counter` over the handing record's `carded` rows' `reason`, computed independently of
the arm that re-derives it the same way.

## The arithmetic

```
resolved 41 + carded 236 + deferred 1093 = 1370  ==  start 1370
```

carded 236 = the 235 NON_SYSTEM rows + the 1 TYPE_MISMATCH row. Rows missing an owner or a reason: **0 of
1329**.

## Criteria, each verdict string as the run printed it

| Criterion | Verdict | Deciding line |
|---|---|---|
| C33R6-AC1 | PASS | `VERDICT: PASS-C33-START-IS-ROUND-5S-MEASURED-DELTA` |
| C33R6-AC2 | PASS | `VERDICT: PASS-C33-EVERY-CARRIED-ROW-ACCOUNTED` |
| C33R6-AC3 | PASS | `VERDICT: PASS-C33-INHERITED-CLASSES-CARRIED-BY-NAME` |
| C33R6-AC4 | PASS | `VERDICT: PASS-C33-APPLIED-FENCE-UNCHANGED` (guard; run pre-work as well as post) |
| C33R6-AC5 | PASS | `VERDICT: PASS-C33-R33-TIMEBOX-RESPECTED` (STOPPED branch, delta filed) |
| C33R6-AC6 | UNVERIFIABLE-BY-INSTRUMENT | judgment; oracle `3.0.0_SA_CVO` at L9. No verdict from this worker. |

Proof instance: `LGIC_ENFORCE.TO-EN-c-33-r6.campaign-continued.proof_of_spec.json` (this folder),
`proof-of-spec-check.py` **VALID rc=0**.

## What was resolved, and on what

25 distinct resources -> **32** `(name, type)` rows appended to `infra/logic/registry/resources.json`
(59 -> 91) -> **41** census rows. Each on TWO independent legs:

- **LEG A** a TYPE-APPROPRIATE Terraform declaration site: the enclosing block's Terraform type must map
  to that census row's own `node_type` under `org/standards/NAMING_SCHEMA.json`'s `tf_type_map`, on the
  `name_attribute` that map declares. Two of the 41 were re-read by hand and matched:
  `wp5-feeder-schedules.tf:49` (`aws_iam_role_policy`, `name = "wsb-49f-model-aua-daily"`) and
  `inf-accounts-v2-daily.tf:197` (`aws_cloudwatch_event_rule`, `name = "inf-accounts-v2-daily"`).
- **LEG B** the system already carried by that resource's OWN IAM role as an existing `resources.json` row
  with its own cited evidence.
- **LEG C** where present, the tf_file header's project code.

**Not the name's leading token** -- that is a SCOPE. `cot-pipeline` alone carries both `etfs` rows
(`cot-etf-ownership-daily-role`) and `mdpf` rows (`cot-rebalancer-runner-role`), so `cot-` resolves no
system at all.

**A defect in my own first cut, caught before the mint:** candidates were keyed on the resource NAME while
`resources.json` is keyed `(name, TYPE)` (`lib/opal_naming.py:1030-1032`), so the first run booked 4
`IAM_POLICY` rows as resolved by a Lambda's citation -- a mint for `('x','LAMBDA')` resolves nothing for
`('x','IAM_POLICY')`. No arm would have caught it.

## The 235 were never one class

Measured over the class, **nine** brace tokens are present, not the two round 5's card named:
`scope` 122, `cadence` 108, `source` 85, `system` 51, `snap` 7, `dim_name` 5, `firm` 1, `d` 1, `dc` 1.
`NAMING_SCHEMA.json` `grade.placeholder` sanctions **four** and names each one's carrier. So the class is
dispositioned per token and partitions over its own printed denominator with **zero remainder**:

```
235 = 112 SCOPE_OR_SOURCE_ONLY + 57 CADENCE_ONLY + 51 CADENCE_PLUS_SYSTEM + 15 UNSANCTIONED
```

The **51** are the group a single label hid: their `{system}` half IS inside this order's grant and their
`{cadence}` half is not, so neither remedy alone clears a row -- minting the system half would have booked
51 resolutions that still carry a brace.

## Rows filed

`LGIC_ENFORCE-W1-S70` -- OBSERVATION, **ARMED**, `disarm_owner` `2.0.0_SA_COO~G`. The 15 UNSANCTIONED rows
carry a brace `grade.placeholder` does not sanction, already present in the row's own `current` (so it is
literal text, not a gap the grade opened); all 15 are `S3Key`/repo python format templates; no declared
source exists for them in any later round. Both criteria select the SAME 15, and read UNSCOPED over all
1370 carried rows, brace-in-`current` returns 15 of 1370 with none outside the class.

## Fence and timebox

- **R-29:** `exemptions.json` byte-identical to the pinned base, **22891 == 22891**, measured before the
  work as well as after. Cleared additionally by PROVENANCE: `generated_locals.tf:1` names its own inputs
  as `over exemptions.json,scopes.json`; the only plan-time registry read under `infra/aws/terraform/` is
  `modules/opal_name/main.tf:82` on `exemptions.json`; `resources.json` reaches Terraform only in two
  GENERATED TEST FIXTURES and no round-6 cell runs `generate`.
- **R-33:** STOPPED. `stopped_on_timebox` true, `delta_riding_next_round` count **1329** owner
  `2.0.0_SA_COO~G`. Two further resources (`inf-gold-layer-runner`, `inf-gold-qa-runner`) were MEASURED on
  both legs and left unminted past the budget; each carries its full chain in its own `reason_detail` so
  round 7 mints it in one step.

## Controls

- **selftest-arms BEFORE any work:** 28 of 28 discriminate, 8 POSITIVE-SATISFIABILITY,
  `VERDICT: PASS-ARMS-DISCRIMINATE`. No arm was unsatisfiable by correct work, so no BLOCKING row was owed.
- **Mutants:** 5, each exercised ALONE, **5 of 5 FIRED**. Two of them target `c33-classes` on purpose
  because that arm has two independent halves. The fence arm was NOT mutated **by lane** --
  `exemptions.json` is outside this order's `<paths>`.
- **Restore:** verified with `git hash-object`, not a byte hash. A raw `sha256` reported RESTORE DRIFT on a
  correct restore, because `core.autocrlf=true` writes CRLF where the instrument wrote LF.
- **Determinism:** every arm twice, identical. The instrument reproduces the record byte-for-byte AFTER its
  own mint (it reads `resources.json` at the pin via `git show`, not from the worktree it writes); the mint
  is idempotent (`0 row(s)`, file md5-identical).
- **Registry validator:** `python lib/opal_naming.py validate` rc=0 before AND after the mint, 17 warnings
  both times -- none of the 32 rows added a warning or was refused.
- **Diff shapes:** `resources.json` 192 insertions / **0 deletions**; the channel 26 insertions / 1
  deletion, that deletion being the previous row's `}` gaining a comma. Channel splice verified after the
  write: fence chosen by PARSING for a list (the file's last `]` is 9336 bytes past the row array's), 147
  -> 148 rows, all four fences still parse, non-ASCII 0 -> 0 and backslash-u 78 -> 78.
- **Instrument tracked:** `r6_campaign_resolve.py` is committed inside this deliverables folder, not left
  in `.scratch/` -- row `LGIC_ENFORCE-S69` is what an untracked cited instrument costs.
