"""ADVI_FIRMBKTS round 4 check for cell FB-g-22 (act 3b's registry rows and the shared-infra wiring: the readers' admission to
opal-data-49financial; the CTO's round-3 ADDENDA 8, 9 and 10), issuer 2.0.0_SA_COO~B1.

It evaluates the tree's REAL registry through the tree's `opal_name` module (terraform console on a mirror tree, no provider,
no AWS) and reads the shared-infra file as text. It touches nothing under the checkout.

--arms policy [--root <tree>] [--base <ref>]  (6 arms)
  P1 the registry's rows: against the base, every existing row of every bucket is byte-identical, and the tree adds exactly the
     permitted set's scoped rows (8: six readers of the ownership key, the performance adapter, the OAI) for opal-data-49financial
     and a top-level `grants` object with exactly the two rows (irpt-holdings-role, irpt-49f-reporting-read-role); every added
     row carries a non-empty reason and a signoff_ref naming the act 3b pair files.
  P2 the grain: every key the rows name is the module's generated ownership key for the firm (never typed another value); the
     performance adapter's prefix list is its holdings gold prefix and the key; the OAI's list is exactly the canonical served
     prefixes of the registered destination classes (the ownership class excluded), each ending /; no wildcard; the actions per
     principal are exactly the permitted set's.
  P3 the module's render of the real registry: `fence_scoped_allow_statements` for the bucket holds exactly the ten Allow
     principals of the permitted set, each at its granted resources only (no Put, no Delete, no bucket-wide resource), and
     `fence_exemption_arns` for the bucket equals the base's list plus the seven new principals (the performance adapter is a
     registry row now); every OTHER bucket's scoped and allow statements are unchanged.
  P4 the shared-infra file: the three hand statements, the performance adapter's data source and the two locals are gone; the
     concat appends `fence_scoped_allow_statements` for the bucket after the scoped Deny statements; the blanket Deny keeps its
     `fence_patterns` and `fence_exemption_arns` lists; nothing else of the file changes (every other base line kept in order).
  P5 the performance adapter's generated Deny equals its hand Deny plus the key: any-other-action NotAction exactly
     [s3:GetObject, s3:ListBucket]; object NotResource exactly {gold prefix*, the key}; listing StringNotLike exactly
     {gold prefix*, the key}.
  P6 the real registry plans clean in the tree's module (plan exit 0).
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r4_modallow as ma  # noqa: E402

BUCKET = ma.BUCKET
ACCOUNT = "313476888478"
TF = "infra/aws/terraform/shared-infra/s3-49financial.tf"
OAI = "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD"
GOLD = "irpt/49financial/gold/holdings_performance_daily/"
READERS = ["lambda-edge-execution-role", "irpt-directory-role", "irpt-export-render-role", "irpt-narrative-role",
           "irpt-status-role", "irpt-ycharts-generate-role"]
GRANTS = ["irpt-holdings-role", "irpt-49f-reporting-read-role"]
ADAPTER = "irpt-performance-adapter-role"


def _role(n):
    return "arn:aws:iam::%s:role/%s" % (ACCOUNT, n)


def _rows(text):
    return json.loads(text)


def _tree_text(root, ref, path):
    if ref:
        return ma._git(root, "show", "%s:%s" % (ref, path)).stdout
    return open(os.path.join(root, *path.split("/")), encoding="utf-8").read()


def _arn_of(r):
    p = r.get("arn") or r.get("principal")
    return p if str(p).startswith("arn:") else _role(p)


def policy(root, base):
    res = []
    reg_t = _rows(_tree_text(root, None, ma.REGF))
    reg_b = _rows(_tree_text(root, base, ma.REGF))
    rows_t = reg_t["exemptions"].get(BUCKET, [])
    rows_b = reg_b["exemptions"].get(BUCKET, [])
    added = rows_t[len(rows_b):]
    others_same = all(reg_t["exemptions"].get(k) == v for k, v in reg_b["exemptions"].items() if k != BUCKET)
    base_kept = rows_t[:len(rows_b)] == rows_b
    sc_names = sorted(_arn_of(r) for r in added)
    want = sorted([_role(n) for n in READERS + [ADAPTER]] + [OAI])
    gr = (reg_t.get("grants") or {}).get(BUCKET, [])
    gr_names = sorted(_arn_of(r) for r in gr)
    gr_other = {k: v for k, v in (reg_t.get("grants") or {}).items() if k != BUCKET}
    has_text = all(str(r.get("reason", "")).strip() and "ACT3B" in str(r.get("signoff_ref", "")).upper().replace("_", "")
                   for r in added + gr)
    ok1 = (others_same and base_kept and sc_names == want and gr_names == sorted(_role(n) for n in GRANTS)
           and not gr_other and has_text and len(added) == 8)
    print("  P1 base rows kept=%s others same=%s added=%d scoped, grants=%d; reason+signoff_ref ok=%s" % (
        base_kept, others_same, len(added), len(gr), has_text))
    res.append(("P1 the registry adds exactly the permitted set's eight scoped rows and two grants rows, nothing else", ok1))

    sys.path.insert(0, os.path.join(root, "lib"))
    sys.path.insert(0, os.path.join(root, "data", "black_diamond", "scripts", "gold"))
    import opal_naming  # noqa: E402
    from lib import platinum_dest as pd  # noqa: E402
    reg = opal_naming._registry()
    classes = reg["platinum_destinations"]["platinum_destinations"]
    own = [r for r in reg["legacy_addresses"]["legacy_addresses"] if str(r.get("key", "")).endswith("-ownership-map")]
    key = None
    for r in own:
        for c in classes:
            if r["template"].startswith(c["legacy_prefix"]):
                key = pd.destination(r["template"], "canonical")[1]
    own_prefix = {c["legacy_prefix"] for c in classes if own and own[0]["template"].startswith(c["legacy_prefix"])}
    served = set()
    for c in classes:
        if c["legacy_prefix"] in own_prefix:
            continue
        dest = pd.destination(c["legacy_prefix"] + "x", "canonical")[1]
        served.add(dest[:-1])
    by_arn = {_arn_of(r): r for r in added}

    def pf(a):
        v = by_arn.get(a, {}).get("prefix")
        return sorted(v if isinstance(v, list) else [v] if v is not None else [])

    def ac(a):
        return sorted(by_arn.get(a, {}).get("actions", []))

    g_ok = all(sorted(r.get("keys", [])) == [key] and sorted(r.get("actions", [])) == ["s3:GetObject"] for r in gr)
    ok2 = (key is not None and all(pf(_role(n)) == [key] and ac(_role(n)) == ["s3:GetObject"] for n in READERS)
           and pf(_role(ADAPTER)) == sorted([GOLD, key]) and ac(_role(ADAPTER)) == ["s3:GetObject", "s3:ListBucket"]
           and pf(OAI) == sorted(served) and ac(OAI) == ["s3:GetObject"] and all(p.endswith("/") for p in pf(OAI))
           and bool(served) and g_ok
           and not any(("*" in p or "?" in p) for r in added for p in (r["prefix"] if isinstance(r["prefix"], list)
                                                                        else [r["prefix"]])))
    print("  P2 key=%s; OAI prefixes=%d expected=%d" % (key, len(pf(OAI)), len(served)))
    res.append(("P2 every grant is the generated key, the adapter holds gold plus the key, the OAI the served prefixes", ok2))

    with tempfile.TemporaryDirectory() as td:
        head = ma._mirror(os.path.join(td, "head"), root, None)
        basem = ma._mirror(os.path.join(td, "base"), root, base)
        allow = ma._eval(head, "local.fence_scoped_allow_statements") or {}
        arns_t = ma._eval(head, "local.fence_exemption_arns") or {}
        arns_b = ma._eval(basem, "local.fence_exemption_arns") or {}
        den_t = ma._eval(head, "local.fence_scoped_statements") or {}
        den_b = ma._eval(basem, "local.fence_scoped_statements") or {}

        al = allow.get(BUCKET, [])
        pr = {}
        for s in al:
            pr.setdefault((s.get("Principal") or {}).get("AWS"), []).append(s)
        want_allow = sorted([_role(n) for n in READERS + GRANTS + [ADAPTER]] + [OAI])
        res_ok = True
        for p, ss in pr.items():
            for s in ss:
                acts = s.get("Action") if isinstance(s.get("Action"), list) else [s.get("Action")]
                if s.get("Effect") != "Allow" or any(a not in ("s3:GetObject", "s3:ListBucket") for a in acts):
                    res_ok = False
                for r in (s.get("Resource") if isinstance(s.get("Resource"), list) else [s.get("Resource")]):
                    if r in ("*", "arn:aws:s3:::%s/*" % BUCKET):
                        res_ok = False
        extra_arns = sorted(set(arns_t.get(BUCKET, [])) - set(arns_b.get(BUCKET, [])))
        want_new = sorted([_role(n) for n in READERS] + [OAI])
        other_same = all(den_t.get(k) == v for k, v in den_b.items() if k != BUCKET) and \
            all(v == [] for k, v in allow.items() if k != BUCKET)
        ok3 = (sorted(pr.keys()) == want_allow and res_ok and extra_arns == [a for a in want_new if a not in
               arns_b.get(BUCKET, [])] and set(want_new) <= set(arns_t.get(BUCKET, [])) and other_same)
        print("  P3 allow principals=%d, new exemption arns=%d, other buckets same=%s" % (len(pr), len(extra_arns),
                                                                                          other_same))
        res.append(("P3 the render holds exactly the ten Allow principals at their granted resources and the new exemptions",
                    ok3))

        # P5
        ds = {s.get("Sid"): s for s in den_t.get(BUCKET, [])}
        idx = None
        for i, r in enumerate(rows_t):
            if r.get("arn") == _role(ADAPTER) or r.get("principal") == ADAPTER:
                idx = [x for x in rows_t if "actions" in x].index(r) + 1
        a_any = ds.get("DenyScopedExemption%dAnyOtherAction" % (idx or 0), {})
        a_obj = ds.get("DenyScopedExemption%dObjectsOutsidePrefix" % (idx or 0), {})
        a_lst = ds.get("DenyScopedExemption%dListingOutsidePrefix" % (idx or 0), {})

        def lst(x):
            return x if isinstance(x, list) else [x]
        ok5 = (idx is not None and sorted(lst(a_any.get("NotAction", []))) == ["s3:GetObject", "s3:ListBucket"]
               and sorted(lst(a_obj.get("NotResource", []))) == sorted(
                   ["arn:aws:s3:::%s/%s*" % (BUCKET, GOLD), "arn:aws:s3:::%s/%s" % (BUCKET, key)])
               and sorted(lst((a_lst.get("Condition", {}).get("StringNotLike", {}) or {}).get("s3:prefix", [])))
               == sorted([GOLD + "*", key]))
        print("  P5 adapter row index=%s" % idx)
        res.append(("P5 the adapter's generated Deny equals its hand Deny plus the key", ok5))

        rc6, _ = ma._plan(head)
        print("  P6 real registry plan rc=%d" % rc6)
        res.append(("P6 the real registry plans clean in the tree's module", rc6 == 0))

    new = _tree_text(root, None, TF)
    old = _tree_text(root, base, TF)
    gone = all(t not in new for t in ("DenyPerformanceAdapter", "irpt_performance_adapter", "f49_adapter_read_prefixes",
                                      "f49_scope"))
    wired = re.search(r"fence_scoped_allow_statements\[aws_s3_bucket\.opal_data_49financial\.bucket\]", new) is not None
    kept_sc = "module.opal_name.fence_scoped_statements[aws_s3_bucket.opal_data_49financial.bucket]" in new
    deny_lists = ("module.opal_name.fence_patterns[\"49financial\"]" in new and
                  "module.opal_name.fence_exemption_arns[aws_s3_bucket.opal_data_49financial.bucket]" in new)
    old_set = set(old.splitlines())
    added_lines = [ln for ln in new.splitlines() if ln not in old_set]
    odd = [ln for ln in added_lines if not (ln.strip().startswith("#") or "fence_scoped_allow_statements" in ln
                                            or not ln.strip())]
    removed = [ln for ln in old.splitlines() if ln not in set(new.splitlines())]
    print("  P4 hand removed=%s wired=%s scoped kept=%s deny lists kept=%s; added lines=%d (unexpected %d), removed=%d" % (
        gone, wired, kept_sc, deny_lists, len(added_lines), len(odd), len(removed)))
    ok4 = gone and wired and kept_sc and deny_lists and not odd
    res.append(("P4 the shared-infra file drops the hand statements, wires the Allow, keeps the rest", ok4))
    order = ["P1", "P2", "P3", "P4", "P5", "P6"]
    res.sort(key=lambda t: order.index(t[0].split()[0]))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("policy",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = ma._root(a.root)
    if not shutil.which("terraform"):
        print("ABSENT: terraform is not on PATH")
        print("ROUND 4 POLICY: 0 of 6 arms")
        sys.exit(1)
    try:
        res = policy(root, ma._base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:200]))
        res = [("the registry, module and file readable at the tree and the base", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 POLICY: %d of 6 arms" % n)
    sys.exit(0 if n == 6 else 1)


if __name__ == "__main__":
    main()
