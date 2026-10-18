"""ck2_replay.py -- AMGT_HARVST HVST-ck-2 step d (round 96, CTO round-95 analysis section 3 item 2). READ-ONLY.

The CHANGED path-component tools run in this process against the REAL stored objects, for BP/_LN_Equity and NG/_LN_Equity
in BOTH spellings (the key as typed and the canonical partition form), and for the control UNH_US_Equity. The gateway is
NOT called. Their harvest_read._client() is replaced by a read-only wrapper around store._default_client() that forwards
list_objects_v2 and get_object on opal-data-harvest and refuses every other operation. The audit sink is a recorder.

For every tool call the replay records the listings the tool made, and reproduces the union rule on those listings
independently of the tool code: a stored object is REACHED under (template, name relative to the key's prefix); the
canonical object wins a same-name collision. A cell is (tool, key): equal when the raw request and the canonical request
reach the same objects (the same (template, name) and the same stored key).

Budget: 4000 requests and 400 MiB of GET body bytes, enforced in the wrapper; the last line counts both.
Usage, from the worktree root:  python -u <this file>   (writes ck2_replay.out beside itself)
"""

import io
import os
import re
import sys
from types import SimpleNamespace
from unittest import mock

ROOT = os.getcwd()
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, GW)
sys.path.insert(0, ROOT)

from app import audit, harvest_figures as hfig, harvest_identity as hid, harvest_keys as hk  # noqa: E402
from app import harvest_read as hr, harvest_research as hres  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "ck2_replay.out")
CK1_OUT = os.path.join(HERE, "ck1_census.out")
BUCKET = "opal-data-harvest"
BUDGET_REQUESTS = 4000
BUDGET_BYTES = 400 * 1024 * 1024
OPAL = "hvst.ck2.replay@opalinvest.com"             # synthetic stand-in principal
TID = "11111111-1111-4111-8111-111111111111"
OID = "22222222-2222-4222-8222-222222222222"
KEYS = ("BP/_LN_Equity", "NG/_LN_Equity")
CONTROL = "UNH_US_Equity"
QCOLS = ["security_key", "fiscal_year", "mnemonic", "value"]

# the changed path-component templates, with the key replaced by <K> (the tag of a listed prefix)
TAG_SET = (
    "management/v1/<K>/",
    "filings/v1/<K>/",
    "drafting/v1/<K>.json",
    "drafting/v1/<K>",
    "peers/v1/<K>/",
    "scores/v1/<K>.json",
    "scores/v1/<K>",
    "posture/v1/<K>/",
    "derived/model_block/<K>/",
    "derived/model_block_fye/<K>/",
    "packs/<K>/",
    "packs/<K>/input_ledger.json",
    "raw/bloomberg/<K>/",
)


class Budget(Exception):
    pass


class ReadOnly(object):
    """Forwards the two read operations on the harvest bucket; counts requests and GET bytes; records every listing."""

    def __init__(self, client):
        self._c = client
        self.requests = 0
        self.bytes = 0
        self.log = None

    def _spend(self):
        self.requests += 1
        if self.requests > BUDGET_REQUESTS or self.bytes > BUDGET_BYTES:
            raise Budget()

    def list_objects_v2(self, **kw):
        if kw.get("Bucket") != BUCKET:
            raise RuntimeError("replay lists %s only; a list named bucket %r" % (BUCKET, kw.get("Bucket")))
        self._spend()
        resp = self._c.list_objects_v2(**kw)
        if self.log is not None:
            self.log.append((kw.get("Prefix", ""), [o["Key"] for o in resp.get("Contents", []) or []]))
        return resp

    def get_object(self, **kw):
        if kw.get("Bucket") != BUCKET:
            raise RuntimeError("replay reads %s only; a get named bucket %r" % (BUCKET, kw.get("Bucket")))
        self._spend()
        resp = self._c.get_object(**kw)
        data = resp["Body"].read()
        self.bytes += len(data)
        if self.bytes > BUDGET_BYTES:
            raise Budget()
        return {"Body": io.BytesIO(data)}

    def __getattr__(self, name):
        raise RuntimeError("replay is read-only: refuses S3 operation %r" % name)


def fingerprint(prefix, raw, canon):
    """(tag, spelling) of a listed prefix for one key pair; (None, None) when it is not a changed template."""
    if raw == canon:
        spelling_text = [(None, raw)]
    else:
        spelling_text = [(hk.CANONICAL, canon), (hk.LEGACY_RAW, raw)]
    for spelling, text in spelling_text:
        if text in prefix:
            tag = prefix.replace(text, "<K>", 1)
            if tag in TAG_SET:
                return tag, spelling
            return None, None
    return None, None


def reached_of(log, raw, canon):
    """{(tag, name): (stored key, spelling)} of the objects a set of listings reaches; the canonical object wins a collision."""
    reached = {}
    for prefix, keys in log:
        tag, sp = fingerprint(prefix, raw, canon)
        if tag is None:
            continue
        for k in keys:
            name = k[len(prefix):]
            if (tag, name) not in reached or sp == hk.CANONICAL:
                reached[(tag, name)] = (k, sp)
    return reached


def emit(lines, text):
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    lines.append(safe)


def tools():
    """(tool label, call(key)) for every changed path-component tool."""
    return (
        ("harvest_get_research", lambda k: hres.harvest_get_research(k)),
        ("harvest_get_filing_analysis", lambda k: hres.harvest_get_filing_analysis(k)),
        ("harvest_get_peers_and_scores", lambda k: hres.harvest_get_peers_and_scores(k)),
        ("harvest_get_fundamentals:model", lambda k: hfig.harvest_get_fundamentals(k, "model")),
        ("harvest_query_columns:model_block", lambda k: hfig.harvest_query_columns("model_block", QCOLS, security_keys=[k])),
        ("harvest_security_coverage", lambda k: hid.harvest_security_coverage(k)),
    )


def run_call(ro, fn):
    ro.log = []
    try:
        fn()
        return list(ro.log)
    finally:
        ro.log = None


def pair_lines():
    """(key, tag, name) of every PAIR line of ck1_census.out, with equal=yes|no."""
    out = []
    with open(CK1_OUT, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("PAIR "):
                continue
            parts = line.split(" ")
            key, template, name = parts[1], parts[2], parts[3]
            tag = template.replace("%s", "<K>")
            if name == "(object)":
                name = ""
            if tag == "packs/<K>/input_ledger.json":
                # the ledger is read from the packs/ listing (harvest_identity._ledger reads the listed packs/<K>/ rows)
                tag, name = "packs/<K>/", "input_ledger.json"
            m = re.search(r" equal=(yes|no) ", line)
            out.append((key, tag, name, m.group(1) if m else "?"))
    return out


def main():
    lines = []
    out_handle = open(OUT_PATH, "w", encoding="utf-8", newline="\n")

    def out(text):
        emit(lines, text)
        out_handle.write(lines[-1] + "\n")
        out_handle.flush()

    ro = ReadOnly(store._default_client())
    principal = SimpleNamespace(email=OPAL, tid=TID, oid=OID)
    recorded = []
    matrix = {}           # (tool, key) -> {"raw": reached, "canon": reached}
    served = {}           # (key, tag, name) -> (stored key, spelling), over every tool call of the key's raw request
    try:
        with mock.patch.object(hr, "_client", lambda: ro), \
                mock.patch.object(audit, "log_call", lambda *a, **kw: recorded.append(a)), \
                mock.patch.object(hr, "get_current_principal", lambda: principal):
            out("CK2-REPLAY-HEADER read-only replay of the changed path-component tools (app/harvest_research.py, "
                "harvest_figures.py, harvest_identity.py) against stored objects; the gateway is not called; bucket %s; "
                "budget requests=%d bytes=%d" % (BUCKET, BUDGET_REQUESTS, BUDGET_BYTES))
            out("CK2-REPLAY-KEYS raw=%s canonical=%s control=%s"
                % (", ".join(KEYS), ", ".join(crosswalk.slash_safe_key(k) for k in KEYS), CONTROL))
            for label, call in tools():
                for key in KEYS:
                    canon = crosswalk.slash_safe_key(key)
                    cell = {}
                    for side, requested in (("raw", key), ("canon", canon)):
                        log = run_call(ro, lambda r=requested: call(r))
                        reached = reached_of(log, key, canon)
                        cell[side] = reached
                        tags = sorted(set(fingerprint(p, key, canon)[0] for p, _k in log) - {None})
                        if not tags:
                            out("REPLAY-UNION %s:none %s objects_reached=0 from_canonical=0 from_legacy_raw=0" % (label, requested))
                        for tag in tags:
                            mine = [(k, sp) for (t, _n), (k, sp) in reached.items() if t == tag]
                            out("REPLAY-UNION %s:%s %s objects_reached=%d from_canonical=%d from_legacy_raw=%d"
                                % (label, tag, requested, len(mine), sum(1 for _k, sp in mine if sp == hk.CANONICAL),
                                   sum(1 for _k, sp in mine if sp == hk.LEGACY_RAW)))
                        for (t, n), (k, sp) in reached.items():
                            served[(key, t, n)] = (k, sp)
                    matrix[(label, key)] = cell
            for label, call in tools():
                log = run_call(ro, lambda: call(CONTROL))
                reached = reached_of(log, CONTROL, CONTROL)
                out("REPLAY-CONTROL %s %s objects_reached=%d" % (CONTROL, label, len(reached)))
            pairs = pair_lines()
            served_n = 0
            unlisted = 0
            for key, tag, name, eq in pairs:
                if tag not in TAG_SET:
                    continue
                hit = served.get((key, tag, name))
                if hit is None:
                    unlisted += 1
                elif hit[1] == hk.CANONICAL:
                    served_n += 1
            n_pairs = sum(1 for key, tag, name, eq in pairs if tag in TAG_SET)
            out("REPLAY-COLLISIONS same_name_pairs=%d canonical_served=%d" % (n_pairs, served_n))
            out("REPLAY-COLLISIONS-DETAIL pair_lines=%d in_changed_templates=%d not_reached_by_any_tool=%d differ_lines=%d"
                % (len(pairs), n_pairs, unlisted, sum(1 for p in pairs if p[3] == "no")))
            equal = 0
            cells = 0
            for label, _call in tools():
                for key in KEYS:
                    cells += 1
                    cell = matrix[(label, key)]
                    same = cell["raw"] == cell["canon"]
                    equal += 1 if same else 0
                    out("REPLAY-CELL %s %s raw_objects=%d canonical_objects=%d same_objects=%s"
                        % (label, key, len(cell["raw"]), len(cell["canon"]), "yes" if same else "no"))
            out("REPLAY-UNION-WHOLE cells=%d equal=%d" % (cells, equal))
            out("REPLAY-UNION-TOTALS gets=%d bytes=%d" % (ro.requests, ro.bytes))
    except Budget:
        out("BUDGET-EXCEEDED gets=%d bytes=%d -- replay stopped at the budget; no REPLAY-UNION-WHOLE line"
            % (ro.requests, ro.bytes))
        out_handle.close()
        return 2
    out_handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
