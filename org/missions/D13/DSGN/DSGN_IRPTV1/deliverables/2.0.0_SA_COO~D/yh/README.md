# Y-H -- the page-walk submit harness (1.0.0_SA_CTO batch 178)

`yh-submit-case.mjs` uploads and submits ONE named case from the Investor Reporting Analysis tab on the local dev build
(port 5174), as a person would. It writes a packet to `tmp/yh-submit/<stamp>-<case>/` (gitignored):
- `packet.json`: case, file sha256 prefix, ids, marks, outcome;
- `page.har`: every API hop, with response content;
- `guard.tsv`: every write the guard aborted;
- screenshots.

The backend join is 2.0.0_SA_COO~Y's:

```
python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/live_walk/backend_join.py <packet>/page.har <packet>/join.json [--journal]
```

## Cases (brief 2 section 4; files in the laptop's Downloads, found by sha256 prefix)

| Case | sha256 prefix | Variant | Expected today |
|---|---|---|---|
| A | 500837992a3b9caa | Overview | READY. HELD: row S279 (a fund ticker fails the upload) until ~Y's fix serves (CTO 104395) |
| typo | 87afdc7db1c58b38 | Overview | NEEDS_CORRECTION (Y-B baseline) |
| D | f0d344fa967504bd | Overview | NEEDS_CORRECTION (Y-B baseline) |
| B, C | 500837992a3b9caa | Comparison / Multi-Comp | refused by the script until brief 2 items 2.1 (and 2.3 for C) land |

## Safety

- Same dormant UI-walker account as `/ui-walk`. It is armed for one run and disarmed in `finally`. The password is read
  in-process and never printed.
- The network guard admits, beyond reads and the walker's own admitted POSTs:
  - the upload re-posts (`POST .../analysis/inputs`, cap 60);
  - ONE submission (`POST .../analysis`).
- Every other write is aborted and logged.
- A live run refuses without `--queue-empty`, the operator's assertion of the solo gate: one job at a time, queue empty,
  nobody signed in to YCharts in a browser (brief 2 section 5.4; the vendor ruling "Yes one at a time with queue
  empty").
- `--fixture` runs the same page drive offline. Both POSTs are answered from the committed producer upload records
  (`portal/.../__tests__/mvp-upload/tests/producer-upload.json`). There is no account and no backend write.

## Proven (2026-10-02, offline)

`--case A --fixture` on portal DEV 16c6690e:
- upload answered NORMALIZED (UP- id captured);
- one submission answered (REQ id captured);
- posts inputs 1 / submissions 1; 0 guard aborts;
- the HAR held 49 hops with content.

`backend_join.py` read the HAR: every hop mapped to its route and Lambda and the UP- id was found. No invocation matched,
as expected for a fixture run. The refusals hold: a live run without `--queue-empty`, and case B.
