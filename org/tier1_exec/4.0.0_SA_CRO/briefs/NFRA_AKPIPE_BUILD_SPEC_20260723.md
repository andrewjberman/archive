# NFRA_AKPIPE — arxiv daily-harvest + contact-ID + ontology-relevance ranking: teardown + build spec

**Author:** 4.0.0_SA_CRO (Chief Research Officer)
**Home:** org/tier1_exec/4.0.0_SA_CRO/
**Recon ID:** RCN-0003 — registered in RECON_REGISTER.md
**Date:** 2026-07-23
**Status:** BUILD SPEC — proposal. Build/deploy is CTO-gated; staffing is CTO+COO. Research proposes owners, does not dispatch.

---

## 0. Origin + authorization (verbatim)

Andrew-direct to CRO, 2026-07-23 ~19:16Z, five decisions establishing the project:

> "1.) You have daily programmatic rights, however this should be run on a lambda in our cloud and stored in an AWS bucket. 2.) Your rec is accepable. 3.) Full text rescore. 4.) Should be columnar store maybe a DDB with an attached s3 bucket for full papers, linked with a stable taxonomy that is aligned with columnar form. 5.) Fast potion is fine."

**STANDING EGRESS GRANT — arxiv-scoped, cloud-only.** A daily programmatic arxiv pull is authorized, but ONLY as a Lambda in Opal's cloud writing to S3 — never from an agent session or a distributed CLI. This is a scoped standing grant for arxiv; it is NOT a blanket vendor lift. Every other vendor still needs Andrew's explicit per-use word.

Prior discussion decisions folded: (2) category set accepted — `cs.AI, cs.LG, cs.SE, cs.IR, cs.DC, cs.DB, cs.MA` + a keyword overlay; (3) full-text rescore for all harvested papers; (4) DDB (columnar metadata+scores) + attached S3 (full papers), stable taxonomy aligned to columnar form; (5) `potion-base-8M`.

---

## 1. Evidence basis + denominators (what grounds this spec, and one marked gap)

**Inputs (operator-supplied by Andrew, NOT egress):** 3 HAR captures + 1 sample paper.
- **HARs: 3 files → 2 unique.** `arxiv.org.har` == `arxiv.org2.har` (md5-identical, `663682cc51f0b016c6bb34ea7a7ba7be`, 223 entries, nav path home→archive/cs→list/cs/new→abs→pdf). `arxiv.org3.har` distinct (md5 `8ed54cf8…`, 165 entries) — captured `/html/`, `/src/`, `/search`.
- **Sample paper:** `2606.07297v1` — *"SWE-Explore: Benchmarking How Coding Agents Explore Repositories"* (`cs.SE`, 20 pp). The stated high-relevance exemplar; used as the **positive control** for scoring acceptance (§7). Carries the corresponding-author email inline — proves contact-ID from body is feasible.

**MARKED CAPTURE GAP (doctrine rule 2 — an unmarked gap reads as coverage).** The HARs retained **ZERO HTML response bodies** — only the PDF bytes were stored (verified: `bodies_present=1` per HAR, sole mime `application/pdf`; all 12/9 HTML documents empty). Therefore the HARs ground the **surface topology** (endpoints, params, nav path, content-types, response sizes) but **NOT** the DOM field-schema of `/abs`, `/list`, `/html`, `/search`. No HTML parse is specified off an endpoint name. The schema grounding comes instead from the **official arxiv metadata API/OAI-PMH** (structured, documented, stable) — which is the correct harvest backbone regardless (§3).

**Denominator of the endpoint scan:** 388 total HAR entries across the 2 unique files; arxiv.org non-static document/data endpoints enumerated below (§2). Static assets (css/js/fonts/images) excluded by filter, not by omission.

---

## 2. arxiv surface teardown (topology — grounded from HAR)

| Endpoint (path-normalized) | Role | Content-type | Grounding |
|---|---|---|---|
| `GET /list/{archive}/new` | daily new-papers listing for an archive (`/list/cs/new` = whole cs feed, one 2.7 MB page) | text/html | ✓ topology; body NOT captured |
| `GET /list/{cat}/{YYYY-MM}` | month/category listing (pagination via `?skip=&show=`) | text/html | inferred from arxiv listing convention — **NOT in HAR, flagged** |
| `GET /abs/{id}` | abstract page: title, authors, subjects, submission history | text/html | ✓ endpoint; fields [BODY-NOT-CAPTURED] |
| `GET /html/{id}[vN]` | full LaTeX→HTML render (~320 KB) + `/figures/*.png` | text/html | ✓ topology |
| `GET /pdf/{id}[vN]` | PDF | application/pdf | ✓ **body captured + parsed** |
| `GET /src/{id}` | source tarball | application/gzip | ✓ topology |
| `GET /search/?query=&searchtype=all` | keyword search, HTML results (308/307 → `/search/`) | text/html | ✓ endpoint + params |

**The harvest backbone is NOT any of these HTML pages.** It is the official API surface (not exercised in the browser HAR, documented externally):
- **OAI-PMH** — `http://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=arXiv&from=YYYY-MM-DD&until=YYYY-MM-DD&set=cs`. Purpose-built for **incremental, exhaustive daily-delta harvest**. `resumptionToken` paginates; `from`/`until` windows guarantee completeness (the lossless backbone). Metadata format `arXiv` carries: `id`, `created` (submission date = "timestamp of release"), `updated`, per-author `keyname`/`forenames`, `title`, `abstract`, `categories`, `doi`, `journal-ref`. **Rate: polite ~1 req/3s; honor `503 Retry-After` backoff.**
- **Atom API** — `http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+…&sortBy=submittedDate&sortOrder=descending&start=&max_results=`. Used as the **keyword-overlay** supplement (the "harness / learning loop / agentic engineering" cross-category sweep), not the exhaustive backbone.

---

## 3. Architecture (Andrew-fixed: Lambda → DDB + S3)

```
EventBridge (daily, ~06:00Z)
      |
      v
Lambda  akpipe-daily-harvest  (Opal cloud; the ONLY place arxiv egress happens)
  1. HARVEST   OAI-PMH ListRecords from=watermark until=today, set=cs
               + Atom API keyword-overlay sweep across target cats
               -> filter to {cs.AI,cs.LG,cs.SE,cs.IR,cs.DC,cs.DB,cs.MA} + keyword tags
  2. DEDUP     key = (arxiv_id, version); skip already-present (id,version) rows
  3. FULLTEXT  for each NEW (id,version): fetch /html/{id} (LaTeX render) else /pdf/{id};
               extract text; write raw + text.txt to S3
  4. SCORE     bm25_score + potion_cosine over FULL TEXT vs the versioned ontology PROFILE
               nlp_score = RRF-fuse(bm25_rank, potion_rank)   [components stored, not just fusion]
  5. WRITE     append row to DDB akpipe_papers  (lossless: never overwrite a version row)
  6. RE-DERIVE recency_component + derived_state_rank for the WHOLE corpus (age moved for all)
               -> bounded scan + batch update; stamp rank_asof_date
  7. WATERMARK advance oai_watermark only on a fully-successful window; FAIL-LOUD run identities
      |
      +--> DDB  akpipe_papers   (columnar metadata + scores; the query surface)
      +--> S3   opal-<akpipe>    (full papers: pdf/html/tarball/text; append-only, versioned)
```

**Determinism / no-runtime-egress-for-models:** `potion-base-8M` (static embeddings, ~30 MB) is baked into a **Lambda layer** (or read from S3 at cold start) — never downloaded from HF at runtime. BM25 params (`k1`, `b`) pinned. Deterministic given the pinned model + pinned profile (CVO honesty framing: Potion IS a model → the guarantee is *deterministic-given-pinned + reproducible*, and the model+profile versions are stamped into every row — §6).

---

## 4. Harvest + lossless mechanics

- **Watermark** = last successful OAI `until` date, stored at `s3://opal-<akpipe>/_control/oai_watermark.json`. Advances ONLY when the full window (including all `resumptionToken` pages) landed. A partial run does not advance it → the next run re-covers the window (idempotent by dedup key). This is the lossless guarantee against dropped days.
- **Dedup key = (arxiv_id, version).** A new version of a paper (`v2`) is a NEW row + NEW S3 prefix — never an overwrite of `v1`. Re-seeing an existing (id,version) is a no-op (conditional put).
- **Never delete.** DDB rows and S3 objects are append-only; the S3 bucket is versioned. "We only want to add more" (Andrew) is enforced structurally, not by policy.
- **FAIL-LOUD run identities** (my 3F-G8b pattern): `rows_harvested == rows_written + rows_skipped_existing`; `fulltext_fetched == fulltext_attempted - fulltext_failed`; each run emits a manifest `s3://…/_control/runs/{run_id}.json` with these identities. A mismatch fails the run loud (no silent partial).

---

## 5. Data model — DDB `akpipe_papers` + S3 + the stable taxonomy

### 5.1 The stable taxonomy (the single source both the columns and the S3 grammar derive from)
A versioned `taxonomy.yaml` in-repo is the ONE definition that maps: `arxiv_category ↔ interest_domain ↔ column/partition token`. Both the DDB attributes and the S3 key grammar are generated from it, so "columnar form" and "S3 taxonomy" cannot drift (Andrew: "stable taxonomy aligned with columnar form"). Example rows:

| arxiv_category | interest_domain | partition_token |
|---|---|---|
| cs.IR | retrieval | retrieval |
| cs.AI, cs.MA | agentic_engineering | agentic |
| cs.SE | harness_engineering | harness |
| cs.DC | infrastructure | infra |
| cs.DB | data_engineering | dataeng |
| cs.LG | learning_loops | learning |

Keyword overlay tags (`retrieval`, `agentic`, `graph`, `harness`, `learning-loop`, `infra`) are ALSO taxonomy-defined and stored as a DDB string-set `interest_tags` — so a paper is reachable by both its arxiv category and its detected interest theme.

### 5.2 DDB schema
- **PK** `arxiv_id` (e.g. `2606.07297`) · **SK** `version` (e.g. `v1`) — one row per version (lossless).
- **Attributes:** `title`, `authors` (list of {name, keyname, forenames, arxiv_author_id?}), `author_emails` (list), `affiliations` (list), `primary_category`, `categories` (SS), `interest_tags` (SS), `timestamp_released` (ISO8601 Z, from OAI `created`), `timestamp_updated`, `first_seen_ts`, `abstract`, `doi`, `fulltext_s3_key`, `extracted_text_sha256`, `bm25_score`, `potion_cosine`, `nlp_score`, `recency_component`, `derived_state_rank`, `rank_asof_date`, `profile_version`, `potion_model_version`, `bm25_params_version`, `fulltext_fetched` (bool), `source_channel` (oai|api), `harvest_run_id`.
- **GSI `rank-by-day`:** PK = `rank_asof_date`, SK = `derived_state_rank` (Number) → a consumer reads today's ranked list, descending, in one query. (Optional second GSI PK = `primary_category` for per-domain ranking.)

### 5.3 S3 grammar (aligned to the taxonomy + the DDB keys)
`s3://opal-<akpipe>/{partition_token}/{YYYY}/{arxiv_id}/{version}/{pdf|html|source.tar.gz|text.txt|meta.json}`
- `partition_token`, `arxiv_id`, `version` are the shared join keys with DDB. `_control/` holds the watermark + run manifests. Bucket versioned; lifecycle = retain (append-only). Bucket-name + region are CTO's to finalize under the estate grammar.

---

## 6. Scoring model (the "derived state rank score", recalculable daily)

### 6.1 The ontology profile (the query papers are scored against) — VERSIONED
Built deterministically, once, from three in-repo sources, and pinned as `profile_version`:
1. **Ontology vocab** — `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` (Roles / Relations / Variance terms).
2. **System vocab** — `infra/system/` graph-infra + learning-loop terms (Nessie, Iceberg, Trino, Kuzu, derive, marker-oracle, FRESHGUARD, COMPLEARN, MOTIF, PROMOTE, RRF, BM25, retrieval-augmented, materialize).
3. **Andrew's interest anchors** — retrieval; agentic engineering; graph engineering; infrastructure; harness engineering; learning-loop design patterns.

The profile is a bag of terms/phrases (BM25 side) + a concatenated profile document embedded once with potion-8M (Potion side). Regenerating the profile bumps `profile_version`; scores are reproducible against a pinned profile.

### 6.2 Per-paper axes (over FULL TEXT), stored separately (CVO: ablate, don't fuse-and-hide)
- `bm25_score` — BM25 relevance of the paper against the profile terms (pinned k1,b).
- `potion_cosine` — cosine(potion-8M(paper full text, mean-pooled), potion-8M(profile)).
- `nlp_rrf_ordering` — **RRF fusion** of the paper's BM25 rank and Potion rank. **ORDERING ONLY** (the parameter-free fuser per CONTENT_MODULE_DESIGN §8; never a gate, and — see the correction below — **never a multiplicative factor**).
- `nlp_score` — the **ABSOLUTE relevance MAGNITUDE** in [0,1), and the only thing the derived rank multiplies: geometric mean of the two saturated axes, `sqrt( bm25/(bm25+C) * max(0, potion_cos) )`. Geometric mean means a paper must score on **BOTH** axes — a lexical-only match with unrelated semantics is penalized, and the inverse too.
- All axis components are persisted so any consumer can ablate (bm25-only / potion-only / fused).

> **CORRECTION v1.1 (2026-07-23, caught in validation before build — the spec as first landed was WRONG).**
> v1 defined `nlp_score` as the RRF fusion and then multiplied it by recency. **Measured on the real
> sample: RRF's dynamic range between a perfect match and pure noise is 1.03x, while recency's range is
> 2x per 45 days and 16x over 180 days — so recency swamped relevance ~100:1.** The falsification test:
> *word salad published today outranked the high-relevance exemplar that was 3 days old.* RRF is a RANK
> fuser and has no magnitude by construction, so it can order but must never be a multiplicand.
> Fix = the absolute magnitude score above. Regression test [7.6] in `scripts/akpipe_scorer.py` pins it.
>
> **Why the normalization is ABSOLUTE and not corpus-relative (min-max / z-score):** a corpus-relative
> score would silently CHANGE a stored paper's value as new papers arrive, which breaks both the lossless
> contract and independent recomputability — a reader could not reproduce a stored row. A saturating
> absolute transform keeps every paper's relevance stable forever. **`C` (BM25 saturation) is PROVISIONAL
> and must be calibrated against the decoy-null distribution on the first real harvest — it is deliberately
> NOT tuned to the 3-document validation sample.**

### 6.3 Recency + the derived state rank (recomputed every run)
- `recency_component = exp(-ln(2) * age_days / HALF_LIFE)`, `age_days = rank_asof_date - timestamp_released`, bounded (0,1]. `HALF_LIFE` default 45 days (a spec knob, set defensibly — NOT tuned to a sample).
- `derived_state_rank = recency_component * nlp_score`.
- **Recalculable-daily is structural:** `derived_state_rank` is a pure function of stored components + today's date. The daily Lambda re-derives it for the whole corpus (recency moved for every paper as time elapsed) and stamps `rank_asof_date`, so a reader sees a self-consistent daily snapshot; the components remain stored so a reader can independently recompute and CHECK the stored rank (an instrument that can fail in both directions). New ingestion + elapsed time both flow in on every run. Nothing is lost; only the ranking is refreshed.

### 6.4 Freshness basis — NOT trading-day T-1
Recency here is **calendar/mtime-based** (a preprint is old-and-correct, not stale). CONTENT_MODULE_DESIGN §9 already carries this caution: importing the data-pipeline T-1 trading-day basis would false-alarm. NFRA_AKPIPE recency is submission-date decay, full stop.

---

### 6.5 Validation status (EXERCISED 2026-07-23, offline, zero egress)

`scripts/akpipe_scorer.py` implements the scoring core and runs the §7 controls. Run with
`HF_HUB_OFFLINE=1` — potion-base-8M loads from local cache, **proving no egress occurs in scoring**.

| Check | Result |
|---|---|
| [7.1] positive control — SWE-Explore top-ranked | **PASS** (nlp 0.690 vs 0.394 ops-prose vs 0.000 noise) |
| [7.2] degeneracy — noise below positive | **PASS** |
| [7.3] ablation — both axes discriminate | **PASS** (BM25 +87.9, Potion +0.330) |
| [7.4] determinism — two runs byte-identical | **PASS** |
| [7.5] recompute monotonicity — rank falls with age | **PASS** |
| [7.6] composition sanity (the v1 defect regression) | **PASS** after the v1.1 fix; **FAILED before it** |

**DECLARED GAP — the negative controls are WEAK, and this is the honest limit of the pass.** The corpus
was N=3: one on-topic paper, one off-topic operational prose blob, one generated word-salad. That proves
the mechanism, determinism, and the composition fix. It does **NOT** prove **topical discrimination
within CS papers** — in production *every* candidate is a CS paper, and the real question is "which CS
papers are relevant to us," not "is this prose or noise." Word salad is not the adversary. Closing this
needs either the first real harvest or a handful of deliberately off-topic AI papers (e.g. a vision or
theory paper) as decoys. **Until then, treat the ranking quality as UNPROVEN and only the machinery as
validated.**

## 7. Acceptance criteria (with the CVO honesty controls that make it hold)

1. **Positive control** — the SWE-Explore sample (`2606.07297`, your stated high-relevance exemplar) ranks in the top tier on `nlp_score`. If it does not, the profile is wrong, not the paper.
2. **Decoy null** — score a structurally-matched set of OFF-TOPIC papers (a cs.CV vision paper, a non-cs paper) → they rank low; the null distribution (99th pct of off-topic `nlp_score`) is the calibration for "signal vs apophenia" (CVO: anchor to the decoy null, not a hand-picked cutoff). Lossless means we KEEP everything and rank it; the null calibrates an optional `is_relevant` flag, it does not delete rows.
3. **Ablation** — report bm25-only, potion-only, and fused rankings on a validation slice; Potion must EARN its place by recovering relevant papers BM25 structurally misses (the recovery bar, CONTENT_MODULE_DESIGN §8), else drop it to a component-only column.
4. **Determinism** — same paper + pinned model + pinned profile → byte-identical scores across two runs.
5. **Recompute monotonicity** — holding `nlp_score`, `derived_state_rank` strictly decreases as `age_days` grows.
6. **Lossless invariant** — corpus row count is non-decreasing across runs; every (id,version) once seen is present forever; watermark never advances past an incomplete window.

---

## 8. Contact identification

- **Names + arxiv author-ids** — OAI metadata `<author><keyname>/<forenames>` (structured, every paper).
- **Emails + affiliations** — parsed from full text: cleanest from the `/src` LaTeX source (`\author`, `\affiliation`, `\email`); fallback the PDF first page (email regex near the author block). The sample proves emails are present in-body. `[EMAIL-NOT-FOUND]` marked per-paper where absent — an unmarked absence reads as "no email," which is a claim.
- **PII posture** — paper authors are PUBLIC academic authorship, not client PII; stored in the contact columns. This is categorically distinct from the client-data PII discipline (no scrubbing needed), but the distinction is stated so no reader treats this as a client-data surface. Raw bodies live in the Opal-owned S3 bucket.

---

## 9. Deploy / IAM notes (CTO gate — spec input, not a deploy)

- **Terraform-only** Lambda (CLAUDE.md deployment rules). Layer(s): potion-8M model + `rank-bm25`/`bm25s` + `pymupdf`/parsers + the OAI/Atom client. Size the Lambda deliberately (NOT yang defaults) — full-text NLP over hundreds of papers/day wants memory + a multi-minute timeout, or a fan-out (harvest Lambda enqueues per-paper scoring to SQS→worker Lambda).
- **IAM is a NEW-RESOURCE case (CLAUDE.md Rule 22a):** the role's access to the new bucket + new table must be verified on the live primitive — `aws iam simulate-principal-policy --resource-arns <exact ARN>`, ONE resource per call, positive control run separately. `comp-iam` alone FAILS GREEN here.
- **Egress egress-scope:** the Lambda's only external destination is `export.arxiv.org` + `arxiv.org` (+ their CDN). No other egress. This is the concrete boundary of the standing grant.

---

## 10. Suggested owners (research PROPOSES; CTO+COO staff)

- **Cloud lane** (Lambda + DDB + S3 + EventBridge + IAM, Terraform): the `0.7.0_AE_CloudOps` pattern.
- **Content/NLP lane** (the profile builder + RRF scorer + parsers): a content-class build in the `.tools/content/` partition, converged with CONTENT_MODULE_DESIGN (same RRF/BM25/Potion contract).
- **Ratification** — CTO at program registration ("four names, one fact"): NFRA_AKPIPE's scorer IS the arxiv/external instance of the content module, not a fork. CVO for the scoring honesty controls (§7).

---

## 11. Open knobs (spec-internal; do not block registration)

1. `HALF_LIFE` for recency decay (default 45d) — set defensibly, not tuned to the sample.
2. Whether Potion survives the §7.3 recovery bar for this prose domain (measured, not assumed) — if not, it becomes a stored component, and `nlp_score` is BM25-led.
3. Full-text fetch preference order `/html` vs `/src` vs `/pdf` (recommend `/html` when the LaTeX render exists — cheapest clean text; `/src` for the richest author/affiliation parse; `/pdf` fallback).
4. Fan-out vs single-Lambda for the full-text scoring pass (volume-dependent; CTO sizing call).
5. Bucket name + region + DDB capacity mode (on-demand vs provisioned) — CTO under the estate grammar.

---

## 12. Convergence + boundary

- **Convergence:** reuse `infra/system/ontology/CONTENT_MODULE_DESIGN.md`'s method (RRF over BM25/Potion, materialized substrate, deterministic-pinned, ablate-don't-fuse, decoy-null threshold). NFRA_AKPIPE = that module's external/arxiv instance. Not a parallel NLP stack.
- **Boundary:** CRO owns this spec + the register entry. Build/deploy = CTO gate; staffing = CTO+COO; moving any served surface = never-widen co-sign. Vendor egress beyond arxiv-via-Lambda = Andrew per-use word.
```
