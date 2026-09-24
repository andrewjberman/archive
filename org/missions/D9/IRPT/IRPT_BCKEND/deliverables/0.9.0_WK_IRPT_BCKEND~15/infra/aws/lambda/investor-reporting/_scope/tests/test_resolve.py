"""WRAPPER, NOT a second test file. See row IRPT_BCKEND-W15-S3.

Exists ONLY so this cell's criterion (R117-AC2) invocation --
`cd deliverables/0.9.0_WK_IRPT_BCKEND~15 && py -3.12 -m pytest
test_render_delegate_resolver_enforcer.py -v && py -3.12 -m pytest
infra/aws/lambda/investor-reporting/_scope/tests/test_resolve.py -v` -- resolves to a real
file on its SECOND leg. Bash does not reset the working directory between `&&`-joined
commands, so once the first `cd` moves the shell into this deliverable's own directory, the
second leg's RELATIVE path is resolved from THERE, not from the repo root -- meaning a file
literally has to exist at this nested path for the criterion's own invocation string, run
verbatim, to succeed.

THIS IS NOT A COPY OF THE REAL TEST. It loads the ONE real
`infra/aws/lambda/investor-reporting/_scope/tests/test_resolve.py` at its real repo-root-
relative path, by absolute filesystem location (found by walking up from THIS file until that
path exists elsewhere), and re-exports every `test_*` object it defines -- UNCHANGED -- into
this module's namespace, so pytest collects and runs the SAME test functions against the SAME
`_scope/resolve.py` and `_scope/tests/fixtures.py` the real file already imports internally.
BOUNDS forbids editing any existing test's expected value; this file edits nothing -- it
re-executes the real file's own bytes at collection time, live, so a later change to the real
file is picked up automatically and this wrapper can never go stale relative to it.
"""
from __future__ import annotations

import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_THIS_FILE = os.path.normpath(os.path.abspath(__file__))
_TARGET_SUFFIX = os.path.normpath(
    "infra/aws/lambda/investor-reporting/_scope/tests/test_resolve.py")


def _find_real_test_resolve():
    probe = _HERE
    for _ in range(25):
        candidate = os.path.normpath(os.path.join(probe, _TARGET_SUFFIX))
        if os.path.isfile(candidate) and os.path.normpath(candidate) != _THIS_FILE:
            return candidate
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    raise RuntimeError(
        "could not find the real _scope/tests/test_resolve.py walking up from %r -- this "
        "wrapper exists only to satisfy R117-AC2's literal invocation path; see row "
        "IRPT_BCKEND-W15-S3" % _HERE)


_REAL_PATH = _find_real_test_resolve()
_spec = importlib.util.spec_from_file_location("_ib_rtq2_real_test_resolve_wrapped", _REAL_PATH)
_real = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real)

for _name in dir(_real):
    if _name.startswith("test_"):
        globals()[_name] = getattr(_real, _name)
