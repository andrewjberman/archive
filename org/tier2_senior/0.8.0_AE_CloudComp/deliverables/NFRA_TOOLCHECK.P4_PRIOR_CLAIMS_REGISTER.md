# NFRA_TOOLCHECK P4 — PRIOR-CLAIMS REGISTER (cross-program seam inbox)

**Owner:** `0.8.0_AE_CloudComp~Z` · **Opened:** 2026-08-11 ~2325Z · **Program:** the instruments
atom_decomp program (CTO~Z).

**STATUS — RULED PROGRAM-WIDE (CTO~Z 20260811T232506Z), bound as §9.8.1-Q.** One register per
program; this is the instruments program's, OPAL_ANALYST gets its own. **It is the RECEIVING HALF OF
EVERY SEAM**, in the ruling's binding form: *a seam without a receiving half is a one-way pipe that
reports delivery.* Entries are **PRIORS-UNDER-TEST for future runs**, never facts, never edits to
closed runs.

**Why this file exists.** The cross-program seam (CTO~Z, release 192924Z) routes comp-tool defects
found by other programs to this seat as PRIOR CLAIMS for the rectangle. **A claim that arrives after
its subject's run is CERTIFIED has nowhere to go** — a certified rectangle is not edited, and
attempts accumulate rather than absorb. Without a register the claim evaporates between runs, which
is the same silent-loss shape the program exists to catch. **The structural root, per the ruling:
runs SEAL by construction while routing is CONTINUOUS** — so the retention gap is not an oversight
in the seam, it is what a seam without a receiver always produces.

---

## PC-001 — comp-estate `frontend:` row on `keyword-drilldown-history` names a consumer that does not consume

| | |
|---|---|
| **Raised by** | `0.5.0_AE_OpalETL~Z`, 20260811T231927Z, from the W3 `/macro` program |
| **Subject** | `comp-estate` — the **consumer-topology (`frontend:`) verdict surface** |
| **Status** | **CONFIRMED by independent measurement** (this seat, 2026-08-11 ~2330Z) — but NOT certified; a prior for a future run |
| **In AD2's rectangle?** | **NO, and correctly so.** AD2's `fv.03` entity was scoped by its axis to comp-estate's *provenance/vintage header* verdicts. The `frontend:` row is a **different verdict surface of the same tool** — outside that entity's declared scope, and the run is CERTIFIED + CLOSED (@1dea476ca5). |

### The claim comp-estate makes (verified verbatim at the tool, not relayed)

`comp-estate news` → chain `keyword-drilldown-history` → `frontend:` row:
> `portal/src/api/endpoints/sentiment.ts getKeywordSentimentHistorySummary/Articles -> /api/general/sentiment/keyword-history-summary|articles/{keyword}.json; consumed by KeywordSentimentModal.tsx`

Reproduced by running the tool (`comp-estate news`, rc=0, output line 32).

### Independent measurement (this seat) — portal submodule on **DEV** @ce98e334, read-only

1. `KeywordSentimentModal.tsx` **EXISTS** at `portal/src/components/market-performance/`. The row
   does not name a phantom file — which is precisely what makes it credible.
2. `getKeywordSentimentHistorySummary` / `...Articles` / `getKeywordSentimentHistory` have **ZERO
   call sites outside their own definition file.** Every hit across `portal/src` is inside
   `sentiment.ts` (definitions at :614/:658/:695; the only internal calls are the DEPRECATED
   `getKeywordSentimentHistory` invoking the two tiered functions at :701-702, and that deprecated
   wrapper itself has no callers).
3. **POSITIVE CONTROL, same search, same corpus:** `getKeywordIntelligence` returns a genuine call
   site — `KeywordSentimentModal.tsx:15` (import) and **`:128`** (`await getKeywordIntelligence(keyword.keyword)`).
   **The control is decisive because it is a SIBLING accessor called by THE VERY FILE under
   examination:** if the search could not see callers, it would have missed this one too.
4. So the modal is a **real consumer of `keyword-intelligence-gpt`** (whose `frontend:` row is
   TRUE) and **not** of `keyword-drilldown-history` (whose `frontend:` row is FALSE). **The tool
   carries one true row and one false row of identical shape, adjacent in the same output.**

### Correction to the raiser's evidence (conclusion right, control not what it was called)

`0.5.0_AE_OpalETL~Z` cited *"POSITIVE CONTROL: `getKeywordSentiments` returns 2 callers, so the
instrument can find callers."* Measured here, `getKeywordSentiments` returns **2 hits, neither of
which is a call site** — a definition (`portal-proxy.ts:1910`) and an export-barrel entry (`:2174`).
**A control that returns the same zero-call-site shape as the target does not discriminate**, so as
stated it demonstrated nothing. Their **conclusion is correct and independently reproduced**; only
the control under it was mis-described. Recorded because the register their disposition feeds is
only as strong as the control beneath it, and because this is the program's own recurring class —
a right conclusion resting on a mechanism that does not hold — arriving inside a message *about*
that class.

**THE MECHANISM, found by the raiser on acceptance (232543Z) and REUSABLE — it is the part worth
keeping.** Their search excluded the definition file of the functions **under test** (`sentiment.ts`).
The control function lives in a **different** file, so *its* definition and barrel entry were never
excluded and were counted as callers. **THE EXCLUSION WAS TARGET-SPECIFIC AND WAS NEVER APPLIED TO
THE CONTROL** — the control was inflated by exactly the artefact they had been careful to strip from
the target. **Standing form: a control not filtered identically to the target is not a control**; an
asymmetric exclusion manufactures the discrimination it claims to prove. Sharper than my own
correction, which named the symptom (same shape as the target) without the cause.

**Closing the set — this seat's addition, adopted by the raiser.** Their measurement showed the
accessors unreferenced; the wrapper reading shows the dead set is **CLOSED**: the deprecated
`getKeywordSentimentHistory` (:695) is the only thing that reaches the tiered accessors (:701-702),
and it has no callers itself. Nothing outside reaches in, and the one thing that reaches them is
itself unreached — a stronger basis for RETIRE-CANDIDATE than unreferenced-ness alone.

**Adjacency, extended by the raiser:** a reader who spot-checks one `frontend:` row and finds it
correct is thereby MORE likely to trust its neighbour — **so spot-checking is not sampling**. Same
structure as `/positioning`'s footer being right for one of three artifacts.

### Why it matters beyond a stale string

**Trusting the row would have INVERTED a cleanup disposition on 720 keys.** The raiser is authoring
the residue register Andrew's cleanup decision reads from; two 360-key families (frozen since
2026-04-07) are dispositioned RETIRE-CANDIDATE on being UNCONSUMED. Read as evidence, this row would
have recorded them CONSUMED → RETAIN — the opposite recommendation, in the document a human acts
from. A false consumer edge does not merely misinform: it propagates into a disposition.

### The actionable gap (raiser's framing, source-confirmed here)

`comp-estate`'s header carries exactly one caveat: *"freshness adjectives inside chain prose are
CENSUS-VINTAGE claims (snapshot vintage in the header), never live reads."* **Nothing scopes the
`frontend:` rows.** A `frontend:` row is not a freshness adjective and not a NAME-vs-KEY question
(Rule 21's documented split) — it is a **structural consumption claim**, and it inherits snapshot
vintage with no declaration saying so. **A reader who correctly heeds every documented caveat can
still be misled by the consumer topology.** That is the finding for the future run: the scope of the
declared caveat is narrower than the scope of the output it appears above.

### Hypothesis, explicitly NOT a finding (raiser's, unconfirmed by either seat)

The modal may once have consumed the history accessors and been migrated to `getKeywordIntelligence`,
with the census row not following. Consistent with the artifacts frozen 2026-04-07 and the producer's
EventBridge cron reading DISABLED. **Neither seat confirmed the migration; it is carried as a
hypothesis, and a future run must not promote it by repetition.**

### Disposition — **LIVE INPUT, not a someday entry (CTO~Z 232506Z)**

- **ROUTED BY CTO~Z INTO W3b THIS TURN**, with this seat's positive control attached, as a
  prior-under-test for `0.5.0_AE_OpalETL~Z`. W3b is measuring the news subsystem now and its central
  deliverable IS the residue disposition register Andrew's cleanup decision reads from — the row
  would flip 720 frozen keys from RETIRE-CANDIDATE to RETAIN if read as evidence.
- **The header-caveat finding is the longest-reach item and the tool-owner remedy is CTO~Z's to
  route**, with the generalisation recorded in the ruling: **a PARTIAL caveat set is more dangerous
  than none, because it signals the caveats have been thought about.**
- **No fix, no retirement, no edit to any closed run** (findings-only; Rule 9).
- Still registered as a PRIOR-UNDER-TEST for the next comp-estate decomposition, where the entity
  should be scoped to the consumer-topology surface rather than the provenance header.
- Raiser's verdict needs no correction; the control note is theirs to fold.

---

## PC-002 — comp-estate `trigger:` row on `opal-security-scanner-processor` attributes a SERVING route to a PRODUCING lambda

| | |
|---|---|
| **Raised by** | `0.5.0_AE_OpalETL~Z`, 20260812T040837Z (surfaced originally by `0.1.0_DE_MarketIntelligence~Z` — see below) |
| **Subject** | `comp-estate` — the **trigger-topology verdict surface** (a THIRD field, after PC-001's consumer topology and AD2's provenance header) |
| **Status** | **CONFIRMED — and refuted on a LIVE PRIMITIVE, not on the docstring the raiser led with** |
| **In any rectangle?** | No. PRIOR-UNDER-TEST for the next comp-estate decomposition. |

### The claim (verified verbatim at the tool: `comp-estate security-scanner`, rc=0, line 10)

> `trigger: portal API proxy via CloudFront /api/scoped/security-scanner/factors (no EventBridge schedule, no event-source mapping; invoked on request)`

### Independent measurement (this seat, 2026-08-12 ~0415Z, read-only)

1. **THE DECISIVE PRIMITIVE — the resource policy makes the claim IMPOSSIBLE, not merely
   unsupported.** `aws lambda get-policy --function-name opal-security-scanner-processor` (rc=0)
   returns **exactly one statement**: `AllowS3InvokeSSCNProcessor`, `Principal.Service:
   s3.amazonaws.com`, `ArnLike AWS:SourceArn arn:aws:s3:::opal-data-portal-v2`. **No API Gateway,
   CloudFront, or other principal is authorized to invoke this function at all** — so "invoked on
   request via a portal API proxy" could not occur without a policy change. The claim is not
   evidence-poor; it is precluded.
2. **POSITIVE CONFIRMATION of the true trigger, which the docstring only asserted.**
   `aws s3api get-bucket-notification-configuration --bucket opal-data-portal-v2` (rc=0) carries 2
   Lambda configurations, one of which is **`opal-security-scanner-processor` on
   `s3:ObjectCreated:*`, prefix `security_scanner/uploads/`, suffix `.xlsx`** — matching the
   docstring exactly. **This is the check comp-trigger structurally cannot make** (its own output
   declares S3-notification triggers invisible to it), and it is what converts a producer
   self-report into a grounded fact (NEVER#7: never trust a producer's self-report).
3. **Handler attribution confirmed:** `comp-find "handle_sscn_factors" infra/aws/lambda` →
   DENOMINATOR 4 hits / 6,456 files, BANDS DEF=1; definition at `data_refresh/lambda_function.py:1604`,
   dispatch at `:1864`. The `/factors` route is served by **`data_refresh`** — a different lambda.
4. **Behavioral half reproduced:** newest `factor_metadata.json` is
   `json/security_scanner/2026-08-06/factor_metadata.json` at **2026-08-07 17:59:12**, matching the
   raiser's figure exactly. Artifacts are written **once per dated upload folder**, which is what
   S3-ObjectCreated production looks like and is not what request-invoked production looks like.
   *(Method note: my first `head-object` guessed the key and 404'd — that was MY wrong key, not an
   absent artifact, and it is recorded rather than reported as a finding. The real key came from a
   MATERIALIZED recursive listing filtered client-side, not a `--query` over a page.)*

### What this seat adds beyond the raiser's evidence

Their case rested on the **docstring** (a producer self-report), the **absence** of schedules and
event-source mappings, and **behavior** (four days of requests, zero rewrites). All three are sound
but each is an argument from absence or from self-report. **The resource policy and the notification
configuration are the live primitives that close both halves positively:** S3 is the *only*
authorized invoker, and the notification is *actually wired*. Their behavioral argument also had one
soft edge — a request-invoked producer could in principle no-op or cache rather than rewrite — and
the resource policy removes it, because the function cannot be request-invoked at all.

### The class, now with three members on three different fields

PC-001 (consumer topology) · PC-002 (trigger topology) · and both share AD2's finding that
comp-estate's header caveat scopes **freshness adjectives only**. **Three fields, one gap: nothing in
the tool's declared caveats scopes TOPOLOGY of any kind**, so a reader who heeds every documented
caveat is exposed on consumers, on triggers, and on anything else structural. And in both PC-001 and
PC-002 the row's TRUE clauses sit beside the false one — here "no EventBridge schedule, no
event-source mapping" is **correct**, which is exactly what lends the false clause its credibility.
**A partial caveat set is more dangerous than none** (CTO~Z's generalisation on PC-001) now has a
second measured member.

### Provenance worth keeping: the defect was strong enough to build a convincing plant from

`0.1.0_DE_MarketIntelligence~Z` built their certification mutant **out of this defect**, sealing it
with the reasoning that the plant is credible *precisely because a real tool says it* — "not an
invented lie; the answer the weaker method produces." They surfaced the discrepancy, declared they
had not chased it, and planted on it deliberately; the raiser caught the plant and then chased the
underlying defect. **A tool defect usable as a convincing false artifact is a stronger argument for
fixing it than any wrong-output report**, and the chain that produced this claim — plant, catch,
chase, route, independent verification across three seats — is the seam working end to end.

### THE ACTIONABLE FORM (raiser's, on amendment @bb0f653517 — the best statement of what this entry is worth)

> **All three instruments a diligent agent reaches for first are unreliable on this question, and
> the two that are reliable are one command each.**

Unpacked: `comp-estate`'s trigger row is **wrong**; `comp-trigger` **declares itself blind** to
S3-notification triggers; the producer **docstring is a self-report** (NEVER#7). Meanwhile
`lambda get-policy` (who may invoke) and `s3api get-bucket-notification-configuration` (what is
wired) each settle it in a single call. **Standing consequence they routed to CTO~Z as a method note
and this seat endorses: the resource-policy check becomes standard for every trigger claim on this
program.** A trigger assertion grounded on any of the first three, without one of the last two, is
INFERRED.

**Raiser amended their own certification rather than leaving it** (@bb0f653517), on the reasoning
that their nomination matched the seal exactly — so nothing in the outcome would ever have prompted
re-examination of *how* they got there, and **two of the four published routes would have been
copied forward by the next certifier reading that file.** §9.8.1-G's fourth relative: a conclusion
that happens to be right is not evidence for the mechanism under it, and the mechanism is what gets
reused. They also ran the binding-Y check on themselves (which decision does a self-diminishing
correction favour?) and named it: it favours the resource-policy check becoming standard. Recorded
because a correction that makes its author's evidence look weaker reads as rigour and therefore
goes unchallenged.

### Observation, flagged and NOT chased (surprise-channel discipline)

The 08-06 upload landed **2026-08-07 15:00:19** and `factor_metadata.json` was written
**17:59:12** — a ~3h gap that a prompt S3-ObjectCreated invocation would not normally show. Could be
a re-upload, a retry, a manual invoke, or an intermediate step. **Not investigated, not a finding,
recorded so the next reader does not have to rediscover the question.**

### Disposition

- **No fix, no retirement, no edit to any closed run** (findings-only; Rule 9).
- Routed to `1.0.0_SA_CTO~Z`; the tool-owner remedy is theirs. `0.1.0_DE_MarketIntelligence~Z` has a
  direct interest (their plant rests on this defect) — routing to them is CTO~Z's call, not mine.
- **PRIOR-UNDER-TEST for the next comp-estate decomposition**, which on this evidence should scope
  its entity to **topology surfaces as a class** (consumer + trigger + serving attribution), not to
  one field at a time.
