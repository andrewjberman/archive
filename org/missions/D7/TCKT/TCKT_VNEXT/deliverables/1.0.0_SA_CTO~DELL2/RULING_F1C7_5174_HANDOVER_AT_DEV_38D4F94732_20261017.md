# RULING f1c7 -- 5174 handed over for TO-R20-RV at DEV 38d4f94732

- **Seat:** `1.0.0_SA_CTO~DELL2`.
- **Date:** 2026-10-17, ~07:0xZ.
- **Row:** dell2-20261017T065843Z-f1c7 (TCKT_VNEXT, OWN-BOX).
- **REC:** 2.0.0_SA_COO~V2's.

## Ruling

5174 is handed over to the R20-RV applier.

**The served sha is origin/DEV `38d4f9473284a585bc217981213b9516e29d3a87`.** I read it at 07:0xZ, and the DEV head equals it. It contains:
- `6cdd0bfd` (R20-pt-1);
- `4d4dc68cae`;
- `8ecad4a5fb` (the revision fix);
- `c6e65bde76` (the Performance set, f1bb).

The ancestry was checked by `merge-base --is-ancestor`, all five reading "in".

**Served by:** the worktree `C:/dev/smoke-template-5174`, detached at that sha. `bun install --frozen-lockfile` ran first. Vite 7.3.5 runs on `--port 5174 --strictPort`, and the server answered HTTP 200.

## Order of use

1. TO-R20-RV runs first.
2. Then FWD-1 window 5, whose DEV floor is now 8ecad4a5fb or later (msg to `~Y2`). That leaves the server's sha valid for window 5 too, inside its weekday band.

## Andrew's use

Andrew may view the Performance tab on the same server at any time. A read-only view does not disturb the run.

**Before the run:** the applier names any change to the server, such as a restart or a different sha. The served sha does not move while R20-RV is open.
