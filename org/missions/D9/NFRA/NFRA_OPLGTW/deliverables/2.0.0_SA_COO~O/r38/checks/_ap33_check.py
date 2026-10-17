"""OPLGTW OG-ap-33 check helper: grades the landing of the AMGT_HARVST release 319c9413a2 on trunk, one mode per criterion.

Usage: python _ap33_check.py <record.json> 1|2|3
Record keys: trunk_base_sha, hvst_sha, release_sha, merge_sha[, stop_row].
  mode 1: the merge commit has exactly the parents trunk_base_sha and hvst_sha; hvst_sha is an ancestor; no conflict marker in any conflicted path.
  mode 2: gateway live bytes: each conflicted path under the gateway app/, deploy script, lib or dashboard equals its blob at release_sha (or trunk_base's when
          release_sha does not carry it), EXCEPT the two three-way paths (CTO decisions 35436 and 35438: app/tools.py, app/destructive_ops.py), which keep BOTH
          sides in trunk's order: no live line lost and no trunk line lost (line multisets), every line merged adds over live exists in trunk_base and every line
          it adds over trunk_base exists in release_sha, and harvest_get_published_analysis is imported (tools.py), registered (tools.py) and allowlisted
          (destructive_ops.py) EXACTLY once each; each conflicted gateway test equals trunk_base's; the registry file legacy_addresses.json equals trunk_base's;
          the EC2_MANIFEST opal-gateway block equals trunk_base's. deploy-to-ec2.sh is a live-blob path (OG-db-1's preflight is re-landed by OG-db-2).
  mode 3: both sides kept: each conflicted mcportal change_management entry carries every non-blank line of both sides; the billing IAM Terraform file carries every
          line either side added to the merge base, or the record names a stop row and no merge exists.
Counts and booleans only; prints RESULT: PASS or RESULT: FAIL as its last line.
"""
import json
import subprocess
import sys

GW = "infra/aws/ec2/opal-gateway"
MANIFEST = "infra/aws/ec2/EC2_MANIFEST.json"
TF = "infra/aws/terraform/opal-gateway/advi_billing_gateway_iam.tf"
LIVE_PREFIXES = (GW + "/app/", GW + "/lib/", GW + "/dashboard/", GW + "/deploy-to-ec2.sh")
CM = "org/critical_paths/change_management/"
REG = "infra/logic/registry/legacy_addresses.json"
MERGE3 = (GW + "/app/tools.py", GW + "/app/destructive_ops.py")
MARKERS = (b"<<<<<<< ", b"\n=======\n", b">>>>>>> ")


def git(*args, check=True):
    r = subprocess.run(["git"] + list(args), capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit("git %s failed rc=%d: %s" % (args, r.returncode, r.stderr.decode("utf-8", "replace")[:200]))
    return r


def blob(ref, path):
    r = git("show", "%s:%s" % (ref, path), check=False)
    return r.stdout if r.returncode == 0 else None


def conflicts(base, hvst):
    r = git("merge-tree", "--write-tree", "--name-only", base, hvst, check=False)
    lines = r.stdout.decode("utf-8", "replace").split("\n")
    out = []
    for ln in lines[1:]:
        if ln == "":
            break
        out.append(ln.strip())
    return out


def keeps_both(live, trunk, merged):
    """CTO 35436/35438: no live line lost, no trunk line lost (line multisets); what merged adds over live exists in trunk, what it adds over trunk exists in live."""
    import collections
    lc, tc, mc = (collections.Counter((x or b"").decode("utf-8", "replace").splitlines()) for x in (live, trunk, merged))
    if (lc - mc) or (tc - mc):
        return False
    return all(k in tc for k in (mc - lc)) and all(k in lc for k in (mc - tc))


def once_each(path, merged):
    s = (merged or b"").decode("utf-8", "replace")
    if path.endswith("/tools.py"):
        return s.count("harvest_published as _hvpub") == 1 and s.count("def harvest_get_published_analysis(") == 1
    return s.count('"harvest_get_published_analysis"') == 1


def lineset(b):
    return {x.strip() for x in (b or b"").decode("utf-8", "replace").split("\n") if x.strip()}


def main():
    rec = json.load(open(sys.argv[1], encoding="utf-8"))
    mode = sys.argv[2]
    base, hvst, rel, merge = (rec.get(k, "") for k in ("trunk_base_sha", "hvst_sha", "release_sha", "merge_sha"))
    stop = rec.get("stop_row")
    ok = True
    confl = conflicts(base, hvst)
    print("conflicted paths (merge-tree of trunk_base and hvst, the denominator): %d" % len(confl))
    if mode == "3" and stop and not merge:
        print("stop row named (%s) and no merge exists" % stop)
        print("RESULT: PASS")
        return 0
    if git("cat-file", "-e", merge + "^{commit}", check=False).returncode != 0:
        print("merge_sha is not a commit here")
        print("RESULT: FAIL")
        return 1
    if mode == "1":
        parents = git("rev-list", "--parents", "-n", "1", merge).stdout.decode().split()[1:]
        pok = parents == [git("rev-parse", base).stdout.decode().strip(), git("rev-parse", hvst).stdout.decode().strip()]
        anc = git("merge-base", "--is-ancestor", hvst, merge, check=False).returncode == 0
        marked = [p for p in confl if any(m in (blob(merge, p) or b"") for m in MARKERS)]
        print("merge parents are exactly trunk_base and hvst: %s; hvst is an ancestor of the merge: %s; conflict markers in %d of %d paths (want 0)"
              % ("yes" if pok else "no", "yes" if anc else "no", len(marked), len(confl)))
        ok = pok and anc and not marked and len(confl) > 0
    elif mode == "2":
        live = [p for p in confl if p.startswith(LIVE_PREFIXES) and p not in MERGE3]
        tw = [p for p in confl if p in MERGE3]
        tests = [p for p in confl if p.startswith(GW + "/tests/")]
        live_ok = sum(1 for p in live if blob(merge, p) == (blob(rel, p) if blob(rel, p) is not None else blob(base, p)))
        tests_ok = sum(1 for p in tests if blob(merge, p) == blob(base, p))
        tw_ok = sum(1 for p in tw if keeps_both(blob(rel, p), blob(base, p), blob(merge, p)) and once_each(p, blob(merge, p)))
        reg_ok = (REG not in confl) or blob(merge, REG) == blob(base, REG)
        man_ok = False
        try:
            a = json.loads(blob(merge, MANIFEST))["services"]["opal-gateway"]
            b = json.loads(blob(base, MANIFEST))["services"]["opal-gateway"]
            man_ok = a == b
        except Exception:
            man_ok = False
        print("gateway live-byte paths %d of %d equal the release blobs; gateway test paths %d of %d equal trunk's; manifest opal-gateway block equals trunk's: %s"
              % (live_ok, len(live), tests_ok, len(tests), "yes" if man_ok else "no"))
        print("three-way paths %d of %d keep both sides once each; registry file equals trunk's: %s" % (tw_ok, len(tw), "yes" if reg_ok else "no"))
        ok = live_ok == len(live) and tests_ok == len(tests) and man_ok and tw_ok == len(tw) and reg_ok
    elif mode == "3":
        cms = [p for p in confl if p.startswith(CM)]
        cm_ok = 0
        for p in cms:
            m = lineset(blob(merge, p))
            if lineset(blob(base, p)) <= m and lineset(blob(hvst, p)) <= m:
                cm_ok += 1
        tf_ok = True
        if TF in confl:
            mb = git("merge-base", base, hvst).stdout.decode().strip()
            m = lineset(blob(merge, TF))
            added = (lineset(blob(base, TF)) | lineset(blob(hvst, TF))) - lineset(blob(mb, TF))
            tf_ok = added <= m and not any(mk in (blob(merge, TF) or b"") for mk in MARKERS)
        print("mcportal change_management entries %d of %d carry both sides; billing IAM Terraform carries both sides' added lines: %s"
              % (cm_ok, len(cms), "yes" if tf_ok else "no"))
        ok = cm_ok == len(cms) and tf_ok
    print("RESULT: PASS" if ok else "RESULT: FAIL")
    return 0 if ok else 1


sys.exit(main())
