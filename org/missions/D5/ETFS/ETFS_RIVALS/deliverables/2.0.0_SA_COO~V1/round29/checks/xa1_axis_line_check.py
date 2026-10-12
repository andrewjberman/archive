"""RIV-xa-1 checks (round 29): the audit page's calendar legend states, in VISIBLE text, what the calendar's day axis is and how
the trade windows are dated -- not only in a cell's hover title.

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: AC1 renders the audit document from a context (`render.render_audit_page`); AC2 publishes the page into a local sink
through the real stage (`publish_page.handler_entry`) and reads `audit.html` back from the sink.
"""
import html
import re

from rivalfunds import homes, publish_page, render
from rivalfunds.tests.test_crorv_layout import _ctx, _hc
from rivalfunds.tests.test_p1_page_and_guardrails import _pin_identity_floors  # noqa: F401  (autouse: the floor is not the subject)
from rivalfunds.tests.test_p2_page_grouped_by_fund import _ev, sink  # noqa: F401  (fixture)

SENTENCE = ("Each calendar column is the day a holdings report was expected; a cell reads repeat when the report received that day "
            "is the same holdings window as the previous report. Trade windows are dated by the report's own date, so a window "
            "can end on a day this calendar marks repeat.")


def _visible(doc: str) -> str:
    """The text a reader sees: scripts and styles dropped, every tag (and so every attribute, a title included) removed."""
    doc = re.sub(r"<(script|style)\b.*?</\1>", " ", doc, flags=re.S | re.I)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", doc)).split())


def _legend_paragraph(doc: str) -> str:
    m = re.search(r'<p class="muted">Calendar legend:(.*?)</p>', doc, flags=re.S)
    assert m, "the calendar legend paragraph is missing"
    return _visible(m.group(1))


def test_ac1_the_audit_documents_legend_states_the_axis_in_visible_text():
    audit = render.render_audit_page(_ctx({"holding_contribution": _hc("IDVZ", "YTD", {"A": 0.02})}))
    assert _visible(audit).count(SENTENCE) == 1
    assert SENTENCE in _legend_paragraph(audit)
    # the existing legend words are all still there (the hover title is untouched; it is not the statement)
    assert "new / repeat / regressed (older than the previous report) / gap / periodic per day" in _legend_paragraph(audit)


def test_ac2_the_published_audit_page_carries_it_and_still_validates(sink):  # noqa: F811
    spec, s = sink
    r = publish_page.handler_entry(_ev(spec))
    assert r["status"] == "OK"
    audit = s.get(homes.page("2026-09-30", "audit.html")).decode("utf-8")
    assert _visible(audit).count(SENTENCE) == 1
    assert render.validate_audit(audit, len(re.findall(r'<details class="trace"', audit)))[0]
