# TO ETFS_SATELLITES.TO-9-DE — the INTERNAL VIEWER's FIRM SELECTION (the last thing between D4 and Andrew's smoke test)

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md — `SAT-c-2` (firm resolution is server-derived **or server-VALIDATED**, never client-ASSERTED) and `SAT-c-3` (visibility gate, not an authorization boundary). **NO new cell.**</decomp_ref>
<certification>Decomp CERTIFIED (`3.0.0_SA_CVO~Z`). No cell added. ⚠ **`SAT-c-2` is cited on its *server-VALIDATED* limb, and that reading is stated rather than assumed:** the viewer EXPRESSES a firm, the router VALIDATES entitlement. **A client-ASSERTED firm that the server accepts unchecked would violate this cell; a client-SELECTED firm the server checks does not.**</certification>
<issued_to>0.4.0_DE_ClientPlatform~S</issued_to>
<executor_class>DE-class (portal, `portal/**` on DEV)</executor_class>
<seating_trigger>SEATED — **same project, same instance, Rule 27 satisfied.** ⭐ This lane built the consumer seam (`TO-8-DE`), holds the four-way state discrimination, and **found this defect** as arm 1 of its own auth control. **The context is already loaded.**</seating_trigger>
<placement>SITE Z (Rule 26). ⛔ `portal/` is a WORK-SITE. **Main tree stays on DEV (Rule 19).**</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T03:0xZ</issued>
<status>complete -- ⭐ **CERTIFIED. THE CERTIFICATE EXISTS AND IS ON ORIGIN.** `cvoZ_ETFS_SATELLITES_TO8DE_TO9DE_CERTIFICATION_20260828.md` @`3f16f616f5`, verdict **CERTIFIED -- 5 of 5, INSTANCE VALID**. Located 15:1xZ by `3.0.0_SA_CVO~Z`; VERIFIED at this seat by containment against `origin/SITEZ` with a SOUND negative control (`origin/CLOUD` tip NOT contained, so the test demonstrably returns NO). ⛔ **THIS FACE PREVIOUSLY READ 'awaiting certification' AND WAS STALE -- the certificate POSTDATES it and nobody updated the face.** ROOT: the face and the certificate are TWO DURABLE RECORDS OF ONE FACT WITH NO NAMED PRIMARY -- the certifier writes one and cannot write the other, the issuer owns the face and has no trigger to return, so they diverge from minute one in the direction of 'outstanding'. Corrected by `2.0.0_SA_COO~Z` as ISSUER. ⚠ **BOUND, STATED BY ITS MEASURER AND NOT PAPERED OVER: this establishes A CERTIFICATE EXISTS for the criteria as they read AT CERTIFICATION TIME. It does NOT establish that no criterion was ADDED to this face afterwards -- that needs a per-face criterion-set diff, NOT RUN.**

⚠ **THE ORIGINAL `<status>` CONTENT FOLLOWS, RESTORED VERBATIM.** `2.0.0_SA_COO~Z` replaced it wholesale at @4253643625 instead of appending, destroying evidence on seven faces (142 lines on one of them). Recovered from `4253643625^` and re-attached. **NOTHING BELOW THIS LINE IS NEW; NOTHING ABOVE IT WAS IN THE ORIGINAL.**

complete — SELF-MARKED by `0.4.0_DE_ClientPlatform~S` 2026-08-28T03:2xZ per `org/XXX.md`:725. **5 of 5 AC met.** Portal `8c2ba9bb` on DEV. ⚠ **`complete` != SMOKE-TESTED:** the renders use FIXTURES and a STUBBED session, so they exhibit the UI's behaviour and NOT that a live cottonwood caller is served — that rung stays inferred-from-source for want of a cottonwood credential. Awaiting `3.0.0_SA_CVO~Z` certification.</status>
<priority>⛔ **P0 — THE LAST OPEN ITEM IN D4.** D4's completion bar is **Andrew's smoke test**, he is an **INTERNAL** viewer, and today an internal viewer sees the Satellites pill and gets a 400. **Every other D4 fix tonight is invisible to that test; this one IS the test.**</priority>
<authority>**ANDREW-DIRECT 2026-08-28 ~01:3xZ:** *"End to end full 'Satellites' view mode on 'Positioning' page."* Shape RULED by `1.0.0_SA_CTO~Z` (msg 12353).</authority>

---

## 1. THE DEFECT (your own measurement, arm 1 of `T7AE-AC3`)

```
index.mjs:227-241   an `opal-capital` caller MUST supply ?firm= or the router 400s before
                    resolving a bucket
modeAccess.ts:118   INTERNAL_FIRM_ID ('opal-capital') IS IN THE SATELLITES ALLOWLIST
=> Opal staff SEE the pill; the fetch behind it returns 400.
```

## 2. ⛔ THE RULING — AND IT INVERTS WHERE THE DEFECT LIVES

`1.0.0_SA_CTO~Z`, msg 12353:

> ⭐ **AN INTERNAL VIEWER IS NOT A FIRM.** They are a viewer entitled to look at **any** firm. So
> `?firm=` is **not a parameter needing a default — IT IS A SELECTION THE VIEWER MAKES EXPLICITLY.**
> ⛔ **THEREFORE THE ROUTER'S 400 IS CORRECT BEHAVIOUR AND STAYS.** It is refusing to guess whose data
> to serve, which is exactly what a firm-scoped route should do when identity does not determine a
> firm. **THE DEFECT IS NOT IN THE ROUTER. IT IS THAT THE UI OFFERS THE PILL WITHOUT OFFERING THE
> SELECTION.**

⛔ **OPTION (a) — a router-side internal default — WAS REFUSED, and the reason binds you too:** it
would create **"a second, forgeable expression of the same boundary"** on a key that carries no firm
segment *on purpose*. ⚠ **And its failure mode is worse than a 400: an internal viewer would silently
receive SOME firm's data with nothing on screen saying which.** ⭐ **A 400 is loud; a plausible wrong
firm is not.** **Do not solve this by defaulting anywhere — not in the router, not in the client.**

## 3. ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `T9DE-AC1` | **An internal viewer gets an explicit FIRM SELECTION on the satellites surface, and the fetch carries what they picked.** ⛔ **NO DEFAULT. NO IMPLICIT FIRM. NO "first firm in the list".** An internal viewer arriving with nothing selected must see **a prompt to select**, never data. | `SAT-c-2` | **MET** -- `useState<string>('')`; query DISABLED while unselected. Unselected render matched 1 of 2 fixtures: the registry was NEVER requested. |
| `T9DE-AC2` | ⛔ **THE SELECTED FIRM IS VISIBLE ON SCREEN WHILE THEY LOOK AT IT.** *"Which firm am I looking at"* **must never be answerable only from memory.** ⚠ **This is the criterion that makes (a)'s refusal meaningful** — the whole objection to a default was silent mislabelling, and an invisible selection re-creates it. **Exhibit it in a read render.** | `SAT-c-3` | **MET** -- header reads COTTONWOOD CAPITAL ADVISORS beside the pills while the 9 books render (`T9DE_render_internal-selected-cot.png`). One carrier; no second display added. |
| `T9DE-AC3` | **FIRM-SCOPED VIEWERS ARE UNCHANGED.** A cottonwood viewer still gets satellites with **no selector and no extra click** — their identity already determines their firm. ⛔ **Show the cottonwood path is BYTE-UNCHANGED in behaviour**; a regression here trades a staff bug for a client bug. | `SAT-c-2` | **MET** -- `T9DE_render_firmscoped-cot.png`: no selector, no extra click, no `?firm=` sent. |
| `T9DE-AC4` | ⛔ **THE 400 STILL RENDERS AS AN ERROR, NEVER AS "no satellites".** `T8DE-AC2`'s four-way discrimination **must survive this change** — re-exhibit it. ⚠ **A selection UI that turns an unselected state into an empty-registry render would destroy the property you built the seam to guarantee.** | `SAT-a-4` | **MET, BY HASH** -- 6 renders, 5 distinct hashes. `unselected c05fc9fd` != `empty 6db0b0cf`; the sole collision is `failed`==`asofnull` (aee1e098), which TO-8-DE designed in. |
| `T9DE-AC5` | ⛔ **RENDERED, NOT GREPPED** — read screenshots of: internal-unselected · internal-selected-cottonwood · firm-scoped-cottonwood. ⚠ **THE CANVAS IS SILVER**; a selector is exactly the kind of new control that arrives ghost-white outside a dark Panel. | `SAT-c-3` | **MET** -- 6 read screenshots; canvas law holds (selector is dark-on-ring, transparent fill, no ghost-white on silver). |

## 4. ⛔ NOT YOURS

- **The router.** ⛔ **The 400 is CORRECT and STAYS.** Do not touch `index.mjs`; do not ask for a default.
- **Entitlement.** ⚠ Whether `internal_admin` may read a given firm is **server-side and already enforced** — `SAT-c-3` is explicit that this is a **visibility gate, not an authorization boundary.** **Do not implement an authorization check in the client.**
- **The producer, the schedule, `ETFS_INGEST`, `D1_CATVIEWS`** — other lanes, other projects.

## 5. ⚠ THE SHAPE OF THE SELECTION IS YOURS

Picker, existing firm switcher, or route param — **`1.0.0_SA_CTO~Z` ruled the PROPERTY, not the widget.** ⭐ **Prefer the existing firm switcher if one is already in the portal: reusing a control the estate already has is Build-Ladder rung 2, and a second firm-selection mechanism is a second carrier of the same choice.**

## 6. REPORTING

Deliverable + read screenshots + proof instance in this lane's `deliverables/`, `safe-commit` under your own author line, non-shell-written message file. Report to `2.0.0_SA_COO~Z`; `3.0.0_SA_CVO~Z` certifies. **ACK on receipt.**
⚠ **`proof-of-spec-check` may return INVALID on vocabulary grounds — FILE THE TRUE VALUES ANYWAY.** Standing ruling: *when an instrument and the truth disagree, the instrument is what changes.*

<proof_of_spec>
  <criterion id="T9DE-AC1" cell_refs="SAT-c-2"/>
  <criterion id="T9DE-AC2" cell_refs="SAT-c-3"/>
  <criterion id="T9DE-AC3" cell_refs="SAT-c-2"/>
  <criterion id="T9DE-AC4" cell_refs="SAT-a-4"/>
  <criterion id="T9DE-AC5" cell_refs="SAT-c-3"/>
  <expected_criteria>T9DE-AC1,T9DE-AC2,T9DE-AC3,T9DE-AC4,T9DE-AC5</expected_criteria>
  <alignment_denominators>cells declared: 3 (SAT-c-2, SAT-c-3, SAT-a-4); criteria: 5. FORWARD — 5 of 5 carry >=1 cell_ref. BACKWARD — 3 of 3 reachable (SAT-c-2 from AC1/AC3, SAT-c-3 from AC2/AC5, SAT-a-4 from AC4). Unmapped 0; untraceable 0. NOTE: no cell is added. `SAT-c-2` is cited on its server-VALIDATED limb — the viewer EXPRESSES a firm and the router VALIDATES it — which is stated in `<certification>` rather than left as a silent stretch of "never client-asserted".</alignment_denominators>
</proof_of_spec>
