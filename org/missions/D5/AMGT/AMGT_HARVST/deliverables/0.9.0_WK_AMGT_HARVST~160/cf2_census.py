"""HVST-cf-2 census (read-only). The effect of the CS61-FIX rule on the 94 securities of the
silver research-report table: fund_of_record and last_stated_position as the code stood at
HEAD (before the change) against the changed code, on the SAME fetched inputs. Run from the
worktree root (unbuffered, stdout to the .out):

    python -u org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~160/cf2_census.py > .../cf2_census.out

Started from HVST-cf-1's cf1_census.py (the misfiled-reports exclusion is applied as typed.reports_for
applies it). Code under test: lib/research/corpus/continuation.py at the worktree (changed), against
its HEAD revision loaded from `git show HEAD:lib/research/corpus/continuation.py` as a second module.

Reads ONLY (through the repo shim .tools/aws, s3api list-objects-v2 and get-object):
  - the silver research-report parts (store.silver_latest, read ONCE);
  - each row's extraction object (v2 when it exists, else v1; continuation._read_reports_with_bytes).
No gold object is read or written. Nothing is written to S3. Budget enforced: 800 requests, 500 MiB.
"""
import importlib.util
import io
import json
import os
import subprocess
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

ROOT = os.getcwd()
sys.path.insert(0, ROOT)
SCRATCH = os.path.join(ROOT, ".scratch", "cf2")
os.makedirs(SCRATCH, exist_ok=True)
GOLD_PREFIX = "amgt/harvest/gold/research-continuation/security_key=%s/"
BUCKET = "opal-data-harvest"
BUDGET_REQUESTS = 800
BUDGET_BYTES = 500 * 1024 * 1024
ALL_SECURITIES_IN_TABLE = 94
HEAD_PATH = "lib/research/corpus/continuation.py"

from botocore.exceptions import ClientError  # noqa: E402

from lib.research.corpus import continuation as cont  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402

# the msys-safe spawn helper (native python -> bash -> the aws shim)
sys.path.insert(0, os.path.join(ROOT, ".tools"))
_spec =importlib.util.spec_from_file_location("msys_argv_guard", os.path.join(ROOT, ".tools", "msys_argv_guard.py"))
_guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_guard)

# the code as it stood at HEAD, loaded as a second module (the "before")
_head_proc = subprocess.run(["git", "show", "HEAD:" + HEAD_PATH], cwd=ROOT, capture_output=True)
if _head_proc.returncode != 0:
    raise SystemExit("git show HEAD:%s rc=%d: %s" % (HEAD_PATH, _head_proc.returncode,
                                                      _head_proc.stderr.decode("utf-8", "replace")[:300]))
_head_file = os.path.join(SCRATCH, "continuation_head.py")
with open(_head_file, "wb") as fh:
    fh.write(_head_proc.stdout)
_head_spec = importlib.util.spec_from_file_location("continuation_head", _head_file)
head = importlib.util.module_from_spec(_head_spec)
_head_spec.loader.exec_module(head)


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


def short(text, n=60):
    if text is None:
        return "absent"
    return text[:n].replace("\r", " ").replace("\n", " ").replace("\t", " ")


def stance_of(position_field):
    value = position_field.get("value")
    if value is None:
        return "none"
    return value.get("stance", "holding")


def field_text(field):
    return field["value"] if field.get("value") is not None else "absent"


client = ShimS3()

# --- the silver rows: read ONCE through the store's own silver reader
latest = store.silver_latest(typed.SOURCE, typed.TABLE, typed.RECORD_KEY_FIELDS, client=client)
silver_rows = list(latest.values())
all_securities = sorted({r.get("security_key") for r in silver_rows})
print("# DENOMINATOR silver_rows=%d distinct_securities=%d (table denominator %d)"
      % (len(silver_rows), len(all_securities), ALL_SECURITIES_IN_TABLE))
print("# METHOD before = continuation.py at HEAD (git show HEAD:%s, loaded as a second module); "
      "after = the worktree continuation.py; both run on the SAME items from _read_reports_with_bytes" % HEAD_PATH)
print("# METHOD CHANGED = fund_of_record or last_stated_position differs in value, absent reason or key set; "
      "position_before/after = the first 60 characters of the value text")
print("# METHOD stance_after = the after value's stance (holding when the key is absent), none when the position is absent")

# the misfiled-reports exclusion, as typed.reports_for applies it (the silver read is not repeated)
excluded = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
print("# EXCLUSION typed.MISFILED_REPORTS applied as typed.reports_for does: %s"
      % ",".join("%s:%s" % (e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS))


def _reports_for(security_key, client=None):
    rows = [r for r in silver_rows if r.get("security_key") == security_key
            and (r.get("security_key"), r.get("report_id")) not in excluded]
    return typed._order_reports(rows)


typed.reports_for = _reports_for

changed_fund = []
changed_position = []
changed_lines = []
holding_changed = []
jp_section_fixed = []
records = 0
unreadable = []
cand_mismatch = []

for sk in all_securities:
    try:
        items_raw = cont._read_reports_with_bytes(sk, client=client)
        items = [(row, doc) for row, _raw, doc, _rk in items_raw]
    except BudgetExceeded:
        raise
    except Exception as exc:  # a security whose extraction cannot be read
        unreadable.append(sk)
        print("UNREADABLE %s %s" % (sk, ("%s: %s" % (type(exc).__name__, str(exc)))[:200].replace("\n", " ")))
        continue
    records += 1

    before_fund, before_pos = head._resolve_fund_and_position(items)
    after_fund, after_pos = cont._resolve_fund_and_position(items)

    # the candidate lists must be identical: only the stance rule and the heading rule move
    before_cands = head._recommendation_candidates_ex(items)[0]
    after_cands = cont._recommendation_candidates_ex(items)[0]
    if [(c[0].get("report_id"), c[2], c[3]) for c in before_cands] != \
            [(c[0].get("report_id"), c[2], c[3]) for c in after_cands]:
        cand_mismatch.append(sk)

    fund_differs = before_fund != after_fund
    position_differs = before_pos != after_pos
    if not (fund_differs or position_differs):
        continue

    before_text = before_pos["value"]["text"] if before_pos.get("value") else None
    after_text = after_pos["value"]["text"] if after_pos.get("value") else None
    stance_after = stance_of(after_pos)

    # HOLDING_CHANGED: a name whose before-value came from a holding line and changed
    before_fund_line = None
    for c in before_cands:
        if cont._FUND_TOKEN_RE.search(c[3]):
            before_fund_line = c[3]
            break
    before_pos_is_holding = bool(before_cands) and cont._line_stance(before_cands[0][3]) == "holding"
    before_fund_is_holding = before_fund_line is not None and cont._line_stance(before_fund_line) == "holding"
    if (fund_differs and before_fund_is_holding) or (position_differs and before_pos_is_holding):
        holding_changed.append(sk)

    if fund_differs:
        changed_fund.append(sk)
    if position_differs:
        changed_position.append(sk)

    if before_text is not None and cont._is_not_recommendation_heading(before_text) and after_pos.get("value") is None:
        jp_section_fixed.append(sk)

    changed_lines.append((sk, stance_after,
                          "CHANGED %s fund_before=%s fund_after=%s position_before=%s position_after=%s stance_after=%s" % (
                              sk, short(field_text(before_fund), 200), short(field_text(after_fund), 200),
                              short(before_text), short(after_text), stance_after)))

for _sk, _stance, line in changed_lines:
    print(line)

allowed = defaultdict(int)
for _sk, stance, _line in changed_lines:
    allowed[stance] += 1
print("ALLOWED_CLASS candidate=%d template=%d unclassified=%d"
      % (allowed["candidate"], allowed["template"], allowed["unclassified"]))
print("HOLDING_CHANGED=%d%s" % (len(holding_changed), (" " + ",".join(holding_changed)) if holding_changed else ""))
print("# CANDIDATE_LIST_MISMATCH=%d%s" % (len(cand_mismatch), (" " + ",".join(cand_mismatch)) if cand_mismatch else ""))
print("JP_SECTION_FIXED=%d%s" % (len(jp_section_fixed), (" " + ",".join(jp_section_fixed)) if jp_section_fixed else ""))
print("# BUDGET requests=%d lists=%d gets=%d nosuchkey=%d bytes=%d" % (
    client.lists + client.gets, client.lists, client.gets, client.nosuchkey, client.get_bytes))
print("CENSUS-CS61-FIX securities=%d changed_fund=%d changed_position=%d gets=%d bytes=%d" % (
    records, len(changed_fund), len(changed_position), client.gets, client.get_bytes))
