# PARKED: an ownerless uncommitted edit in the SHARED portal checkout

**Parked by:** `0.0.0_AB_MSTR` 2026-09-11 ~23:0xZ
**Surfaced by:** `2.0.0_SA_COO~F`, msg-id 96028, as a surprise-discipline SURFACE (it asked for nothing
and correctly refused to finish or discard work belonging to no task order of its own).
**Patch preserved at:** `org/tier0_exec/0.0.0_AB_MSTR/parked/PARKED_20260911_portal_package_json_overrides_orphan.patch`
(311 bytes, `git -C portal diff -- package.json` at DEV `84a86c10`).

## THE ARTIFACT

`portal/package.json`, working tree only, never staged, never committed. Inside `"overrides"`:

```
-    "lodash": "4.18.1"
+    "lodash": "4.18.1",
+    "baseline-browser-mapping": "latest",
+    "caniuse-lite": "1.0.30001810"
```

## WHAT IS MEASURED, AND WHAT CANNOT BE

| fact | value | instrument |
|---|---|---|
| worktree mtime | 2026-09-11 01:52:39 EDT = **05:52:39Z** | `stat` on the file |
| portal HEAD when found | `DEV 84a86c10` | `git rev-parse` |
| carried by `C:/tmp/wk-dsgn-1e/portal` | NO | grep for the token, 0 hits |
| carried by `.worktrees/d13-visual-elevation/portal` | NO | grep for the token, 0 hits |
| named in any IRPT_FNTEND task order `<paths>` | NO, denominator 18 | `2.0.0_SA_COO~F`'s scan |
| **author** | **STRUCTURALLY UNAVAILABLE** | see below |

⛔ **ATTRIBUTION IS NOT MERELY UNKNOWN HERE, IT IS UNAVAILABLE, AND THE DISTINCTION MATTERS.** An
UNCOMMITTED worktree edit leaves no author anywhere: no commit, no index entry, no hook row, no
audit line. `org/mcp/agent-spawn-audit.log` was read around the mtime and it records message-send
and spawn guard rows, **not worktree writes** -- it cannot answer this question and was the wrong
instrument. The mtime is the only fact, and it survived a full device reboot. **Do not let a later
reader convert this absence into an accusation of whichever seat happened to be live at 05:52Z.**

## THE HAZARD, AND WHY IT IS CURRENTLY HELD

`2.0.0_SA_COO~F` named it exactly: an uncommitted edit in a SHARED checkout has no owner in the
record, so **a later portal commit taken with a broad pathspec sweeps it in silently under whoever's
author line runs.** That is the CLAUDE.md 14b shared-index class, one repo over.

A second, independent defect in the content: **`"latest"` as a pinned override is not a pin.** It
resolves differently on different days, so a build that passes today can fail tomorrow with no diff
to explain it. Whatever is decided about ownership, that value should not survive into a commit as
written.

**WHAT IS HOLDING THE RISK DOWN RIGHT NOW IS THE PORTAL FREEZE, NOT THIS PARK RECORD.** Andrew's
standing word is "nobody does any portal promotes until i say so" -- no DEV push, no gitlink bump.
While no portal commit happens at all, nothing can sweep it. **The hazard re-arms the moment the
freeze lifts**, which is precisely when nobody will be thinking about a seventeen-hour-old
uncommitted edit.

## OWNER AND UN-PARK CONDITION

- **OWNER:** UNASSIGNED. No seat may claim it on the strength of being live at the mtime, and no
  seat may discard it -- `0.0.0_AB_MSTR` did not revert, clean, stash or commit it, and it sits in
  the worktree exactly as found.
- **UN-PARK CONDITION:** the moment Andrew lifts the portal freeze, and **BEFORE** any portal commit
  taken with a pathspec broad enough to include `package.json`. At that point it is a one-line call:
  adopt it under a named owner with `latest` replaced by a real pin, or discard it and restore the
  patch from the file above if it turns out to have been wanted.
- **NOT A BLOCKER** for IRPT_FNTEND round 2: `2.0.0_SA_COO~F`'s workers commit narrow pathspecs from
  their own worktree pairs and cannot sweep it.

Nothing here is lost if the answer is "discard" -- the patch is preserved in this directory and the
restore is one `git apply`.
