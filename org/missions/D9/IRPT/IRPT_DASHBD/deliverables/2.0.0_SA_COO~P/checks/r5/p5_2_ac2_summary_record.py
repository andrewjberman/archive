"""DB5-2-AC2 -- the per-client summary's address is the naming builder's output, and a local dry run over the 49 Financial directory
built one summary per client.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~1/CLIENT_SUMMARY_R5.json:
  {"builder_call": "address(...)", "address_example": "s3://...", "clients": n, "accounts_covered": m, "seconds": s,
   "shape": {...}, "directory_source": "<where the client -> accounts map was read>"}
Grades: address_example starts with "s3://" and names "/platinum/reporting/"; the builder_call, run by THIS check through
lib/opal_naming.py with the record's own arguments, is not refused (the call is eval'd only as address(...) with literal args);
clients > 0 and accounts_covered > 0 and seconds > 0; shape is a non-empty object; directory_source is non-empty.
Usage: python <this file> <repo_root>
"""
import ast
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/CLIENT_SUMMARY_R5.json"


def fail(msg):
    print("FAIL: " + msg)
    print("DB5-2-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    p = root / REC
    if not p.is_file():
        fail("no record at %s" % REC)
    r = json.loads(p.read_text(encoding="utf-8"))
    ex = str(r.get("address_example", ""))
    if not ex.startswith("s3://") or "/platinum/reporting/" not in ex:
        fail("address_example is not a platinum/reporting address: %r" % ex)
    call = str(r.get("builder_call", ""))
    try:
        node = ast.parse(call, mode="eval").body
    except SyntaxError:
        fail("builder_call does not parse: %r" % call)
    if not (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "address"
            and all(isinstance(a, ast.Constant) for a in node.args) and not node.keywords):
        fail("builder_call is not address(<literal args>): %r" % call)
    sys.path.insert(0, str(root / "lib"))
    import opal_naming
    try:
        got = opal_naming.address(*[a.value for a in node.args])
    except Exception as exc:  # noqa: BLE001
        fail("the builder refused the call: %s" % exc)
    if got != ex:
        fail("builder answered %r, the record says %r" % (got, ex))
    for k in ("clients", "accounts_covered", "seconds"):
        try:
            if float(r.get(k)) <= 0:
                fail("%s is not positive" % k)
        except (TypeError, ValueError):
            fail("%s is not a number" % k)
    if not isinstance(r.get("shape"), dict) or not r["shape"]:
        fail("shape is empty")
    if not str(r.get("directory_source", "")).strip():
        fail("directory_source is empty")
    print("OK: builder address %s; %s clients, %s accounts, %ss" % (ex, r["clients"], r["accounts_covered"], r["seconds"]))
    print("DB5-2-AC2 PASS")


if __name__ == "__main__":
    main()
