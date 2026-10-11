"""ADVI_FIRMBKTS round 4 check for cell FB-g-27 (act 3c: the exec-summary generator's fence row for the canonical advisors
directory; the CTO's round-3 ADDENDUM 11), issuer 2.0.0_SA_COO~B1.

Reads the registry as JSON and the module through `terraform console` on mirror trees (no provider, no AWS).

--arms row [--root <tree>] [--base <ref>]  (4 arms)
  E1 the registry adds EXACTLY ONE scoped row under opal-data-49financial, for `exec-summary-generator-role`, `actions`
     exactly [s3:GetObject, s3:ListBucket, s3:PutObject] (no PutObjectAcl, no Delete), `prefix` exactly the one directory the
     module's `class_prefix` gives for the legacy class `platinum/advisors/`; every base row, every other bucket and the
     `grants` object are byte-identical; the row carries a reason and a signoff_ref naming the act 3c pair.
  E2 the module's render of the real registry: the bucket's Allow statements are the base's plus exactly two for the new
     principal (Get on the directory, List bounded to it) and NO Allow names a write action; the Deny statements for the new
     row carry s3:PutObject in the any-other-action NotAction and the objects-outside-prefix Action, with NotResource the
     directory; `fence_exemption_arns` gains exactly that role.
  E3 every OTHER bucket's scoped and allow statements are unchanged.
  E4 the real registry plans clean in the tree's module.
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r4_modallow as ma  # noqa: E402

BUCKET = ma.BUCKET
ROLE = "arn:aws:iam::313476888478:role/exec-summary-generator-role"
LEGACY = "platinum/advisors/"


def _lst(x):
    return x if isinstance(x, list) else [x]


def _txt(root, ref, path):
    if ref:
        return ma._git(root, "show", "%s:%s" % (ref, path)).stdout
    return open(os.path.join(root, *path.split("/")), encoding="utf-8").read()


def row(root, base):
    res = []
    t = json.loads(_txt(root, None, ma.REGF))
    b = json.loads(_txt(root, base, ma.REGF))
    rows_t, rows_b = t["exemptions"].get(BUCKET, []), b["exemptions"].get(BUCKET, [])
    added = rows_t[len(rows_b):]
    others = all(t["exemptions"].get(k) == v for k, v in b["exemptions"].items() if k != BUCKET)
    same_grants = t.get("grants") == b.get("grants")
    with tempfile.TemporaryDirectory() as td:
        head = ma._mirror(os.path.join(td, "head"), root, None)
        basem = ma._mirror(os.path.join(td, "base"), root, base)
        cp = (ma._eval(head, "local.class_prefix") or {}).get("49financial", {})
        directory = cp.get(LEGACY)
        r = added[0] if len(added) == 1 else {}
        arn = r.get("arn") or r.get("principal")
        pre = r.get("prefix")
        ok1 = (len(added) == 1 and rows_t[:len(rows_b)] == rows_b and others and same_grants and arn == ROLE
               and sorted(r.get("actions", [])) == ["s3:GetObject", "s3:ListBucket", "s3:PutObject"]
               and (pre if isinstance(pre, list) else [pre]) == [directory] and bool(directory)
               and str(r.get("reason", "")).strip() != "" and "ACT3C" in str(r.get("signoff_ref", "")).upper().replace("_", ""))
        print("  E1 added=%d base kept=%s others same=%s grants same=%s directory=%s" % (
            len(added), rows_t[:len(rows_b)] == rows_b, others, same_grants, directory))
        res.append(("E1 the registry adds exactly the one exec-summary scoped row and nothing else", ok1))

        a_t = (ma._eval(head, "local.fence_scoped_allow_statements") or {})
        a_b = (ma._eval(basem, "local.fence_scoped_allow_statements") or {})
        d_t = (ma._eval(head, "local.fence_scoped_statements") or {})
        d_b = (ma._eval(basem, "local.fence_scoped_statements") or {})
        n_t = (ma._eval(head, "local.fence_exemption_arns") or {}).get(BUCKET, [])
        n_b = (ma._eval(basem, "local.fence_exemption_arns") or {}).get(BUCKET, [])
        new_allow = [s for s in a_t.get(BUCKET, []) if s not in a_b.get(BUCKET, [])]
        writes = [s for s in a_t.get(BUCKET, []) if any(x in ("s3:PutObject", "s3:PutObjectAcl", "s3:*")
                                                          for x in _lst(s.get("Action", [])))]
        new_deny = [s for s in d_t.get(BUCKET, []) if s not in d_b.get(BUCKET, [])]
        obj = [s for s in new_deny if "ObjectsOutsidePrefix" in str(s.get("Sid"))]
        anyo = [s for s in new_deny if "AnyOtherAction" in str(s.get("Sid"))]
        ok2 = (len(new_allow) == 2
               and all((s.get("Principal") or {}).get("AWS") == ROLE for s in new_allow)
               and sorted(x for s in new_allow for x in _lst(s.get("Action"))) == ["s3:GetObject", "s3:ListBucket"]
               and not writes
               and len(obj) == 1 and sorted(_lst(obj[0].get("Action"))) == ["s3:GetObject", "s3:PutObject"]
               and _lst(obj[0].get("NotResource")) == ["arn:aws:s3:::%s/%s*" % (BUCKET, directory)]
               and len(anyo) == 1 and sorted(_lst(anyo[0].get("NotAction"))) == [
                   "s3:GetObject", "s3:ListBucket", "s3:PutObject"]
               and sorted(set(n_t) - set(n_b)) == [ROLE])
        print("  E2 new allow=%d write allows=%d new deny=%d new exemption arns=%s" % (
            len(new_allow), len(writes), len(new_deny), sorted(set(n_t) - set(n_b))))
        res.append(("E2 the render adds the Get and List Allows and the Put-bearing Deny, no write Allow", ok2))

        same_other = all(d_t.get(k) == v for k, v in d_b.items() if k != BUCKET) and \
            all(a_t.get(k) == a_b.get(k, []) for k in a_t if k != BUCKET)
        print("  E3 other buckets unchanged=%s" % same_other)
        res.append(("E3 every other bucket renders unchanged", same_other))

        rc, _ = ma._plan(head)
        print("  E4 plan rc=%d" % rc)
        res.append(("E4 the real registry plans clean in the tree's module", rc == 0))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("row",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = ma._root(a.root)
    if not shutil.which("terraform"):
        print("ABSENT: terraform is not on PATH")
        print("ROUND 4 EXEC ROW: 0 of 4 arms")
        sys.exit(1)
    try:
        res = row(root, ma._base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:200]))
        res = [("the registry and module readable", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 EXEC ROW: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
