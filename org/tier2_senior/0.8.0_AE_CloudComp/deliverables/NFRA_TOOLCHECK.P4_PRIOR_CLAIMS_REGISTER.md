# NFRA_TOOLCHECK P4 — PRIOR-CLAIMS REGISTER (cross-program seam inbox)

**Owner:** `0.8.0_AE_CloudComp~Z` · **Opened:** 2026-08-11 ~2325Z · **Program:** the instruments
atom_decomp program (CTO~Z).

**Why this file exists.** The cross-program seam (CTO~Z, release 192924Z) routes comp-tool defects
found by other programs to this seat as PRIOR CLAIMS for the rectangle. **A claim that arrives after
its subject's run is CERTIFIED has nowhere to go** — a certified rectangle is not edited, and
attempts accumulate rather than absorb. Without a register the claim evaporates between runs, which
is the same silent-loss shape the program exists to catch. Entries here are **PRIORS-UNDER-TEST for
a FUTURE run** (per the standing seed-(a) ruling), never facts, and never edits to a closed run.

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

### Disposition

- **No fix, no retirement, no edit to any closed run** (findings-only; Rule 9).
- Routed to `1.0.0_SA_CTO~Z` as program owner; the tool-owner remedy is theirs to route.
- **Registered as a PRIOR-UNDER-TEST for the next comp-estate decomposition**, where the entity
  should be scoped to the consumer-topology surface rather than the provenance header.
- Raiser's register needs no correction on its verdict; the control note is theirs to fold.
