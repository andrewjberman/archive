# NFRA_CTLPLN FWD-18 -- one blocked download tried on purpose on site Z (2.0.0_SA_COO~C, 2026-10-15)

PRD FWD-18: a download tried on purpose is stopped on a Dell and on site Z and the person is told the route that works. dell1 has stopped one (PIP_NO_INDEX=1, no route named); site Z is untried (CVO re-grade 2026-10-13).

**The ask (one):** `0.0.0_AB_MSTR~Z`, on site Z run once, from any scratch folder, `python org/devices/kit_pip_no_egress.py wrap -- download six` (the kit is in the repository after a pull; it refuses before any network request), and put the printed refusal, its exit code and the time in the note of your acknowledgement. Do not install or change anything on site Z; if the kit would reach the network, do not run it and say so.
