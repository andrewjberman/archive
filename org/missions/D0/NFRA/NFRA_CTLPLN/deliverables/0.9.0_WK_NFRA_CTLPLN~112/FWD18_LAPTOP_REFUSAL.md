# FWD-18 laptop arm -- a download tried on purpose is stopped and told the route that works

Run once, in the worktree `C:/Users/AndrewBerman/Desktop/ajb_wk/ctlpln-112` (branch `wk-NFRA_CTLPLN-112`), from its root.

Command (the kit at its own path, environment `PIP_NO_INDEX=1` set on the child):

    PIP_NO_INDEX=1 python org/devices/kit_pip_no_egress.py wrap -- download six

Exit code: `3` (the kit's `REFUSED_RC`).

Printed stdout: empty (0 bytes).

Printed stderr, verbatim (one line, 123 bytes including the newline):

    REFUSED: this box does not download. Ask the laptop: org/devices/intake/ (request, check, Taildrop). No request was made.

Does the refusal name the route that works? Yes. It names `org/devices/intake/`, the folder that holds request, check and Taildrop.

Why no request was made: `wrap` calls `classify()` on the pip arguments before it starts any process. The verb `download` is in `DOWNLOAD_VERBS` and carries no `--no-index`, so `classify()` returns REFUSE with the fixed REFUSAL string, and `wrap` returns 3 without running `python -m pip`. `PIP_NO_INDEX=1` is the second guard in the child environment; this path never starts pip, so the guard is not exercised here. The same refusal, with zero connections to a counting loopback listener, is also asserted by `.tools/tests/test_round20_fetch_device.py --wrapper`.

Limit (from the kit's own docstring): the wrapper is bypassed by anyone who types a different interpreter or calls pip without it. The real control is a network egress policy, which is outside this cell.
