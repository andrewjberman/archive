# Pillar-text editability — SCOPE (pre-build), OPAL_INVPHL follow-on

**Author:** 0.4.0_DT_ClientPlatform · **To:** 2.0.0_SA_COO · **2026-08-12** · **Status:** SCOPE ONLY, no code written

**Authority:** Andrew-direct 2026-08-12, VERBATIM: *"for edit rights yes i would like to make that
text editable just want it to be extremely light and client-facing do not want overwrought process
architecture around this should be extremely simple setup"*

## The answer in one line

**The chain already exists end to end.** Move the pillar copy into the CMA Excel workbook Yang
already maintains; the **existing** `yang-generate-cma` Lambda already emits that workbook into the
**existing** JSON the Philosophy page already fetches; Yang/Manav already have a **client-facing
upload page in the portal** that already runs that generator. Nothing new is created at any layer.

## Grounded, not assumed

| Fact | Evidence |
|---|---|
| The page fetches a served JSON today | `portal-proxy.ts:1377` -> `/api/general/capital-markets/assumptions.json` (+ `:1414` views) |
| A live Lambda generates it **from Excel** | `yang-generate-cma`, `python3.11`, *"Generate Capital Market Assumptions and SAA Views from Excel files"*, State Active, `infra/aws/lambda/v2_portal/08_capital_market_assumptions/configs/yang-generate-cma.json` |
| Publishers already have a **client-facing** upload surface | `portal/src/pages/DataRefresh/` — tabs Upload / Emergency Rollback / History; `FileDropZone.tsx:78` accepts `.pkl,.json,.xlsx,.csv`; API `/api/scoped/data-refresh/upload-urls` + `/trigger` |
| That pipeline **already runs the CMA generator** | `PipelineProgress.tsx` STEP_GROUPS `generators.steps` contains **`GenerateCMA`** |

⚡ **The decisive one is the last row.** `GenerateCMA` is already a step in the upload pipeline, so
"Yang changes a word" already has a path to production that does not touch code.

## The shape

**Where the content lives:** a sheet in the CMA workbook (the artifact Yang already edits).
**Who writes it:** Yang / Manav, directly, no intermediary.
**Their literal steps:** edit the sheet -> open Data Refresh in the portal -> drop the workbook ->
the pipeline runs `GenerateCMA` -> the page serves the new wording. **No code edit, no PR, no
deploy, no PROD promote.**

**Net-new code — three small edits, no new anything:**
1. `yang-generate-cma`: parse one additional sheet, emit a `philosophy_pillars` block into the JSON it already writes.
2. `portal-proxy.ts`: one optional field on `CMAAssumptionsResponse`.
3. `PhilosophyPillars.tsx`: read served copy when present, **fall back to the repo copy already shipped**.

**The fallback is deliberate and load-bearing:** a missing sheet, a failed parse, or a stale artifact
degrades to exactly today's live behaviour. Editability cannot introduce a blank page.

**What does NOT get built (Andrew's ceiling, verbatim from COO's list):** no CMS · no admin console
or edit UI · no auth/permission layer · no approval workflow · no draft/publish or versioning · no
new Lambda · no new bucket · no new DynamoDB table · no new component. **No new artifact of any
kind** — every layer this touches already exists and already runs.

## The ambiguity you flagged — it does not bifurcate the build

You asked whether *"client-facing"* describes the CONTENT or requires a client-facing EDITOR. I read
it your way (the content). **But it does not matter here, and that is worth more than picking a
side:** the editing surface in this design *is* client-facing — the portal's own Data Refresh page,
which Yang/Manav log into. **Both readings land on the same build**, so no question needs to go to
Andrew and no guess is being made. If he meant something a third way, the fallback design absorbs it.

## What I have NOT grounded — the one real unknown

**I have not read `yang-generate-cma`'s source.** Its config shows `CodeSize: 2476` bytes, which is
small enough that it likely fetches the workbook rather than embedding logic, but **I am not going to
infer the insertion point from a byte count.** Confirming the sheet-parse insertion point is the
first act of the build, and if that Lambda turns out not to read a workbook Yang controls, **the
design changes and I come back rather than minting anything.**

## Surprise-channel finding (no action taken)

`data/yang_pkl/scripts/README_CMA_PIPELINE.md` documents a **local-script** architecture —
`generate_cma_assumptions.py` / `generate_opal_views.py`, run by hand with an `--no-upload` flag,
writing `s3://opal-data-portal-s3/cma/assumptions.json`. **Measured: neither script exists anywhere
in the estate** (`comp-find --name "generate_cma*"` = 0 hits over 25,559 files), and the portal
serves `/api/general/capital-markets/…`, not the `/cma/…` path the README names. The live mechanism
is the `yang-generate-cma` Lambda inside the Data Refresh pipeline. **Declarative drift on a doc a
future reader would reasonably follow** — and it would have sent me to build a manual local step
Yang would have had to run himself, which is the opposite of "extremely light".

## Ask

GO / push back on this shape. On GO I confirm the Lambda insertion point first and report before
writing anything beyond that.
