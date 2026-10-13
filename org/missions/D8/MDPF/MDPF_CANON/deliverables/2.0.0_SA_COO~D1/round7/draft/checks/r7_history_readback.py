#!/usr/bin/env python3
"""MDPF_CANON round 7, cell CN-j-1 -- the ISSUER'S acceptance read of the first publisher run that carries the history leaf
platinum/mdpf/{scope}/category-views-history.json (the FWD-9 Client chips' history; CTO rulings msgs 5086-5088, PRD v2.15).

Read-only against the SERVED plane and the gold tier (list/get/head). It reads the S3 objects the portal route resolves to; it does not
call the /api/general/mdpf/{scope}/category-views-history.json route itself (that edge hop is the CloudOps read of the deploy order).
Prints dates, counts and field names; never an account id and never a client dollar level.

  python r7_history_readback.py read [--scope S ...]
        default scopes: 49financial inflection cottonwood global. Run it after the first scheduled publisher run (13:50Z) that follows the
        CN-j-1 deploy.
  python r7_history_readback.py selftest
        builds a synthetic leaf per scope OFFLINE (no write) from the real dated gold category-views objects with the assembly rule of the
        order (Step 1), runs H2-H5 on it (must PASS), then plants three defects (a missing node read as 0.0; an unsorted date; an extra
        field) and requires each to turn the named arm RED, each beside a positive control.

Arms (a line `  <ARM> PASS|FAIL|SKIP <detail>` each, then `ROUND 7 HISTORY READBACK: k of n arms`, n = 9, k = the PASS count; exit 0 only
when no arm FAILs and any SKIP is the one allowed kind, H9 with no deploy ledger found):
  H1 the leaf exists at platinum/mdpf/<scope>/category-views-history.json in opal-data-portal-v2 for every scope and parses as a JSON object
  H2 its dates[] equal the dates of the dated gold category-views objects under opal-data-assets portal/gold/mdpf/<scope>/category-views/,
     less the dates it names in omitted[] (denominators printed per scope)
  H3 each of the two arrays equals nodes.Client.children["Client - Opal Supervised" | "Client - Opal Unsupervised"].aum of that date's
     dated object to the cent; a dated object lacking a node (or a numeric aum) gives null, never 0.0; a measured 0.0 stays 0.0
  H4 dates are ISO, strictly ascending with no duplicate, the three arrays have equal length, n_dates == len(dates), every array cell is a
     number or null
  H5 the key set is exactly the declared shape (+ _provenance), schema and leaf and scope are as declared, omitted[] rows carry only
     {date, reason}, _provenance carries only declared keys, and no digit run of six or more appears in any non-provenance string
  H6 the last-date entry equals the served latest platinum/mdpf/<scope>/category-views.json's Client node values, and that object's
     as_of is that date (the as-of chips and the history agree)
  H7 the newest publisher run manifest carries history_rows for the four leaves (published or unchanged, empty omitted, n_dates as the
     leaf's), the pre-existing 18 pair rows are unchanged in count and none is a history key, all_present true, missing_pairs empty; the
     pointer latest.json, when readable, carries the same four history_rows
  H8 the existing served leaves are untouched in data: for each of the manifest's 18 pair rows the served object equals its gold source
     object apart from _provenance (the publisher is a 1:1 projection); the unlisted-key census under platinum/mdpf/<scope>/ is printed
  H9 each leaf's LastModified is after the CN-j-1 deploy ledger's close (a ledger entry under org/critical_paths/change_management/ naming
     the history leaf); no ledger found -> SKIP, a ledger found and not CLOSED -> FAIL
"""
from __future__ import annotations

import copy
import datetime
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

GOLD_BUCKET = "opal-data-assets"
GOLD_PREFIX = "portal/gold/mdpf"
SERVE_BUCKET = "opal-data-portal-v2"
SERVE_PREFIX = "platinum/mdpf"
MANIFESTS = SERVE_PREFIX + "/_manifests/"
SCOPES = ("49financial", "inflection", "cottonwood", "global")
LEAF = "category-views-history"
SCHEMA = "mdpf-category-views-history/v1"
SOURCE_TYPE = "category-views"
CLIENT_NAMES = ("Client - Opal Supervised", "Client - Opal Unsupervised")
CONTENT_KEYS = ("schema", "leaf", "scope", "n_dates", "dates", "client_supervised", "client_unsupervised", "omitted")
LEAF_KEYS = frozenset(CONTENT_KEYS) | frozenset(("_provenance",))
PROV_KEYS = frozenset(("written_by", "written_at", "source_keys", "source_count", "source_vintages"))
EXPECTED_PAIR_ROWS = 18
CENT = 0.0051
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LONG_DIGITS = re.compile(r"\d{6,}")
LEDGER_TOKENS = ("category-views-history", "cn-j-1", "history-leaf", "history_leaf")
ARM_NAMES = ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9")


# ------------------------------------------------------------------------------------------------ S3 reads
def _client(kind: str):
    import boto3
    from botocore.config import Config
    return boto3.client(kind, region_name="us-east-1",
                        config=Config(read_timeout=30, connect_timeout=10, retries={"max_attempts": 2}))


def _list(s3, bucket: str, prefix: str) -> list:
    """[(key, LastModified)] for every object under prefix (paginated client-side)."""
    out, tok = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        out += [(o["Key"], o["LastModified"]) for o in r.get("Contents", [])]
        if not r.get("IsTruncated"):
            return out
        tok = r.get("NextContinuationToken")


def _get(s3, bucket: str, key: str) -> tuple:
    """(bytes or None, error code or '')."""
    try:
        return s3.get_object(Bucket=bucket, Key=key)["Body"].read(), ""
    except Exception as exc:  # noqa: BLE001 -- a failed read is data for the arm, never a crash
        code = getattr(exc, "response", {}).get("Error", {}).get("Code", type(exc).__name__)
        return None, str(code)


def _get_many(s3, bucket: str, keys: list) -> dict:
    keys = list(keys)
    if not keys:
        return {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        res = list(pool.map(lambda k: _get(s3, bucket, k), keys))
    return dict(zip(keys, res))


def _jloads(raw):
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except ValueError:
        return None


def _date_of(key: str) -> str:
    return key.rsplit("/", 1)[-1][:-5]


def _opt_all(argv: list, name: str) -> list:
    out = []
    for i, a in enumerate(argv):
        if a == name and i + 1 < len(argv):
            out.append(argv[i + 1])
    return out


# ------------------------------------------------------------------------------------------------ the assembly rule (Step 1 of the order)
def _num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _node_aum(obj, name: str):
    """nodes.Client.children[name].aum as a float, or None when the node or a numeric aum is absent (ABSENT IS NOT ZERO)."""
    try:
        return _num(obj["nodes"]["Client"]["children"][name]["aum"])
    except (KeyError, TypeError, IndexError):
        return None


def assemble(scope: str, dated: dict) -> tuple:
    """dated: {YYYY-MM-DD: body bytes}. Returns (content, omitted) exactly as the order's Step 1 defines it."""
    dates, sup, uns, omitted = [], [], [], []
    for d in sorted(dated):
        try:
            obj = json.loads(dated[d])
        except (ValueError, TypeError):
            omitted.append({"date": d, "reason": "unparseable"})
            continue
        if not isinstance(obj, dict):
            omitted.append({"date": d, "reason": "not_an_object"})
            continue
        as_of = obj.get("as_of")
        if isinstance(as_of, str) and as_of[:10] != d:
            omitted.append({"date": d, "reason": "as_of_differs_from_key"})
            continue
        dates.append(d)
        sup.append(_node_aum(obj, CLIENT_NAMES[0]))
        uns.append(_node_aum(obj, CLIENT_NAMES[1]))
    content = {"schema": SCHEMA, "leaf": LEAF, "scope": scope, "n_dates": len(dates), "dates": dates,
               "client_supervised": sup, "client_unsupervised": uns, "omitted": omitted}
    return content, omitted


def dated_gold(s3, scope: str) -> dict:
    """{date: body bytes} for every dated gold category-views object of the scope (a failed read is kept as b'' -> unparseable)."""
    keys = [k for k, _ in _list(s3, GOLD_BUCKET, "%s/%s/%s/" % (GOLD_PREFIX, scope, SOURCE_TYPE))
            if k.endswith(".json") and DATE_RE.match(_date_of(k))]
    got = _get_many(s3, GOLD_BUCKET, keys)
    return {_date_of(k): (got[k][0] if got[k][0] is not None else b"") for k in keys}


# ------------------------------------------------------------------------------------------------ small helpers for the arms
def _same(a, b) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) < CENT


def _each(ctx: dict, fn):
    """Run fn(scope, doc) for each scope with a leaf document; a scope without one fails the arm as NOT EVALUABLE."""
    ok, parts = True, []
    for sc in ctx["scopes"]:
        doc = ctx["leaf"].get(sc)
        if not isinstance(doc, dict):
            ok = False
            parts.append("%s: NOT EVALUABLE (no leaf, H1)" % sc)
            continue
        good, detail = fn(sc, doc)
        ok = ok and good
        parts.append("%s: %s" % (sc, detail))
    return ("PASS" if ok else "FAIL"), "; ".join(parts)


# ------------------------------------------------------------------------------------------------ the arms
def h1(ctx: dict) -> tuple:
    ok, parts = True, []
    for sc in ctx["scopes"]:
        doc = ctx["leaf"].get(sc)
        if isinstance(doc, dict):
            parts.append("%s: present (n_dates=%s)" % (sc, doc.get("n_dates")))
        else:
            ok = False
            parts.append("%s: ABSENT (%s)" % (sc, ctx["leaf_err"].get(sc) or "unparseable or not an object"))
    return ("PASS" if ok else "FAIL"), "; ".join(parts)


def h2(ctx: dict) -> tuple:
    def one(sc, doc):
        gold = set(ctx["dated"].get(sc) or {})
        leaf = list(doc.get("dates") or [])
        om = [o.get("date") for o in (doc.get("omitted") or []) if isinstance(o, dict)]
        good = (set(leaf) == gold - set(om) and set(om) <= gold and len(set(leaf)) == len(leaf))
        return good, "leaf %d dates, gold %d dated objects, omitted %d" % (len(leaf), len(gold), len(om))
    return _each(ctx, one)


def h3(ctx: dict) -> tuple:
    def one(sc, doc):
        dates = list(doc.get("dates") or [])
        arrs = (doc.get("client_supervised") or [], doc.get("client_unsupervised") or [])
        bad, cells, nulls = [], 0, 0
        for i, d in enumerate(dates):
            raw = (ctx["dated"].get(sc) or {}).get(d)
            obj = _jloads(raw) if raw is not None else None
            for j, name in enumerate(CLIENT_NAMES):
                cells += 1
                want = _node_aum(obj, name) if isinstance(obj, dict) else None
                got = _num(arrs[j][i]) if i < len(arrs[j]) else "missing"
                if got == "missing" or not _same(got, want):
                    bad.append("%s/%s" % (d, "sup" if j == 0 else "uns"))
                if want is None:
                    nulls += 1
        return (not bad), "%d cells compared, %d expected-null, %d mismatch%s" % (
            cells, nulls, len(bad), (" (first %s)" % ", ".join(bad[:3])) if bad else "")
    return _each(ctx, one)


def h4(ctx: dict) -> tuple:
    def one(sc, doc):
        dates = doc.get("dates")
        sup, uns = doc.get("client_supervised"), doc.get("client_unsupervised")
        if not (isinstance(dates, list) and isinstance(sup, list) and isinstance(uns, list)):
            return False, "dates or an array is not a list"
        iso = all(isinstance(d, str) and DATE_RE.match(d) for d in dates)
        asc = all(dates[i] < dates[i + 1] for i in range(len(dates) - 1)) if iso else False
        lens = len(dates) == len(sup) == len(uns) and doc.get("n_dates") == len(dates)
        cells = all(c is None or _num(c) is not None for c in list(sup) + list(uns))
        return (iso and asc and lens and cells), "iso=%s strictly_ascending=%s lengths_and_n_dates=%s cells_number_or_null=%s (n=%d)" % (
            iso, asc, lens, cells, len(dates))
    return _each(ctx, one)


def _strings(node, out: list):
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for k, v in node.items():
            out.append(str(k))
            _strings(v, out)
    elif isinstance(node, list):
        for v in node:
            _strings(v, out)


def h5(ctx: dict) -> tuple:
    def one(sc, doc):
        keys = set(doc)
        shape = keys == LEAF_KEYS
        head = doc.get("schema") == SCHEMA and doc.get("leaf") == LEAF and doc.get("scope") == sc
        om = doc.get("omitted")
        omok = isinstance(om, list) and all(isinstance(o, dict) and set(o) == {"date", "reason"} for o in om)
        prov = doc.get("_provenance")
        provok = isinstance(prov, dict) and set(prov) <= PROV_KEYS
        strs = []
        _strings({k: v for k, v in doc.items() if k != "_provenance"}, strs)
        longrun = [s for s in strs if LONG_DIGITS.search(s)]
        good = shape and head and omok and provok and not longrun
        extra = sorted(keys ^ LEAF_KEYS)
        return good, "keyset_exact=%s%s header=%s omitted_shape=%s provenance_keys=%s long_digit_strings=%d" % (
            shape, (" (diff %s)" % extra) if extra else "", head, omok, provok, len(longrun))
    return _each(ctx, one)


def h6(ctx: dict) -> tuple:
    s3 = ctx["s3_serve"]

    def one(sc, doc):
        dates = doc.get("dates") or []
        if not dates:
            return False, "leaf has no dates"
        raw, err = _get(s3, SERVE_BUCKET, "%s/%s/category-views.json" % (SERVE_PREFIX, sc))
        obj = _jloads(raw)
        if not isinstance(obj, dict):
            return False, "served latest category-views unreadable (%s)" % (err or "unparseable")
        as_of = str(obj.get("as_of") or "")[:10]
        i = len(dates) - 1
        sup = _num((doc.get("client_supervised") or [None] * len(dates))[i])
        uns = _num((doc.get("client_unsupervised") or [None] * len(dates))[i])
        good = (as_of == dates[i] and _same(sup, _node_aum(obj, CLIENT_NAMES[0])) and _same(uns, _node_aum(obj, CLIENT_NAMES[1])))
        return good, "last leaf date %s, served latest as_of %s, chips equal=%s" % (
            dates[i], as_of or "none", _same(sup, _node_aum(obj, CLIENT_NAMES[0])) and _same(uns, _node_aum(obj, CLIENT_NAMES[1])))
    return _each(ctx, one)


def _manifests(ctx: dict) -> tuple:
    """(newest manifest dict, its key, prior manifest dict or None, prior key) from the publisher's run manifests."""
    if "manifests" in ctx:
        return ctx["manifests"]
    s3 = ctx["s3_serve"]
    keys = [(k, lm) for k, lm in _list(s3, SERVE_BUCKET, MANIFESTS) if k.endswith(".json") and not k.endswith("latest.json")]
    keys.sort(key=lambda kv: kv[1])
    newest = _jloads(_get(s3, SERVE_BUCKET, keys[-1][0])[0]) if keys else None
    prior = _jloads(_get(s3, SERVE_BUCKET, keys[-2][0])[0]) if len(keys) > 1 else None
    ctx["manifests"] = (newest, keys[-1][0] if keys else None, prior, keys[-2][0] if len(keys) > 1 else None)
    return ctx["manifests"]


def h7(ctx: dict) -> tuple:
    newest, nkey, prior, _pk = _manifests(ctx)
    if not isinstance(newest, dict):
        return "FAIL", "no publisher run manifest found under %s" % MANIFESTS
    hist = newest.get("history_rows")
    rows = newest.get("rows") if isinstance(newest.get("rows"), dict) else {}
    parts, ok = ["manifest %s" % (nkey or "").rsplit("/", 1)[-1]], True
    if not isinstance(hist, dict):
        return "FAIL", parts[0] + ": no history_rows field"
    for sc in ctx["scopes"]:
        row = hist.get("%s/%s" % (sc, LEAF))
        doc = ctx["leaf"].get(sc)
        good = (isinstance(row, dict) and row.get("status") in ("published", "unchanged")
                and row.get("serve_key") == "%s/%s/%s.json" % (SERVE_PREFIX, sc, LEAF)
                and not (row.get("omitted") or []) and isinstance(doc, dict) and row.get("n_dates") == doc.get("n_dates"))
        ok = ok and good
        parts.append("%s: %s" % (sc, ("%s n_dates=%s" % (row.get("status"), row.get("n_dates"))) if isinstance(row, dict) else "NO ROW"))
    pair_ok = len(rows) == EXPECTED_PAIR_ROWS and not any(LEAF in k for k in rows)
    prior_rows = prior.get("rows") if isinstance(prior, dict) and isinstance(prior.get("rows"), dict) else None
    same_as_prior = (len(prior_rows) == len(rows)) if prior_rows is not None else None
    flags = newest.get("all_present") is True and (newest.get("missing_pairs") or []) == []
    ok = ok and pair_ok and flags
    parts.append("pair rows %d (expect %d, none a history key)=%s; prior run rows equal=%s; all_present/missing_pairs ok=%s" % (
        len(rows), EXPECTED_PAIR_ROWS, pair_ok, same_as_prior, flags))
    raw, err = _get(ctx["s3_serve"], SERVE_BUCKET, MANIFESTS + "latest.json")
    ptr = _jloads(raw)
    if isinstance(ptr, dict):
        ph = ptr.get("history_rows")
        pok = isinstance(ph, dict) and all(("%s/%s" % (sc, LEAF)) in ph for sc in ctx["scopes"])
        ok = ok and pok
        parts.append("pointer history_rows present=%s" % pok)
    else:
        parts.append("pointer latest.json unread (%s), not graded" % (err or "unparseable"))
    return ("PASS" if ok else "FAIL"), "; ".join(parts)


# The publisher serves a category-views document WITHOUT the two document-level taxsma fields its gold source carries (measured
# 2026-10-13 on the 13:50Z run: 3 of 4 category-views rows differ from gold by exactly these two keys; the TAXSMA rollout switch is OFF).
# That is existing behaviour, not this cell's: H8 sets the two keys aside for category-views rows only and counts how many rows needed it.
TAXSMA_DOC_FIELDS = ("taxsma_contract_version", "taxsma_coverage")


def _strip(obj, extra=()):
    return {k: v for k, v in obj.items() if k != "_provenance" and k not in extra} if isinstance(obj, dict) else obj


def h8(ctx: dict) -> tuple:
    newest, _nk, _p, _pk = _manifests(ctx)
    if not isinstance(newest, dict) or not isinstance(newest.get("rows"), dict):
        return "FAIL", "no publisher run manifest with rows to compare"
    pairs = [(v.get("serve_key"), v.get("source_key")) for v in newest["rows"].values() if isinstance(v, dict)]
    pairs = [(a, b) for a, b in pairs if a and b]
    served = _get_many(ctx["s3_serve"], SERVE_BUCKET, [a for a, _ in pairs])
    source = _get_many(ctx["s3_gold"], GOLD_BUCKET, [b for _, b in pairs])
    bad, taxsma_only = [], 0
    for a, b in pairs:
        so, go = _jloads(served[a][0]), _jloads(source[b][0])
        extra = TAXSMA_DOC_FIELDS if a.endswith("/category-views.json") else ()
        if not (isinstance(so, dict) and isinstance(go, dict) and _strip(so, extra) == _strip(go, extra)):
            bad.append(a)
        elif extra and _strip(so) != _strip(go):
            taxsma_only += 1
    listed = set()
    for sc in ctx["scopes"]:
        listed |= {k for k, _ in _list(ctx["s3_serve"], SERVE_BUCKET, "%s/%s/" % (SERVE_PREFIX, sc)) if k.endswith(".json")}
    known = {a for a, _ in pairs} | {"%s/%s/%s.json" % (SERVE_PREFIX, sc, LEAF) for sc in ctx["scopes"]}
    unlisted = sorted(listed - known)
    return ("PASS" if not bad else "FAIL"), (
        "%d of %d pair rows: served == gold source apart from _provenance (%d differ%s; %d category-views rows differ only by the two "
        "taxsma document fields the publisher does not serve, existing behaviour); census under the scopes: %d json keys, %d not a "
        "manifest pair or a history leaf (printed, not graded)" % (
            len(pairs) - len(bad), len(pairs), len(bad), (": " + ", ".join(bad[:3])) if bad else "", taxsma_only, len(listed),
            len(unlisted)))


def _repo_root():
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=20,
                             cwd=os.path.dirname(os.path.abspath(__file__)))
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def h9(ctx: dict) -> tuple:
    root = ctx.get("repo_root") or _repo_root()
    d = os.path.join(root, "org", "critical_paths", "change_management") if root else None
    names = []
    if d and os.path.isdir(d):
        names = [n for n in os.listdir(d) if n.endswith(".md") and any(t in n.lower() for t in LEDGER_TOKENS)]
    if not names:
        return "SKIP", "ledger not found (no change_management entry names the history leaf); LastModified not compared"
    name = sorted(names)[-1]
    with open(os.path.join(d, name), encoding="utf-8", errors="replace") as fh:
        head = fh.read(4000)
    m = re.search(r"CLOSED[^\n]*?closed\s+(\d{8}T\d{6}Z)", head)
    if not m:
        return "FAIL", "ledger %s found but not CLOSED" % name
    closed = datetime.datetime.strptime(m.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc)
    ok, parts = True, []
    for sc in ctx["scopes"]:
        try:
            lm = ctx["s3_serve"].head_object(Bucket=SERVE_BUCKET, Key="%s/%s/%s.json" % (SERVE_PREFIX, sc, LEAF))["LastModified"]
        except Exception as exc:  # noqa: BLE001
            ok = False
            parts.append("%s: head failed (%s)" % (sc, type(exc).__name__))
            continue
        after = lm > closed
        ok = ok and after
        parts.append("%s: after close=%s" % (sc, after))
    return ("PASS" if ok else "FAIL"), "ledger %s closed %s; %s" % (name, m.group(1), "; ".join(parts))


ARMS = {"H1": h1, "H2": h2, "H3": h3, "H4": h4, "H5": h5, "H6": h6, "H7": h7, "H8": h8, "H9": h9}


def _run(ctx: dict, names) -> list:
    out = []
    for n in names:
        status, detail = ARMS[n](ctx)
        print("  %s %s %s" % (n, status, detail))
        out.append((n, status))
    return out


# ------------------------------------------------------------------------------------------------ commands
def cmd_read(argv: list) -> int:
    scopes = tuple(_opt_all(argv, "--scope")) or SCOPES
    for sc in scopes:
        if sc not in SCOPES:
            print("unknown scope %r (expected one of %s)" % (sc, ", ".join(SCOPES)))
            return 2
    s3g = _client("s3")
    s3s = s3g
    ctx = {"scopes": scopes, "s3_gold": s3g, "s3_serve": s3s, "leaf": {}, "leaf_err": {}, "dated": {}}
    for sc in scopes:
        raw, err = _get(s3s, SERVE_BUCKET, "%s/%s/%s.json" % (SERVE_PREFIX, sc, LEAF))
        doc = _jloads(raw)
        ctx["leaf"][sc] = doc if isinstance(doc, dict) else None
        ctx["leaf_err"][sc] = err
        ctx["dated"][sc] = dated_gold(s3g, sc)
    res = _run(ctx, ARM_NAMES)
    k = sum(1 for _, s in res if s == "PASS")
    print("ROUND 7 HISTORY READBACK: %d of %d arms" % (k, len(ARM_NAMES)))
    skipped = [n for n, s in res if s == "SKIP"]
    if skipped:
        print("SKIPPED: %s (allowed: no deploy ledger found yet)" % ", ".join(skipped))
    failed = [n for n, s in res if s == "FAIL"]
    return 0 if not failed and all(n == "H9" for n in skipped) else 1


def _synthetic_ctx(dated_by_scope: dict) -> dict:
    leaf = {}
    for sc, dated in dated_by_scope.items():
        content, _om = assemble(sc, dated)
        doc = dict(content)
        doc["_provenance"] = {"written_by": "selftest", "written_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                              "source_keys": [], "source_count": len(dated), "source_vintages": {}}
        leaf[sc] = doc
    return {"scopes": tuple(dated_by_scope), "leaf": leaf, "leaf_err": {}, "dated": dated_by_scope}


def cmd_selftest(_argv: list) -> int:
    s3 = _client("s3")
    dated = {sc: dated_gold(s3, sc) for sc in SCOPES}
    problems = []
    print("selftest: dated gold category-views objects read: %s" % ", ".join("%s=%d" % (sc, len(dated[sc])) for sc in SCOPES))
    ctx = _synthetic_ctx(dated)
    base = _run(ctx, ("H2", "H3", "H4", "H5"))
    for n, s in base:
        if s != "PASS":
            problems.append("base %s did not PASS on the synthetic leaves" % n)

    # a positive control for the null rule: remove the Supervised node from one real dated object (global); the assembled leaf must hold null
    sc, d = "global", sorted(dated["global"])[len(dated["global"]) // 2]
    mutated = copy.deepcopy(dated)
    obj = json.loads(mutated[sc][d])
    del obj["nodes"]["Client"]["children"][CLIENT_NAMES[0]]
    mutated[sc][d] = json.dumps(obj).encode("utf-8")
    ctx_null = _synthetic_ctx(mutated)
    i = ctx_null["leaf"][sc]["dates"].index(d)
    print("selftest: positive control (node removed at %s %s): leaf cell is %r" % (sc, d, ctx_null["leaf"][sc]["client_supervised"][i]))
    if ctx_null["leaf"][sc]["client_supervised"][i] is not None:
        problems.append("a missing node did not assemble to null")
    if h3(ctx_null)[0] != "PASS":
        problems.append("H3 refused the null rule's own leaf")

    # D1: the missing node read as 0.0
    d1 = copy.deepcopy(ctx_null)
    d1["leaf"][sc]["client_supervised"][i] = 0.0
    r = h3(d1)[0]
    print("  PLANT D1 a missing node read as 0.0 -> H3 %s (%s)" % (r, "expected RED" if r == "FAIL" else "NOT RED"))
    if r != "FAIL":
        problems.append("D1 did not turn H3 RED")

    # D2: an unsorted date (two dates and their cells swapped together, so only the order is broken)
    d2 = copy.deepcopy(ctx)
    lf = d2["leaf"]["global"]
    j = len(lf["dates"]) // 2
    for key in ("dates", "client_supervised", "client_unsupervised"):
        lf[key][j], lf[key][j + 1] = lf[key][j + 1], lf[key][j]
    r = h4(d2)[0]
    print("  PLANT D2 an unsorted date -> H4 %s (%s)" % (r, "expected RED" if r == "FAIL" else "NOT RED"))
    if r != "FAIL":
        problems.append("D2 did not turn H4 RED")

    # D3: an extra field
    d3 = copy.deepcopy(ctx)
    d3["leaf"]["global"]["account_ids"] = ["x"]
    r = h5(d3)[0]
    print("  PLANT D3 an extra field -> H5 %s (%s)" % (r, "expected RED" if r == "FAIL" else "NOT RED"))
    if r != "FAIL":
        problems.append("D3 did not turn H5 RED")

    for p in problems:
        print("selftest PROBLEM: %s" % p)
    print("ROUND 7 HISTORY READBACK SELFTEST: %s" % ("OK" if not problems else "FAILED"))
    return 0 if not problems else 1


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("read", "selftest"):
        print(__doc__)
        return 2
    return {"read": cmd_read, "selftest": cmd_selftest}[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
