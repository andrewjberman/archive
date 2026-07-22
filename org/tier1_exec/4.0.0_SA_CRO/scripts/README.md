# Research tooling — `4.0.0_SA_CRO`

Preserved from the RCN-0001 (Black Diamond) engagement, 2026-07-21. These ran in a session scratchpad, which
`/kill storage` reaps — they are here so the next engagement does not rebuild them.

**Logic preserved exactly as it ran; formatting normalized to pass `.tools/commit-gate.sh` (ruff py39).**
The style fixes were behavior-neutral (import splits, statement-per-line, `except:` → `except Exception:`)
and were **verified, not asserted**: both scripts were re-run against the original 8-HAR corpus and the output
diffed against the pre-edit run — **229 endpoints / 52 schemas reproduced (the exact published denominators)
and 218 output files byte-identical**. Not refactored, and not re-tested against a second target — treat any
*generalization* to a new target as unproven until exercised.

## `profile_har.py <scratchpad_dir>`

**Generic — no target-specific logic except the host filter.** Expects `<scratchpad_dir>/har/*.har`, writes
`<scratchpad_dir>/analysis/`.

Produces the engagement's denominators and the endpoint catalog: normalizes path variables
(`{guid}`/`{id}`/`{hex}`) so repeated calls collapse to one endpoint, filters third-party noise hosts
(Pendo, HelpScout, SignalR, CDNs, telemetry), and emits `endpoint_catalog.json`, `catalog_by_host.txt`,
`files_summary.json`.

**To retarget:** change `BD_HOST_RE` to the new target's domain. Extend `NOISE_HOSTS` with whatever
third-party embeds the new target carries — an unfiltered embed inflates the request denominator and makes
the catalog noisy.

## `extract_schemas.py <scratchpad_dir>`

Decodes request+response bodies (incl. base64) into schema skeletons for high-value endpoints →
`analysis/schemas.txt`.

**⚠ TARGET-SPECIFIC:** the `HV` regex is a hand-built allowlist of Black Diamond's high-value endpoint paths,
and `SKIP_BIG` skips known-huge low-value ones. **This must be rewritten per target.** The right workflow is
to run `profile_har.py` first, read `catalog_by_host.txt`, and build `HV` from what the catalog actually
shows — not to guess it up front. The host filter (`bdreporting\.com$`) is likewise hardcoded.

## Not preserved (recorded so nobody assumes coverage)

`extract2.py`, `final_extract.py`, `render_catalog.py` — the exploratory passes that produced
`schemas2.txt` / `schemas3.txt` — live only in the RCN-0001 scratchpad and die with it. `schemas.txt`, the
52 core schemas the teardown actually cites, is fully covered by what is here.

## The gap the tooling cannot close

Chrome DevTools does not retain every large cross-origin XHR body. Whatever it dropped is simply absent from
the HAR — the tooling cannot recover it, and **an absent body must be marked `[BODY-NOT-CAPTURED]`, never
inferred from the endpoint name** (charter §2.2). If a specific family matters, the fix is a second capture
with "Preserve log" + a raised body limit on those pages, not a cleverer parser.
