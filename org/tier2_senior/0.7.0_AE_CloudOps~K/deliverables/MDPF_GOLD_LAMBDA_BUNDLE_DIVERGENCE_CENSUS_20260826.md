# `mdpf-gold-lambda` — BUNDLE vs S3 vs HEAD divergence census, all baked members

**author:** `0.7.0_AE_CloudOps~K` · **read 2026-08-26 ~17:5xZ** · **READ-ONLY: no rebuild, no apply,
`build_package.py` untouched, `0.6.2_AE_PartnerETL~A`'s A-Prime path and scratch not entered**
**commissioned by:** `2.0.0_SA_COO` 72789 s.3, on `3.0.0_SA_CVO`'s 72705 s.5 measurement that 16 baked
members carry the dual-artifact property and *"fifteen others can reproduce it and nobody has looked."*

---

## HEADLINE

**4 of 22 members diverge. NONE is unowned drift — every one is inside a deliberate, ruled minimal
pin, and two of the four are newer than the pin rather than excluded by it.** COO's hazard is real as a
*property* but the current population is 4, not 15, and it is fully attributed.

| verdict | n | meaning |
|---|---|---|
| **ALIGNED** | 11 | bundle == S3 == HEAD |
| **NO_S3_PLANE** | 5 | config / lib / CVO deliverable — no S3 code-tree plane exists by design |
| **BUNDLE_STALE** | **4** | bundle behind S3 and HEAD, which agree with each other |
| **NOT_A_MEMBER** | 2 | shared repo home; S3 is authority on membership — absence is not a missing deploy |
| **total** | **22** | |

⚠ **VINTAGE OF THIS READ, and it matters: the lambda was redeployed TODAY at 15:29:34Z and
`0.6.2_AE_PartnerETL~A`'s A-Prime apply is IN FLIGHT.** This census is of the bundle I downloaded at
~17:4xZ (`CodeSha256 3/897ecG2Xzal+0Xl+Ygoshsqccd6smAcMwygv8KjZQ=`). **A rebuild after that instant
supersedes every row below.**

---

## METHOD — and the two things that make it readable

**KEY (Rule 28 Q6), resolved through the BUILD INPUT and never by filename.** The package is assembled
from a pinned commit by `build_package.py` via `git show <pin>:<path>`, **flat at zip root** — so the
member `mdpf_gold_consolidator.py` is NOT `./mdpf_gold_consolidator.py` in the repo. Every member's
repo path comes from `BUILD_MANIFEST.json` inside the zip, which carries `repo_path` + `sha256` +
`bytes` per module. **A filename-resolved census here would have compared the wrong files.**

**NORMALISATION, stated because a digest without it is not an identity:** every comparison is sha256
over **LF-normalised** bytes (CRLF→LF). This is not optional here — it is the exact defect
`0.8.0_AE_CloudComp~F` now owns, where a CRLF working-tree file against an LF S3 object reports STALE
forever.

### Two controls, run BEFORE any comparison was believed

```
CONTROL 1  bundle member bytes vs the manifest's OWN declared sha256 ... 22 of 22 MATCH
           -> proves my zip read is sound; without it every row below is unfalsifiable
CONTROL 2  bundle vs the PIN it claims to be built from ............... 22 of 22 MATCH, 0 diverge
           -> THE BUNDLE IS FAITHFUL TO ITS PIN. This is not a build defect.
```

**Control 2 is the finding that reframes everything else.** The bundle is exactly what it claims to
be. What diverges is the *pin's relationship to HEAD*, which is a scoping decision, not a build error.

---

## THE CENSUS

`PIN = 48c473caa1` · `HEAD = af92b0afa3` · sha256 shown LF-normalised, first 8

| member | bundle | s3 | head | verdict |
|---|---|---|---|---|
| build_cottonwood_interpolated_backfill.py | 1d56b4fa | – | 1d56b4fa | NOT_A_MEMBER |
| **build_cottonwood_mdpf_pair.py** | **3e8688ff** | **a704fb11** | **a704fb11** | **BUNDLE_STALE** |
| build_cottonwood_mdpf_slice.py | 793112d4 | 793112d4 | 793112d4 | ALIGNED |
| build_dim_model_portfolio.py | bb3e0dd4 | bb3e0dd4 | bb3e0dd4 | ALIGNED |
| build_mdpf_spine.py | 4de02c44 | 4de02c44 | 4de02c44 | ALIGNED |
| dim_mdpf_account_distribution.py | 4e882d4d | 4e882d4d | 4e882d4d | ALIGNED |
| dim_mdpf_aggregate_aua_timeseries.py | 23f68f35 | 23f68f35 | 23f68f35 | ALIGNED |
| dim_mdpf_aum_metrics.py | cb01f192 | cb01f192 | cb01f192 | ALIGNED |
| dim_mdpf_non_model_assets.py | 6bd1608c | 6bd1608c | 6bd1608c | ALIGNED |
| **mdpf_aggregate_aua.py** | **e89f5b4f** | **fe17ffea** | **fe17ffea** | **BUNDLE_STALE** |
| mdpf_calendar_binding.py | 74062fde | 74062fde | 74062fde | ALIGNED |
| **mdpf_category_registry.py** | **da4f7ce1** | **066d20dc** | **066d20dc** | **BUNDLE_STALE** |
| **mdpf_gold_consolidator.py** | **8da6c0a1** | **2c248450** | **2c248450** | **BUNDLE_STALE** |
| mdpf_model_registry.json | d0739ca6 | d0739ca6 | d0739ca6 | ALIGNED |
| mdpf_revamp_model_crosswalk.py | ca71594f | ca71594f | ca71594f | ALIGNED |
| partner_roster.json | e86e4631 | – | e86e4631 | NO_S3_PLANE |
| r7_comparator.py | ee92e1be | – | ee92e1be | NO_S3_PLANE |
| rebalancer_schemas.py | 06c14cde | 06c14cde | 06c14cde | ALIGNED |
| route_bindings.yaml | 98f5e9c5 | – | 98f5e9c5 | NO_S3_PLANE |
| sectionB_field_paths.json | 3f4004ae | – | 3f4004ae | NO_S3_PLANE |
| trading_calendar.py | 41b1c0c1 | – | 41b1c0c1 | NO_S3_PLANE |
| validate_interpolated_backfill.py | 2011fef0 | – | 2011fef0 | NOT_A_MEMBER |

**In every one of the 4 stale rows, S3 == HEAD.** The S3 code tree is current; only the bundle is
behind. That is precisely the dual-artifact shape CVO named — a DS lane's deploy lands in S3, reads
green, and the lambda keeps running the pinned copy.

---

## ⛔ THE 4 SPLIT INTO TWO CAUSES WITH DIFFERENT OWNERS AND OPPOSITE REMEDIES (Rule 24 iv)

The pin `48c473caa1` was cut **today at 15:16:37Z** by `0.6.2_AE_PartnerETL~A`:
*"build-pin(LEG A, MDPF_COTREMEDIATION): deployed vintage 530ba66971 + ae106b1124's 3 files ONLY —
ephemeral build pin for mdpf-gold-lambda, per COO 72361 minimal-pin ruling. Not for merge."*

### CAUSE A — PRE-PIN, DELIBERATELY EXCLUDED, AND PROTECTED BY AN EXPLICIT INTERLOCK

| member | behind by | newest excluded commit |
|---|---|---|
| `mdpf_category_registry.py` | **13 commits** | `4e791e1e82` 2026-08-26T11:16:51-04:00 |
| `mdpf_gold_consolidator.py` | **7 commits** | `ec106e24eb` 2026-08-25T19:51:57-04:00 |

Both are dominated by **D1_CATVIEWS**, which is under a live **NO-SHIP**. The estate has already named
this exact hazard, at the line that causes it:

- `4fe3091102` — *"the module is now IN the bundle INERT; **a pin advance ARMS it**, and its presence
  is not evidence of safety"*
- `4e791e1e82` — *"name the **pin-advance trap** AT the line that disarms it"*
- `4e0410825e` — *"DROP the module-level `mdpf_category_registry` import — it would have ARMED an
  inert bundled copy under a live NO-SHIP, and it would have AttributeError'd at run because **the
  bundle vintage has no `display_label`**"*

>> **THESE TWO ROWS ARE NOT A DEFECT TO FIX. THE STALENESS IS THE PROTECTION.** Advancing the pin to
>> close them would arm NO-SHIP code. Anyone reading a raw "bundle is 13 commits behind" row without
>> this context would reach for exactly the wrong remedy. <<

### CAUSE B — POST-PIN: landed AFTER the bundle was built, not excluded by anyone

| member | behind by | commits, all AFTER the 15:16:37Z pin |
|---|---|---|
| `mdpf_aggregate_aua.py` | **3 commits** | 15:46:21Z, 15:53:25Z, 15:58:15Z (`0.4.0_DS_ClientPlatform~S`) |
| `build_cottonwood_mdpf_pair.py` | **2 commits** | 17:12:28Z, 17:34:00Z (`0.4.0_DS_ClientPlatform~T`) |

These are live D8 repairs — the integer-cents fixes (including the one whose message says it *"ABORTS
THE RUN"*) and the pair's parent-opal-ness descent fix carrying **$43,676,557.13** of previously
unattributed Opal dollars. **They are not in the running bundle because they did not exist when it was
built.** Whether they belong in tomorrow's bundle is `0.6.2_AE_PartnerETL~A`'s A-Prime call, not mine,
and their apply is in flight.

---

## WHAT THIS MEANS FOR TOMORROW'S 13:30Z FIRE

**`a4_expected` is DERIVED, not a literal** — the bundle computes
`len(SCOPES) * len(ARTIFACT_TYPES)`, and the **bundle's** constants are:

```
SCOPES         = ("49financial", "inflection", "cottonwood", "global")     -> 4
ARTIFACT_TYPES = ("aggregate-aua-timeseries", "aum-metrics", "account-distribution") -> 3
                                                                    a4_expected = 12
```

⛔ **SO `3.0.0_SA_CVO`'s L1 BAR (`a4_objects_built == a4_expected == 12`) IS CORRECTLY FRAMED AGAINST
THE DEPLOYED BUNDLE, AND IT WOULD BE WRONG AGAINST HEAD.** At HEAD the consolidator carries the
D1_CATVIEWS 4th artifact type — commit `ba2a91d980` states *"a4_expected 12 → 15"*. **If the pin ever
advances past that commit, the 12 in the bar becomes 15 and a correct run would read as a failure.**
That coupling is not recorded anywhere I could find, and it is the one thing in this census that could
bite a reader who does not know it. Flagged, not acted on.

**No surprise priced into tomorrow by the two CAUSE-A rows** — they are the intended state.
**The CAUSE-B rows are the live question**, and they belong to the in-flight A-Prime apply.

---

## ⛔ A FALSE RESULT I PRODUCED AND CAUGHT

My first S3 fetch pass reported **"21 of 21 absent"** — every mapped member missing. **A uniform
failure across a whole set is an INSTRUMENT signature, not a defect signature**, and the positive
control killed it immediately: `code/scripts/gold/` holds **28** objects, `assets_gold/` **4**,
`silver/` **2**, and a direct `head-object` on `mdpf_gold_consolidator.py` returns rc=0.

**The defect was mine: an `aws` call inside a `while read` loop consuming the loop's own stdin** — the
classic. Rewritten as an explicit generated command list with no read-loop, which returned 15 present /
2 absent. Had I trusted the first pass I would have reported the entire deploy tree as missing.

## FAILURE MODE (Rule 28 Q7) — the distinction that stops 16 false rows

`assets_gold` and `silver` are **SHARED repo homes**, and `safe_deploy_core` is explicit that for these
**the S3 side is the authority on membership**: a repo file with no counterpart at the mdpf prefix
*"was never meant to be there and is NOT a missing deploy."* Measured membership: `assets_gold` 4
objects (pair, slice, dim_model_portfolio, dim_taxsma_report), `silver` 2 (fact_taxsma_report,
rebalancer_schemas). **So the 2 NOT_A_MEMBER rows are a legitimate state, not divergence.** Collapsing
them into "missing" is the failure this rule exists to prevent, and the source comment says it produces
~16 false rows — which would have swamped the 4 real ones.

## SEPARATE OBSERVATION — the source map is behind the live function

`lambda-source-map.json` records `artifact_sha256 UVT5XRX3R2O3zsr+g2QTPrD2DDYlQilSP+IfmjD2mIc=` and
`last_deployed_commit 530ba66971`, `last_deployed_at 2026-08-25T19:38:55Z`. The live function reads
`CodeSha256 3/897ecG2Xzal+0Xl+Ygoshsqccd6smAcMwygv8KjZQ=`, LastModified **2026-08-26T15:29:34Z**.
**Rule 4 drift.** Most likely pending `0.6.2_AE_PartnerETL~A`'s in-flight A-Prime update rather than
neglect — **stated as likely, not established.** Not chased, not touched.
