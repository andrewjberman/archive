"""HVST-ce-2 census (read-only). The effect of the round-90 pdf line rule on the
whole silver research-report population. Run from the worktree root:

    python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~156/ce2_census.py

Reads ONLY: the silver research-report parts (amgt/harvest/silver/research-report/,
read via store.silver_latest) and each row's extraction object (v2 when it
exists, else v1, via continuation._read_reports_with_bytes). Every S3 call goes
through the repo shim `.tools/aws` (s3api list-objects-v2 / get-object only).
Nothing is written to S3. Budget: at most 800 requests and 500 MiB, enforced.

Method: the BEFORE arm is continuation.py at HEAD (git show HEAD:...), loaded as a
second module; the AFTER arm is the working-tree continuation.py. Both run
_resolve_fund_and_position on the same items. typed.reports_for is replaced by the
same filter-and-order over the silver rows read ONCE (the reader's own
_order_reports), so each silver part is fetched once, not once per security.
"""
import importlib.util
import io
import json
import os
import subprocess
import sys

ROOT = os.getcwd()
sys.path.insert(0, ROOT)
DELIV = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~156"
SCRATCH = os.path.join(ROOT, ".scratch", "ce2")
os.makedirs(SCRATCH, exist_ok=True)

from botocore.exceptions import ClientError  # noqa: E402

from lib.research.corpus import continuation as new_mod  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BUDGET_REQUESTS = 363  # AMENDMENT 1 remaining budget: order total 1200, used 837 before this run
BASE_COMMIT = "8005ccbacb"  # the pre-round-90 base: the BEFORE arm of every census reading
BUDGET_BYTES = 480 * 1024 * 1024  # AMENDMENT 1 remaining bytes (order total 700 MiB)
ALL_SECURITIES_IN_TABLE = 94

# the msys-safe spawn helper (native python -> bash -> the aws shim)
sys.path.insert(0, os.path.join(ROOT, ".tools"))
_spec = importlib.util.spec_from_file_location("msys_argv_guard", os.path.join(ROOT, ".tools", "msys_argv_guard.py"))
_guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_guard)


class BudgetExceeded(RuntimeError):
    pass


class ShimS3:
    """get_object / get_paginator('list_objects_v2') over `.tools/aws s3api`."""

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
        return [{"Key": o["Key"]} for o in (body.get("Contents") or [])]

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


client = ShimS3()

# --- the BEFORE arm: continuation.py at HEAD, as a second module
head_src = subprocess.run(["git", "show", BASE_COMMIT + ":lib/research/corpus/continuation.py"],
                          capture_output=True, check=True, cwd=ROOT).stdout
head_path = os.path.join(SCRATCH, "continuation_head.py")
with open(head_path, "wb") as fh:
    fh.write(head_src)
_hspec = importlib.util.spec_from_file_location("continuation_head", head_path)
old_mod = importlib.util.module_from_spec(_hspec)
_hspec.loader.exec_module(old_mod)

# --- the silver rows: read ONCE through the store's own silver reader
latest = store.silver_latest(typed.SOURCE, typed.TABLE, typed.RECORD_KEY_FIELDS, client=client)
silver_rows = list(latest.values())
all_securities = sorted({r.get("security_key") for r in silver_rows})
print("DENOMINATOR silver_rows=%d distinct_securities=%d (table denominator %d)"
      % (len(silver_rows), len(all_securities), ALL_SECURITIES_IN_TABLE))


def _reports_for(security_key, client=None):
    rows = [r for r in silver_rows if r.get("security_key") == security_key]
    return typed._order_reports(rows)


typed.reports_for = _reports_for


def _flat(text, n):
    if text is None:
        return "absent"
    return (text[:n]).replace("\r", " ").replace("\n", " ").replace("\t", " ")


out_lines = []
value_to_value = []
absent_before_changed = 0
changed_lines = 0
changed_fund = 0
changed_position = 0
ran = 0
unreadable = []

for sk in all_securities:
    try:
        items_raw = new_mod._read_reports_with_bytes(sk, client=client)
        items = [(row, doc) for row, _raw, doc, _rk in items_raw]
        bykey = {row["bronze_key"]: row["report_id"] for row, _raw, _doc, _rk in items_raw}
        f_b, p_b = old_mod._resolve_fund_and_position(items)
        f_a, p_a = new_mod._resolve_fund_and_position(items)
    except BudgetExceeded:
        raise
    except Exception as exc:  # a security whose extraction cannot be read
        unreadable.append(sk)
        out_lines.append("UNREADABLE %s %s" % (sk, ("%s: %s" % (type(exc).__name__, str(exc)))[:200].replace("\n", " ")))
        continue
    ran += 1

    fv_b = f_b["value"]
    fv_a = f_a["value"]
    pv_b = p_b["value"]
    pv_a = p_a["value"]
    fund_changed = fv_b != fv_a
    pos_changed = pv_b != pv_a
    if fund_changed:
        changed_fund += 1
    if pos_changed:
        changed_position += 1
    # AMENDMENT 1 check: a value-to-value change is a change where BEFORE and AFTER are both values and differ
    # (fund_of_record or last_stated_position). Expected 0.
    if (fv_b is not None and fv_a is not None and fv_b != fv_a) or \
            (pv_b is not None and pv_a is not None and pv_b != pv_a):
        value_to_value.append(sk)
    if not (fund_changed or pos_changed):
        continue
    if fv_b is None and pv_b is None:
        absent_before_changed += 1

    ids = []
    if fund_changed and f_a.get("citation"):
        ids.append(bykey.get(f_a["citation"]["report_key"], f_a["citation"]["report_key"]))
    if pos_changed and p_a.get("citation"):
        rid = bykey.get(p_a["citation"]["report_key"], p_a["citation"]["report_key"])
        if rid not in ids:
            ids.append(rid)
    changed_lines += 1
    out_lines.append("CHANGED %s fund_before=%s fund_after=%s position_before=%s position_after=%s report_id=%s" % (
        sk,
        fv_b if fv_b is not None else "absent",
        fv_a if fv_a is not None else "absent",
        _flat(pv_b["text"], 60) if pv_b else "absent",
        _flat(pv_a["text"], 60) if pv_a else "absent",
        "+".join(ids) if ids else "none",
    ))

out_lines.append("CHANGED_LINES %d" % changed_lines)
out_lines.append("ABSENT_BEFORE_BOTH=%d of CHANGED=%d" % (absent_before_changed, changed_lines))
for _sk in value_to_value:
    out_lines.append("VALUE_TO_VALUE_SECURITY %s" % _sk)
out_lines.append("VALUE_TO_VALUE=%d" % len(value_to_value))
out_lines.append("BUDGET requests=%d lists=%d gets=%d nosuchkey=%d bytes=%d" % (
    client.lists + client.gets, client.lists, client.gets, client.nosuchkey, client.get_bytes))
out_lines.append("CENSUS securities=%d changed_fund=%d changed_position=%d gets=%d bytes=%d" % (
    ran, changed_fund, changed_position, client.gets, client.get_bytes))

path = os.path.join(ROOT, DELIV, "ce2_census.out")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(out_lines) + "\n")
print("WROTE %s lines=%d" % (path, len(out_lines)))
