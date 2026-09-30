"""IB-pr-193 AC1 -- a refused async replay logs stage REFUSED, never FAILED (its pointer did not change).

Usage: python p19_3_ac1_async_log.py <worktree root>
Arm A: run_async_submit on an event whose submit_async.run raises AsyncSubmitRefused prints one irpt_export_async
line with stage "REFUSED" and re-raises the same exception.
Arm B (control): an ExportBuildFailed from submit_async.run still prints stage "FAILED" and re-raises.
"""
import contextlib
import io
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
export = root / "infra/aws/lambda/investor-reporting/export"
for path in (export, export.parent, export.parent / "_authz", export.parent / "_ids", export.parent / "reports",
             root / "lib"):
    sys.path.insert(0, str(path))
import entry  # noqa: E402
import submit_async  # noqa: E402

ok = True


def arm(exc, want):
    global ok
    original = submit_async.run
    submit_async.run = lambda event, **kw: (_ for _ in ()).throw(exc)
    buf = io.StringIO()
    raised = None
    try:
        with contextlib.redirect_stdout(buf):
            entry.run_async_submit({submit_async.MARKER: {"export_revision": "exr_check"}})
    except Exception as err:
        raised = err
    finally:
        submit_async.run = original
    stages = [json.loads(line)["irpt_export_async"]["stage"] for line in buf.getvalue().splitlines()
              if line.startswith("{") and "irpt_export_async" in line]
    good = stages == [want] and raised is exc
    print("%s %s: stages %r, re-raised %s" % ("PASS" if good else "FAIL", type(exc).__name__, stages, raised is exc))
    ok = ok and good


arm(submit_async.AsyncSubmitRefused("no BUILDING pointer for this revision; the async leg runs once"), "REFUSED")
arm(submit_async.ExportBuildFailed("build failed"), "FAILED")
if ok:
    print("P19-3-AC1 PASS")
else:
    print("P19-3-AC1 FAIL")
sys.exit(0 if ok else 1)
