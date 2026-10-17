"""HVST-cf-1 census (read-only). What verb each of the 94 securities' RECOMMENDATION
lines uses before its fund token, and which SERVED fund_of_record came from a line
that is not a holding. Run from the worktree root (unbuffered, stdout to the .out):

    python -u org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~159/cf1_census.py > .../cf1_census.out

Code under test: lib/research/corpus/continuation.py at the worktree HEAD (holds HVST-ce-2
and HVST-ce-6). Candidates come from continuation._recommendation_candidates_ex(items);
the fund-supplying candidate is the first candidate whose content names a fund token
(the code's own rule); the position-supplying candidate is the first candidate. The
census re-runs continuation._resolve_fund_and_position and checks its own mirror against it (RECON).

Reads ONLY (through the repo shim .tools/aws, s3api list-objects-v2 and get-object):
  - the silver research-report parts (store.silver_latest, read ONCE);
  - each row's extraction object (v2 when it exists, else v1; continuation._read_reports_with_bytes);
  - for the 31 names in round90/ce4_securities.txt, the newest stored gold object under
    amgt/harvest/gold/research-continuation/security_key=<KEY>/ (by LastModified).
Nothing is written to S3. Budget enforced: 800 requests, 500 MiB.
"""
import importlib.util
import io
import json
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

ROOT = os.getcwd()
sys.path.insert(0, ROOT)
SCRATCH = os.path.join(ROOT, ".scratch", "cf1")
os.makedirs(SCRATCH, exist_ok=True)
CE4_FILE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_W1/round90/ce4_securities.txt")
GOLD_PREFIX = "amgt/harvest/gold/research-continuation/security_key=%s/"
BUCKET = "opal-data-harvest"
BUDGET_REQUESTS = 800
BUDGET_BYTES = 500 * 1024 * 1024
ALL_SECURITIES_IN_TABLE = 94

from botocore.exceptions import ClientError  # noqa: E402

from lib.research.corpus import continuation as cont  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402

# the msys-safe spawn helper (native python -> bash -> the aws shim)
sys.path.insert(0, os.path.join(ROOT, ".tools"))
_spec =importlib.util.spec_from_file_location("msys_argv_guard", os.path.join(ROOT, ".tools", "msys_argv_guard.py"))
_guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_guard)


class BudgetExceeded(RuntimeError):
    pass


class ShimS3:
    def __init__(self):
        self.lists = 0
        self.gets = 0
        self.get_bytes = 0
        self.nosuchkey = 0

    def _spend(self):
        if self.lists + self.gets + 1 > BUDGET_REQUESTS:
            raise BudgetExceeded("request budget %d exceeded" % BUDGET_REQUESTS)

    def _aws(self, args):
        return _guard.msys_safe_run(["bash", ".tools/aws", "s3api"] + args, cwd=ROOT,
                                    capture_output=True, text=True, timeout=120)

    def get_paginator(self, name):
        assert name == "list_objects_v2", name
        return _Paginator(self)

    def list_prefix(self, bucket, prefix):
        self._spend()
        self.lists += 1
        proc = self._aws(["list-objects-v2", "--bucket", bucket, "--prefix", prefix, "--output", "json"])
        if proc.returncode != 0:
            raise RuntimeError("list-objects-v2 rc=%d: %s" % (proc.returncode, proc.stderr.strip()[:300]))
        body = json.loads(proc.stdout or "{}")
        return [{"Key": o["Key"], "LastModified": o.get("LastModified", "")} for o in (body.get("Contents") or [])]

    def get_object(self, Bucket, Key):
        self._spend()
        self.gets += 1
        out = os.path.join(SCRATCH, "obj.bin")
        if os.path.exists(out):
            os.remove(out)
        proc = self._aws(["get-object", "--bucket", Bucket, "--key", Key, out])
        if proc.returncode != 0:
            text = (proc.stderr or "") + (proc.stdout or "")
            if "NoSuchKey" in text or "404" in text or "Not Found" in text:
                self.nosuchkey += 1
                raise ClientError({"Error": {"Code": "NoSuchKey", "Message": text.strip()[:200]}}, "GetObject")
            raise RuntimeError("get-object rc=%d: %s" % (proc.returncode, text.strip()[:300]))
        with open(out, "rb") as fh:
            raw = fh.read()
        os.remove(out)
        self.get_bytes += len(raw)
        if self.get_bytes > BUDGET_BYTES:
            raise BudgetExceeded("byte budget %d exceeded" % BUDGET_BYTES)
        return {"Body": io.BytesIO(raw)}


class _Paginator:
    def __init__(self, client):
        self.client = client

    def paginate(self, Bucket, Prefix):
        yield {"Contents": self.client.list_prefix(Bucket, Prefix)}


def flat(text, n):
    if text is None:
        return "absent"
    return text[:n].replace("\r", " ").replace("\n", " ").replace("\t", " ")


def normalise_phrase(content):
    """content up to (not including) the first fund token, lowercased, digit runs -> <N>,
    whitespace collapsed, trimmed; no fund token -> [no fund token]."""
    m = cont._FUND_TOKEN_RE.search(content)
    if not m:
        return "[no fund token]"
    head = content[:m.start()].lower()
    head = re.sub(r"\d+", "<N>", head)
    head = re.sub(r"\s+", " ", head).strip()
    return head if head else "[empty before fund token]"


client = ShimS3()

# --- the silver rows: read ONCE through the store's own silver reader
latest = store.silver_latest(typed.SOURCE, typed.TABLE, typed.RECORD_KEY_FIELDS, client=client)
silver_rows = list(latest.values())
all_securities = sorted({r.get("security_key") for r in silver_rows})
print("# DENOMINATOR silver_rows=%d distinct_securities=%d (table denominator %d)"
      % (len(silver_rows), len(all_securities), ALL_SECURITIES_IN_TABLE))
print("# METHOD continuation.py at worktree HEAD; candidates = continuation._recommendation_candidates_ex(items); "
      "via=old is the label-start rule, via=line is the pdf-line fallback (one list per security, never mixed)")
print("# METHOD fund-supplier = first candidate whose content names a fund token; position-supplier = first candidate; "
      "phrase = content before the first fund token, lowercased, digit runs -> <N>, whitespace collapsed")
print("# METHOD sort: PHRASE by count descending then phrase ascending; section b counts ONE candidate per security "
      "(the fund-supplier, else the first candidate when it has no fund token); POSITION lists the rest")


def _reports_for(security_key, client=None):
    # the same filter as typed.reports_for (lib/research/corpus/typed.py:596-600): the MISFILED_REPORTS
    # exclusion is part of the code under test, so it is applied here too (the silver read is not repeated)
    excluded = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
    rows = [r for r in silver_rows if r.get("security_key") == security_key
            and (r.get("security_key"), r.get("report_id")) not in excluded]
    return typed._order_reports(rows)


print("# EXCLUSION typed.MISFILED_REPORTS applied as typed.reports_for does: %s"
      % ",".join("%s:%s" % (e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS))
typed.reports_for = _reports_for

# ---------------------------------------------------------------------------
# pass 1: every security, the candidate list and the two supplying candidates
# ---------------------------------------------------------------------------
records = {}
unreadable = []
recon_mismatch = []
for sk in all_securities:
    try:
        items_raw = cont._read_reports_with_bytes(sk, client=client)
        items = [(row, doc) for row, _raw, doc, _rk in items_raw]
        cands_raw, line_only = cont._recommendation_candidates_ex(items)
        fund_field, pos_field = cont._resolve_fund_and_position(items)
    except BudgetExceeded:
        raise
    except Exception as exc:  # a security whose extraction cannot be read
        unreadable.append(sk)
        print("UNREADABLE %s %s" % (sk, ("%s: %s" % (type(exc).__name__, str(exc)))[:200].replace("\n", " ")))
        continue

    via = "line" if line_only else "old"
    cands = []
    for row, document, locator, content in cands_raw:
        m = cont._FUND_TOKEN_RE.search(content)
        cands.append({
            "report_id": row.get("report_id"),
            "report_class": row.get("report_class"),
            "period": row.get("period"),
            "ftype": document.get("type"),
            "locator": locator,
            "content": content,
            "raw": flat(content, 120),
            "phrase": normalise_phrase(content),
            "fund": m.group(1) if m else None,
            "via": via,
        })
    fund_idx = next((i for i, c in enumerate(cands) if c["fund"]), None)
    pos_idx = 0 if cands else None

    # RECON: the census mirror must reproduce the code's own two fields
    code_fund = fund_field["value"]
    mirror_fund = cands[fund_idx]["fund"] if fund_idx is not None else None
    code_pos_text = pos_field["value"]["text"] if pos_field["value"] else None
    mirror_pos_text = cands[0]["content"][:500] if cands else None
    if code_fund != mirror_fund or code_pos_text != mirror_pos_text:
        recon_mismatch.append(sk)
        print("RECON_MISMATCH %s code_fund=%s mirror_fund=%s" % (sk, code_fund, mirror_fund))

    records[sk] = {"cands": cands, "fund_idx": fund_idx, "pos_idx": pos_idx, "via": via,
                   "code_fund": code_fund, "code_pos": pos_field["value"]}

ran = len(records)

# ---------------------------------------------------------------------------
# section b: PHRASE lines (one counted candidate per security)
# ---------------------------------------------------------------------------
phrase_secs = defaultdict(list)   # phrase -> [(sk, cand)]
position_only = []                # (sk, cand) where the position candidate is not the fund candidate
for sk in sorted(records):
    rec = records[sk]
    if not rec["cands"]:
        continue
    if rec["fund_idx"] is not None:
        counted = rec["cands"][rec["fund_idx"]]
    else:
        counted = rec["cands"][0]
    phrase_secs[counted["phrase"]].append((sk, counted))
    if rec["fund_idx"] != rec["pos_idx"]:
        position_only.append((sk, rec["cands"][rec["pos_idx"]]))

ordered = sorted(phrase_secs.items(), key=lambda kv: (-len(kv[1]), kv[0]))
for phrase, members in ordered:
    vias = {c["via"] for _sk, c in members}
    via_tag = "both" if len(vias) > 1 else next(iter(vias))
    examples = [sk for sk, _c in members][:3]
    rep = members[0][1]
    print("PHRASE n=%d | %s | via=%s | e.g. %s | raw=%s" % (
        len(members), phrase, via_tag, ",".join(examples), rep["raw"]))

# variants: every distinct raw under each phrase, with its count (so normalisation hides nothing)
for phrase, members in ordered:
    raws = defaultdict(list)
    for sk, c in members:
        raws[c["raw"]].append(sk)
    if len(raws) > 1:
        for raw, sks in sorted(raws.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            print("VARIANT phrase=%s | n=%d | e.g. %s | raw=%s" % (phrase, len(sks), ",".join(sks[:3]), raw))

# ---------------------------------------------------------------------------
# section c: NAMES (one line per security with a fund_of_record)
# ---------------------------------------------------------------------------
ce4_list = []
with open(CE4_FILE, encoding="utf-8") as fh:
    for line in fh:
        s = line.strip()
        if s:
            ce4_list.append(s)
ce4 = set(ce4_list)
for k in sorted(ce4):
    if k not in records:
        print("CE4_NOT_IN_SILVER %s" % k)

# served objects for the 31 (pass 2, after the code pass)
served = {}
for sk in ce4_list:
    if sk not in records:
        continue
    lst = client.list_prefix(BUCKET, GOLD_PREFIX % sk)
    if not lst:
        served[sk] = {"gold": "ABSENT", "n_objects": 0}
        continue
    newest = sorted(lst, key=lambda o: o["LastModified"])[-1]
    resp = client.get_object(Bucket=BUCKET, Key=newest["Key"])
    doc = json.loads(resp["Body"].read().decode("utf-8"))
    f = (doc.get("fields") or {}).get("fund_of_record") or {}
    p = (doc.get("fields") or {}).get("last_stated_position") or {}
    served[sk] = {
        "gold": os.path.basename(newest["Key"]),
        "n_objects": len(lst),
        "last_modified": newest["LastModified"],
        "method": doc.get("method_version"),
        "fund": f.get("value"),
        "position_text": (p.get("value") or {}).get("text") if isinstance(p.get("value"), dict) else None,
        "position_fund": (p.get("value") or {}).get("fund") if isinstance(p.get("value"), dict) else None,
    }

with_fund = 0
rebuilt_with_fund = 0
for sk in sorted(records):
    rec = records[sk]
    if rec["fund_idx"] is None:
        continue
    with_fund += 1
    fc = rec["cands"][rec["fund_idx"]]
    in_ce4 = sk in ce4
    if in_ce4:
        rebuilt_with_fund += 1
        sv = served.get(sk, {})
        matches = "yes" if sv.get("fund") == fc["fund"] else "no"
    else:
        matches = "n/a"
    print("NAME %s | phrase=%s | fund=%s | via=%s | rebuilt_in_ce4=%s | report_id=%s | served_matches_code=%s"
          " | class=%s period=%s type=%s | raw=%s" % (
              sk, fc["phrase"], fc["fund"], fc["via"], "yes" if in_ce4 else "no", fc["report_id"], matches,
              fc["report_class"], fc["period"], fc["ftype"], fc["raw"]))

# POSITION: the position-supplying candidate where it is not the fund-supplying candidate
for sk, c in position_only:
    print("POSITION %s | phrase=%s | fund=%s | via=%s | report_id=%s | class=%s period=%s type=%s | raw=%s" % (
        sk, c["phrase"], c["fund"], c["via"], c["report_id"], c["report_class"], c["period"], c["ftype"], c["raw"]))

# ---------------------------------------------------------------------------
# section d: NOFUND (first candidate has no fund token) and NOCAND
# ---------------------------------------------------------------------------
with_position = 0
for sk in sorted(records):
    rec = records[sk]
    if not rec["cands"]:
        print("NOCAND %s" % sk)
        continue
    with_position += 1
    if rec["fund_idx"] is None:
        c = rec["cands"][0]
        print("NOFUND %s | phrase=%s | via=%s | report_id=%s | class=%s period=%s type=%s | raw=%s" % (
            sk, c["phrase"], c["via"], c["report_id"], c["report_class"], c["period"], c["ftype"], c["raw"]))

# ---------------------------------------------------------------------------
# served objects for the 31: what the gateway serves from the stored gold now
# ---------------------------------------------------------------------------
for sk in ce4_list:
    if sk not in records:
        continue
    rec = records[sk]
    code_fund = rec["cands"][rec["fund_idx"]]["fund"] if rec["fund_idx"] is not None else None
    sv = served.get(sk, {})
    print("SERVED %s | code_fund=%s | served_fund=%s | served_gold=%s | n_objects=%s | last_modified=%s | method=%s"
          " | served_position_fund=%s | served_position=%s" % (
              sk, code_fund, sv.get("fund"), sv.get("gold"), sv.get("n_objects"), sv.get("last_modified"),
              sv.get("method"), sv.get("position_fund"), flat(sv.get("position_text"), 120)))

print("# RECON mismatches=%d" % len(recon_mismatch))
print("# BUDGET requests=%d lists=%d gets=%d nosuchkey=%d bytes=%d" % (
    client.lists + client.gets, client.lists, client.gets, client.nosuchkey, client.get_bytes))
print("PHRASES distinct=%d" % len(phrase_secs))
print("CENSUS-C-S61 securities=%d with_fund=%d with_position=%d rebuilt_in_ce4=%d gets=%d bytes=%d" % (
    ran, with_fund, with_position, rebuilt_with_fund, client.gets, client.get_bytes))
