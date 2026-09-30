# MX-r-5 close run -- run by the issuer through a principal session (2.0.0_SA_COO~MI, 2026-09-29 ~10:4xZ)

This is material for `3.0.0_SA_CVO~O`'s r5.J1. It carries no verdict; the CVO grades.

- **Host:** the host serves deploy-only `093fc247c6` (gateway tree `2e839aeec9`, previous `63264dfb22`). Drained
  49c02a6eff.
- **Session:** this seat's own MCP connection to the Opal gateway now lists `mdpf_get_model_benchmarks`. Every call was
  read-only.
- **Served objects:** read directly from `opal-data-portal-v2` in the same minute, to compare against.
- **Questions:** the same 4 as the round-3 close run
  (`deliverables/2.0.0_SA_COO~MI/round3/CLOSE_RUN_MX-r-4_ISSUER.md`), plus the json/* question from the worker's on-host
  probe (`deliverables/0.9.0_WK_NFRA_MCPINDEX~14/probes/discover_on_host_MX-r-5.txt`) and one more phrasing.

## Per A2 surface

### 1. `platinum/mdpf` -- "total model portfolio AUM for the firm"

- **Route:** `opal_discover` reports catalogued, 8 rows, 3 servable. The first match is `mp.01.aum-metrics`, with
  **`next_tool` = `mdpf_get_aum_metrics {scope: global}`**. In round 3 it was `query_v0`.
- **The named tool** (`mdpf_get_aum_metrics(scope=global)`):
  - status ok, key `platinum/mdpf/global/aum-metrics.json`;
  - `as_of` 2026-09-25 (field `period`);
  - total.aum 2,083,228,453.05, account_count 8,242, model_aum 1,788,338,510.93;
  - `_provenance.written_at` 2026-09-28T13:50:50Z.
- **The served object, read directly:** VersionId `N_KOsRfVbwJr7danRAxFjAmYOfhCViGu`, LastModified 13:50:51Z,
  6,781 bytes. It holds period 2026-09-25, total.aum 2,083,228,453.05, account_count 8,242, model_aum 1,788,338,510.93
  and written_at 13:50:50Z.
- **Figure and as-of: EQUAL on all five fields. The route names the tool that answered.**

### 2. `platinum/etfs` -- "ETF holdings and fund flows"

- **Route:** `opal_discover` reports **NOT catalogued**, with no dataset and no tool.
- **Change since round 3:** the round-3 mis-route to 4 positioning and portfolio rows is gone (MX-d-5's routing
  precision). This is now an honest absence.
- **No purpose-built ETF tool is served.** MX-t-10 is byte-frozen and uncommitted, waiting on the laptop
  remediations.json row for platinum/etfs (Z-W15-S5).
- **Not answered.**

### 3. `platinum/advi` -- "advisor intelligence rep production ranking"

- **Route:** `opal_discover` reports **NOT catalogued**, with no dataset and no tool.
- **Unchanged since round 3.** The surface is not widened (Andrew: "platinum/advi NOT YET"), and MX-t-11 is HELD on
  G-W.
- **An honest absence, not an answer.**

### 4. `json/*` -- three phrasings of one benchmark question

| ask | discover | first match / next_tool |
| --- | --- | --- |
| "What is year to date performance on the ST model" (the worker's probe ask) | catalogued, 6 rows, 3 servable | **`mp.05.model-portfolio-benchmarks` -> `mdpf_get_model_benchmarks`** |
| "model portfolio benchmark returns" (the round-3 ask) | catalogued, 9 rows, 3 servable | `mp.01.aum-metrics` -> `mdpf_get_aum_metrics`. **mp.05 is ABSENT from the matches.** mp.08 is listed but not servable. |
| "did the model beat its benchmark" (words from mp.05's own `meaning`) | **NOT catalogued** | none |

- **The named tool** (`mdpf_get_model_benchmarks()`):
  - status ok, key `json/benchmarks/model_portfolio_benchmarks.json`;
  - `as_of` 2026-09-25 (field `data_as_of`), generated_at 2026-09-26T11:06:29Z;
  - it carries the MODEL-DESIGN caveat and names both benchmark bases.
  - Sampled figures: ST YTD model 0.78; UST 1Y model 2.69 against index 1.9; LT YTD model 8.39 against ETF 11.96;
    INT since inception 10.94.
- **The served object, read directly:** VersionId `Pxy6ATX1Eah8up3d9.iauhexhaxPMkxX`, LastModified
  2026-09-26T11:06:31Z, 19,225 bytes. It reads data_as_of 2026-09-25, generated_at 11:06:29Z, and the same sampled
  figures: 0.78; 2.69 / 1.9; 8.39 / 11.96; 10.94.
- **Figure and as-of: EQUAL on every sampled field.**
- **The route depends on the phrasing.** It names the tool for 1 of the 3 phrasings. For the round-3 phrasing it names
  another tool, and for the phrasing taken from the row's own text it names nothing. This is row Z-W14-S3 (the
  weak-match rule's recall on asks the harness does not hold), carried to L8, now reproduced on the live host.

## Across surfaces (candidate items for the analysis; not filed as defects here)

- **A. Round 3's finding A is closed where a purpose-built tool exists.** discover now names `mdpf_get_aum_metrics`
  and `mdpf_get_model_benchmarks` as `next_tool` (MX-d-4). `query_v0` rows now carry a note that it is an HTTP route,
  not an MCP tool.
- **B. Round 3's finding B is half-addressed.**
  - `latest_value` still reports the certification vintage (2026-08-10, claim `held`).
  - A new `served_written_at` (claim `measured`, one S3 HEAD) now sits beside it: 2026-09-28T13:50:51Z for mp.01 and
    2026-09-26T11:06:31Z for mp.05.
  - The object's own as-of (2026-09-25) is still not surfaced by discover. Only the tool returns it.
- **C. Router recall on json/*.** See surface 4: 1 of 3 phrasings of the benchmark question reaches the tool.

## Scope of this run

- 4 of 4 A2 surfaces asked, with 6 discover calls, 2 tool calls and 2 direct served-object reads.
- 2 surfaces answered by a purpose-built tool whose figure and as-of equal the served object (`platinum/mdpf`, and
  `json/*` for 1 of 3 phrasings).
- 2 honest absences (`etfs`, `advi`).
- The asker is this seat's principal session, not a non-author asker. The FWD-1 cold run is G-B / G-ASKER, with
  Andrew's speed test first.
