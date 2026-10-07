# Rule-24 record: the fabric enum {laptop, site-z, dell1, dell2}

Task order NFRA_CTLPLN.TO-CT-c-6 (round 3, PRD C-PLACEMENT, FWD-7), worker 0.9.0_WK_NFRA_CTLPLN~5. The change: `FABRIC_ENUM` in
`.tools/to-pipeline-gate.py:93` went from `("laptop", "site-z")` to `("laptop", "site-z", "dell1", "dell2")`. The check lower-cases and
strips the value before the membership test; `.tools/missions-tree-index.py` reads the tuple from the gate's source by AST and holds no
copy, so it agrees by construction (its self-test arm 14 compares the AST read to an independent regex read: 38/38 PASS).

## (i) MECE over the declared domain "a box in org/devices/DEVICES.json"

| Register `name` (DEVICES.json) | Register aliases | Enum value | Resolves via `lib/devices.py resolve()` |
|---|---|---|---|
| laptop | cloud-local | laptop | laptop |
| sitez | site-z, Z | site-z | `resolve("site-z")` -> sitez |
| dell1 | (none) | dell1 | dell1 |
| dell2 | (none) | dell2 | dell2 |

Subtraction, register minus enum by exact string: `sitez` is held by the register and not by the enum. Enum minus register: `site-z`
is held by the enum and not by the register as a `name`. They are one box: `site-z` is a registered ALIAS of `sitez` (the alias source
cites "PRD C-PLACEMENT's fabric enum"). Measured plainly: the register KEY is `sitez` and the enum VALUE is `site-z`; the two spellings
differ and the gate does no alias resolution (it compares the stripped lower-cased string to the tuple). This is not mine to resolve and
I did not change either spelling. After the change every register box has exactly one enum value, and every enum value names exactly one
register box; no box is covered twice. `dell3` resolves to None in the register and is refused by the gate (test arm).

## (ii) Same grain

Each value is one box (one physical machine), the same grain as a register row. `laptop` and `site-z` were already box-grain; `dell1`
and `dell2` are each one Dell. No value names a group of boxes, a lane family (the ~Z and ~W lane families both run on the site-Z box,
`.tools/prd_signoff_lib.py:465`) or a role.

## (iii) Intent coherence

One axis: which box executes this project. A value says where the project's workers and COO lane run; it does not say what the project
is, who owns it, or its stage.

## (iv) State coherence: what a change of the value does NOT move

Changing a project row's `fabric` does not move: its `placement` (the separate field naming the box and lane family), its `coo_lane`
(the lane the tree row names), its inbound queue (queue names derive from the device register, not from this value), its `dep_stage`,
or its `directive`. `.tools/sequence-check.py` compares the project's fabric to the box's register name with hyphens stripped
(`:346-348`), so a Dell project is `mine` only on its own Dell; the per-fabric COO cap (`capacity()`, `caps.get(box)`) reads None for a
box the SEQUENCE.yaml `capacity.coo_sessions` map does not list, which moves nothing. No `project.json` row was flipped by this order;
those rows are the CTO's.

## Admission arm, as measured (`python .tools/tests/test_fabric_enum_dell.py`)

dell1, dell2, laptop, site-z admitted; `"DELL1 "` (capitals and a trailing space) is ALSO ADMITTED, because the check strips and
lower-cases (this is the existing behaviour for every value, not new); `dell3` is refused ("NOT in the ratified enum").

## Token census (`python .tools/tests/fabric_value_census.py`)

Scope: tracked files under `.tools/`, `lib/`, `org/devices/`, `org/modules/`, `.claude/skills/`, `org/standards/` (git ls-files; binaries
and files over 1 MB skipped). A hit is `site-z` or `sitez` on a word boundary (case-insensitive) within the same line as, or within three
lines of, the word `fabric`. The classification table is path-keyed inside the script, with `path:line` overrides for the two files that
mix classes (`surprise-row-gate.py` is a one-line COMPARES inside a file of comments and fixtures; `to-pipeline-gate.py:93` is the
ENUM-SOURCE inside a file whose other hits are display text). Every hit was classified by reading it.

```
.claude/skills/daily-sprint/SKILL.md:9  DISPLAY  | directives, the work done both by the local fabric and the sitez fabric and rewrite the attached
.claude/skills/daily-sprint/SKILL.md:39  DISPLAY  | 5. **Cross-fabric:** site-Z landings come from ferried records at parity (cite the record/commit);
.claude/skills/govern/SKILL.md:81  DISPLAY  | > the sitez MSTR~Z. I have tried to keep the fabrics relatively quarantined by assigning them
.claude/skills/govern/SKILL.md:90  DISPLAY  | sitez-placed set. Terse; measured beats complete. Their answer folds into the next cycle report.
.claude/skills/integrate-directives/SKILL.md:82  DISPLAY  | python .tools/integrate-directives.py digest --ref origin/CLOUD      # or origin/SITEZ
.claude/skills/integrate/SKILL.md:9  DISPLAY  | > ONE TRUNK -- retire SITEZ, site Z works on CLOUD.
.claude/skills/integrate/SKILL.md:18  DISPLAY  | LD-0613. The last `SITEZ` tip is tag `archive/SITEZ-20260924`. The portal has run this way on one `DEV` all along.
.claude/skills/mstr-kill/SKILL.md:205  DISPLAY  | fabric on this device (the `~X` cohort fence and its site-Z analogue stand) â€” that is MSTR's
.claude/skills/mstr-review/SKILL.md:139  DISPLAY  | > too, so a site-Z pass finds 6/6 canonical Tier-1 serials absent, raises a fabric-wide
.claude/skills/self-drive/SKILL.md:10  DISPLAY  | 2. *"Then make this loop a skill called /self-drive, where the user can write /self-drive to a single project or group of projects as a func
.claude/skills/self-drive/SKILL.md:29  DISPLAY  | - `laptop directives` / `sitez directives` â€” every LIVE directive whose `device` is that fabric.
.claude/skills/self-drive/SKILL.md:42  DISPLAY  | **0.2 Device guard (Rule 26 + the coordination-only law).** Resolve THIS device the way the estate already does (`bash .tools/agentbus-sqs.s
.tools/agentbus-sqs.sh:112  DISPLAY  | # governance instrument could read. So a reviewer had to HAND-COPY "[laptop, sitez]" into the review.
.tools/comp-system:17  DISPLAY  | #                              #   default compile (site-Z --help incident 2026-08-20, @f5155c2aba)
.tools/direct-act-order.py:494  FIXTURE  | criteria_text=criteria_text, round_n="1", fabric="site-z",
.tools/direct-act-order.py:533  FIXTURE  | criteria_text=criteria_text, round_n="14", fabric="site-z",
.tools/direct-act-order.py:558  FIXTURE  | criteria_text=criteria_text, round_n="14", fabric="site-z",
.tools/hooks/presence-stamp.sh:12  DISPLAY  | #   device   `.tools/agentbus-sqs.sh device` (laptop | sitez), the fabric's one device resolver
.tools/integrate-directives.py:18  DISPLAY  | integrate-directives compare [--json]     per row, with an authority verdict (--b defaults to the archived SITEZ tip)
.tools/prd-header-notify.py:49  DISPLAY  | # LANE-HOMED RECIPIENT (2026-09-03, 1.0.0_SA_CTO on 0.0.0_AB_MSTR~Z's site-Z finding, relay 93296 item 2): the
.tools/prd_signoff_lib.py:465  DISPLAY  | separates DEVICES, not lane families. Both the ~Z and the ~W families run on the site-Z device, and Andrew split
.tools/prd_signoff_lib.py:467  DISPLAY  | fabric explicitly to work on RESAPP while the ~Z agents work on POSN_ASTTAX." Both rows read fabric=site-z, so a
.tools/proof-of-spec-check.py:208  DISPLAY  | #     `broker.py` passed because an exclusion about the site-Z FABRIC LEG happens to
.tools/sequence-check.py:550  FIXTURE  | "D": {"dep_stage": "REGISTERED", "status": "active", "fabric": "site-z", "_act": "abc 2026-09-19T00:00:00+00:00"},
.tools/sequence-check.py:569  FIXTURE  | rows["N"] = {"dep_stage": "EXECUTING", "status": "active", "fabric": "site-z", "_act": "abc 2026-09-19T00:00:00+00:00",
.tools/sequence-check.py:573  FIXTURE  | doc["projects"]["N"] = {"fabric": "site-z", "stage": 1, "waits_on": []}
.tools/surprise-row-gate.py:627  DISPLAY  | # remediation_row.schema.json:21, SITEZ by censusing the rows -- and converged on the identical
.tools/surprise-row-gate.py:900  DISPLAY  | 100 already-committed laptop rows arriving by an authorised CLOUD->SITEZ merge read as native
.tools/surprise-row-gate.py:925  DISPLAY  | CLOUD->SITEZ leg, with the gate's refusal text citing Andrew correctly the whole time. A guard
.tools/surprise-row-gate.py:2042  COMPARES  | id_fabric = "site-z" if (m and m.group("z")) else "laptop"
.tools/surprise-row-gate.py:2052  DISPLAY  | out.append("%s: fabric=%r but the id %s the Z- infix, which means %r. site-z iff the id "
.tools/surprise-row-gate.py:2053  DISPLAY  | "carries Z-." % (rid, row["fabric"], "carries" if id_fabric == "site-z" else "lacks",
.tools/surprise-row-gate.py:2737  DISPLAY  | # Measured: 100 already-committed IRPT_FNTEND rows arriving by an authorised CLOUD->SITEZ
.tools/surprise-row-gate.py:3487  FIXTURE  | ("identity half: X_PRJ-W2-S1 with project X_PRJ agrees; X_PRJ-Z-W2-S1 reads site-z",
.tools/surprise-row-gate.py:3489  FIXTURE  | and any("site-z" in x for x in _check_row({"id": "X_PRJ-Z-W2-S1", "project": "X_PRJ", "fabric": "laptop"}, "INVESTIGATION", {"properties": {
.tools/tests/test_direct_act_order.py:170  FIXTURE  | (proj / "project.json").write_text('{"fabric": "site-z", "dep_stage": "EXECUTING"}\n', encoding="utf-8")
.tools/to-pipeline-gate.py:93  ENUM-SOURCE  | FABRIC_ENUM = ("laptop", "site-z", "dell1", "dell2")
.tools/to-pipeline-gate.py:2313  DISPLAY  | # cannot have work dispatched against it -- the laptop and site-Z fabrics are different worlds
.tools/to-pipeline-gate.py:2317  DISPLAY  | return ["%s: project %s declares NO fabric. Step 3 requires the laptop-vs-site-Z call to "
.tools/to-pipeline-gate.py:3101  DISPLAY  | print("[to-pipeline-gate --sweep] fabric across org/projects/  (step-3 laptop-vs-site-Z fork)")
.tools/to-pipeline-gate.py:3256  DISPLAY  | # orders (each verified present at origin/SITEZ with `git cat-file -e`) were refused as "a NEW
lib/research/filings/fetch.py:37  DISPLAY  | EGRESS: Andrew-direct 2026-09-15 ~05:42Z @dfa63b6d92, "The whole sitez fabric
lib/research/social/collect.py:40  DISPLAY  | ~05:42Z, "The whole sitez fabric has free egress this session").
org/devices/DEVICES.json:42  ENUM-SOURCE  | "name": "sitez",
org/devices/DEVICES.json:44  ENUM-SOURCE  | "site-z",
org/devices/DEVICES.json:47  ENUM-SOURCE  | "aliases_source": "site-z: PRD C-PLACEMENT's fabric enum; Z: the lane-letter suffix of existing per-box files (INVESTIGATION_v1.Z.md), read 
org/devices/test_readers.py:103  FIXTURE  | rc, out = bash(["device"], dict(base, AGENTBUS_DEVICE="site-z", AGENTBUS_REG_KEY=NO_KEY))
org/devices/test_readers.py:104  FIXTURE  | results.append(("environment: AGENTBUS_DEVICE=site-z resolves sitez", rc == 0 and "device: sitez" in out
org/modules/graph/tests/nerves_resolve_battery/run_battery.py:153  FIXTURE  | r = nr.resolve("SITEZ::CLAUDE.md")
org/modules/graph/tests/nerves_resolve_battery/run_battery.py:155  FIXTURE  | assert r.fabric == "SITEZ", r.fabric
org/modules/graph/tests/nerves_resolve_battery/run_battery.py:315  FIXTURE  | there = nr.resolve("SITEZ::CLAUDE.md")
org/standards/PRD_HEADER.schema.json:20  ENUM-SOURCE  | "enum": ["laptop", "site-z"],
org/standards/test_artifact_coverage_both_grammars.py:16  DISPLAY  | exclusion about the site-Z fabric leg contains the word "broker". A false FAIL is loud and gets
FABRIC-CENSUS files_scanned=1692 hits=53 enum_source=5 compares=1 display=33 fixture=14 unclassified=0 ok=True
```

Counts: files_scanned=1692, hits=53, ENUM-SOURCE=5, COMPARES=1, DISPLAY=33, FIXTURE=14, UNCLASSIFIED=0.

Reading of the non-DISPLAY hits:
- ENUM-SOURCE (5): `.tools/to-pipeline-gate.py:93` (edited here); `org/devices/DEVICES.json:42,44,47` (the register's `sitez` name, its
  `site-z` alias, and the alias-source note: read, never edited); `org/standards/PRD_HEADER.schema.json:20` (a second enum literal
  `["laptop", "site-z"]` for the PRD header's fabric: NOT in the grant, still two values; rowed).
- COMPARES (1, outside the grant): `.tools/surprise-row-gate.py:2042` -- `id_fabric = "site-z" if (m and m.group("z")) else "laptop"`,
  then `:2051` refuses a new surprise row whose `fabric` differs from `id_fabric`. A two-way branch on the pair: a Dell-box row carrying
  its true fabric is refused. Not edited; rowed as NFRA_CTLPLN-W5-S1 together with the PRD_HEADER.schema.json enum (ARMED, disarm
  owner 2.0.0_SA_COO~C).
- COMPARES inside the two grant files: none. `to-pipeline-gate.py` reads FABRIC_ENUM at the refusal and the sweep flag, both by
  membership in the tuple, so they follow the enum. `missions-tree-index.py` holds no site-z token.
- FIXTURE (14): self-test or test data that writes `site-z` rows (`direct-act-order.py`, `sequence-check.py`, `test_direct_act_order.py`,
  `test_readers.py`, `run_battery.py` -- whose `SITEZ::` fabric is the nerves resolver's trunk name, a different use of the word --
  and two `surprise-row-gate.py` self-test lines).
- DISPLAY (33): skills prose, comments, error text.

Census blind spot (the denominator printed bounds it): a reader that compares a fabric value with neither the token `site-z`/`sitez`
within three lines of the word `fabric` is not a hit. Besides the hit list I read `.tools/sequence-check.py:183-215, 301, 340-350,
396-408` (found because they handle `fabric`) and grepped the scoped tree for `!= "laptop"` and fabric-vs-"laptop" comparisons (none).
