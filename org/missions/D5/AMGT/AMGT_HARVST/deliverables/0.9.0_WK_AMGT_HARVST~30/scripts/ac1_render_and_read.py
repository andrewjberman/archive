#!/usr/bin/env python
"""AC1 -- HVST-y-3: render the TimelinePanel on the validation security's page, on PORT 5174
ONLY, and print everything a human then reads the screenshot against.

WHAT THIS SCRIPT DOES:
  1. Builds a CONSTRUCTED overlay fixture + a dense timeline-range fixture (2026-01-01 through a
     fixed last day, one row per day, no gap) for the validation security (`992_HK_Equity`,
     Lenovo -- spec section 8's own validation security; this is a rendering proof over
     constructed data, not the round's live-data judgment criterion, which is HVST-y-1's).
  2. Starts `bun run dev --port 5174 --strictPort --host 127.0.0.1` from the portal checkout
     (unless something is already answering on 5174 -- then it is reused, never killed, since it
     may be a sibling worker's live server on the same shared tree).
  3. Runs the portal's own canonical render instrument, `scripts/ui-smoke.mjs`, against
     `/security-analysis/992_HK_Equity` with those fixtures, `--strict`, and `--expect-text`
     assertions on the rendered day-count-vs-denominator caption and the first/last day.
  4. Independently recomputes the expected day count (days between the fixture's own
     `floor_date` and its last day, inclusive) in Python and compares it to the number of
     series rows the fixture itself carries -- the two are asserted equal BEFORE the render even
     runs (a fixture-construction self-check), and ui-smoke's own --expect-text assertions
     re-confirm the SAME equality was what actually rendered.
  5. Saves the screenshot under this cell's deliverables directory. The worker then reads that
     PNG with the Read tool and states what is visible -- this script prints the numbers; it does
     not substitute for that read (task order section 4, AC1).

If any step cannot run, this prints which step failed and its error text and exits non-zero --
it never falls back to a unit test.
"""
import datetime
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "..", ".."))
PORTAL_DIR = os.path.join(WORKSPACE_ROOT, "portal")
DELIVERABLES_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(DELIVERABLES_DIR, "scripts")
FIXTURES_PATH = os.path.join(SCRIPTS_DIR, "ac1_fixtures.generated.json")
SCREENSHOT_PATH = os.path.join(DELIVERABLES_DIR, "ac1_header_region.png")
PORT = 5174
SECURITY_KEY = "992_HK_Equity"
ROUTE = f"security-analysis/{SECURITY_KEY}"
FLOOR_DATE = "2026-01-01"
LAST_DAY = "2026-09-27"  # T-1 of today (2026-09-28) -- inside the trading-calendar frontier, not itself a claim about a real landed row.

# Days that carry PARTIAL / DENIED, scattered through the range so the dense-vs-marked contrast
# is visible in one screenshot. Every other day in range is COMPLETE.
PARTIAL_DAYS = {"2026-03-12", "2026-05-04", "2026-07-19"}
DENIED_DAYS = {"2026-02-20", "2026-06-08"}


def daterange_inclusive(start_iso, end_iso):
    start = datetime.date.fromisoformat(start_iso)
    end = datetime.date.fromisoformat(end_iso)
    days = []
    d = start
    while d <= end:
        days.append(d.isoformat())
        d += datetime.timedelta(days=1)
    return days


def build_series():
    days = daterange_inclusive(FLOOR_DATE, LAST_DAY)
    series = []
    for i, day in enumerate(days):
        status = "PARTIAL" if day in PARTIAL_DAYS else "DENIED" if day in DENIED_DAYS else "COMPLETE"
        # A gentle wave plus a few spikes, deterministic (no randomness) -- some real zero
        # (quiet) COMPLETE days included on purpose (i % 11 == 0), same as a genuinely quiet run.
        base = 0 if i % 11 == 0 else (i * 7) % 23
        spike = 40 if i % 53 == 0 else 0
        score = 0 if status != "COMPLETE" and base == 0 else base + spike
        articles = 0 if score == 0 else max(1, score // 5)
        series.append({
            "date": day,
            "mention_score": score,
            "articles_total": articles,
            "tier_a": articles // 4,
            "tier_b": articles // 4,
            "tier_c": articles // 4,
            "tier_d": articles - 3 * (articles // 4),
            "mention_count_total": articles,
            "publishers_distinct": min(articles, 3),
            "trailing_7d_sum": score,
            "trailing_30d_sum": score,
            "cumulative_ytd": score,
            "data_status": status,
            "breakout_ratio": None,
            "z_score": None,
        })
    return series, days


def build_overlay_fixture():
    return {
        "security_key": SECURITY_KEY,
        "identity": {
            "security_key": SECURITY_KEY,
            "identity_status": "MEASURED",
            "crosswalk_vintage": "2026-09-15",
            "display_ticker": "992 HK",
            "bloomberg": "992 HK",
            "requested": SECURITY_KEY,
            "identity_basis": "crosswalk/v1",
            "company_name": "Lenovo Group Ltd",
        },
        "header_figures": [],
        "description": {
            "status": "SERVED",
            "source": "D-1 drafting/v1 company_description sentence 1",
            "marked": "machine",
            "text": "Lenovo Group is a China-domiciled technology company (AC1 constructed fixture).",
            "field": "sections[company_description].sentences[0]",
            "generated": True,
            "evidence": ["P0000"],
            "verbatim_check": "PASS",
            "header_scalars_measured": [],
            "reason": None,
        },
        "feed": {
            "items": [
                {
                    "article_key": "A1", "publisher": "Reuters", "published_at": "2026-09-27T10:00:00Z",
                    "url": "https://example.test/a1", "title": "AC1 constructed feed item 1",
                },
                {
                    "article_key": "A2", "publisher": "Bloomberg", "published_at": "2026-09-26T09:00:00Z",
                    "url": "https://example.test/a2", "title": "AC1 constructed feed item 2",
                },
            ],
            "item_count": 2,
            "order": "newest first by published_at (P-1's own order)",
            "most_discussed_basis": "ABSENT -- P-1 carries no discussion count",
            "coverage_status": "SERVED",
            "store_item_count": 2,
            "states": {"missing_body": 0, "malformed": 0, "denied": 0, "partial": 0},
            "complete": True,
            "key_forms": [],
            "window": {"start_date": "2026-08-28", "end_date": "2026-09-27", "days": 30},
            "reason": None,
            "source": "AC1 constructed fixture",
            "social": {"status": "not stated by the server", "items": []},
        },
        "posture": {"status": "ABSENT", "security_key": SECURITY_KEY, "reason": "AC1 fixture carries no posture", "posture_read": None},
        "axis_reads": [],
        "chatter": None,
        "price": None,
        "peers": None,
        "bloomberg_session_state": "UNKNOWN",
    }


def main():
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    series, days = build_series()
    expected_denominator = len(daterange_inclusive(FLOOR_DATE, LAST_DAY))
    rendered_day_count = len(series)
    print(f"STEP 1 -- fixture construction: {rendered_day_count} series rows for range {FLOOR_DATE}..{LAST_DAY}")
    print(f"STEP 1 -- independent denominator (days between {FLOOR_DATE} and {LAST_DAY} inclusive): {expected_denominator}")
    if rendered_day_count != expected_denominator:
        print(f"FAIL: fixture is not dense -- {rendered_day_count} rows != {expected_denominator} denominator")
        sys.exit(1)
    print("STEP 1 -- PASS: fixture day count equals the days-in-range denominator (no gap), before the render even runs.")

    overlay = build_overlay_fixture()
    timeline_range = {
        "security_key": SECURITY_KEY,
        "floor_date": FLOOR_DATE,
        "series": series,
        "events": [],
    }
    # AC1 does not click a day, so no day-dissection fixture is declared -- a declared-but-never-
    # hit fixture would fail ui-smoke's own --strict FIXTURES-MATCH check, and AC1's own two
    # routes (overlay, timeline range) are the only ones this render exercises.
    fixtures = {
        f"/security/{SECURITY_KEY}/overlay": overlay,
        f"/security/{SECURITY_KEY}/timeline": timeline_range,
    }
    with open(FIXTURES_PATH, "w", encoding="utf-8") as f:
        json.dump(fixtures, f)
    print(f"STEP 2 -- wrote fixtures: {FIXTURES_PATH}")

    started_server = False
    proc = None
    if not port_answers(PORT):
        print(f"STEP 3 -- nothing answering on {PORT}, starting bun dev server")
        try:
            proc = subprocess.Popen(
                ["bun", "run", "dev", "--port", str(PORT), "--strictPort", "--host", "127.0.0.1"],
                cwd=PORTAL_DIR,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            )
        except FileNotFoundError as exc:
            print(f"FAIL at STEP 3 (start bun dev server): {exc}")
            sys.exit(1)
        started_server = True
        deadline = time.time() + 60
        while time.time() < deadline:
            if port_answers(PORT):
                break
            if proc.poll() is not None:
                out = proc.stdout.read() if proc.stdout else ""
                print(f"FAIL at STEP 3 (bun dev server exited early, rc={proc.returncode}):\n{out[-2000:]}")
                sys.exit(1)
            time.sleep(1)
        else:
            print(f"FAIL at STEP 3: port {PORT} never answered within 60s")
            if proc:
                proc.terminate()
            sys.exit(1)
        print(f"STEP 3 -- PASS: dev server answering on {PORT}")
    else:
        print(f"STEP 3 -- port {PORT} already answering (reusing an existing server, not started by this run)")

    try:
        cmd = [
            "node", "scripts/ui-smoke.mjs", ROUTE, SCREENSHOT_PATH,
            "--port", str(PORT),
            "--fixtures", FIXTURES_PATH,
            "--wait", "4500",
            "--expect", '[data-timeline-panel="SERVED"]',
            "--expect", "[data-header-feed]",
            "--expect-text", f"[data-timeline-first-day]::{FLOOR_DATE}",
            "--expect-text", f"[data-timeline-last-day]::{LAST_DAY}",
            "--expect-text", "[data-timeline-day-count-caption]::no gap",
            "--expect-text", f"[data-timeline-day-count-caption]::{rendered_day_count} of {expected_denominator}",
            "--strict",
        ]
        print("STEP 4 -- running:", " ".join(cmd))
        result = subprocess.run(cmd, cwd=PORTAL_DIR, capture_output=True, text=True, timeout=180)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"STEP 4 -- ui-smoke.mjs exit code: {result.returncode}")
    except subprocess.TimeoutExpired as exc:
        print(f"FAIL at STEP 4 (ui-smoke.mjs timed out): {exc}")
        sys.exit(1)
    finally:
        if started_server and proc is not None:
            # `bun run dev` execs vite as a CHILD process; Popen.terminate() on Windows signals
            # only the immediate process and leaves the vite grandchild bound to the port (measured
            # this run -- a bare terminate() left node.exe still LISTENING on 5174 after "PASS").
            # taskkill /T kills the whole tree.
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, text=True)
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass
            print("STEP 5 -- dev server process tree (started by this run) terminated (taskkill /T /F)")

    print(f"RENDERED_DAY_COUNT={rendered_day_count} DENOMINATOR={expected_denominator} EQUAL={rendered_day_count == expected_denominator}")
    print(f"SCREENSHOT={SCREENSHOT_PATH}")
    print("NEXT: the worker reads SCREENSHOT with the Read tool and states what is visible (AC1's own requirement).")
    sys.exit(0 if result.returncode == 0 else 1)


def port_answers(port):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2)
        return True
    except urllib.error.URLError:
        return False
    except Exception:
        return False


if __name__ == "__main__":
    main()
