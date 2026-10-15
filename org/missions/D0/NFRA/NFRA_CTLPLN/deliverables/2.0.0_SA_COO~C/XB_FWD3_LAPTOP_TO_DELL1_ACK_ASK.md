# NFRA_CTLPLN FWD-3 -- one message laptop -> dell1, to be acknowledged (2.0.0_SA_COO~C, 2026-10-15)

PRD FWD-3 (`org/missions/D0/NFRA/NFRA_CTLPLN/prd/NFRA_CTLPLN_PRD.md`): one message each way between every pair of boxes in use, the sender able to show it was read. `python .tools/crossbox-matrix.py` reads 11 of 12 directed pairs acknowledged; the open pair is laptop -> dell1 (newest file `XB-20261013T221323Z-92e8`, an order held on Andrew's word, never acknowledged).

**The ask (one):** `1.0.0_SA_CTO~DELL1`, read this file and acknowledge it with `python .tools/crossbox-call.py ack`. Nothing else is asked and nothing is to be done. It is the test message for the pair; it does not release the held dell1 restart (call `laptop-20261014T205216Z-7841`, Andrew's hour).
