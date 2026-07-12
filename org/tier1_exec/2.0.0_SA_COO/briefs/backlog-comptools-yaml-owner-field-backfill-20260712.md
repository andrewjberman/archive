# tool-hygiene backlog: backfill an `owner:` field for every tool in comp-tools.yaml

**`2.0.0_SA_COO`, 2026-07-12.** *Tool-hygiene backlog (COO-tracked), clusters with `deferred-comp-deadgrant-boto3-conversion-backlog-20260711.md`
+ the gate-dirty sweep (`c972ed2a8`) -- all "tool metadata/hygiene" work. Homed here per `1.0.0_SA_CTO` (`012216Z`)
as the durable single home so it doesn't age out of an MCP note. NON-URGENT.*

---

## THE GAP (surfaced during the comp-routes fix-TO routing, 2026-07-12)

`org/modules/graph/comp-tools.yaml` defines each tool's usage/subcommands but carries **NO `owner:` field**. When
the comp-routes false-`auth:NONE` fix-TO needed routing (`fixTO-comp-routes-false-authnone-on-client-composed-urls-20260712.md`,
`005efdc9e`), the owner could not be pinned from the manifest -- CTO had to **hand-resolve** it (comp-routes backend
= `org/modules/graph/routes_cli.py`, consumed by `pii_cli.py` -> `org/modules/graph` = CTO-gated). **A tool with no
registered owner cannot be routed on autopilot** -- every dispatch to it needs a human to trace the backend to a lane.

## THE TASK

Backfill an `owner:` field for **every** tool in `comp-tools.yaml` (e.g. `comp-routes` -> graph-platform/DE, etc.),
so a fix-TO / dispatch resolves the owner from the manifest, not by hand-tracing the backend module.

- **DATA home:** `comp-tools.yaml` (graph-platform surface) -- **CTO-gated edit** when picked up.
- **TASK tracking:** this backlog entry (COO). Yours-to-track / CTO-to-gate-the-edit; no duplication.
- Consider pairing with `graph-call-manifest.yaml` (CTO's original suggestion) so the two catalogs agree on ownership.
- Ground each owner from the tool's BACKEND module -> lane (as CTO did for routes_cli.py), not from memory; a
  wrong `owner:` is worse than none (mis-routes on autopilot). Cross-check against any lane/CODEOWNERS source.

## PRIORITY / DISPOSITION

NON-URGENT. No correctness/security impact -- it is a routing-convenience/manifest-completeness item; the current
fallback (hand-resolve the backend) works, it just isn't autopilot-routable. Pick up in a capacity window alongside
the other tool-hygiene backlog items. **Opened-not-parked** (a real, if minor, gap -- Andrew's harness-vs-tool law:
tracked with an exit, not indefinitely deferred).

**Attribution:** surfaced by `2.0.0_SA_COO` during the comp-routes fix-TO routing; homed to the COO tool-hygiene
backlog + scoped by `1.0.0_SA_CTO` (`012216Z`).
