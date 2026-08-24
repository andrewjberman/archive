# TO ETFS_INGEST.TO-3 — the C2 GOLD HOME RE-POINT (`INGEST-T3-1`), scripts half: move the DEFAULTS, not the env

<task_order id="ETFS_INGEST.TO-3" project="ETFS_INGEST">
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED vintage) — cells `INGEST-T3-1` (gold home re-point, SCRIPTS half) and `INGEST-INV-4` (script env DEFAULTS == deployed env). The DEPLOY half is `ETFS_POSITIONING.TO-5` — see "The seam" below.</decomp_ref>
<certification>✅ **CERTIFIED** — `3.0.0_SA_CVO~Z`, certificate @422bdb431b, **bound to `@fcdf042972` and no other vintage**. **Not uncertified-on-face: cut after certification.** ⛔ **What the signature does NOT buy, in the certifier's words:** the run is **REDUCED-COHORT** — one independent perspective, the author's; *a certifier is the second reader, not the cohort*, and nobody has independently re-enumerated the operative surfaces. Premise-oracle verification was **a SAMPLE, NOT A CENSUS** (3 of 36 re-run, 3 of 3 reproducing; the other 33 unverified and not asserted).</certification>
<issued_to>DS-class (`data/**` per Rule 13). Seated: `0.4.0_DS_ClientPlatform~Z`.</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>SEATED. ⛔ **SEQUENCED BEHIND `ETFS_INGEST.TO-2`** — TO-2's conventions do not gate the re-point technically, but both touch the producer's contract and interleaving them makes a single review surface carry two unrelated intents. Finish TO-2's rulings first, or tell me you want them concurrent and I will re-sequence.</seating_trigger>
<placement>**SITE Z** (Rule 26; D4 is SITEZ until the project is done). You author; **AE-class applies.** No apply crosses a fabric.</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-24T20:5xZ</issued>
<status>staged — begins on GO</status>
<priority>P2 — **cheap now, dearer every week.** The producer is days old with ONE consumer and the target is greenfield. Every partition written to the old home is another object a later migration would have to reconcile.</priority>
<authority>Andrew-direct 2026-08-24 word (4): *"…to unified gold parquet format in **opal-data-etfs/gold/** for platinum json serving in opal-data-portal-v2"*, ruled at ~20:0xZ (*"all recs approved, proceed"* → **C2 RULED**, CTO~Z msg 4845). CLAUDE.md Rule 13 (lane split), Rule 17b (tiers; the amendment is routed to base CTO and does NOT gate this), Rule 22a (verify on the right layer).</authority>
</task_order>

## THE MEASURED STATE — re-derive it; do not cite mine

| fact | measured at the COO seat 2026-08-24 ~20:0xZ |
|---|---|
| the target | `opal-data-etfs/gold/` = **0 objects**, and `gold/` **does not appear at all** in the bucket's top-level listing. **Greenfield** |
| where gold writes today | `opal-data-assets/portal/gold/etfs/positioning/{book,holding}/date=…`, newest partition **`date=2026-08-21`** |
| the producer's knobs | `etf_positioning_gold.py:91-92` — `GOLD_BUCKET = os.environ.get("ETFS_GOLD_BUCKET", "opal-data-assets")`, `GOLD_ROOT = os.environ.get("ETFS_GOLD_ROOT", "portal/gold/etfs/positioning")` |
| the publisher's read root | `etf_positioning_publisher.py:62-63` — **the same two defaults**, read at `:183` / `:190`, and reported in the manifest at `:389` as `source_gold` |
| the write boundary | `_assert_write_boundary()` at `:160-178`, called at `:680` and `:763`. **TWO limbs:** the `FORBIDDEN_WRITE_PREFIXES` deny list (`:95-101`) **and** a positive limb `if not full.startswith(GOLD_BUCKET + "/" + GOLD_ROOT): raise` |
| the suite | `test_etf_positioning_upgrade_forward.py`, 284 lines. ⚠ **It uses a `check(name, ok, detail)` harness with a `main() -> int`, NOT `def test_*`.** `grep -c "def test_"` returns **0** and that is a pattern that cannot match, not an absent suite — *I made that mistake first and checked before writing it down* |

## ⛔ THE TWO THINGS THAT MAKE THIS MORE THAN A STRING CHANGE

### (1) MOVE THE **DEFAULTS**, NOT THE ENV — an env-only re-point reproduces the defect this project exists to fix

The env vars **already exist** and their defaults point at the **old** home. So there are two ways to
land C2, and one of them is the bug:

- **env-only** — set `ETFS_GOLD_BUCKET` / `ETFS_GOLD_ROOT` on the deployed function and leave the
  code defaults alone. Works. **And it leaves the tree saying one thing while the deployed config
  says another — which is `F2`'s exact class**, the applied-env-vs-running-code disagreement that is
  the reason ETFS_INGEST has a first act at all. **A later reader of `data/etfs/scripts/gold/` would
  correctly conclude the producer writes to `opal-data-assets`, and be wrong.**
- **defaults** — change `:91-92` and `:62-63` so the code's own answer is the right one, and let the
  env remain an override nobody needs to set. ⛔ **DO THIS ONE.**

**`INGEST-INV-4` is the criterion that proves you did:** after the deploy, the deployed env and the
code defaults must **agree** — not merely both be present.

### (2) AFTER THE RE-POINT, THE DENY LIST IS THE ONLY THING BETWEEN THIS PRODUCER AND A SIBLING'S LIVE TERRITORY

Today the producer writes to `opal-data-assets` and every forbidden prefix names `opal-data-etfs` —
**a different bucket entirely**, so the deny list is belt-and-braces.
**After the re-point the producer writes INTO `opal-data-etfs`, the same bucket that holds
ETFS_CANON's live `platinum/etf_ownership_dashboard.json` (6,411 B, refreshed 2026-08-24T16:00:03Z),
`daily/{49financial,cottonwood,inflection}/`, and `etf_history.csv`.**

> ⛔ **A GUARD THAT WAS REDUNDANT BECOMES LOAD-BEARING, WITHOUT ITS TEXT CHANGING.** That is the whole
> risk of this TO. `opal-data-etfs/gold/` is **not** in the deny list (correct — it is the new
> target), and the positive limb follows the re-point automatically because it is keyed to the
> configured values. ~~**So nothing in the guard needs editing**~~ **EXERCISE IT.**

### ⛔ AMENDMENT (21:4xZ) — "NOTHING IN THE GUARD NEEDS EDITING" IS **FALSE**, AND AC3'S OWN EXERCISE IS WHAT PROVED IT. THE ONE-LINER IS **AUTHORIZED**.

`0.4.0_DS_ClientPlatform~Z` ran AC3, got all three mandated cases right *and kept going*, and found
that the positive limb `full.startswith(GOLD_BUCKET + "/" + GOLD_ROOT)` **carries no trailing
separator**. **Re-derived at the COO seat, reproducing the limb exactly as written:**

| case | as written (no separator) | with the separator |
|---|---|---|
| `opal-data-etfs/gold/book/date=…` | PERMITTED | PERMITTED |
| `opal-data-etfs/platinum/…` | REFUSED-BY-DENY-LIST | REFUSED-BY-DENY-LIST |
| `opal-data-etfs/silver/holdings/…` | REFUSED-BY-POSITIVE-LIMB | REFUSED-BY-POSITIVE-LIMB |
| **`opal-data-etfs/gold_backup/…`** | ⛔ **PERMITTED** | REFUSED-BY-POSITIVE-LIMB |
| **`opal-data-etfs/goldarchive/…`** | ⛔ **PERMITTED** | REFUSED-BY-POSITIVE-LIMB |
| **`opal-data-etfs/gold-tmp/…`** | ⛔ **PERMITTED** | REFUSED-BY-POSITIVE-LIMB |

⛔ **AUTHORIZED: land the one-liner IN THIS TO, IN THE SAME COMMIT as the re-point** —
`if not full.startswith(GOLD_BUCKET + "/" + GOLD_ROOT + "/"):` plus the separator in the message.
**Same commit, so the widened state never exists in the record at all.** Add the three sibling cases
to AC3's exercise (six cases, not three).

> ⚠ **AND ONE CORRECTION IN DS~Z's FAVOUR, from a control they did not run: THE BUG IS
> PRE-EXISTING, NOT INTRODUCED BY THE RE-POINT.** I tested the OLD long root and
> `opal-data-assets/portal/gold/etfs/positioning_backup/…` was **ALSO PERMITTED**. The separator was
> missing all along. **What the re-point changed is not the flaw but its REACHABILITY** — a
> four-letter generic root has plausible siblings (`gold_backup`, `gold-tmp`) where a long specific
> one did not. **So DS~Z did not shrink the guard; they made a latent flaw reachable and then found
> it.** The fix is an improvement to a pre-existing weakness, not a repair of self-inflicted damage,
> and the record should say so.

**Their reachability bound stands and is why this is OBSERVATION, not BLOCKING:** the producer never
writes a caller-supplied key — every write composes `GOLD_ROOT + "/" + table + "/date=" + as_of` —
so no live path reaches a sibling prefix today. **A defense-in-depth loss, not an open hole.** They
stated that bound rather than letting the finding read scarier than it is, *and* refused to let it
read as harmless, "because the guard's entire job is to catch the write nobody predicted."

## The seam — this TO is the SCRIPTS half only

**`ETFS_POSITIONING.TO-5` (AE-class, `0.7.0_AE_CloudOps`) is the DEPLOY half** and is currently
`ACTIVE — queued behind TO-2's remaining leg`. CTO~Z's C2 ruling: *"TO-5's schedule apply follows the
re-point — **one deploy, not two**."*
**So: you land the scripts; the re-pointed code goes out on TO-5's existing apply. Do not ask for a
separate deploy, and do not apply anything yourself** (Rule 13). ⚠ **`etf-positioning-producer` does
not exist on the applied plane today** (`ResourceNotFoundException`) **and is absent from
`lambda-source-map.json`** — so TO-5's apply is a first-mint, and Rule 4's map entry is part of it
(surprise item Z-S-F, riding TO-5). **Nothing about that is yours; it is stated so you know what your
code is landing into.**

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`INGEST-TO3-AC1`** | **The DEFAULTS move, in BOTH files.** `etf_positioning_gold.py:91-92` and `etf_positioning_publisher.py:62-63` default to `opal-data-etfs` / a `gold`-rooted path in the **`{table}/date={D}/`** grammar. **Quote both before/after.** ⛔ **An env-only change FAILS this criterion** | `INGEST-T3-1`, `INGEST-INV-4` | **SOURCE** |
| **`INGEST-TO3-AC2`** | **The manifest does not lie about provenance.** `etf_positioning_publisher.py:389`'s `source_gold` follows the re-point, and the publisher's read path (`:183`, `:190`) resolves to the new root. **Show a rendered `source_gold` string** | `INGEST-T3-1` | **SOURCE + DATA** |
| **`INGEST-TO3-AC3`** | ⛔ **EXERCISE THE WRITE BOUNDARY — BOTH LIMBS, AFTER THE RE-POINT. A read of the deny list is not this criterion.** Show: (a) a write to the **new** target is **PERMITTED**; (b) a write to **`opal-data-etfs/platinum/…`** is **REFUSED** by the deny limb (ETFS_CANON's live territory, now the same bucket); (c) a write to some **other** `opal-data-etfs` prefix outside the gold root is **REFUSED** by the positive limb. **Three cases; (b) and (c) fail for DIFFERENT reasons and a test that cannot tell them apart has not exercised the guard** | `INGEST-T3-1` | **EXERCISED** |
| **`INGEST-TO3-AC4`** | **The suite still passes, and you state its true denominator.** Run `test_etf_positioning_upgrade_forward.py` and report **rc taken WITHOUT a pipe** plus the pass/fail counts its own `check()` harness prints. ⛔ **Do not report a `def test_` count — that pattern cannot match this suite** | `INGEST-T3-1`, `INGEST-T3-2` | **EXERCISED** |
| **`INGEST-TO3-AC5`** | **NO DATA MIGRATION, AND NO DELETION.** The existing `opal-data-assets/portal/gold/etfs/positioning/` partitions **stay exactly where they are**. This TO re-points the PRODUCER FORWARD; it does not move, copy, backfill, or delete a single object. **State the object count at the old home before and after — it must be UNCHANGED** | `INGEST-T3-1` | **DATA** |

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>⛔ **WITHDRAWN — THIS MANDATE WAS UNEXECUTABLE AND IT WAS MINE.** I required `comp-pipescript io etf_positioning_gold.py --pipeline etfs`. **`etfs` IS NOT IN THE ENUM.** Measured at the COO seat, true rc without a pipe: `--pipeline etfs` → **rc=2**, argparse `invalid choice: 'etfs'`; `--pipeline all` → **rc=1**, `Unknown script in tree [all]`, and the tool states on its own face that this is NOT a bd fallback. **`comp-pipescript` DOES NOT MODEL THE ETFS TREE AT ALL** — the valid choices are bd/inf/cot/mdpf/advi variants. **DO NOT RUN IT AND DO NOT SUBSTITUTE `--pipeline bd-gold`, which would return a confident answer about the WRONG TREE.**</run>
      <expect>Nothing. The step is withdrawn. **`0.4.0_DS_ClientPlatform~Z` surfaced this on TO-2, checked TWO ways rather than declaring a gap on one refusal — the check that caught it is theirs, not mine.**</expect>
      <if_mismatch>n/a. ⛔ **THE DEFECT WAS MINE: I MANDATED AN INVOCATION I HAD NOT EXERCISED.** `etfs` is a plausible value for this project and it does not exist. A mandate is a claim that a command runs, and I made it without running it. Routed as a comp-tool COVERAGE GAP (the sanctioned CLAUDE.md §21 lane), not as a build.</if_mismatch>
    </step>
    <step>
      <run>python -c "import ast,io; [print(n.lineno, ast.dump(n)[:0] or l) for l in [0]]" — i.e. **read the publisher's read path directly**: `grep -n "GOLD_ROOT\|GOLD_BUCKET" data/etfs/scripts/gold/etf_positioning_publisher.py`</run>
      <expect>Every site that composes a gold key: `:62-63` (the defaults), `:183` (the table key), `:190` (the book prefix), `:389` (`source_gold` in the manifest). **That four-site list IS the consumer surface `comp-pipescript` would have given you** — you enumerate it by reading, because no tool models this tree.</expect>
      <if_mismatch>A fifth site means the re-point has a surface this TO did not price. STOP and surface to COO~Z.</if_mismatch>
    </step>
    <step>
      <run>comp-blast etf_positioning_gold</run>
      <expect>Downstream limited to the publisher. The gold parquet is NOT a served key and has ONE consumer — that is what makes this cheap today.</expect>
      <if_mismatch>STOP and surface. A second consumer converts this from a re-point into a coordinated change.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>bash .tools/commit-gate.sh (both .py files)</run>
      <expect>PASS — py_compile + ds-precommit-check + ruff. `from __future__ import annotations` intact (Rule 15).</expect>
      <if_mismatch>STOP. `--force` does NOT bypass a gate FAILURE.</if_mismatch>
    </step>
    <step>
      <run>python data/etfs/scripts/gold/test_etf_positioning_upgrade_forward.py ; echo "rc=$?"</run>
      <expect>rc=0, taken WITHOUT a pipe (a pipe gives you the last stage's rc, not the suite's).</expect>
      <if_mismatch>Do not commit. A re-point that breaks the upgrade-forward proof is not a re-point.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>the AC3 three-case boundary exercise, against the committed code</run>
      <expect>permit / deny-by-list / deny-by-positive-limb, each distinguishable by its refusal message.</expect>
      <if_mismatch>Surface to COO~Z. After this re-point the guard is the only separation from a sibling's live bucket.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
  <!-- ISSUANCE half (COO~Z). POSITIONAL invocation — no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json INGEST-TO3-AC1,INGEST-TO3-AC2,INGEST-TO3-AC3,INGEST-TO3-AC4,INGEST-TO3-AC5
       ⛔ CHECK THE RC, NEVER THE OUTPUT STRING (the usage banner contains "Exit 0 = VALID"), and take
       the rc WITHOUT A PIPE. The coverage diff is BIDIRECTIONAL. -->
  <criterion id="INGEST-TO3-AC1" cell_refs="INGEST-T3-1, INGEST-INV-4"/>
  <criterion id="INGEST-TO3-AC2" cell_refs="INGEST-T3-1"/>
  <criterion id="INGEST-TO3-AC3" cell_refs="INGEST-T3-1"/>
  <criterion id="INGEST-TO3-AC4" cell_refs="INGEST-T3-1, INGEST-T3-2"/>
  <criterion id="INGEST-TO3-AC5" cell_refs="INGEST-T3-1"/>
  <expected_criteria>INGEST-TO3-AC1,INGEST-TO3-AC2,INGEST-TO3-AC3,INGEST-TO3-AC4,INGEST-TO3-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_INGEST.TO-3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Premise oracles — run at pickup

| premise | the read that falsifies it |
|---|---|
| the target is greenfield | `aws s3 ls s3://opal-data-etfs/gold/ --recursive \| wc -l` → **0** — ⛔ **pair it with a sibling that must be NON-zero** (`aws s3 ls s3://opal-data-etfs/silver/holdings/ \| wc -l` → **72**), *because a nonexistent prefix also returns 0 and a zero from a query that could not have returned anything else is not evidence* |
| the defaults point at the old home | `grep -n "ETFS_GOLD_BUCKET\|ETFS_GOLD_ROOT" data/etfs/scripts/gold/etf_positioning_{gold,publisher}.py` → 4 hits, all defaulting to `opal-data-assets` / `portal/gold/etfs/positioning` |
| the old home has live partitions | `aws s3 ls s3://opal-data-assets/portal/gold/etfs/positioning/ --recursive \| tail -4` → `date=2026-08-21` present |
| the deny list does not name the new target | `sed -n '95,101p' data/etfs/scripts/gold/etf_positioning_gold.py` → `opal-data-etfs/gold/` **absent** (correct) |
| the producer has one consumer | `comp-blast etf_positioning_gold` |

## Standing constraints

- **Rule 13:** you author `data/**`; **you do not apply.** The deploy is TO-5's.
- **NEVER#3:** the served platinum key and ETFS_CANON's live artifact are **untouched**. If your work
  implies moving a served key, **stop and route it to me** — that needs never-widen sign-off.
- **No shadow path, no parallel emitter, no standing comparator.** Build it correctly and port.
- **No alarm, no SNS, no SES, no freshness checker, no monitor.**
- **Commit to your own lane; do NOT push.** Report as **"landed LOCAL @hash, rides integration"** or
  **"on origin/SITEZ @hash (ls-remote read)"** — never a bare "landed".
- **Read the number, then write the sentence.**
- **Surprise channel:** `org/surprise_channel/ETFS_INGEST/` (`3.0.0_SA_CVO~Z`), coordinate `-Z-S{n}`.
  **OBSERVATION never interrupts; BLOCKING routes same-turn to me, cc CVO~Z; ARMED names a disarm
  owner same-turn. DISARMED ≠ REMEDIATED.** Mid-round the spec is **FROZEN** — route, do not adjudicate.
- **Status moves with the act, by you, in the same turn.**

## Why this is P2 and not P1

Nothing downstream is blocked on it: the gold producer works today, the publisher reads it, and the
platinum artifact serves. **The cost of waiting is not breakage, it is arithmetic** — every scheduled
run writes another partition to the old home, and the re-point's price is the number of objects a
future reader has to reconcile between two homes. **It is cheapest on the day the target is still
empty, and today it is empty.**
