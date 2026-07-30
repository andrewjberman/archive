# `partial` FULL-ESTATE CONSUMER CENSUS — gate on the ETFS_AVGCAP re-key

**archetype:** TRACE
**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-30
**Commissioned:** 2.0.0_SA_COO 20260730T105831Z (+ narrowing 110018Z) · **Verdict for:** 1.0.0_SA_CTO~C
**Emitter vintage:** `data/etfs/scripts/gold/avgcap_monthly_average.py` @ `3380a45f66`
**Authorization:** census only. **I am not authorized to make the change and did not.**

---

## VERDICT (one line)

**The re-key is CODE-SAFE and NOT SEMANTICS-SAFE.** Nothing outside the emitting script reads
`partial` — proven in four scopes with positive controls — and all three branch sites are inside
the emitter, rendering to **stdout only, never into the artifact**. But the field's *meaning*
changes, a published methodology brief quotes a `[PARTIAL]`-tagged dollar figure, and **the
graph half of this census is structurally unavailable for ETFS**, so "no external consumer"
rests on text search alone. Details and bounds below.

---

## 0. FIRST FINDING: ~C's line citations do not resolve at HEAD

~C's excerpt cited `:215 :220 :231 :247 :328`. At `3380a45f66` those lines are **comments and a
blank line**; the real sites are `:205 :235 :240 :271 :287 :368 :380` — the file moved ~40 lines.
Rule 22: *a line citation without a vintage is not a citation.* I re-derived every site rather
than trusting the offsets, **and re-deriving found a site ~C's list does not contain (`:380`, a
second render).**

`:220-223` also already carries a prior reasoning trace, worth quoting because it pre-answers
part of the question:

> `partial` IS DELIBERATELY UNTOUCHED. It is a consumed field whose value propagates to a
> render, and re-keying it is gated on a full-estate consumer census (~C). These counts make its
> real behaviour — **it tracks a LATE START, not coverage** — checkable from the file without
> changing what it reports.

---

## 1. The consumer set, re-derived at HEAD, with BRANCH vs CARRY

| site | code | BRANCH / CARRY |
|---|---|---|
| `:205` | `partial = covered_days < n_window_days` | **COMPUTE** (the definition being re-keyed) |
| `:235` | `"partial": partial,` | CARRY → into the persisted artifact |
| `:240` | `or any(e["partial"] for e in etf_results)` | **BRANCH** — boolean read feeding `window_partial` |
| `:271` | `"partial": window_partial,` | CARRY → into the persisted artifact |
| `:287` | `"partial": pr["window"]["partial"],` | CARRY → into the persisted artifact |
| `:368` | `tag = " [PARTIAL]" if pr["window"]["partial"] else ""` | **BRANCH** — render |
| `:380` | `f"{' [PARTIAL]' if r['partial'] else ''}"` | **BRANCH** — render *(absent from ~C's list)* |

**All 7 sites are in ONE file — the emitter itself.** Three branch; three carry; one computes.

### The two renders are stdout, NOT a partner-facing artifact

`:368` and `:380` sit under a literal `# human summary` comment and feed `print()`. The
persisted artifact is written at `:388` (`json.dump`) and uploaded at `:393`
(`put_object` → `ETFS_BUCKET`), and it carries the **boolean field**, never the `[PARTIAL]`
string. Estate-wide, the literal `[PARTIAL]` appears in **8 matches / 4 files**: these 2 code
sites plus 6 in docs — **it is never written to a file or to S3 by any code.**

**This answers COO's narrowing (110018Z) from source rather than by coordination:** the render is
**INTERNAL / operator-facing as of 2026-07-30**. Corroborating, both proven zeros:
`render_month_end.py` (the renderer ~A md5-verified) contains `partial` **0 times**, and
`infra/aws/lambda/etfs-reports-orchestrator/` (exists, 1 `.py`) contains it **0 times**. So the
flag does not reach the month-end email, its PDF, or its CSVs.

---

## 2. Scopes searched, each with its denominator and its control

**Positive control on every scan: `window_partial`** — a token known to exist at `:239`. Found.
So no zero below is a broken retrieval.

| scope | predicate | result | denominator |
|---|---|---|---|
| workspace repo | field-shaped `"partial"` | 53 matches / 32 files | scanned **24,420 of 26,415** files in scope |
| workspace repo | `['partial']` | 3 / 2 files | same |
| workspace repo | `partial:` | 60 / 45 files | same |
| workspace repo | word-shaped `partial` | **≥200, TRUNCATED** | scanned only **1,438 of 26,415** before the cap |
| **portal** (separate repo) | field-shaped `['"]partial['"]｜.partial` | **0** | **382** `.ts/.tsx/.js` files under `portal/src` |
| `etfs-reports-orchestrator` | `partial` | **0** | dir exists, 1 `.py` |
| `render_month_end.py` | `partial` | **0** | file exists (`data/etfs/scripts/presentation/`) |

**The word-shaped count is not a denominator — it is a capped sample.** Reported only to show
why the field-shaped predicate was necessary.

**PORTAL REACH PROVEN BEFORE THE ZERO WAS ACCEPTED.** A repo-scoped scan can stop at a submodule
boundary. Control: `TicketCenter` — found by direct grep at `portal/src/App.tsx` and
`portal/src/pages/TicketCenter/TicketCenter.tsx`, and by `comp-grep` at `portal/CLAUDE.md` +
`portal/src/App.tsx`. Both tools reach inside `portal/`. **Therefore the portal zero is a
measured zero, not an unreached one.**

### Every non-emitter `"partial"` hit is a DIFFERENT field (enumerated, not waved off)

`.tools/validator.py:584,738` `buckets['partial']` (TO status buckets) · `gold_dispatch.sh` ×3
trees `[ "$TARGET" = "partial" ]` (a **dispatch mode**) · `cottonwood_aua.py:72` `STATE_PARTIAL`
(measurability state) · `seeking_alpha_scraper*` `blocking_severity` · `requests/status_codes.py`
HTTP 206 · and **mdpf `partial: 08242234-only`** — a different flag on ownership rows, which is a
genuine name collision worth knowing about on a payment surface.

`avgcap_bd_rps_recon.py` reads S3 (`DAILY_PREFIX/{partner}/{day}.json` — the **daily** slices,
not the monthly artifact) and contains `partial` **0 times**.

---

## 3. THE GRAPH HALF OF THIS CENSUS IS UNAVAILABLE — and I proved the tools work

Both graph instruments COO named **refused rather than returning a zero**, which is correct
behaviour and also a real coverage gap on the rebate-basis pipeline:

- **`comp-blast avgcap_monthly_average.py` → NOT-FOUND**, stating its own denominator (2,252
  nodes; `.tools/*` and `org/modules/*` structurally excluded) and saying explicitly: *"This is
  a NOT-FOUND, not a 'nothing breaks' clear."* Retried on a function name (`list_partner_dates`)
  → also NOT-FOUND; its near-matches are all `inf`/`bd`/`cot` nodes. **The ETFS gold tree appears
  absent from the dependency graph.**
- **`comp-pipescript io` → REFUSED rc=2** (the 2026-07-30 hardening that killed the silent
  bd-tree default — working exactly as intended). `--pipeline etfs` is an **invalid choice**: the
  accepted set is `{bd-gold, inf-gold, bd-silver, inf-silver, bd-bronze, inf-bronze, cot-bronze,
  inf-manual-api, mdpf, cot-gold, cot-silver, cot, all, bd, inf}`. **`etfs` is not in it.**
- **POSITIVE CONTROL that comp-blast is not simply broken:** `comp-blast
  dim_mdpf_aggregate_aua_timeseries` returns a populated HOLD block with 4 claims. The tool
  works; the ETFS absence is coverage, not failure.

> **So the "no external consumer" finding rests on TEXT SEARCH ALONE.** A dynamic or
> string-constructed read of `partial` would be invisible to it — the same
> dynamic-key blindness `comp-blast`'s own contract declares. I am not able to close that with
> the graph, and I am not going to imply I did.

---

## 4. NAMED BOUNDS — surfaces I could not reach, stated instead of implied as zero

1. **Consumers of the S3 artifact outside this repo.** The artifact is uploaded to `ETFS_BUCKET`
   and carries `partial` as a boolean. A notebook, a dashboard, a partner's own tooling, or a
   human reading the JSON cannot be enumerated from here. **UNSEARCHABLE from this vantage.**
2. **A published doc quotes a tagged value — and it goes stale on a re-key.**
   `docs/briefs/ETFS_AVGCAP_W1_methodology_v1.md:40` documents the flag's semantics, and `:77`
   quotes **`$82,220,800.00 [PARTIAL]`**. This is a *found*, searchable consumer, and it is
   documentation rather than code, so no gate protects it.
3. **An operator reading the stdout tag** during a gold run. Internal, unenumerable, low stakes.
4. **The graph census (§3).** Structurally unavailable for ETFS.

---

## 5. WHY "CODE-SAFE" DOES NOT MEAN "SAFE"

`:205` defines `partial = covered_days < n_window_days`, and `covered_days` counts from
`first_written` onward. The file's own comment states the consequence: **it tracks a LATE START,
not coverage.** Carry-forward fills days *after* `first_written`, so a month with few written
days but an early first observation yields `covered_days == n_window_days` → **`partial = False`**.
That is the recorded June behaviour (49financial, 17 written days in a 30-day window, shipped
`partial=False`).

So re-keying to WRITTEN coverage is **not a refinement of the same concept — it changes what the
field means**, and it will flip rows `false → true` on exactly the carry-heavy months that
matter to a rebate basis.

**On the two-wave question:** COO's law is *render learns the value before the producer emits it,
never the same wave.* Here all three branch sites are **in the same file as the producer**, so
they change atomically and the code does not require two waves. **The two-wave requirement
instead falls on the non-code consumers** — the methodology brief (§4.2) and any artifact reader
outside the repo (§4.1) — which learn nothing automatically and must be updated *before* the
semantics flip.

---

## 6. RECOMMENDATION to ~C (a census verdict, not a decision)

1. **No code blocker.** Zero external branch sites, proven in four scopes with controls.
2. **Do not treat that as clearance.** Update `ETFS_AVGCAP_W1_methodology_v1.md` (both `:40`
   semantics and the `:77` quoted figure) **before** the flip, or the published record silently
   contradicts the artifact.
3. **Decide the artifact-reader question explicitly** (§4.1) rather than by assumption. It is
   the only genuinely unsearchable surface with payment relevance.
4. **Consider renaming rather than re-keying.** A new field (`partial_written`) alongside the
   existing one preserves every current reading and makes the discriminator explicit — the same
   preserve-the-residue pattern WS-E4's `verdict_basis` used. A silent flip of an existing
   boolean is the one shape that cannot be told from an estate change after the fact.
5. **Own the ETFS graph gap** (§3) as its own item: the pipeline that computes what a partner is
   paid is invisible to both `comp-blast` and `comp-pipescript`.

---

## 7. Compiler Tools

| Tool | Command | Result | Note |
|---|---|---|---|
| comp-grep | `window_partial`, `"partial"`, `['partial']`, `partial:`, `partial`, `[PARTIAL]`, `avgcap*`, `TicketCenter` | PASS | Printed its scanned/total denominator on every run; flagged its own truncation on the word-shaped scan. |
| comp-blast | emitter script, then a function name, then an mdpf positive control | **REFUSED (NOT-FOUND) ×2, PASS on control** | Said "NOT-FOUND, not a 'nothing breaks' clear" and printed its 2,252-node denominator. Exemplary. |
| comp-pipescript | `io ... --pipeline etfs` | **REFUSED rc=2** | The 07-30 hardening working: refused rather than defaulting to bd-gold and returning a clean zero. Revealed `etfs` is not a known pipeline. |
| direct grep | `portal/src` field shapes + reach control | PASS | Used because portal is a separate repo; reach proven before the zero was accepted. |

**What worked:** every instrument that could not answer **said so with its denominator**, which is
the only reason this census has a defensible bound rather than a false zero.
**What failed:** nothing. Two tools refused correctly; that is not failure.
**Gap found:** ETFS is absent from the dependency graph AND from `comp-pipescript`'s pipeline set
— on the pipeline that produces the partner-rebate basis. Recorded as §6.5.
