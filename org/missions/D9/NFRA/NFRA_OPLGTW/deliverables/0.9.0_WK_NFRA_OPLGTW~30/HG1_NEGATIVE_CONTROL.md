# OG-hg-1 negative control (0.9.0_WK_NFRA_OPLGTW~30)

Method: the pre-change `halt_gate_worker_issuer` is restored by pointing the fixture at the pre-change library:
`git show 2cb25e2cf0:.tools/halt-gate-check.sh > .scratch/old-halt-gate-check.sh` then
`HALT_GATE_LIB="$PWD/.scratch/old-halt-gate-check.sh" bash .tools/halt-gate-worker-order-test.sh` (the fixture's
`HALT_GATE_LIB` override; default is the library beside it).

## Old function, literal output (rc=1)

```
FAIL: case 1 gate rc=3, expected 0 with the issuer named (release tree predates the order)
FAIL: case 2 gate rc=0, expected a refusal for an order whose last tag is complete
PASS: case 3 first tag complete, LAST tag pending is admitted
PASS: case 4 a [STOP] to the issuer halts the worker (rc=2, no override)
```

Case 1 and case 2 FAIL under the old function, as the order requires:
- case 1: the old function reads only `HALT_GATE_REPO_ROOT` HEAD, the release tree holds no order, rc=3 refusal.
- case 2: the release tree carries a copy of the order whose FIRST tag reads `staged`; the old `grep -m1` reads that
  tag and admits (rc=0) an order whose LAST tag is `complete`.

Cases 3 and 4 PASS under the old function only because by then the fixture's release tree carries case 2's order copy
(first tag `staged`), which the old first-tag read admits; they do not discriminate old from new and are not claimed to.
(An earlier fixture draft that left the release tree without the order let case 2 pass under the old function for the
wrong reason, a refusal for absence; it was changed so case 2 fails on the first-tag read itself.)

## New function, literal output (rc=0)

```
PASS: case 1 release tree predates the order; shared-root order admitted, issuer 2.0.0_SA_COO~O named
PASS: case 2 LAST tag complete (earlier tag staged) is not admitted (rc=3)
PASS: case 3 first tag complete, LAST tag pending is admitted
PASS: case 4 a [STOP] to the issuer halts the worker (rc=2, no override)
```
