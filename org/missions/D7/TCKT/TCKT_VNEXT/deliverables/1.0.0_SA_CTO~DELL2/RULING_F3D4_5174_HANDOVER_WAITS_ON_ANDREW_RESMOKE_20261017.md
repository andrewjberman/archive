# Ruling on call dell2-20261017T015850Z-f3d4: the 5174 handover for TO-R20-RV

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~02:1xZ. **RULED: not yet.** Andrew smoked 1f525845 at about 01:02Z and found Cottonwood empty. The
Cottonwood read path is being built, ruled A @6bfcbcf2cc, and he re-smokes when it lands. 5174 is his smoke server, and switching its checkout
during his smoke would show him a different build. So the handover happens at the FIRST of these:
1. Andrew approves row f1bb (or its successor), or says he is done with 5174.
2. Andrew releases 5174 in words.

When either happens, this seat names ONE DEV sha at or past `4d4dc68cae` (it carries R20-pt-1 `6cdd0bfd` and window 5's cell), in the order
TCKT R20-RV and then FWD-1 window 5. After both runs it puts Andrew's smoke copy back if he still needs it. This is a timing ruling only;
nothing about the runs changes.

-- `1.0.0_SA_CTO~DELL2`
