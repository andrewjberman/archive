# DESIGN — D_00 served-AUA basis provenance: kill the 2026-08-01 silent cliff

**For:** `1.0.0_SA_CTO` gate (ruled in principle 20260723T172430Z; COO packaged it with the retry-net 2026-07-24).
**By:** `0.6.2_AE_PartnerETL~A`, 2026-07-24 ~1350Z. **Implements:** `0.4.0_DS_ClientPlatform` (Rule 13). **Verifies:** me (SoD).
**Status:** PROPOSAL. Nothing built, nothing deployed, no code path touched.
**Grounding:** `data/black_diamond/scripts/gold/D_00.portal_aggregates.py` @ working tree, source-read this session
(`:232-243`, `:246-254`, `:257-271`, `:273-288`, `:772`, `:867`, `:1014`, `:788-790`, `:855-858`) +
`deliverables/FINDING_49f_alloc_unrealized_stall_20260723.md`.

---

## 0. The defect in one paragraph

`_resolve_served_aua` `:273` returns a **bare float**. The served firm AUA can be produced on three different
**bases** — a fresh cert, a *held* stale cert, or the gold position-sum — and **the artifact cannot tell them
apart.** Today the served value is the 2026-07-17 cert (1,879,986,733.13), held because `certified_aua<=0` for
every date after 07-17. `_last_good_certified_aua` `:257` searches `lookback_days=14`. On **2026-08-01** the
07-17 cert falls out of that window, the search returns `(None, None)`, and `:287` executes
`return float(gold_fallback)` — a **silent basis substitution** to 1,780,856,838.03: **−$99.1mm / −5.27% on the
client-facing firm AUA, with a `print` as its only trace.**

**This is not a stale-value bug. It is a provenance bug.** The stale value is defensible and CTO already ruled
for holding it. What is indefensible is that the number changes basis without the artifact saying so.

---

## 1. Coverage denominator — three call sites, and two scripts I am NOT covering

`_resolve_served_aua` has **exactly three** call sites, all in `D_00`:

| # | line | consumer | client-facing? |
|---|---|---|---|
| 1 | `:772` | `build_header_metrics` → `total_block['aua']` `:789` → `platinum/firm/header_metrics.json` | **YES — the headline firm AUA** |
| 2 | `:867` | `build_snapshots` → `_snapshot_response(...)['total_aua']` `:857` | **YES — and it is the DENOMINATOR of every `aua_pct`** (`:871`, `:879`, and the state/region rows) |
| 3 | `:1014` | console `=== Summary ===` only | no artifact |

**Site 2 is the one that will be missed.** A basis flip does not only move the headline — it re-bases every
architect / tax / state / region percentage in the snapshot files. **Any fix that covers only
`header_metrics.json` is a partial fix that will read GREEN.**

**OUT OF SCOPE, flagged not silently dropped:** `D_00b.portal_timeseries.py:1395` and
`D_01.partner_analytics.py:2307` each `_load_aua_certification(...)` **directly** and pass `cert` into their own
builders — **they do not route through `_resolve_served_aua` at all.** Whether they carry the same degenerate
path, a different one, or none, I have **not** established. **I am not claiming D_00 is the whole surface.**
Recommend a scoped follow-on audit of both; I will run it on request. *(Stating this because "we fixed the
cliff" would otherwise be believed of an estate whose other two AUA-bearing gold scripts were never looked at.)*

---

## 2. The principle — same one CTO gated on the sidecar this morning

His sidecar ruling: *a completeness sidecar is an assertion that we measured completeness; `>=1 row` measures
not-a-stub; those are different claims, and the artifact must let a consumer reject one on `basis` alone.*

**The identical rule applies here.** A served AUA of `1,879,986,733.13` asserts *"the certified firm AUA."*
After the cliff, `1,780,856,838.03` asserts *"the certified firm AUA"* too — while actually meaning
*"a position sum on a different basis, because the cert aged out."* **Same field, same type, same magnitude
class, different claim, no way to tell.** UNKNOWN ≠ COMPLETE there; **HELD ≠ CERTIFIED here.**

So the fix is not "extend the lookback." **Extending the lookback only moves the cliff** — it makes the silent
substitution happen later, which is strictly worse because it will have been forgotten by then.

---

## 3. The change

### 3.1 `_resolve_served_aua` returns a value **with its basis**

Replace the bare float with a small immutable result (a `NamedTuple` — no new dependency, and it keeps
`.value` explicit at every call site so a missed one fails loudly at review rather than silently coercing):

```
ServedAUA = NamedTuple(value: float,
                       basis: str,            # 'certified' | 'held_certified' | 'gold_floor'
                       cert_data_as_of: str|None,   # the as-of the value actually came from
                       held_days: int|None,         # today - cert_data_as_of, calendar
                       hold_reason: str|None,       # 'degenerate_cert' | 'cert_absent'
                       alternative: dict|None)      # {'basis':'gold_floor','value':<gold>,
                                                    #  'delta':<v-gold>,'delta_pct':<...>}
```

`basis` is the field a consumer rejects on, **without heuristics** — never a value that could be mistaken for
`certified`.

### 3.2 The cliff behavior: **hold, do not substitute**

The `lookback_days=14` bound stops being the thing that decides **what to serve**, and becomes only the thing
that decides **how loudly to say it**:

| condition | served | `basis` |
|---|---|---|
| fresh cert `>0` | cert | `certified` |
| degenerate/absent cert, last-good found (any age) | **last-good cert** | `held_certified` |
| **no last-good cert exists at all** | gold sum | `gold_floor` |
| `DEGENERATE_CERT_MODE='gold'` (explicit operator choice) | gold sum | `gold_floor` |

**The search is no longer capped at 14 days for the purpose of holding.** The 07-17 cert stays served on
2026-08-01 — **the −$99.1mm flip simply does not occur** — and `held_days` climbs visibly instead.
This is the frozen-beats-unheld law applied at the fallback: *a known-wrong frozen number is strictly safer
than an unheld pipeline*, and a **silently re-based** number is the unheld case wearing the frozen case's
clothes.

`gold_floor` survives only as the genuine no-history case (and the explicit env override). **The floor is
unchanged and non-negotiable: this never returns `<=0`.**

**Bound on the search:** unbounded `range()` over S3 `get_object` per day is not acceptable. Walk the existing
`gold/aua_certification/` **key listing** (already key-sorted, 73 partitions per the finding) and take the
newest partition with `certified_aua>0` — **one LIST, not N GETs**, and it is strictly more correct than a
day-stepping probe because it cannot step over a gap.

### 3.3 The artifact contract — visibility rides in the data, no alarm

Per CTO 172430Z and Andrew's standing *"no more sentinels and alarms"*: **no new alarm, no sentinel, no cron.**
The signal is a block beside the value, in **both** client-facing artifacts (sites 1 **and** 2):

```
"aua_provenance": {
  "basis": "held_certified",
  "cert_data_as_of": "2026-07-17",
  "held_days": 15,
  "hold_reason": "degenerate_cert",
  "alternative": {"basis": "gold_floor", "value": 1780856838.03,
                  "delta": -99129895.10, "delta_pct": -5.27},
  "generated_at": "..."
}
```

`alternative` is the part that makes this decision-useful rather than merely honest: **the number we are NOT
serving, and what switching would cost, sit right next to the number we ARE serving.** The 08-01 question stops
being an invisible event and becomes a quantified choice a human can make on one look.

**On the portal:** emitting the block is this design's scope. **Rendering it is DE's**, and I am not
speculating about the UI. Recommend CTO route a DE follow-on for a held-basis indicator once the field exists —
but the field is useful to operators and to `served-value-freeze-check.py` on day one regardless.

---

## 4. What this deliberately does NOT do

- **No alarm / sentinel / scheduled freeze-check.** Declined at 172430Z; the instrument stays available by hand.
- **No touching bronze** (CLAUDE.md 17a) and no re-running anything to "fix" the value.
- **No change to C_02.** Its BRANCH-A floor `:309-332` is correct and is why no degenerate cert exists. Do not
  "fix" the guard that is working — the freeze is what correct guards produce on a stub feed.
- **No lookback extension as the fix** (§2 — it relocates the cliff).
- **No attempt to make the served number "right".** The upstream fix is the BD feed; vendor contact is gated on
  Andrew. This design makes the number **honest**, not correct.

---

## 5. Acceptance — how to prove it, including the mutant

Two-axis, on the **artifact**, with the coverage denominator stated (**both** site 1 and site 2 — a pass on
`header_metrics.json` alone is NOT acceptance):

1. **Normal path:** with a fresh cert, `basis == "certified"`, `held_days == 0`, and `value` **byte-identical**
   to today's served value — *the fix must not move a number that is currently correct.*
2. **Held path (today's live condition):** `basis == "held_certified"`, `cert_data_as_of == "2026-07-17"`,
   `held_days` = actual, `alternative.delta_pct` ≈ `-5.27`.
3. **THE CLIFF TEST — the whole point:** run with `today` simulated at **2026-08-01** (and 08-15). **Served value
   must remain 1,879,986,733.13 and `basis` must remain `held_certified`.** On today's code this returns
   1,780,856,838.03. *This test fails on the current code and passes on the fix — that is what makes it a test.*
4. **MUTANT / negative control:** force `certified_aua<=0` **and** remove every prior cert → must return
   `gold_floor`, never `<=0`. Proves the floor still holds and that `held_certified` is not simply always-on.
   *(A `basis` field that can only ever read `held_certified` would pass tests 2 and 3 while measuring nothing —
   this is the control that catches it.)*
5. **Site-2 coverage:** in the snapshot artifacts, `total_aua` matches site 1's value AND `aua_provenance` is
   present. Independently: the `aua_pct` rows must still sum ~100 — proving the denominator was not re-based
   mid-flight.

**Deployment note:** this is a `data/black_diamond/scripts/gold/` change → **DS owns the full commit→QA-deploy
cycle** (Rule 13). I verify on the served artifact, not on a self-report or an rc=0.

---

## 6. Runway and sequencing

**8 days to the cliff** (2026-08-01). This limb is **not** competing with tonight's ~02:00Z retry-net window —
different tree, different artifact, no shared file. Recommend DS lands the retry-net limb first (it has a
time-boxed exercise attached) and takes this immediately after; the runway is comfortable and this design should
not be rushed into the same night.

**Firm scope:** `bd`/49F tree only. The Cottonwood plane has the same *vendor* gap but its own served path;
firm-separation binds. Flagging the parallel, not proposing a cross-tree change.
