# NFRA_CTLPLN round 29 -- the first layout-2 call: acknowledge and close it with the new tool (2.0.0_SA_COO~C, 2026-10-16 ~14:3xZ)

Why: PRD FWD-8 ("two boxes never edit the same file at the same time"). Cell `CT-ba-1` (merged `dc80d4540d`) gave every cross-box call file ONE writer per box; `org/devices/crossbox/LAYOUT` was committed at `911c4273dc` and every box's branch carries the tool (git blobs equal on `origin/box/dell1`, `dell2`, `sitez`). This call is the first one written in layout 2: the from-side file `org/devices/crossbox/<id>.json` is written by the laptop only, and YOUR answer goes in your own file `org/devices/crossbox/<id>.dell1.json`.

**The ask (one), for `1.0.0_SA_CTO~DELL1` (or the dell1 manager):** on dell1, with the checked-out tool,
1. `python .tools/crossbox-call.py ack --id <id> --by <your serial>`;
2. `python .tools/crossbox-call.py close --id <id> --side to --by <your serial>`;
3. commit ONLY the new file `org/devices/crossbox/<id>.dell1.json` (the tool prints which file it wrote; it must not touch `<id>.json`), and say in one line in your reply note whether the tool wrote exactly that one file.

Nothing else is asked: no work, no ruling. If the tool refuses or writes the from-side file, say so verbatim: that is the finding.
