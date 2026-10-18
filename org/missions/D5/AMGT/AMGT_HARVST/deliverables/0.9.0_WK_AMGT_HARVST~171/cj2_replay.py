"""cj2_replay.py -- AMGT_HARVST HVST-cj-2 step 1d. READ-ONLY replay of the CHANGED gateway research tools against the REAL
stored objects. The gateway is NOT called: the tools run in this process, and their harvest_read._client() is replaced by
a read-only wrapper around store._default_client() that forwards list_objects_v2 and get_object on opal-data-harvest and
refuses every other operation. The audit sink is a recorder (no file is written). The principal is a synthetic
Opal-domain stand-in, as in the offline tests.

Prints cj2_replay.out (newline="\n", ASCII). Also writes the 95 decoded continuation keys to
cj2_continuation_keys.txt here and to tests/fixtures/cj2_continuation_keys.txt (the offline equality arm reads it).

Budget: 3000 requests and 300 MiB, enforced in the wrapper.

Usage, from the worktree root:  python -u <this file>
"""

import io
import os
import sys
from types import SimpleNamespace
from unittest import mock

ROOT = os.getcwd()
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, GW)
sys.path.insert(0, ROOT)

from app import audit, harvest_read as hr, harvest_research as hres  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cj2_replay.out")
KEYS_PATH = os.path.join(HERE, "cj2_continuation_keys.txt")
FIXTURE_PATH = os.path.join(GW, "tests", "fixtures", "cj2_continuation_keys.txt")
BUCKET = "opal-data-harvest"
BUDGET_REQUESTS = 3000
BUDGET_BYTES = 300 * 1024 * 1024
OPAL = "hvst.cj2.replay@opalinvest.com"     # synthetic stand-in principal
TOKEN = crosswalk.SLASH_SAFE_TOKEN
CONTINUATION_TABLE = "amgt/harvest/gold/research-continuation/"


class BudgetExceeded(Exception):
    pass


class ReadOnly(object):
    """Forwards the two read operations on the harvest bucket; counts requests and GET bytes."""

    def __init__(self, client):
        self._c = client
        self.requests = 0
        self.bytes = 0

    def _spend(self):
        self.requests += 1
        if self.requests > BUDGET_REQUESTS or self.bytes > BUDGET_BYTES:
            raise BudgetExceeded("requests=%d bytes=%d" % (self.requests, self.bytes))

    def list_objects_v2(self, **kw):
        if kw.get("Bucket") != BUCKET:
            raise RuntimeError("replay reads %s only; a list named bucket %r" % (BUCKET, kw.get("Bucket")))
        self._spend()
        return self._c.list_objects_v2(**kw)

    def get_object(self, **kw):
        if kw.get("Bucket") != BUCKET:
            raise RuntimeError("replay reads %s only; a get named bucket %r" % (BUCKET, kw.get("Bucket")))
        self._spend()
        resp = self._c.get_object(**kw)
        data = resp["Body"].read()
        self.bytes += len(data)
        if self.bytes > BUDGET_BYTES:
            raise BudgetExceeded("requests=%d bytes=%d" % (self.requests, self.bytes))
        return {"Body": io.BytesIO(data)}

    def __getattr__(self, name):
        raise RuntimeError("replay is read-only: refuses S3 operation %r" % name)


def emit(lines, text):
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    lines.append(safe)


def parts_of(out):
    """The five parts of the research answer, each present (True) or absent (False)."""
    return {
        "dossier": bool(out.get("dossier_key")),
        "continuation": bool(out.get("continuation_key")),
        "ai_fill": bool(out.get("ai_fill_key")),
        "research_reports": bool(out.get("research_reports")),
        "management_roster": out.get("management_roster") is not None,
    }


def fields_line(label, out):
    p = parts_of(out)
    roster = out.get("management_roster") or {}
    exec_ok = bool(roster.get("bloomberg_exec_officers"))
    return ("%s dossier=%s continuation=%s ai_fill=%s reports=%d exec_officers=%s"
            % (label, "yes" if p["dossier"] else "no", "yes" if p["continuation"] else "no",
               "yes" if p["ai_fill"] else "no", len(out.get("research_reports") or []),
               "yes" if exec_ok else "no"))


def decode_child(segment):
    """The canonical raw key of one security_key= child name (the module's rule, read from crosswalk)."""
    return crosswalk.security_key_from_slash_safe(segment) if TOKEN in segment else segment


def continuation_keys(client, lines):
    """The decoded keys of the continuation table's security_key= children, by one delimiter listing."""
    keys = []
    for page in client.get_paginator_list(CONTINUATION_TABLE):
        for common in page.get("CommonPrefixes", []) or []:
            seg = common["Prefix"][len(CONTINUATION_TABLE):].rstrip("/")
            if seg.startswith("security_key="):
                keys.append(decode_child(seg[len("security_key="):]))
    return sorted(set(keys))


class _Listing(object):
    """Adapter for the delimiter listing of the continuation table through the read-only wrapper."""

    def __init__(self, ro):
        self._ro = ro

    def get_paginator_list(self, prefix):
        token = None
        while True:
            kw = {"Bucket": BUCKET, "Prefix": prefix, "Delimiter": "/"}
            if token:
                kw["ContinuationToken"] = token
            resp = self._ro.list_objects_v2(**kw)
            yield resp
            if not resp.get("IsTruncated"):
                return
            token = resp.get("NextContinuationToken")


def main():
    lines = []
    out_handle = open(OUT_PATH, "w", encoding="utf-8", newline="\n")

    def out(text):
        emit(lines, text)
        out_handle.write(lines[-1] + "\n")
        out_handle.flush()

    ro = ReadOnly(store._default_client())
    principal = SimpleNamespace(email=OPAL, tid="11111111-1111-4111-8111-111111111111",
                                oid="22222222-2222-4222-8222-222222222222")
    recorded = []
    with mock.patch.object(hr, "_client", lambda: ro), \
            mock.patch.object(audit, "log_call", lambda *a, **kw: recorded.append(a)), \
            mock.patch.object(hr, "get_current_principal", lambda: principal):
        try:
            out("CJ2-REPLAY-HEADER read-only replay of the changed gateway research tools (app/harvest_research.py) "
                "against stored objects; the gateway is not called; bucket %s; budget requests=%d bytes=%d"
                % (BUCKET, BUDGET_REQUESTS, BUDGET_BYTES))
            keys = continuation_keys(_Listing(ro), lines)
            with open(KEYS_PATH, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(keys) + "\n")
            os.makedirs(os.path.dirname(FIXTURE_PATH), exist_ok=True)
            with open(FIXTURE_PATH, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(keys) + "\n")
            out("CONTINUATION-KEYS n=%d table=%s slash_keys=%d" % (
                len(keys), CONTINUATION_TABLE.rstrip("/"), sum(1 for k in keys if "/" in k)))

            whole_count = 0
            calls = 0
            for req in ("BP/_LN_Equity", "BP-SLASH-_LN_Equity", "NG/_LN_Equity", "NG-SLASH-_LN_Equity"):
                res = hres.harvest_get_research(req)
                calls += 1
                out(fields_line("REPLAY %s" % req, res))
                p = parts_of(res)
                whole = all(p.values())
                whole_count += 1 if whole else 0
                absent = sorted(res.get("parts_absent", {}).keys())
                out("REPLAY-PARTS %s whole=%s absent_parts=%s dossier_key=%s continuation_key=%s ai_fill_key=%s"
                    % (req, "yes" if whole else "no", ",".join(absent) or "none",
                       res.get("dossier_key") or "none", res.get("continuation_key") or "none",
                       res.get("ai_fill_key") or "none"))

            ctl = hres.harvest_get_research("UNH_US_Equity")
            out(fields_line("REPLAY-CONTROL UNH_US_Equity", ctl) + " whole=%s"
                % ("yes" if all(parts_of(ctl).values()) else "no"))

            # the OLD prefix building, as a copy: the requested key is used as it was typed, with no normalizer
            with mock.patch.object(hres, "canonical_security_key", lambda k: k), \
                    mock.patch.object(hres, "slash_safe_key", lambda k: k):
                for req in ("BP/_LN_Equity", "BP-SLASH-_LN_Equity"):
                    old = hres.harvest_get_research(req)
                    out(fields_line("REPLAY-OLD %s" % req, old))

            # the non-partition prefixes the tools build from the caller's spelling, both spellings, read by listing
            for template in ("filings/v1/%s/", "management/v1/%s/", "peers/v1/%s/", "posture/v1/%s/",
                             "scores/v1/%s.json", "drafting/v1/%s.json"):
                for k in ("BP/_LN_Equity", "BP-SLASH-_LN_Equity", "NG/_LN_Equity", "NG-SLASH-_LN_Equity"):
                    prefix = template % k
                    n = 0
                    token = None
                    while True:
                        kw = {"Bucket": BUCKET, "Prefix": prefix}
                        if token:
                            kw["ContinuationToken"] = token
                        resp = ro.list_objects_v2(**kw)
                        n += len(resp.get("Contents", []) or [])
                        if not resp.get("IsTruncated"):
                            break
                        token = resp.get("NextContinuationToken")
                    out("REPLAY-PREFIX %s objects=%d" % (prefix, n))

            out("REPLAY-WHOLE keys=2 forms=4 whole=%d" % whole_count)
            out("REPLAY-TOTALS gets=%d bytes=%d" % (ro.requests, ro.bytes))
        except BudgetExceeded as exc:
            out("BUDGET-EXCEEDED %s -- replay stopped; no REPLAY-WHOLE line" % exc)
            out_handle.close()
            return 2
    out_handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
