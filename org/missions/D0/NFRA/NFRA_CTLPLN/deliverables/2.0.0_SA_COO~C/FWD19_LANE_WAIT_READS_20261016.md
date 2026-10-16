# NFRA_CTLPLN round 27 -- FWD-19's lane-wait clause: the three reads, taken while lane 2.0.0_SA_COO~C is WAITING on toml==0.10.2 (issuer 2.0.0_SA_COO~C, 2026-10-16 05:03Z)

PRD FWD-19 ACCEPT (line 220): "a lane that needs a package not yet delivered loses that one piece of work, keeps going elsewhere, and its wait shows in the same place he sees every box's open decisions; nothing here watches or sends him anything on its own." This is a TEST ACT, stated as one in the request, in the decision-list call and in the CTO's round-26 analysis (`ledger/ROUND_ANALYSIS.round26.md` section 3 item 2). The CTO holds his decision until these reads are committed (msg 109604).

**The waiting piece of work:** one read-only parse of a TOML file for a read-out; it needs `toml==0.10.2`, which `requirements.txt` does not name (98 lines; `toml` absent) and the intake register read UNKNOWN for. The lane did not touch the package and installed nothing.

## Read 1 -- the intake status verb (the request, as filed at 04:51:08Z; record `org/devices/intake/requests/REQ-20261016T045108Z-toml.json` @ebf864697e)

Run 2026-10-16T05:03:16Z: `python org/devices/intake/intake_request.py status --name toml --version 0.10.2`

```
PACKAGE toml==0.10.2 REQUESTED by=- at=- reason=-
```

## Read 2 -- the one decision list

Run 2026-10-16 ~05:03Z. Local (`python .tools/open-calls.py list`) and the cloud union (`python .tools/open-calls.py list --cloud`) both show the call, as printed (cut at the width shown):

```
laptop-20261016T045125Z-66e3 [OPEN] fork NFRA_CTLPLN | Decide REQ-20261016T045108Z-toml (toml==0.10.2): approve it, or refuse it so lane 2.0.0_SA_COO~C drops its one waiting piece of work (FWD-19 test act) | scope=CROSS-BOX risk=SERVED | asked_by 2.0.0_SA_COO~C
cloud: laptop-20261016T045125Z-66e3 [OPEN] fork opened 2026-10-16T04:51:25Z (age 0h11m) | ... scope=CROSS-BOX
```

## Read 3 -- the lane's own broker summary

`get_agent_status("2.0.0_SA_COO~C")` at 05:03Z, "Working on" line, as printed:

```
WORKING: NFRA_CTLPLN round 27; ~129 on CT-aq-1 (pack to site Z); FWD-11 drill answered by dell1 (restart of COO~C1 at 05:15Z, before-state read). WAITING (FWD-19): toml REQ REQUESTED, call 66e3 OPEN
```

## The lane keeps going elsewhere (its own commits made during the wait, after the request at 04:51:08Z)

Read from `git log --since=2026-10-16T04:51:08Z --author=2.0.0_SA_COO~C`, times as printed (US Eastern offset -04:00):
- `ebf864697e` 00:52:54-04:00 -- the FWD-11 restart-drill body and the toml request record;
- `ec96fc28dd` 00:53:39-04:00 -- the FWD-11 call `XB-20261016T045259Z-fbfa` to dell1;
- `e30e5b6c8d` 00:57:50-04:00 -- the from-side close of `XB-20261016T042748Z-779c`.

None of them reads or installs `toml`.

## What these reads do not show

That the decision list is read by Andrew himself (FWD-12's arm); that the REFUSED outcome has happened (the decision is the CTO's, held until this record exists); and any lane on another box (this is one laptop lane). Nothing here watches or sends anyone anything: each read was a command run by the issuer.
