# ETFS_SATELLITES.TO-9-DE -- the INTERNAL VIEWER's FIRM SELECTION

**Seat:** `0.4.0_DE_ClientPlatform~S` · **Issuer:** `2.0.0_SA_COO~Z` · **Certifies:** `3.0.0_SA_CVO~Z`
**Cells:** `SAT-c-2` (server-VALIDATED limb) · `SAT-c-3` · `SAT-a-4`
**Portal commit:** `8c2ba9bb` on `DEV` (5 files, +183/-12) · TO read at HEAD `2974d1876b`

---

## 1. THE RULING THIS IMPLEMENTS

`1.0.0_SA_CTO~Z`: **an internal viewer is not a firm.** They may look at any firm, so their firm is
not determined by identity and `?firm=` is **a SELECTION, not a parameter needing a default**.
**The router's 400 is CORRECT and is untouched.** The defect was that the UI offered the Satellites
pill without offering the selection.

⛔ **No default anywhere -- not in the router, not in the client.** A client-side default would be
the twin of the refused router-side one, with the same failure mode: the viewer sees *some* firm's
data with nothing saying which. **A 400 is loud; a plausible wrong firm is not.**

## 2. ACCEPTANCE CRITERIA

### `T9DE-AC1` -- explicit selection, no default · **MET**

`useState<string>('')` -- not `'global'` (which has **no bucket**), not the first firm, not a
remembered value. The query is **DISABLED** while unselected, so the correct 400 is never provoked
just to render a prompt.

**Evidence that no fetch happens, as a by-product of the instrument:** the unselected render matched
**1 of 2** fixtures -- the registry was never requested. The selected render matched **2 of 2**.

### `T9DE-AC2` -- the selected firm is visible while they look at it · **MET**

`T9DE_render_internal-selected-cot.png`: the header reads **COTTONWOOD CAPITAL ADVISORS** beside the
mode pills, for as long as the nine books are on screen. **A second display of the same fact was
deliberately NOT added** -- one carrier, and the control is it.

### `T9DE-AC3` -- firm-scoped viewers unchanged · **MET**

`T9DE_render_firmscoped-cot.png`: a cottonwood viewer sees **no selector** and needs **no extra
click**; identity already determines the firm, so **no `?firm=` is sent**. The header carries only
the mode pills.

### `T9DE-AC4` -- the discrimination survives, and is now FIVE-way · **MET, BY HASH**

```
unselected      c05fc9fd65e27304   <- NEW, and DISTINCT FROM empty (the criterion)
selected-cot    f25e774db7d2b535
served-empty    6db0b0cf03b83b78
fetch-failed    aee1e0984d455587  \  BYTE-IDENTICAL, intentionally -- both are
as_of null      aee1e0984d455587  /  "could not be loaded"
firm-scoped     d186a8d5108520bd
```

**6 renders, 5 distinct hashes, and the one collision is the one `TO-8-DE` designed in.**
`unselected != empty` is decided by hash comparison, not by my reading of two screenshots.

### `T9DE-AC5` -- rendered, not grepped · **MET**

Six read screenshots. Canvas law holds: the new selector is **dark text on a ring with a transparent
fill** on the silver canvas -- not a ghost-white control outside a dark Panel.

## 3. BUILD LADDER -- WHAT WAS REUSED, AND THE ONE THING THAT WAS NOT

**REUSED (rung 2):** `PageSurfaceControl` (shared ui component) · the `internal = isInternal() ||
isDev()` predicate · the `internal ? selected : claims.firmId` pattern -- **which is CTO's ruled
shape already written twice** (`ModelPortfolios.tsx:335`, `AdvisorIntelligence/index.tsx:53`).

⛔ **NOT REUSED: `ALL_MDPF_PARTNER_FIRMS`.** It is module-private to a 2400-line page, it contains
`global` which has **no bucket**, and importing a page into a page for one constant is the wrong
dependency. **The selectable set is DERIVED from `MODE_FIRM_ALLOWLIST.satellites` minus the internal
id**, so a firm can never be *offered* on the picker without being *entitled* to the mode -- one
carrier, and the two cannot drift.

## 4. ⛔ THE LANDMINE, CARRIED INTO THE BUILD RATHER THAN REDISCOVERED

The selector's id is portal-canonical (`cottonwood`); the router builds `"opal-data-" + firmParam`
and needs the **slug** (`cot`). `bucketSuffix` is now **exported** from `advisor-intelligence.ts` and
applied at the wire boundary in `getSatelliteRegistry`.

Its own comment records what omitting it cost: `bucketSuffix('cottonwood')` falling through built
`opal-data-COTTONWOOD` and **rendered Andrew's INTERNAL cottonwood view EMPTY on 2026-06-22** -- same
viewer, same param, same router branch. **Exported rather than copied: two carriers of that mapping
is exactly what the P0 cost.**

## 5. INSTRUMENT CHANGE

`ui-smoke.mjs` gains `--pick <value>`. `--select` fires **before** the ordered step list, which is
correct for a dropdown present at load and **structurally cannot reach a control that only exists
after a click**. `--pick` runs as an ordered step. **ADDITIVE** -- `--select` is untouched, so no
existing caller's run is re-ordered.

## 6. GATES

```
tsc -b --noEmit    rc=0   (proven able to fail earlier this session: planted TS2322 -> rc=2)
eslint             rc=0   across all five changed files
non-ASCII          0 added lines -- one slipped in and was caught BEFORE commit
commit-gate        reads no .ts/.tsx -- NOT cited as validation
```

## 7. SURFACED, NOT SOLVED

- **`'Cottonwood Capital Advisors'` now has a FIFTH carrier** in this codebase. The alternatives were
  importing a page module or minting a shared firm-registry this TO has no mandate to own.
  **Firm display names want one home and do not have one.**
- **`bucketSuffix`'s home is wrong** for a wire-protocol translator -- it lives in one page's
  endpoint module. The single carrier was preserved and **the relocation surfaced rather than
  invented**, because moving it is a naming/ownership decision this TO does not carry.

## 8. WHAT THIS DOES NOT CLOSE

⚠ **The renders use FIXTURES and a STUBBED session, not a live cottonwood credential.** They exhibit
the UI's behaviour -- selector presence, no-default, the five-way discrimination, the firm label on
screen -- **not** that a real cottonwood caller is served by the live route. That rung stays as
`3.0.0_SA_CVO~Z` left it: **inferred from source, not exercised**, for want of a cottonwood
credential on this device.
⚠ The `firm-scoped` render uses `--firm cottonwood`, which sets a **stub claim**, not a real bearer.
It tests the client's branch, and nothing about the auth plane.
