# deploy_ledger backlog reconciliation -- post-reader-loosening

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-24T~1355Z
**Scope:** CTO's SHRUNK scope, ruling 214257Z (writer leg DROPPED). Item (a): reconciliation report over
what stays flagged after the reader loosening @9438f17fa. Item (b): convention fix for the accrual.
**Archetype:** VALIDATE

---

## BOTTOM LINE

**All three still-flagged ledgers are CLOSED IN FACT.** None is a half-landed deploy. Every one carries
explicit terminal evidence written by a human at close time; all three are invisible to the loosened
reader because their terminal marker is in a spelling neither reader limb matches.

**This is the case CTO reserved:** *"Do NOT touch the writer unless the reconciliation report surfaces a
class the loosened reader cannot read -- then back to CTO's gate WITH the instance."* **Two distinct
unreadable shapes, three instances, all enumerated below.** No mechanical pass made; that stays at the gate.

**And the accrual cause is confirmed, not inferred:** all three were **hand-authored**, never written by
`deploy_ledger.py`. This is a CONVENTION gap in the lanes, not a defect in the writer -- which is exactly
why CTO's drop of the writer leg was correct, and why a writer fix would have moved nothing.

---

## METHOD (and why it is not regex-reasoning)

I did not conclude from reading the patterns. I **imported the live module and ran its own reader
functions** against each file, with **positive controls chosen to discriminate**:

```
python -> importlib load .tools/deploy_ledger.py -> _md_status() / _has_close_marker() / _is_terminal_status()
```

| file | `_md_status()` | `_has_close_marker()` | terminal? | verdict |
|---|---|---|---|---|
| `20260722T2310Z_cot-advi-fix-silver-coerce` | `None` | `False` | `False` | **UNREADABLE** |
| `20260723T0133Z_cottonwood-mdpf-served-publish` | `None` | `False` | `False` | **UNREADABLE** |
| `20260723T1849Z_mdpf-allfirms-serve` | `None` | `False` | `False` | **UNREADABLE** |
| **POS-CTRL** `20260723T1052Z_6d-cottonwood-dispatcher-wiring` | `'CLOSED -- nothing stranded -- closed 20260723T110100Z'` | `False` | **`True`** | READS TERMINAL |
| **POS-CTRL** `20260723T1102Z_ws1-lever-a-age-bound` | `'CLOSED -- nothing stranded -- closed 20260723T1112Z'` | `False` | **`True`** | READS TERMINAL |

**The controls do real work here.** An all-`None` column across five files would have meant a broken
probe, not three findings. 2/2 controls returning a parsed terminal status establishes the reader is
functioning, so the three `None`s are the files' shape and not my instrument. (This is the
banked lesson: a sweep that cannot find a known-present instance is a broken instrument reporting silence.)

**Scan denominator:** `check --all` enumerated **3 of 3 sentinels** plus the `change_management/*.md`
bypass sweep; the three below are the complete set of `BYPASS: UNINDEXED OPEN LEDGER` hits. Nothing sampled.

---

## THE TWO UNREADABLE SHAPES

Both reader limbs are **line-anchored** (`^\s*(?:[-*+>]\s+)?`), which is the load-bearing detail.

### SHAPE A -- terminal marker present but MID-LINE (2 instances)

```
20260722T2310Z_cot-advi-fix-silver-coerce        :3
20260723T0133Z_cottonwood-mdpf-served-publish    :3
    **Ledger opened:** 2026-07-22T~23:05Z (deploy-start) · **Closed:** 2026-07-22T~23:10Z (COMPLETE, verified)
                                                          ^^^^^^^^^^^^ real, correct, and INVISIBLE
```

`_has_close_marker` matches `^\s*(?:[-*+>]\s+)?\*\*(?:date\s+closed|closed):\*\*\s*\S` -- anchored at line
start. Here `**Closed:**` sits **mid-line, after a `·` separator**, so the anchor never engages. The author
did write a bolded close marker in the sanctioned spelling; they put it on the same line as the open marker.

### SHAPE B -- bare unbolded terminal token, no `Status` keyword (1 instance)

```
20260723T1849Z_mdpf-allfirms-serve               :18
    CLOSED: 2026-07-23T18:52Z -- publish complete, report to CTO+COO+DE+DT sent same turn.
```

Fails **both** limbs independently: `_md_status` requires `**status:**` / `**status: ...**` / `## status:`
(no `Status` keyword present at all), and `_has_close_marker` requires the `**Closed:**` bold span (this is
unbolded). Line-start anchoring is satisfied; the *spelling* is what misses.

### For contrast -- the canonical form the writer already emits correctly

```
20260723T1052Z_6d-cottonwood-dispatcher-wiring   :3
    **Status:** CLOSED -- nothing stranded -- closed 20260723T110100Z
```

---

## CLOSURE EVIDENCE -- each is genuinely closed, cited per file

| ledger | terminal evidence in the file | assessment |
|---|---|---|
| `cot-advi-fix-silver-coerce` (DS) | `**Closed:** 2026-07-22T~23:10Z (COMPLETE, verified)`; code @`2ed963ef6` to `s3://opal-data-cot/code/silver/`, **content-verified S3 ETag `bee95d18a61e28873fe739d54516b745` == local MD5, 35,351 B**; auth chain CTO gate 224919Z -> COO GO 225533Z | **UNAMBIGUOUS closed.** Not mine to stamp. |
| `cottonwood-mdpf-served-publish` (DS) | `**Closed:** 2026-07-23T~01:33Z (COMPLETE, content-verified)`; three-part auth chain (Andrew-direct override 01:0xZ + CTO co-sign 012337Z ETag-pinned + COO counter-sign 013145Z with identities independently recomputed) | **UNAMBIGUOUS closed.** Not mine to stamp. |
| `mdpf-allfirms-serve` (opened by DS; **disposition assigned to me** per CTO 214257Z) | `CLOSED: 2026-07-23T18:52Z -- publish complete, report to CTO+COO+DE+DT sent same turn.`; **6/6 served keys byte-identical**, each with size + ETag cited; per-key staged-md5 assert -> put -> fresh-GET byte-compare -> ListObjectsV2; authority CTO serve-fire 184804Z on COO clean counter-sign 184724Z + DE render @`5ae6762da` | **UNAMBIGUOUS closed.** Mine to disposition. |

**Zero half-landed deploys in the flagged set.** The RED signal was entirely a legibility artifact.

---

## WHY THE WRITER LEG WAS CORRECTLY DROPPED (confirming CTO's ruling on evidence)

All three files are **UNINDEXED** -- no sentinel. They were **never produced by `deploy_ledger.py`**; they
are hand-authored markdown. Therefore:

- **A writer fix moves nothing.** `cmd_close`'s `_write_entry` already renders the canonical
  `**Status:** CLOSED -- ...` (proven by both positive controls). The writer was never the defect.
- **The `.md`-is-a-RENDERING contract is not implicated for these three.** That contract binds
  writer-managed entries reconstructed from a sentinel. These have no sentinel, so a hand-added status
  line neither races the writer nor trips Layer-3 drift. *(This is why stamping the one assigned to me
  below is safe, and it would NOT be safe on a sentinel-backed entry.)*
- **The accrual is a CONVENTION gap** -- promote/serve lanes hand-authoring ledger `.md`s without ever
  calling `deploy_ledger.py`. This confirms `~D`'s carry read (7 -> 12 unindexed, 4 from 07-23) as a
  convention-note-to-lanes problem, **not** an N-conversions problem.

---

## THE OPEN QUESTION FOR CTO'S GATE (not actioned)

The reader can be loosened to absorb both shapes, but **each option trades legibility against a real
false-positive risk**, and this is a call about what counts as a close signal -- not a mechanical edit:

| option | closes | risk |
|---|---|---|
| **A.** un-anchor `_has_close_marker` (allow mid-line `**Closed:**`) | Shape A (2) | a `**Closed:**` quoted in *prose* about another ledger would read as this one's close |
| **B.** accept a line-leading bare `CLOSED:` / `COMPLETE:` token | Shape B (1) | narrative lines beginning `CLOSED: ...` inside a body would false-close |
| **C.** leave the reader; fix the CONVENTION only | 0 now | existing files stay flagged forever, so the RED channel keeps carrying known-good noise -- and a channel that cries wolf is how a real half-landed deploy gets ignored |

**My read, offered as a recommendation and not acted on:** **C for the future, plus a bounded B.** The
`_STATUS_LINE_PATTERNS` ordering is already documented as LOAD-BEARING (strict-canonical first, because the
colon-inside pattern captures EMPTY from the canonical form) -- so any new pattern must be appended with
that ordering hazard in mind, and a regression guard already exists for exactly that class. **Option A
worries me most**: un-anchoring is the change most likely to match prose, and these ledgers quote each
other. I would rather the reader stay slightly strict and the convention get fixed than widen a matcher
until it reads narrative text as state -- **loosening a matcher until nothing is flagged retires the
control** (the same shape as the 3-tier copy-verify lesson).

**Requesting: CTO ruling on A / B / C before any reader change.** No mechanical pass will be made without it.

---

## ITEM (b) -- CONVENTION FIX (the durable half)

**Target:** the `/prod-deploy` skill text + the deploy-protocol docs, at next touch; DT adopts from the
next promote.

**Content:** promote/serve lanes that hand-author a `change_management/*.md` must either (i) use
`deploy_ledger.py open` / `close-leg` / `close` -- which produces a sentinel and the canonical
`**Status:**` line for free -- or (ii) if hand-authoring, put `**Status:** CLOSED -- <why> -- closed <ts>`
**on its own line**, never appended mid-line after a `·`.

**BLOCKED ON A LANE GRANT, surfaced not worked around:** both `docs/deployment/**` and the `/prod-deploy`
skill are **BASE_EXEC**-lane paths; `0.7.0_AE_CloudOps` is not in `permitted_agents` and `safe-commit`
blocks in block mode. **I did not `--force`.** This needs CTO/COO/DT to land, or a lane grant. (Same wall
hit today on `docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md`, handed to COO @135050Z.)

---

## ALSO IN THE SWEEP -- 3 HELD-STALE, all correctly held (no action)

Reported for completeness so the denominator is honest. **None is half-landed**; each is genuinely blocked
on an external/sovereign provision, which is a *refusal*, not an unfinished deploy:

- `freshguard-leg4-writer-wiring-finish` (15.0d) -- **FAIL BY DESIGN.** L4 is a measured refusal; the
  criterion is SPENT for its `T_d` and a re-test needs a new one. **Do not re-run, do not close.**
- `freshguard-leg5-v2-parity-drift` (15.3d) -- gated on a sovereign-provisioned read-only GitHub PAT.
- `scty-premcp-p1-layer2-phase1-readonly-scope` (15.3d) -- gated on an Andrew/IT interactive MS-login
  read-only token.

---

## DE-DUP LEG (CTO: verify-only)

`check --all` was run as a deliberate re-sweep with suppression bypassed (`--all` exists precisely so a
census is not answered from a suppression cache). **No re-flood:** 3 BYPASS + 3 HELD-STALE, matching the
expected post-reader-fix set. De-dup verified working; nothing rebuilt.

---

## WHAT I CHANGED

One evidence-cited status stamp on the single ledger CTO assigned to me
(`20260723T1849Z_mdpf-allfirms-serve`), whose closure evidence is unambiguous and which carries no
sentinel. **No mechanical pass. No writer change. DS's two left untouched** -- they are not mine to stamp,
and they are the standing instances for CTO's gate decision above.
