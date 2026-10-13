"""FB-k-4 read-only helper: summarise saved `aws iam get-role-policy` / `get-policy-version` JSON files.

For each statement prints the Sid, Effect, Action list and Resource list (ARNs and bucket or key patterns;
no condition values, no principal values beyond the ARN shape). Read-only: it opens the files it is given.

Usage: python -I planinv_fb_k4_iam_summary.py <policy.json> [<policy.json> ...]
"""
import json
import sys


def _doc(obj):
    doc = obj.get("PolicyDocument", obj)
    if isinstance(doc, str):
        from urllib.parse import unquote
        doc = json.loads(unquote(doc))
    return doc


def _list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def summarise(path):
    with open(path, encoding="utf-8") as fh:
        obj = json.load(fh)
    doc = _doc(obj)
    print("POLICY %s (role=%s policy=%s)" % (path.split("/")[-1], obj.get("RoleName", "-"), obj.get("PolicyName", "-")))
    for i, st in enumerate(_list(doc.get("Statement"))):
        print("  stmt[%d] sid=%s effect=%s" % (i, st.get("Sid", "-"), st.get("Effect")))
        print("    actions=%s" % ",".join(_list(st.get("Action")) or _list(st.get("NotAction"))))
        print("    resources=%s" % ",".join(_list(st.get("Resource")) or _list(st.get("NotResource"))))
        if "Principal" in st:
            p = st["Principal"]
            print("    principal=%s" % (json.dumps(p) if not isinstance(p, dict) else ",".join(
                "%s:%s" % (k, ",".join(_list(v))) for k, v in p.items())))
        if "Condition" in st:
            print("    condition_keys=%s" % ",".join(sorted(st["Condition"].keys())))


def main(paths):
    for p in paths:
        summarise(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
