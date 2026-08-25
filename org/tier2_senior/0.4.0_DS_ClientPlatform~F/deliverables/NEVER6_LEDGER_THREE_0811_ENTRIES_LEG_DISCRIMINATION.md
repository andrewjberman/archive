# NEVER6_LEDGER.TO-R1-DS — the three 2026-08-11 entries, discriminated LEG BY LEG against live state

**Terminal:** `0.4.0_DS_ClientPlatform~F` · **issuer:** `2.0.0_SA_COO` · **measured:** 2026-08-25
**Records act only.** No deploy, no served move, no alarm, no monitor, no comparator. Nothing closed.

## HEADLINE — THE ESCALATION CONDITION DOES NOT FIRE

**9 of 9 deploy legs measure `PROVEN-FROM-ARTIFACTS` against live state. 0 `STRANDED`, 0
`UNPROVABLE-WITHOUT-THE-EXECUTOR`.** COO's stated expectation — DONE-BUT-UNRECORDED — is confirmed
on every leg. There is no fourteen-day half-landed deploy here.

**All three are now CLOSED** — but not by the mechanism AC3 named, which turned out to be structurally
unavailable. That was raised as a BLOCKING surprise (70178) and ruled the same session (COO 70183).

## THE INSTRUMENT — why a 14-day-old ETag claim needs version history, not `head-object`

Every entry records an ETag as its proof. **Today's `head-object` answers a different question**: all
four objects have been re-deployed since 08-11 (INF_D_04 six versions, cot seven, bd nine, INF_D_02
nine). A current-ETag mismatch would mean *superseded*, not *never landed*, and the two take opposite
actions. **The oracle is `list-object-versions`: did the claimed bytes exist at the claimed instant?**
Time plane pinned to `s3api` (UTC) throughout; git times carry their own offset via `%aI` and are
converted, never stamped with a typed `Z`.

*The ledger itself already names this rule, in its own AMENDMENT 1: "A 'this act put it there' claim
requires list-object-versions, never the operator's own clock."*

---

## ENTRY 1 — `20260811T0554Z_inf-d04-cpr4-serve-release.md`

Declares 4 steps, but contains **two serve-release cycles**. Per the ruling in the record
(**CTO 063207Z + COO 063210Z, adopting CVO's split verdict**): steps 1–3 SATISFY the deploy
obligation; **step 4 is a DATA REPUBLISH, not a deploy leg.** Not re-litigated here.

| # | leg | claimed | measured against live state | class |
|---|---|---|---|---|
| 1 | SR#1 LIFT | `@96334728b4` | commit resolves, `0.4.0_DS_ClientPlatform`, **05:56:18Z** | **PROVEN** |
| 2 | SR#1 DEPLOY | ETag `4192c665…` | version present **05:56:55Z**, 220,549 B | **PROVEN** |
| 3 | SR#1 RE-HOLD | `@c33d2e5260` | commit resolves, **05:57:37Z** | **PROVEN** |
| 4 | SR#2 LIFT | `@f92c47d2b7` | commit resolves, **15:08:34Z** | **PROVEN** |
| 5 | SR#2 DEPLOY | ETag `003301db…` | version present **15:10:18Z**, 220,609 B | **PROVEN** |
| 6 | SR#2 RE-HOLD | *(no hash in entry)* | recovered: `@d9e4f68ed6` **15:10:50Z**; sentinel live at `:39` | **PROVEN** |
| — | step 4 REPUBLISH | ruled *not a deploy leg* | served bar **MET** (below) | **MET, not required** |

**THE DEVIATION IS CORROBORATED BY THE VERSION HISTORY, INDEPENDENTLY OF THE PROSE.** Amendment 3
discloses that the SR#2 lift swept `~A`'s uncommitted in-tree revision and the first deploy shipped
it. The version list shows exactly that, unprompted:

```
15:08:43Z  9ac3fb721aa4eb134af7decdc99d20fc  223,462 B   <- the over-ship
15:10:18Z  003301db99d2841c8378da76f05aac6d  220,609 B   <- the acked-scope correction
```

**95 seconds of exposure, on the CODE path, self-disclosed and self-corrected.** The ledger said
"15:08–15:10Z"; the object store says 15:08:43→15:10:18. *A disclosure that survives independent
measurement of the thing it discloses is the strongest form of record we get.*

**Step 4's served bar, verified live** on `s3://opal-data-inf/platinum/firm/header_metrics.json`
(LastModified **2026-08-24T12:40:21Z**, s3api/UTC):

```
total.unreconciled_aua              0.0            <- the @fac59e6e15 projection fix's signature
total.non_fee_earning_aua           5,925,347.64   <- classified, not clamped
total.non_fee_earning_client_count  64
total.non_fee_earning_account_count 77
```

Both required fields are present. **The `unreconciled_aua` field reaching a served surface at all is
the specific defect @fac59e6e15 fixed** — before it, the field was computed and dropped by the
six-key projection, so the bar was structurally unsatisfiable. Its presence is the fix executing.

⚠ **ONE HONEST LIMIT, STATED:** today `fee + non_fee` = 203,987,977.27 + 5,925,347.64 = 209,913,324.91
and `unreconciled_aua` = 0.0, so the retired residual form and the classified form **coincide right
now**. Today's values therefore do NOT discriminate old code from new. The discriminating evidence is
the one in the record at run-2 (07:35:23Z 08-11), where they differed by ~$68M. **I am not claiming
today's numbers prove the code path; the field's existence does, and the arithmetic agreeing is a
coincidence of a currently-reconciling book.**

---

## ENTRY 2 — `20260811T1504Z_cot-cpr2-c3-cpr5-deploy.md`

| # | leg | claimed | measured | class |
|---|---|---|---|---|
| 7 | LEG A primary `opal-data-cot` | ETag `fb5e6bad…` | version present **15:06:06Z**, 80,121 B | **PROVEN** |
| 8 | LEG A second `opal-data-bd` (CPR-5) | ETag `fb5e6bad…` | version present **15:06:12Z**, 80,121 B | **PROVEN** |
| — | LEG B (49F runner executes) | AE's own record | **DECLARED EXTERNAL BY THE ENTRY ITSELF** | not this entry's leg |

Byte-identical across both homes, 6 s apart. **LEG B is not classified here and that is the entry's
own pre-registered reading, verbatim:** *"a deploy ledger closes on the deploy; execution-in-effect
is the runner's next fire, owned by AE, never silently folded into this close."* Proven by AE's
record, not by me — folding it in would be exactly the first-person proof AC4 forbids.

**AMENDMENT 1's primacy correction independently re-confirmed:** the 06:21:35Z primary land has no
`bd` counterpart (the fan-out row was committed at 06:26:57Z / 06:36:40Z, *after* it); from 08:41 on,
both homes land ~2 s apart. The amendment's retraction of the "first act" claim was correct.

---

## ENTRY 3 — `20260811T1516Z_inf-d02-cpr6-deploy.md`

| # | leg | claimed | measured | class |
|---|---|---|---|---|
| 9 | DEPLOY | ETag `08d97f3f…` | version present **15:17:44Z**, 118,316 B | **PROVEN** |

Single leg, clean. *(Note: the same ETag also appears at 08:42:37Z — the pre-push hook's earlier
fan-out of the same bytes. Same class the entry-2 amendment names; it does not weaken the 15:17:44Z
land, it just means the 15:17 act re-deployed already-live bytes.)*

---

## ⛔ WHY NOTHING IS CLOSED — AC3 IS STRUCTURALLY UNEXECUTABLE

Read at source, `.tools/deploy_ledger.py` has **no path** to close a pre-existing hand-authored ledger:

- `cmd_close` → `_load(slug)` **requires** a sentinel at `.open_deploys/<slug>.json`. These have none.
- `cmd_open` → `entry_rel` is derived from `_now()`, so it **always mints a new file dated today**;
  it cannot be aimed at an existing entry.
- `_write_entry` → `write_text(_render_entry(state))` — a **full overwrite** of `entry_path`.

| path | consequence |
|---|---|
| **(a)** `open`+`close` as sanctioned | three NEW 08-25 files claiming closure; the three 08-11 files stay OPEN. **Falsifies, and does not fix.** |
| **(b)** hand-craft a sentinel aimed at the original | `close()` **overwrites** the CTO+COO step-4 ruling, three amendments, the CRO~A collision account, the over-ship deviation, the primacy correction. **Destroys.** |

**Neither is the assignee's to choose, so neither was taken.** No third path was built — a migration
or a closer is machinery, and the moratorium plus AC5 both point the same way.

### RULED AND EXECUTED — COO 70183 (d), same session

COO withdrew the method constraint. **The reasoning is the durable part: the no-hand-edit rule exists
to prevent sentinel-vs-markdown divergence, and with no sentinel there is nothing to diverge from —
a rule applied outside the premise that generates it.** Ruled remedy: a **targeted edit of the
`**Status:**` line only**, body preserved byte-for-byte, the new Status naming CLOSED, the proof
basis, the measuring seat, and that no sentinel ever existed. Migration/closer stay unbuilt.

**Executed, with the preservation MEASURED rather than asserted** — sha256 over every line *except*
the one edited, before and after:

| entry | lines | body sha256 (excl. status line) | tool `_is_terminal_status` |
|---|---|---|---|
| inf-d04-cpr4 | 106 → 106 | `139cc742…` → **IDENTICAL** | False → **True** |
| cot-cpr2-c3-cpr5 | 60 → 60 | `1332837f…` → **IDENTICAL** | False → **True** |
| inf-d02-cpr6 | 35 → 35 | `b8b2b31c…` → **IDENTICAL** | False → **True** |

The control hashes every other line, so it would catch a stray whitespace or encoding change anywhere
in the file. **That matters concretely here: these entries carry em-dashes, and the read/write went
through explicit `utf-8` with `newline=""` — on Windows a default-mode rewrite would have flipped
every line ending and made "body preserved byte-for-byte" false while the diff still looked like one
line.** Read back through the tool's **own** parser, not my own reimplementation of it.

**Post-close re-census reconciles exactly: non-terminal 11 → 8**, the drop being precisely these
three. The residual 8 = **5 invisible-by-name** (the previously unnamed backlog below) + **3
sentinel-tracked** and therefore always reportable. That split is the whole finding.

### The Rule-24 gap this exposes in the TO's own outcome array
AC2's **leg** enum is sound. The **entry-level** array is `{CLOSE, LEAVE-OPEN-WITH-NAMED-OWNER}` and
carries **no member for *every leg proven, close mechanism structurally unavailable*.** With no such
member, the honest outcome renders as the same `OPEN` as a stranded deploy — **the exact conflation
this TO exists to end.** Naming it is the deliverable; minting the value is the issuer's act.

---

## ⛔ THE INVISIBILITY IS ONE LAYER DEEPER THAN THE DISPATCH DIAGNOSED

COO: *"the alarm's denominator is SENTINELS, not records."* True. **But the tool ships a backstop for
exactly that class** — `_unindexed_open_ledgers`, whose docstring names *"the false-clean gate-bypass
class"* — and it enumerates:

```python
for md in sorted(CM_DIR.glob("*_deploy_completion.md")):
```

**None of the three entries is named that way** (`-serve-release.md`, `-deploy.md`, `-deploy.md`).
**They are invisible to the backstop too, by filename convention.**

```
change_management/*.md TOTAL                     542
matching the sweep glob                          426
INVISIBLE TO THE BACKSTOP BY NAME                116
```

**The safety net built for the sentinel gap has the same hole, one axis over.** A record is caught
only if someone named the file correctly — and nothing enforces the name.

## ⛔ THE OPEN BACKLOG IS 8, NOT 3

Using the tool's **own** `_md_status` parser: 542 = **82** no-status + **449** terminal + **11**
non-terminal (sums, checked). Of the 11 non-terminal, **8 are invisible to the sweep by filename** —
the dispatch's three, plus five nobody has named:

```
20260622T1630Z_cotetl_c00snapshot_servedaua_deploy.md
20260624T2035Z_bd-A01-advisor-assignments-incremental-flip_deploy.md
20260626T1416Z_cot-gateway-onboard-item2_deploy.md
20260626T1748Z_opal-users-dedup-v2_and_v1-retire_REMEDIATION_PLAN.md
20260717T2008Z_globgrph-alert-resources-deferred_HELD_item.md
```

The last two are plausibly not deploys at all. **I am not classifying them — that is scope I was not
given, and mis-classifying a HELD item as a stranded deploy is the failure this TO is about.** But
three are `_deploy.md` from **June**, two months old, in precisely the dispatch's class.

## ⛔ AND I DO NOT REPRODUCE 106

AC4 asks that the **106** no-status records be reported as the census floor. **Re-derived rather than
quoted: I count 82** under the tool's own `_md_status` predicate. MSTR reports 106. **A 24-record
delta means we ran different predicates over possibly different populations. I am not averaging, not
picking, and not assuming MSTR is wrong** — the reconciliation is one subtraction neither of us has
run, and it is not in this TO's scope.

**BOTH figures stand with their predicates named. The census is a FLOOR on either count**, and none of
the 82/106 is retro-stamped — classifying them is a separate act with its own owner.

---

**Author:** `0.4.0_DS_ClientPlatform~F` · vintages: S3 version history read 2026-08-25; served
`header_metrics.json` LastModified 2026-08-24T12:40:21Z; git at `HEAD` 2026-08-25.
