"""RIV-xa-2 checks (round 30): the audit page's day-axis sentence sits BESIDE EVERY CALENDAR -- inside each fund's own <article>,
directly above or below the calendar's table -- and not only in the section legend (round-29 analysis ruling 1; the CVO's rows
D1-C-S19: the legend is 13,384 to 20,425 px from the calendars, so it is out of view when a calendar is centred).

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: the audit page is published into a local sink through the real stage (`publish_page.handler_entry`) with G2 coverage
rows for TXUE and BASG (two calendars that render) and none for IDVZ (a calendar that reads unavailable: the negative arm).
Whether the sentence is in the same viewport as a centred calendar on the SERVED page is J1 (the CVO's), read at the production URL.
"""
import html
import re

from rivalfunds import homes, publish_page
from rivalfunds.tests.test_p1_page_and_guardrails import _pin_identity_floors  # noqa: F401  (autouse: the floor is not the subject)
from rivalfunds.tests.test_p2_page_grouped_by_fund import DAY, _ev, _write_coverage, sink  # noqa: F401  (fixture)

SENTENCE = ("Each calendar column is the day a holdings report was expected; a cell reads repeat when the report received that day "
            "is the same holdings window as the previous report. Trade windows are dated by the report's own date, so a window "
            "can end on a day this calendar marks repeat.")

ROWS = [
    {"fund_id": "TXUE", "expected_date": "2026-09-25", "source": "bloomberg", "actual_report_date": "2026-09-25", "status": "new", "g1_source_used": "bloomberg"},
    {"fund_id": "TXUE", "expected_date": "2026-09-28", "source": "bloomberg", "actual_report_date": "2026-09-25", "status": "repeat", "g1_source_used": "bloomberg"},
    {"fund_id": "BASG", "expected_date": "2026-09-25", "source": "issuer", "actual_report_date": "2026-09-24", "status": "periodic", "g1_source_used": "issuer"},
    {"fund_id": "BASG", "expected_date": "2026-09-28", "source": "issuer", "actual_report_date": "2026-09-28", "status": "new", "g1_source_used": "issuer"},
]


def _visible(doc: str) -> str:
    doc = re.sub(r"<(script|style)\b.*?</\1>", " ", doc, flags=re.S | re.I)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", doc)).split())


def _articles(doc: str):
    return re.findall(r'<article data-fund="([A-Z]+)".*?</article>', doc, flags=re.S), \
        [m.group(0) for m in re.finditer(r'<article data-fund="[A-Z]+".*?</article>', doc, flags=re.S)]


def _published(sink_pair):
    spec, s = sink_pair
    _write_coverage(s, ROWS)
    r = publish_page.handler_entry(_ev(spec))
    assert r["status"] == "OK", r
    return s.get(homes.page("2026-09-30", "audit.html")).decode("utf-8")


def _adjacent(block: str) -> bool:
    """The sentence's own paragraph is the immediate sibling of the calendar wrapper: directly before it or directly after it."""
    doc = html.unescape(block)
    s = re.escape(SENTENCE)
    before = rf'<p[^>]*>[^<]*{s}[^<]*</p>\s*<div class="calwrap">'
    after = rf'</table></div>\s*<p[^>]*>[^<]*{s}[^<]*</p>'
    return bool(re.search(before, doc) or re.search(after, doc))


def test_ac1_every_rendered_calendar_has_the_sentence_beside_it_and_an_unavailable_one_has_none(sink):  # noqa: F811
    doc = _published(sink)
    funds, blocks = _articles(doc)
    ok = [(f, b) for f, b in zip(funds, blocks) if 'data-calendar-status="ok"' in b]
    unavailable = [(f, b) for f, b in zip(funds, blocks) if 'data-calendar-status="unavailable"' in b]
    assert {f for f, _ in ok} >= {"TXUE", "BASG"}, f"the denominator is 2 rendered calendars at least; saw {[f for f, _ in ok]}"
    assert any(f == "IDVZ" for f, _ in unavailable), "the negative arm needs a fund whose calendar reads unavailable"
    for f, b in ok:
        assert _visible(b).count(SENTENCE) == 1, f"{f}: the sentence must be in this fund's own article exactly once"
        assert _adjacent(b), f"{f}: the sentence must be the paragraph directly above or below the calendar"
    for f, b in unavailable:
        assert SENTENCE not in _visible(b), f"{f}: no calendar renders, so no axis sentence is stated beside it"


def test_ac2_the_section_legend_copy_stays_and_the_page_total_is_one_plus_the_calendars(sink):  # noqa: F811
    doc = _published(sink)
    funds, blocks = _articles(doc)
    n_ok = sum('data-calendar-status="ok"' in b for b in blocks)
    legend = re.search(r'<p class="muted">Calendar legend:(.*?)</p>', doc, flags=re.S)
    assert legend and SENTENCE in _visible(legend.group(1)), "the section legend keeps its copy of the sentence"
    assert _visible(doc).count(SENTENCE) == 1 + n_ok
