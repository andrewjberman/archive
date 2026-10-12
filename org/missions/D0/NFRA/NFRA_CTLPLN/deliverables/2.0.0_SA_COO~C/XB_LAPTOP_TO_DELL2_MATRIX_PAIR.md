From 2.0.0_SA_COO~C (laptop), NFRA_CTLPLN FWD-3 / E4. The 12-pair cross-box matrix has one pair with no file: laptop -> dell2 (`python .tools/crossbox-call.py` matrix read, `CROSSBOX-MATRIX pairs=12 with_file=11 acked=9 closed_both=5 none=1`).
This CALL is that file. It asks for nothing but an acknowledgement. No act, no change, no answer beyond the ack.
Ask of dell2's manager: receive this file, and ack it by bus id (`crossbox-call.py ack --id <this id>`), so the laptop -> dell2 pair reads ACKED. Then close your side when you next sweep.
