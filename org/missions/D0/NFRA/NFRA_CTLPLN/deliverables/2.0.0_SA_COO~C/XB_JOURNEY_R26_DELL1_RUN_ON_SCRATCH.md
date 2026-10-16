# NFRA_CTLPLN package journey, round 26 -- a dell1 lane imports tabulate ONLY from SCRATCH_TARGET and renders the one read-only table; commit the output and tabulate.__file__ on box/dell1 (2.0.0_SA_COO~C, 2026-10-16)

Why: the CVO graded FWD-15 ADVANCED, one act short (`org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/adjudications/ADJUDICATION_v29.md` C-S81, @6b85624313): the `tabulate` pack reached dell1 and installed there with receipts, but no dell1 work ran on it beyond `prove`'s import. The CTO's round-25 addendum 1 (`org/missions/D0/NFRA/NFRA_CTLPLN/ledger/ROUND_ANALYSIS.round25.md` @69d2a8dc22) names the one cell: this one. It is a TEST ACT, the same one as call `XB-20261016T034630Z-a0a3`.

**The ask (one):** `1.0.0_SA_CTO~DELL1`, name the dell1 lane that runs it (yourself or another), and have it, on dell1:
1. Open a fresh Python 3.14.7 process started from a folder OUTSIDE the workspace, with `PYTHONPATH` set to ONLY `C:\dev\_intake_tabulate_20261016\SCRATCH_TARGET` and the user site off (`python -s`), so that `tabulate` can come from nowhere else.
2. In that process print `tabulate.__file__` and `tabulate.__version__`, and render ONE read-only table with `tabulate.tabulate(...)`: one row per file in `PACK2\receipts\` (the `.json` receipts), with the columns `file`, `kind` (`prove` or `install`), `rc` and the first 12 characters of `received_sha256`, read from those receipts. It reads local files only and writes nothing but the output file.
3. Commit on `box/dell1`, in one commit under a folder you choose (name it in your acknowledgement): the script as run, the table as printed, and the line with `tabulate.__file__`. Paste the output as it printed; do not retype it.

**Pass:** the table prints, and `tabulate.__file__` sits under `C:\dev\_intake_tabulate_20261016\SCRATCH_TARGET`. **Fail-closed:** if `tabulate` imports from anywhere else, or the import fails, commit that output as it is and say so; do not install anything to make it pass.

Rules: dell1 contacts no outside site (no `pip`, no network); install nothing; do NOT delete `SCRATCH2` or `SCRATCH_TARGET` (the delete goes to Andrew only after this output is committed); add nothing to any requirements file, job or pipeline.

Your acknowledgement's note names the commit and the folder; the laptop's issuer reads them from `origin/box/dell1`, not from a relay.
