"""ETFS_RIVALS.TO-APPLY-R28-aw1 -- read AMENDMENT 1's conditions (a) and (b) in one invocation.

(a) the five rivalfunds Lambdas' runs of the 11:00Z chain have EACH logged a REPORT line
    (print each REPORT line whole);
(b) no REPORT shows Duration above 720,000 ms, and no run of the chain logged `Status: timeout`,
    a `Task timed out`, or an unhandled error.

Read-only. Exits 0 only when BOTH hold for all five functions; anything else is a STOP whose
reason is printed. The order's instruction on a STOP is to apply nothing and name the condition.

INSTRUMENT NOTES, because each of these has bitten this estate:
  - filter-log-events is PAGINATED. This auto-paginates with nextToken and counts client-side;
    it never reads a page as the answer.
  - "could not read the log group" and "read it, found no REPORT" are DIFFERENT outcomes and are
    reported separately. A zero that cannot say what it looked through is not an absence.
  - every bound is epoch MILLISECONDS in UTC, computed from an explicit UTC datetime. No literal
    `Z` is ever typed into a date format string.
  - the chain's entry schedule is EventBridge SCHEDULER (not a Rule) named etfs-rivalfunds-daily,
    cron(0 7 ? * MON-FRI *) in America/New_York -- so 11:00Z is a DST-DEPENDENT rendering of
    07:00 ET, true in EDT and 12:00Z in EST. The window is passed in rather than assumed.
  - that schedule targets fetch-holdings-lambda, while etfs-rivalfunds-sweep-daily (09:00 ET =
    13:00Z) targets daily-lambda. The names are counterintuitive; do not infer which fire a log
    line belongs to from the function name.

Usage:
  python aw1_window_conditions_ab.py <since-utc ISO, e.g. 2026-10-09T10:55:00> [<until-utc ISO>]
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import sys

# `.tools/aws` is an MSYS shell script, so a bare subprocess.run of it dies
# FileNotFoundError [WinError 2] -- CreateProcess cannot execute it. CLAUDE.md names the remedy:
# "Python spawning ANY MSYS binary -> .tools/msys_argv_guard.py msys_safe_run()". Measured here
# before this file was committed, not discovered inside the apply window.
# Found by walking UP to the directory that holds `.tools`, never by counting parents: a
# parents[N] index is silently wrong the moment this file moves, and it is also the kind of
# device-specific assumption LD-0405 forbids. DERIVE, do not hardcode.
def _find_tools() -> pathlib.Path:
    for d in pathlib.Path(__file__).resolve().parents:
        if (d / ".tools" / "msys_argv_guard.py").is_file():
            return d / ".tools"
    raise RuntimeError("could not locate .tools/ above %s" % __file__)


_TOOLS = _find_tools()
sys.path.insert(0, str(_TOOLS))
from msys_argv_guard import msys_safe_run  # noqa: E402

FUNCTIONS = (
    "etfs-rivalfunds-daily-lambda",
    "etfs-rivalfunds-fetch-holdings-lambda",
    "rivalfunds-build-canonical-shape-lambda",
    "rivalfunds-build-silver-lambda",
    "rivalfunds-publish-page-lambda",
)
DURATION_CAP_MS = 720_000.0
FAILURE_MARKERS = ("Task timed out", "Status: timeout", "errorType", "Unhandled",
                   "UnhandledException", "Runtime exited")


def epoch_ms(iso: str) -> int:
    dt = datetime.datetime.fromisoformat(iso).replace(tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() * 1000)


def aws_json(args: list[str]) -> dict:
    """One AWS call through the estate's MSYS guard. stderr is surfaced; a failure is RAISED,
    never silently read as an empty result -- the caller must be able to tell "could not read"
    from "read it, found nothing"."""
    env = {**os.environ, "MSYS_NO_PATHCONV": "1"}  # ARN/path args must not be mangled
    r = msys_safe_run([str(_TOOLS / "aws"), *args], capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError("aws %s -> rc=%d: %s" % (args[0], r.returncode, (r.stderr or "").strip()[:300]))
    return json.loads(r.stdout or "{}")


def filter_all(group: str, start_ms: int, end_ms: int, pattern: str) -> list[dict]:
    """Every matching event across EVERY page -- nextToken followed to exhaustion."""
    events: list[dict] = []
    token = None
    pages = 0
    while True:
        args = ["logs", "filter-log-events", "--log-group-name", group,
                "--start-time", str(start_ms), "--end-time", str(end_ms),
                "--filter-pattern", pattern, "--output", "json"]
        if token:
            args += ["--next-token", token]
        out = aws_json(args)
        pages += 1
        events += out.get("events", [])
        token = out.get("nextToken")
        if not token or pages > 50:
            break
    return events


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    since = sys.argv[1]
    until = sys.argv[2] if len(sys.argv) > 2 else datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    s_ms, e_ms = epoch_ms(since), epoch_ms(until)
    print("WINDOW READ: %s .. %s UTC (epoch ms %d .. %d)" % (since, until, s_ms, e_ms))
    print("DENOMINATOR: %d function(s) the chain invokes\n" % len(FUNCTIONS))

    with_report, without_report, unreadable = [], [], []
    breaches, failures = [], []

    for fn in FUNCTIONS:
        group = "/aws/lambda/%s" % fn
        print("--- %s" % fn)
        try:
            reports = filter_all(group, s_ms, e_ms, "REPORT")
        except RuntimeError as exc:
            unreadable.append((fn, str(exc)))
            print("  COULD NOT READ -- not an absence: %s" % exc)
            continue

        if not reports:
            without_report.append(fn)
            print("  READ the group, found 0 REPORT line(s) in the window -- condition (a) NOT met here")
        else:
            with_report.append(fn)
            for ev in reports:
                line = ev.get("message", "").rstrip()
                print("  %s" % line)
                for tok in line.split():
                    pass
                # Duration is the first "Duration: <n> ms" field of a REPORT line
                m = line.split("Duration:")
                if len(m) > 1:
                    try:
                        dur = float(m[1].split()[0])
                        if dur > DURATION_CAP_MS:
                            breaches.append((fn, dur))
                    except (ValueError, IndexError):
                        print("    WARN: could not parse a Duration from that REPORT line")

        try:
            bad = filter_all(group, s_ms, e_ms, "?\"Task timed out\" ?\"Status: timeout\" ?errorType ?Unhandled")
        except RuntimeError as exc:
            unreadable.append((fn, "failure sweep: %s" % exc))
            print("  FAILURE SWEEP COULD NOT READ: %s" % exc)
            continue
        for ev in bad:
            msg = ev.get("message", "").rstrip()
            if any(k in msg for k in FAILURE_MARKERS):
                failures.append((fn, msg[:200]))
                print("  FAILURE MARKER: %s" % msg[:200])
        print()

    print("=" * 72)
    print("(a) REPORT line present : %d of %d function(s)" % (len(with_report), len(FUNCTIONS)))
    if without_report:
        print("    MISSING on          : %s" % ", ".join(without_report))
    if unreadable:
        print("    UNREADABLE (not an absence) : %s" % ", ".join(f for f, _ in unreadable))
    print("(b) Duration > %.0f ms   : %d breach(es)%s"
          % (DURATION_CAP_MS, len(breaches),
             (" -- " + ", ".join("%s %.0fms" % b for b in breaches)) if breaches else ""))
    print("    failure markers     : %d" % len(failures))

    ok = (len(with_report) == len(FUNCTIONS) and not unreadable
          and not breaches and not failures)
    print()
    if ok:
        print("CONDITIONS (a) AND (b): BOTH MET. (c) is the clock and (d) is the re-plan -- read those next.")
    else:
        print("STOP. Conditions (a)/(b) are NOT both met. Apply NOTHING; name the failing condition in "
              "the report section and commit it.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
