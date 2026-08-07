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

---

## `pyfield_probes/` — RCN-0006, the Python field-grain measurements

**Preserved 2026-08-07 per charter §8** (*"preserve the tooling, not just the findings; scratchpads
are reaped"*). **Every number below reached `docs/architecture/NFRA_PYFIELD_PRD.md`**, so these exist
so `1.0.0_SA_CTO~D` can act on the instruction I gave them twice — **re-derive before the PRD rests
on it.** They could not re-derive what lived only in a reapable scratchpad.

> **PRESERVED AS BEHAVIOURALLY IDENTICAL, NOT BYTE-IDENTICAL — and the distinction was forced.**
> Byte-identical was the intent; the **universal commit-gate (Rule 14) correctly blocked on ruff**
> (`E401` imports-on-one-line, `E701` statement-after-colon — 44 findings, all cosmetic). `ruff format`
> normalised all five; **zero behavioural change**, and that is PROVEN rather than asserted:
> ```
> paramtest  -> 421 / 9.4%          (matches published)
> flowspike  -> 24.3% / 75.7%       (matches published)
> twoaxis    -> 1810 union / 41.1%  (matches published)
> baseprobe  -> 697 / 4897 = 14.2%  (matches published RATIO; see the denominator note)
> ```
> Same resolution as the RCN-0001 tooling: normalise, then re-run and reproduce the published
> denominators. **Pre-format md5s** — colprobe `4e74f4a2…`, baseprobe `2960558c…`, flowspike
> `f39f182e…`, paramtest `ad07c2d7…`, twoaxis `54424a5c…`.
>
> ⚠ **DENOMINATOR PROVENANCE — a 1-count discrepancy, resolved and worth the note.** I published
> "4,896 subscripts" against `baseprobe`; **4896 is `flowspike`'s total** (1190+3216+490) and
> `baseprobe` reports **4897**. The two probes classify non-`Name` bases slightly differently. Not
> corpus drift — file count and tree are unchanged. **I quoted one probe's denominator under another
> probe's name**, which changes no conclusion and is exactly the provenance error these probes exist
> to measure. **Each probe's denominator belongs to that probe.**

| probe | question | published result |
|---|---|---|
| `colprobe.py` | of all column-ish subscripts, what share is statically resolvable? | **77.9%** (83 files, 24,210 lines) — **a SUBSCRIPT figure, NOT a column figure** |
| `baseprobe.py` | can the BASE NAME discriminate DataFrame from dict? | **NO** — 166 distinct bases; **14.2–15.8%** match any df-ish convention, unchanged in a 75%-pandas tree |
| `flowspike.py` | what does flow-local inference (binding-side) reach? | **24.3%** on the gold trees |
| `paramtest.py` | is the unresolved mass FUNCTION PARAMETERS? | **NO — 9.4%.** A hypothesis I formed and **refuted**; the alarming reading was available and wrong |
| `twoaxis.py` | are binding-side and usage-side additive or overlapping? | **largely independent** — union 41.1% vs 27.6% binding-alone; overlap 34.6% |

### ⚠ THE THREE CAVEATS THAT MATTER MORE THAN THE NUMBERS

1. **`twoaxis.py`'s `USAGE_MARKERS` SET IS HAND-CHOSEN AND THE RESULT IS 3× SENSITIVE TO IT.**
   Measured: **12 strict markers → +3.8 pts · 36 (as written) → +13.5 · 48 wide → +14.5.**
   **The published +13.5 is the middle of a range, not a measurement.** Use **+3.8** if a single
   number must carry a decision — it is the one that cannot be accused of being tuned. *(To re-run the
   sensitivity, regex-replace the whole multi-line `USAGE_MARKERS` literal and **compile the variant
   before running it** — a line-oriented `sed` silently breaks it and, piped through `grep`, the
   failure reads as an empty result.)*
2. **SUBSCRIPT ≠ COLUMN.** These count `x["lit"]` subscripts. The corpus is genuinely mixed — dicts,
   JSON records, API responses, loop vars. **No column denominator exists**, so no
   "resolve X% of columns" bar can be set from any of these figures.
3. **TARGET-SPECIFIC:** written for **pandas-idiom Python** in `data/*/scripts/`. Run against
   **non-held-out trees only** (`etfs`, `find`, `inf/gold`, `assets/gold`); **`bd`/`cot`/`mdpf` and the
   assets monolith are UNSWEPT.** The constructor and marker sets are pandas-shaped and would need
   replacing for any other idiom.

### Reproduce

```bash
python colprobe.py  data/etfs/scripts data/find
python baseprobe.py data/inf/scripts/gold data/assets/scripts/gold
python flowspike.py data/inf/scripts/gold data/assets/scripts/gold
python paramtest.py data/inf/scripts/gold data/assets/scripts/gold
python twoaxis.py   data/inf/scripts/gold data/assets/scripts/gold
```

**Each prints its own denominator.** None is a comp-tool, none is registered, none is on the rail —
they are **measurements, not instruments**, and they carry no tests. Treat any figure as
re-derivable-in-principle rather than verified.
