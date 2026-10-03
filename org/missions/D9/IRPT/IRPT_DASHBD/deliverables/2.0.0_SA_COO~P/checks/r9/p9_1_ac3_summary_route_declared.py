"""DB9-1-AC3 -- the summary read is DECLARED on the same read Lambda: the handler's ROUTES and the Terraform route agree.

Grades:
  - infra/aws/lambda/investor-reporting/reporting/entry.py, imported, carries a ROUTES key that is a GET under
    /api/scoped/investor-reporting/reporting/ containing "summary", mapped to an operation in ENTRY's operations;
  - the account route "GET /api/scoped/investor-reporting/reporting/{account_id}/{which}" is still in ROUTES (unchanged);
  - that exact summary route key string appears in infra/aws/terraform/investor-reporting/reporting-read/ (locals.tf or api.tf).
Usage: python <this file> <repo_root>
"""
import sys
from pathlib import Path

ENTRY_DIR = "infra/aws/lambda/investor-reporting/reporting"
TF_DIR = "infra/aws/terraform/investor-reporting/reporting-read"
ACCOUNT_ROUTE = "GET /api/scoped/investor-reporting/reporting/{account_id}/{which}"


def fail(msg):
    print("FAIL: " + msg)
    print("DB9-1-AC3 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    sys.path.insert(0, str(root / ENTRY_DIR))
    sys.path.insert(0, str(root))
    try:
        import entry  # noqa: E402
    except Exception as exc:  # noqa: BLE001
        fail("cannot import the read route's entry.py: %s: %s" % (type(exc).__name__, exc))
    routes = getattr(entry, "ROUTES", {})
    if routes.get(ACCOUNT_ROUTE) is None:
        fail("the account route is no longer in ROUTES")
    summ = [k for k in routes if k.startswith("GET /api/scoped/investor-reporting/reporting/") and "summary" in k]
    if len(summ) != 1:
        fail("ROUTES carries %d summary route(s): %s" % (len(summ), summ))
    key = summ[0]
    ops = getattr(getattr(entry, "ENTRY", None), "operations", None) or {}
    if routes[key] not in ops:
        fail("the summary route maps to %r, which is not one of ENTRY's operations %s" % (routes[key], sorted(ops)))
    tf = "".join(p.read_text(encoding="utf-8") for p in sorted((root / TF_DIR).glob("*.tf")))
    if key not in tf:
        fail("the route key %r is not declared in %s" % (key, TF_DIR))
    print("OK: %r -> %s, declared in Terraform; the account route unchanged" % (key, routes[key]))
    print("DB9-1-AC3 PASS")


if __name__ == "__main__":
    main()
