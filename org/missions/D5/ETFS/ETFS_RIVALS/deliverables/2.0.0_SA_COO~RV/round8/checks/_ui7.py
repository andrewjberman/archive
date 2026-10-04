"""Round-7 copy of round 6's _ui.py for the RIV-rd-* checks (issuer-written, 2.0.0_SA_COO~RV), renamed _ui7 so it
never shadows another writer's module; the code is unchanged. Round 6's text: a small DOM over the renderer's
HTML (stdlib html.parser), the text a reader sees, and fixture builders for a fund view, its trade windows and a page
context.
Offline: no S3, no vendor.

Two text readings, both over element text only (attribute values such as `title` tooltips and `data-*` hooks are never
text):
  - `text(node)`: everything a reader can reach, closed <details> included (they open on a click);
  - `face(node)`: what a reader sees WITHOUT opening anything: a closed <details> shows only its <summary>."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser

try:  # parsed page text carries entities such as &rarr;; a cp1252 pipe must print them escaped, never raise
    sys.stdout.reconfigure(errors="backslashreplace")
except (AttributeError, ValueError):
    pass

VOID = frozenset(("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"))
SKIP = frozenset(("style", "script"))
PAGE_DAY = "2026-09-30"


class Node:
    """One element: `tag`, `attrs` (a boolean attribute reads ""), `children` (Node or str), `parent`, and `start`, the
    offset of its start tag in the parsed source."""

    def __init__(self, tag, attrs, parent=None, start=0):
        self.tag, self.parent, self.start, self.children = tag, parent, start, []
        self.attrs = {k: ("" if v is None else v) for k, v in attrs}

    def iter(self):
        yield self
        for ch in self.children:
            if isinstance(ch, Node):
                yield from ch.iter()

    def all(self, attr, value=None):
        """Every element under this one (itself included) carrying `attr`, equal to `value` when given."""
        return [n for n in self.iter() if attr in n.attrs and (value is None or n.attrs[attr] == value)]

    def cls(self, name):
        return [n for n in self.iter() if name in (n.attrs.get("class") or "").split()]

    def tags(self, tag):
        return [n for n in self.iter() if n.tag == tag]

    @property
    def closed(self) -> bool:
        return self.tag == "details" and "open" not in self.attrs


class _Builder(HTMLParser):
    def __init__(self, src: str):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node("#root", [])
        self._lines = [0] + [m.end() for m in re.finditer("\n", src)]

    def _off(self) -> int:
        ln, col = self.getpos()
        return self._lines[ln - 1] + col

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur, self._off())
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur, self._off()))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(html: str) -> Node:
    b = _Builder(html)
    b.feed(html)
    b.close()
    return b.root


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\u2212", "-").replace("\xa0", " ")).strip()


def _walk(node: Node, out: list, face_only: bool, skip) -> None:
    for ch in node.children:
        if isinstance(ch, str):
            out.append(ch)
        elif ch.tag in SKIP or (skip is not None and skip(ch)):
            continue
        elif face_only and ch.closed:
            for s in ch.children:
                if isinstance(s, Node) and s.tag == "summary":
                    out.append(" ")
                    _walk(s, out, face_only, skip)
                    out.append(" ")
        else:
            out.append(" ")
            _walk(ch, out, face_only, skip)
            out.append(" ")


def text(node, skip=None) -> str:
    """All element text under `node` (a Node or an HTML string), closed <details> included; tags read as spaces,
    whitespace collapsed, U+2212 read as '-'. `skip(n)` drops a subtree."""
    node = parse(node) if isinstance(node, str) else node
    out: list = []
    _walk(node, out, False, skip)
    return _norm("".join(out))


def face(node, skip=None) -> str:
    """The text seen without opening anything: a closed <details> (this node included) shows only its <summary>."""
    node = parse(node) if isinstance(node, str) else node
    if node.closed:
        node = next((s for s in node.children if isinstance(s, Node) and s.tag == "summary"), Node("#none", []))
    out: list = []
    _walk(node, out, True, skip)
    return _norm("".join(out))


def inside(node: Node, pred) -> bool:
    """True when `node` or an ancestor satisfies `pred`."""
    while node is not None:
        if pred(node):
            return True
        node = node.parent
    return False


# ---- fixtures --------------------------------------------------------------------------------------------------------


def recon(cash=2, ca=0, income=0, received=0.0, funded=0, status=None, reason=None) -> dict:
    """One G6 row as the renderer reads it."""
    return {
        "cash_lines_excluded": cash,
        "corporate_action_count": ca,
        "income_event_count": income,
        "income_received_base": received,
        "income_funded_trade_count": funded,
        "status": status,
        "reason": reason,
    }


def trade(
    ws: str,
    we: str,
    name="Apple Inc",
    key="AAPL_US_Equity",
    action="add",
    confidence="CLEAN",
    key_resolution="RESOLVED",
    kind="security_id",
    bronze="s3://opal-data-etfs/bronze/fixture/aapl-2026-09-29.json",
    sha="ab" * 32,
) -> dict:
    """One G5 trade with its two-report trace, in the shape publish_page hands the renderer."""

    def side(d, q):
        return {
            "date": d,
            "key": key,
            "quantity": q,
            "market_value": q * 10.0,
            "weight": 0.01,
            "held": True,
            "file": {"source": "bloomberg", "capture_origin": "census:fixture", "bronze_uri": bronze, "sha256": sha},
        }

    return {
        "action": action,
        "name": name,
        "security_key": key,
        "security_key_kind": kind,
        "counterpart_security_key": None,
        "shares_before": 100.0,
        "shares_after": 150.0,
        "discretionary_shares": 50.0,
        "est_price": 10.0,
        "est_notional": 500.0,
        "weight_before": 0.01,
        "weight_after": 0.015,
        "confidence": confidence,
        "key_resolution": key_resolution,
        "key_resolved": True,
        "window_widened": False,
        "flow_adjusted": False,
        "income_funded": False,
        "window_start": ws,
        "window_end": we,
        "window_trading_days": 1,
        "flow_factor": 1.0,
        "trace": {"prior": side(ws, 100.0), "later": side(we, 150.0)},
    }


def window(ws: str, we: str, trades=(), rec=None) -> dict:
    return {
        "window_start": ws,
        "window_end": we,
        "trades": list(trades),
        "recon": recon() if rec is None else rec,
        "no_move": 0,
        "cash_equiv": 0,
    }


def fund_view(
    fund: str,
    role="rival",
    group="G1",
    status="updated",
    latest_date="2026-09-30",
    latest_source="bloomberg",
    windows=(),
    reason=None,
    fund_name=None,
    day="2026-10-02",
) -> dict:
    """A renderer fund view (publish_page `_fund_view` keys); excluded totals summed from the windows' G6 rows."""
    ws = list(windows)
    recs = [w["recon"] for w in ws if w.get("recon")]
    ex = (
        {
            "cash": sum(int(r["cash_lines_excluded"]) for r in recs),
            "ca": sum(int(r["corporate_action_count"]) for r in recs),
            "income": sum(int(r["income_event_count"]) for r in recs),
            "income_funded": sum(int(r["income_funded_trade_count"]) for r in recs),
        }
        if recs
        else {"cash": None, "ca": None, "income": None, "income_funded": None}
    )
    return {
        "fund": fund,
        "group": group,
        "role": role,
        "policy": "bloomberg_first",
        "day": day,
        "fund_name": fund_name,
        "latest_date": latest_date,
        "latest_source": latest_source,
        "prior_date": None,
        "report_dates": [],
        "revisions": {latest_date: "fixture-rev"} if latest_date else {},
        "files": {},
        "windows": ws,
        "truncated": 0,
        "excluded": ex,
        "n_trades": sum(len(w["trades"]) for w in ws),
        "calendar": None,
        "checks": [],
        "status": status,
        "reason": reason,
        "kind": "ok" if status == "updated" else "failed",
    }


def page_ctx(funds: list, a1=None, day="2026-10-02") -> dict:
    """A renderer page context with every fund in one group G1 (home = the first home fund, else the first fund)."""
    home = next((f["fund"] for f in funds if f["role"] == "home"), funds[0]["fund"])
    return {
        "day": day,
        "groups": [{"group_id": "G1", "home": home, "funds": funds}],
        "checks": [],
        "g0_note": "fixture",
        "a1": {} if a1 is None else a1,
        "n_updated": sum(1 for f in funds if f["status"] == "updated"),
        "n_funds": len(funds),
    }


def put_table(s, table: str, rows: list, rev: str, day: str = PAGE_DAY) -> None:
    import io

    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import homes

    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(homes.address("rivalfunds", "etfs", "gold", table, f"date={day}", f"{table}-{rev}.parquet"), buf.getvalue())


def publish_with(tables: dict) -> tuple:
    """The round-5 page fixture (test_p2's TXUE/BASG books, G5 replayed) plus `tables` {table: rows} planted as the
    day's gold A1 tables; the A1 producer pre-step is OFF so only planted tables exist. One publish of PAGE_DAY. Returns
    (result, html); an unpublished page reads as ""."""
    import os

    import _common as c

    c.setup_path()
    from rivalfunds import homes, publish_page

    os.environ[publish_page.PRODUCE_ENV] = "0"
    spec, s, _ = c.page_fixture()
    for t, rows in tables.items():
        put_table(s, t, rows, "20260930T020000Z-uuuuuuuuuuuu")
    r = publish_page.handler_entry({"date": PAGE_DAY, "mode": "daily", "batch_id": "uipg", "sink": spec})
    try:
        html = s.get(homes.page(PAGE_DAY, "index.html")).decode("utf-8")
    except Exception:  # noqa: BLE001 -- an unpublished page reads as empty and the checks fail on it
        html = ""
    return r, html


TREND = (  # (axis, bucket, name, lean, net, gross, n_windows, reading, trend_mark)
    ("security", "S1", "Intuit Inc", "into", 22973442.0, 50000000.0, 5, "tilt", "0 0 0 0 + + + + + 0"),
    ("security", "S2", "Arthur J Gallagher", "away", -1340000.0, 1500000.0, 1, "bet", ". . . . . . . 0 - 0"),
    ("sector", "Energy", None, "into", 30000000.0, 31000000.0, 4, "tilt", "0 + + 0 0 0 0 0 0 0"),
    ("sector", "Industrials", None, "away", -2000000.0, 2100000.0, 1, "bet", "0 0 0 0 0 0 0 0 - 0"),
)


def bt_rows(fund: str = "TXUE", end: str = "2026-10-02") -> list:
    """buying_trend rows in the A1 contract for one fund (TREND): two security lines and two sector lines, each lean."""
    rank: dict = {}
    out = []
    for axis, b, name, lean, net, gross, nw, reading, mark in TREND:
        rank[(axis, lean)] = rank.get((axis, lean), 0) + 1
        out.append(
            {
                "fund_id": fund,
                "role": "rival",
                "window_start": "2026-01-02",
                "window_end": end,
                "n_trading_days": 189,
                "axis": axis,
                "bucket": b,
                "security_name": name,
                "net_notional_base": net,
                "gross_notional_base": gross,
                "n_windows": nw,
                "lean": lean,
                "rank": rank[(axis, lean)],
                "reading": reading,
                "trend_mark": mark,
                "n_refused_windows": 0,
                "claim": "INFERRED",
                "revision": "fx",
            }
        )
    return out


def account(
    fund: str,
    kind: str,
    text_: str,
    grounding="PASS",
    reason=None,
    cited=(),
    observed=(),
    inferred=(),
    invalidation="a reversal of the adds",
    vintages=None,
    manifest=None,
    run_id="runU",
    model="stub-model-x",
) -> dict:
    """One research_hypotheses row (the A1 contract) as load_a1 hands it to the renderer: list/dict fields
    JSON-encoded."""
    import json

    return {
        "run_id": run_id,
        "item_id": kind,
        "fund_id": fund,
        "kind": kind,
        "text": text_,
        "observed": json.dumps(list(observed)),
        "inferred": json.dumps(list(inferred)),
        "cited_rows": json.dumps(list(cited)),
        "invalidation": invalidation,
        "input_vintages": json.dumps(vintages or {}),
        "web_reads": "[]",
        "grounding": grounding,
        "grounding_reason": reason,
        "model_version": model,
        "prompt_version": "v1",
        "input_manifest": json.dumps(manifest or {}),
        "produced_at": "2026-10-02T02:00:00Z",
    }


def hc_rows(
    fund: str, period: str, values: dict, sectors: dict | None = None, priced: bool = True, end: str = PAGE_DAY
) -> list:
    """holding_contribution rows for one fund x period in the A1 contract. `values` {bucket: contribution}; `sectors`
    {sector: contribution}. `priced=False` writes the shape gold_holding_contribution writes for a period with no priced
    holding: every contribution and rank null, n_ranked 0, n_missing = the number of holdings."""

    def block(axis, vals):
        n = len(vals)
        best = {b: i + 1 for i, (b, _) in enumerate(sorted(vals.items(), key=lambda kv: (-kv[1], kv[0])))}
        worst = {b: i + 1 for i, (b, _) in enumerate(sorted(vals.items(), key=lambda kv: (kv[1], kv[0])))}
        return [
            {
                "fund_id": fund,
                "role": "rival",
                "period": period,
                "period_start": "2026-07-01",
                "period_end": end,
                "axis": axis,
                "bucket": b,
                "security_name": (f"Name {b}" if axis == "security" else None),
                "contribution": v if priced else None,
                "price_coverage": "full" if priced else "none",
                "n_days_priced": 20 if priced else 0,
                "n_days_period": 20,
                "rank_best": best[b] if priced else None,
                "rank_worst": worst[b] if priced else None,
                "n_ranked": n if priced else 0,
                "n_missing": 0 if priced else n,
                "claim": "INFERRED",
                "revision": "fx",
            }
            for b, v in vals.items()
        ]

    return block("security", values) + block("sector", sectors or {})
