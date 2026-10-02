"""RIV-ps-1 AC1 (ROUND_ANALYSIS.round6.md section 3 item 3, second half): a planted heavy day refuses loudly and keeps
the prior page; a medium day publishes without the holding dialogs. Source: the round-6 page is 1,833,385 B against
the 2,097,152-B gateway cap (`infra/aws/ec2/opal-gateway/app/rivalfunds_view.py:35` MAX_BYTES; the gateway serves the
newest `date=` prefix, `:69`, `:124`). Base ed61068340 already carries both mechanisms:
`publish_page.py:719-721` returns FAILED with the byte count before any write when the page is over MAX_PAGE_BYTES
(`:242`, since 5d9d7bf96e), and `render.py:1433-1443` re-renders without the holding dialogs above DIALOG_SOFT_CAP
1,950,000 (`data-holding-dialogs="off"`, since CRO~RV's layout pass 95af466e67). This check is expected to PASS at
base: a CONTROL, and the item's refusal half is REALIZED by that code, not a cell. Not graded here: the first half
(the trend sparks' 320,789 B of growth moved behind the holding popover, or capped).

Interface: `publish_page.handler_entry(event)` -> {"status", "outputs", "marker", "detail"}; the page at
`homes.page(day, "index.html")`, its manifest at `homes.page(day, "manifest.json")`; a holding dialog is an element
carrying `data-hd`; a page without them carries `data-holding-dialogs="off"`. The cap graded is the gateway's literal
2,097,152 B, not the product constant; the soft cap is read from `render.DIALOG_SOFT_CAP` (the medium plant sits
between the two).

Offline, local sink: the round-5 page fixture (test_p2's TXUE/BASG books, G5 replayed), A1 producer pre-step off, AI
gate unset. Planted A1 tables: holding_contribution, 20 TXUE YTD holdings with 10,000-character names (20 dialogs);
input_census, n missing price rows with ~1,000-character subjects (the byte knob, about 2 KB a row).
  1. 2026-09-29, 10 census rows -> the PRIOR page, published with its dialogs;
  2. 2026-09-30, 1,500 rows (about 3 MB) -> refused;
  3. 2026-09-30, 10 then 110 rows -> two light publishes calibrating the bytes per row;
  4. 2026-09-30, rows sized so the page WITH dialogs lands midway between 1,950,000 and 2,097,152 -> the medium day;
  5. 2026-09-30, 1,500 rows again -> a heavy re-publish over an existing page.
  - (a) control: the light page keeps every holding dialog (20 `data-hd`, no `data-holding-dialogs="off"`);
  - (b) the heavy day returns FAILED, no outputs, no marker, with a byte count over 2,097,152 in its detail;
  - (c) the heavy day writes nothing under its page prefix (no index.html, no manifest.json, no revisions/), and the
    prior day stays the newest published day with its bytes unchanged;
  - (d) the medium day publishes (OK or PARTIAL) at or under 2,097,152 B with no `data-hd` dialog and
    `data-holding-dialogs="off"`, its predicted size with dialogs above 1,950,000;
  - (e) the heavy re-publish returns FAILED and leaves the day's index.html, manifest.json and object list as they were.
Base: PASS expected on every limb."""
import hashlib
import importlib.util
import math
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

_UI = pathlib.Path(__file__).resolve().parents[2] / "round6" / "checks" / "_ui.py"
_spec = importlib.util.spec_from_file_location("_rivals_r6_ui", _UI)
u = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(u)

D0, D1 = "2026-09-29", "2026-09-30"
CAP = 2 * 1024 * 1024  # the gateway's MAX_BYTES (rivalfunds_view.py:35) as a literal: the gateway is the authority
HEAVY = 1500
SUBJ = "y" * 1000


def hc_plant(day):
    vals = {f"H{i:02d}": (0.001 * (i + 1) if i < 10 else -0.001 * (i - 9)) for i in range(20)}
    rows = u.hc_rows("TXUE", "YTD", vals, end=day)
    for r in rows:
        if r["axis"] == "security":
            r["security_name"] = f"Holding {r['bucket']} " + "Long Name " * 1000
    return rows


def census(day, n):
    return [{"date": day, "input_kind": "price", "subject": f"P{i:05d}-{SUBJ}", "fund_id": "TXUE", "role": "rival",
             "status": "missing", "as_of": None, "location": "s3://fixture", "reason": "no G4 row", "fallback": None}
            for i in range(n)]


def sha(b) -> str:
    return "absent" if b is None else hashlib.sha256(b).hexdigest()[:12]


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import ai_stage, homes, markers, publish_page, render

    os.environ[publish_page.PRODUCE_ENV] = "0"
    os.environ.pop(ai_stage.ENABLE_ENV, None)
    cap, soft = CAP, render.DIALOG_SOFT_CAP
    print(f"gateway cap {cap}; product MAX_PAGE_BYTES {publish_page.MAX_PAGE_BYTES}, DIALOG_SOFT_CAP {soft}")
    spec, s, _ = c.page_fixture()
    seq = iter(range(1, 100))

    def publish(day, n, batch):
        rev = f"{day.replace('-', '')}T{next(seq):06d}Z-{'%012x' % n}"
        u.put_table(s, "holding_contribution", hc_plant(day), rev, day)
        u.put_table(s, "input_census", census(day, n), rev, day)
        r = publish_page.handler_entry({"date": day, "mode": "daily", "batch_id": batch, "sink": spec})
        page = s.get(homes.page(day, "index.html")) if s.exists(homes.page(day, "index.html")) else None
        print(f"publish {day} rows {n} [{batch}]: {r.get('status')} | page {None if page is None else len(page)} B |",
              str(r.get("detail"))[:150])
        return r, page

    def objs(day):
        return sorted(s.list(homes.page(day) + "/"))

    def newest_day():
        days = {m.group(1) for x in s.list(homes.page("")) for m in [re.search(r"date=(\d{4}-\d{2}-\d{2})/", x)] if m}
        return max(days) if days else None

    def dialogs(page):
        root = u.parse(page.decode("utf-8")) if page else u.parse("")
        return len(root.all("data-hd")), len(root.all("data-holding-dialogs", "off"))

    def refused(r, batch, day):
        nums = [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]{5,}", str(r.get("detail")))]
        return (r.get("status") == "FAILED" and not r.get("outputs") and not r.get("marker")
                and markers.get_marker(publish_page.STAGE, day, batch, spec) is None and any(x > cap for x in nums))

    _, prior = publish(D0, 10, "ps-prior")
    nd, off = dialogs(prior)
    v.check(prior is not None and len(prior) < soft and nd == 20 and off == 0,
            f"(a) control: the light page ({None if prior is None else len(prior)} B) keeps every holding dialog "
            f"({nd} data-hd, {off} data-holding-dialogs=off)")

    r2, _ = publish(D1, HEAVY, "ps-heavy")
    v.check(refused(r2, "ps-heavy", D1),
            "(b) the heavy day returns FAILED, no outputs, no marker, a byte count over the cap in its detail")
    after = s.get(homes.page(D0, "index.html")) if s.exists(homes.page(D0, "index.html")) else None
    print("heavy day objects:", objs(D1), "| newest day:", newest_day(), "| prior sha", sha(prior), "->", sha(after))
    v.check(not objs(D1) and newest_day() == D0 and sha(after) == sha(prior),
            "(c) the heavy day writes nothing under its page prefix; the prior day stays the newest, bytes unchanged")

    _, p10 = publish(D1, 10, "ps-cal-10")
    _, p110 = publish(D1, 110, "ps-cal-110")
    per_row = (len(p110) - len(p10)) / 100.0 if p10 and p110 else 0.0
    target = (soft + cap) // 2
    n_med = 110 + math.ceil((target - len(p110)) / per_row) if per_row > 0 else 0
    predicted = len(p110) + (n_med - 110) * per_row if p110 else 0
    print(f"calibration: {per_row:.1f} B per census row; medium plant {n_med} rows, predicted {predicted:.0f} B with "
          "dialogs")
    r4, med = publish(D1, n_med, "ps-medium")
    nd, off = dialogs(med)
    v.check(r4.get("status") in ("OK", "PARTIAL") and med is not None and len(med) <= cap and nd == 0 and off >= 1
            and soft < predicted < cap,
            f"(d) the medium day (predicted {predicted:.0f} B with dialogs) publishes at "
            f"{None if med is None else len(med)} B without its holding dialogs ({nd} data-hd, {off} off)")

    def state(day):
        man = homes.page(day, "manifest.json")
        return objs(day), sha(s.get(man) if s.exists(man) else None)

    before = state(D1)
    r5, again = publish(D1, HEAVY, "ps-heavy-2")
    after = state(D1)
    print("re-publish: objects", len(before[0]), "->", len(after[0]), "| manifest sha", before[1], "->", after[1],
          "| index sha", sha(med), "->", sha(again))
    v.check(refused(r5, "ps-heavy-2", D1) and sha(again) == sha(med) and after == before,
            "(e) the heavy re-publish returns FAILED and leaves the day's index.html, manifest.json and objects as "
            "they were")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
