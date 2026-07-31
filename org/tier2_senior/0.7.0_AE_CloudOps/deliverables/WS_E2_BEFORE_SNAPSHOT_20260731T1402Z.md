# WS-E2 — STEP 0 BEFORE-SNAPSHOT (contractual before-evidence)

**Lane:** `0.7.0_AE_CloudOps` (base) — dedicated WS-E2 lane per MSTR 134751Z, arch-gated by base CTO 133230Z
**Captured:** `2026-07-31T14:02:23Z` (computed offset, never a hand-typed Z)
**Program:** NFRA_VELOCITY / ESTATE / WS-E2 — Trigger-graph re-sequencing
**Status:** STEP 0 COMPLETE. No typing performed yet; no live infrastructure touched.

---

## 1. TWO-SYSTEM TRIGGER CENSUS — printed denominator

**The two numbers are stated SEPARATELY and are never summed into a single headline figure.**
`aws events list-rules` alone is structurally blind to EventBridge Scheduler; a one-system census is
silently 12 short (specimen #2, the blindness this wave exists to fix).

| System | Total | ENABLED | DISABLED |
|---|---|---|---|
| EventBridge **Rules** | **142** | 123 | 19 |
| EventBridge **Scheduler** schedules | **12** | 10 | 2 |

Region: **us-east-1**. Raw census output: `.runtmp_e2_census_20260731T1402Z.txt` (working copy).

**DRIFT vs the PRD's last measure.** The ESTATE PRD §WS-E2 records *"~143 + 11 at last measure."*
Live at this vintage it is **142 + 12** — both limbs moved. This is why the vintage is cited rather
than the figure being carried forward; a re-used denominator is a stale record with authority.

### Grounding — three independent instruments, not one

1. **`comp-trigger --list`** (the comp-which-routed tool). Self-test run BEFORE trusting its output:
   **10/10 PASS**, including `nowrite.control_can_fire` — a positive control proving the detector
   can actually find real method calls rather than passing by finding nothing.
2. **Raw live AWS** (`aws events list-rules` / `aws scheduler list-schedules`, us-east-1) — agrees
   exactly: 142 and 12.
3. **My own independent tally** of the census body by line class — agrees exactly: 142 / 12, and the
   ENABLED+DISABLED splits sum correctly within each system.

### Region denominator — a THIRD axis, closed by measurement

CTO's spec names the two-system blindness. It does not name a **region** blindness, and
`comp-trigger` declares itself `region us-east-1` only — so a single-region census could have been
silently short in the identical shape. Closed rather than assumed:

**17 regions ENUMERATED** (`aws ec2 describe-regions`), each probed for both systems.
**Exactly 1 region (us-east-1) holds any trigger.** us-east-1 = 142 rules + 12 schedules.

The single-region scope is therefore **correct, and now measured**. It was not correct-by-assumption.

---

## 2. TWO INSTRUMENT FINDINGS FOUND WHILE CAPTURING THIS (both are the named class)

### F-1 — `aws events list-rules --query 'length(Rules)'` reports **100** when the truth is **142**

The AWS CLI auto-paginates and applies `--query` **per page**, emitting two separate numbers
(`100` then `42`). An agent reading "the count" gets a clean, plausible, **wrong 100** — with no
error, no truncation warning, and no tell. Confirmed directly: `--max-items 100` returns a live
`NextToken`, so the truncation is real and silent.

This is the same failure class as specimen #2 itself — a structurally short census that renders as a
confident number — and it sits on the exact command this workstream is built around.
**Control:** sum the pages (`| awk '{s+=$1} END{print s}'`), or read the tool's printed denominator.
A wrong number is more dangerous than a zero: a zero invites suspicion, a plausible count does not.

### F-2 — my own region sweep silently reported `REGIONS_WITH_TRIGGERS=0`

The first sweep used `bc`, which is **absent** from the Git Bash 3.6.7 default install (CLAUDE.md
Rule 16 names `bc`'s neighbours; `bc` belongs on that list). Every count collapsed to `0` through the
`|| echo 0` fallback, and the sweep reported a clean, total, false negative — **the estate has no
triggers outside us-east-1** would have been "confirmed" by an instrument that could not count.

It was caught **only** because us-east-1 was a known-present positive control that the sweep failed
to find. The verdict "0 regions" was contradicted by a fact already in hand. Without that control
this would have banked as a measured closure of the region axis.
*A sweep that cannot find a known-present instance is a broken instrument reporting silence.*

---

## 3. THE NINE PROCESS DECLARATIONS — pinned at this vintage

Registry: `org/modules/graph/estate-contracts/`. **All confirmed present on `origin/CLOUD`**
(positive-controlled with `git cat-file -e`, not inferred from a local working tree).

| # | Subject | File | lifecycle_class |
|---|---|---|---|
| 1 | `process:mdpf-daily-trigger` | mdpf | UNDECLARED |
| 2 | `process:mdpf-daily-runner` | mdpf | UNDECLARED |
| 3 | `process:mdpf-freshness-checker` | mdpf | UNDECLARED |
| 4 | `process:yang-benchmarks-etf-returns` | model-portfolios | UNDECLARED |
| 5 | `process:yang-ingest-dynamodb-market-data` | model-portfolios | UNDECLARED |
| 6 | `process:yang-peer-performance` | model-portfolios | UNDECLARED |
| 7 | `process:yang-pipeline-orchestration` | model-portfolios | UNDECLARED |
| 8 | `process:MA-08-yang-generate-volatility` | model-portfolios | UNDECLARED |
| 9 | `process:yang-volatility-orphan` | model-portfolios | UNDECLARED |

**3 mdpf + 6 model-portfolios = 9.** Matches the arch-gate's stated split exactly.

**Vintage pins:**
- `mdpf.contracts.yaml` @ `7ed8a737ac` (2026-07-31T09:42:35-04:00, `0.7.0_AE_CloudOps~D`)
- `model-portfolios.contracts.yaml` @ `abb3ed61a6` (2026-07-31T08:57:52-04:00, `0.7.0_AE_CloudOps~D`)

**All 9 carry `lifecycle_class: UNDECLARED`** — producer-asserted only, solicitation outstanding on
MSTR's track. This is exactly why the park is scoped to delete-decisions and nothing else: **no
lifecycle value exists anywhere in the registry to decide a DEAD question with.**

---

## 4. THE RECORD HELD — reporting the arch-gate's own test result

Base CTO 133230Z reason 3 made this assignment a **test**: *"THE OVERLAP KNOWLEDGE IS ON ORIGIN, NOT
IN ~D's HEAD … If a new seat cannot pick this up from the record, then the record failed and I would
rather discover that now than believe it."*

**Result: the record carried it.** From origin alone — without asking `~D` anything — I recovered the
9 process declarations, the artifact/process split (6 process / 1 artifact in the model-portfolios
tranche, with only the artifact counting toward breadth), the before-pin scope, and the reasoning
behind the E2 defer. `model-portfolios.contracts.yaml:18-40` states the split, its
over-approximation, and its shrink condition **in the file**, explicitly so the reasoning could not
be left behind in messages.

That last part is the load-bearing half and it is worth naming: the author wrote down not just the
decision but *why it is temporary and what retires it* — **"A CONSERVATIVE PROXY NEVER REVISITED
BECOMES A PERMANENT TAX JUSTIFIED BY A MEASUREMENT NOBODY TOOK."** That is the sentence that made a
cold successor able to pick this up correctly, and it is the reason no briefing call was needed.

---

## 5. FIRST TYPED VIOLATION CANDIDATE — declaration and live state AGREE

Not yet a finding; recorded as the entry point for the typing pass.

`process:mdpf-daily-trigger` **declares its own violation** in E1:
> `cadence: "event-only: S3 ObjectCreated on the INF spine completion marker; no schedule of its own"`

The live census independently shows `mdpf-daily-refresh-trigger` as **`(event-pattern)`** with no
cron expression. **E1's declaration and E2's live census agree, derived independently.**

This is the schedule-floor law's named specimen — the mechanism that froze the client-facing Model
Portfolios product for six days with fresh inputs sitting unused. It needs **no lifecycle value**, so
under the arch-gate it **PROCEEDS**; nothing about it parks.

`process:yang-volatility-orphan` is the predicted first *park* instance (census-flagged
orphan-candidate, lifecycle UNDECLARED). Per the ruling: if typing says violation + deletion-
candidate, the **DELETE parks and the schedule-floor typing lands.**

---

## 6. THE BOUND ON THIS CENSUS — what it could NOT have seen

**`T = 154` is the EVENTBRIDGE-ADDRESSABLE trigger population. It is NOT the population of things that can
start a pipeline.** Stated in the census's own voice, because a denominator that does not declare its own
scope will be read as total.

**What is genuinely closed** (measured, not assumed): both systems (Rules AND Scheduler); all 17 regions;
and **all event buses — exactly one (`default`) exists, holding exactly 142 rules.** The EventBridge escape
hatches are shut, and the partition (20 event-pattern + 122 scheduled = 142, no residue) is complete **for
EventBridge rules.**

**What this census is structurally blind to — a THIRD CLASS: producer-to-producer DIRECT INVOKE.**
Not hypothetical. Source-authored and named, `infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py:246-261`
(read directly, verbatim):

> *"There are FOUR armed paths into this function, and only three are EventBridge rules … the silver
> aggregator — DIRECT lambda invoke — **NOT a rule; invisible to `list-rule-names-by-target` AND to
> `get-policy`** (an IAM-role caller needs no resource-policy statement). Disabling the rules is a
> **PLACEBO** … **THE DOORS ARE NOT THE CHOKEPOINT.** This function is: every path must pass through it.
> Assert here."*

**Measured live, independently, before reading that source:** `inf-gold-trigger` fires daily at
`13:47:24Z` with `{"mode": "full", "source": "aggregator"}` while **all three** of its EventBridge rules
are DISABLED and its resource policy names **only** those three. Three instruments — the trigger graph, the
resource policy, and a repo source search — each reported truthfully and none could see the live driver.

⚠ *That source comment describes two of the rules as ENABLED; they are DISABLED today. The comment is a
point-in-time record and its enumeration is what is load-bearing, not its state column.*

### Consequence for WS-E2's acceptance clause

**The schedule-floor law sees EventBridge. A direct-invoke-driven pipeline is outside its reach.** So
"zero unscheduled production pipelines" cannot be certified from this census alone — the census cannot
enumerate the direct-invoke class, and that limit belongs beside the intent limit already routed to CTO.

> **A CONTROL CAN BE CORRECT, DOCUMENTED, LIVE — AND STILL INVISIBLE TO EVERY INSTRUMENT AIMED AT ITS
> LAYER. The only thing that found this one was READING THE FUNCTION.**

This is E5's boundary standard applied to this census, with a source-authored specimen — the same
discipline that made all 17 regions a measurement instead of an assumption.

---

## 7. POSTURE

Zero live infrastructure touched. No deploy-completion ledger entry opened — deliberately, so that an
open entry continues to mean exactly what it is supposed to mean. No alarm, SNS topic, freshness
checker or monitor built or proposed (moratorium binds hard here, and E2 is precisely the wave whose
findings invite one). No timing finding will be called a defect before it is resolved against the
trading calendar.
