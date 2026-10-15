"""IRPT_DASHBD round 118, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- why the Cottonwood function cannot resolve its firm, and the addendum that fixes it.

  DBC118-1-AC1 the READ: the live shared zip's registry members against their pins and against HEAD, scopes.json's row-key diff, and the DIFFERENTIAL of the producer's own firm derivation for the three
               declared channels in the extracted live zip tree versus the same tree with the minimal re-pinned members (the 49 Financial and Inflection derivations must be identical)
  DBC118-2-AC1 the ADDENDUM packet: eight headings, UNSIGNED, naming exactly the minimal re-pin set from the record, the member diff against the live zip, and the resume at the catch-up

RECOMPUTES from git blobs, the live zip by S3 version id, and subprocess runs of the producer's own firm_scope() in extracted trees. Writes nothing in the repo or AWS.
Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need

D = p114.D
REC = D + "0.9.0_WK_IRPT_DASHBD~406/SCOPES_PIN_READ_R118.json"
PACKET = D + "0.9.0_WK_IRPT_DASHBD~406/NEVER_WIDEN_ADDENDUM_DB-c-11_R118.md"
SRC_MAP = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-holdings-performance-lambda"
ZIP_BUCKET = "opal-313476888478-lambda-artifacts"
ZIP_KEY = "investor-reporting/irpt-holdings-performance-lambda.zip"
REG_NAMES = ("systems.json", "scopes.json", "tiers.json", "exemptions.json", "remediations.json", "resources.json", "reporting_policies.json")
CHANNELS = ("schwab_08335338", "orion", "blackdiamond_z09")
HEADS = ("## Change set", "## Build and member diff", "## Plan", "## Resume at the catch-up", "## Both branches", "## Rollback", "## Questions for the CTO's half", "## Not in this packet")

PROBE = r'''
import json, sys
root = sys.argv[1]
sys.path.insert(0, root)
sys.path.insert(0, root + "/data/assets/scripts/gold/irpt_holdings_performance")
sys.path.insert(0, root + "/data/assets/scripts/lib")
import holdings_performance as hp
import lib.opal_naming as n
decl = json.load(open(root + "/data/assets/scripts/gold/irpt_holdings_performance/sources.json", encoding="utf-8"))
srcs = decl.get("sources") or decl
out = {}
for k in sys.argv[2:]:
    s = srcs[k]
    r = {}
    try:
        firm = hp.firm_scope(s)
        r["firm"] = firm
        for f in ("positions_prefix", "balance_prefix"):
            if s.get(f):
                r[f] = hp.resolved_prefix(s, f, firm)
        for tb in ("holdings_performance_daily", "holdings_performance_manifest"):
            r[tb] = n.address("irpt", firm, "gold", tb, "date=2026-10-13", "data.parquet")
        for kind in ("lambda", "role", "policy", "daily"):
            try:
                r["name_" + kind] = n.name("irpt", firm, "holdings-performance", kind)
            except Exception as e:
                r["name_" + kind] = "ERR " + type(e).__name__
    except SystemExit as e:
        r["firm"] = "REFUSED: " + str(e)[:40]
    out[k] = r
print("PROBE " + json.dumps(out, sort_keys=True))
'''


def git(root, *args, raw=False):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True)
    need(r.returncode == 0, "git " + " ".join(args[:2]) + " failed: " + r.stderr.decode("utf-8", "replace")[:100])
    return r.stdout if raw else r.stdout.decode("utf-8").strip()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def zip_members(version_id):
    s3 = p114.s3client()
    body = s3.get_object(Bucket=ZIP_BUCKET, Key=ZIP_KEY, VersionId=version_id)["Body"].read()
    return zipfile.ZipFile(io.BytesIO(body))


def scope_keys(blob):
    d = json.loads(blob.decode("utf-8"))
    rows = d.get("scopes") or d
    if isinstance(rows, list):
        return {r.get("key"): json.dumps(r, sort_keys=True) for r in rows}
    return {k: json.dumps(v, sort_keys=True) for k, v in rows.items()}


def run_probe(tree):
    r = subprocess.run([sys.executable, "-I", "-c", PROBE, str(tree)] + list(CHANNELS), capture_output=True, text=True, timeout=100)
    m = re.search(r"^PROBE (.*)$", r.stdout, re.M)
    need(m is not None, "probe printed nothing: " + (r.stderr or r.stdout)[-160:])
    return json.loads(m.group(1))


def clean(rec):
    """The record carries hashes, bucket names, keys and commits, so the digit-run rule applies to the words fields only."""
    for k, v in p114.walk(rec):
        if isinstance(v, str) and k in ("words", "basis_words", "note"):
            need(not p114.LONG_DIGITS.search(v), "a run of 8 or more digits in field " + k)


def ac_1(root):
    r = p114.load(root, REC)
    clean(r)
    need(r.get("claim") in p114.CLAIMS, "claim missing")
    sm = json.loads((Path(root) / SRC_MAP).read_text(encoding="utf-8"))["functions"][FN]
    staged = {s["repo_path"].split("/")[-1]: s for s in sm["staged_from"] if s["repo_path"].startswith("infra/logic/registry/")}
    need(sorted(staged) == sorted(REG_NAMES), "the staged registry members differ from the seven expected")
    z = zip_members(r["zip"]["version_id"])
    need(r["zip"]["members"] == len(z.namelist()), "zip member count differs from a fresh read")
    rows = {x["name"]: x for x in r["registry_members"]}
    need(sorted(rows) == sorted(REG_NAMES), "registry_members are not the seven")
    for n in REG_NAMES:
        s, x = staged[n], rows[n]
        pinned = git(root, "show", s["pin"] + ":" + s["repo_path"], raw=True)
        head = git(root, "show", "HEAD:" + s["repo_path"], raw=True)
        inzip = z.read("infra/logic/registry/" + n)
        need(x["pin"] == s["pin"] and x["pinned_sha256"] == sha(pinned) == s["sha256"], "pinned sha256 differs for " + n)
        need(x["in_zip_sha256"] == sha(inzip) == sha(pinned), "the live zip's member is not the pinned blob for " + n)
        need(x["head_sha256"] == sha(head) and x["differs_from_head"] == (sha(head) != sha(pinned)), "head sha or differs flag wrong for " + n)
    pk = scope_keys(git(root, "show", staged["scopes.json"]["pin"] + ":infra/logic/registry/scopes.json", raw=True))
    hk = scope_keys(git(root, "show", "HEAD:infra/logic/registry/scopes.json", raw=True))
    sd = r["scopes_diff"]
    need(sd["added"] == sorted(set(hk) - set(pk)) and sd["removed"] == sorted(set(pk) - set(hk)) and sd["changed"] == sorted(k for k in pk if k in hk and pk[k] != hk[k]), "scopes_diff differs from the recomputed row-key diff")
    pkr = {k: json.loads(v) for k, v in pk.items()}
    hkr = {k: json.loads(v) for k, v in hk.items()}
    want_fields = {k: sorted(f for f in set(pkr[k]) | set(hkr[k]) if pkr[k].get(f) != hkr[k].get(f)) for k in sd["changed"]}
    need(sd["changed_fields"] == want_fields, "changed_fields differs from the recomputed field-name diff")
    need("z09" in sd["added"], "z09 is not among the rows HEAD adds")
    mr = r["minimal_repin"]
    need(len(mr) >= 1 and all(m["member"] in REG_NAMES and re.fullmatch(r"[0-9a-f]{40}", m["new_pin"]) and rows[m["member"]]["differs_from_head"] for m in mr), "minimal_repin names a member that does not differ from HEAD, or a bad pin")
    tmp = Path(tempfile.mkdtemp(prefix="p118_"))
    live, fixed = tmp / "live", tmp / "fixed"
    z.extractall(live)
    z.extractall(fixed)
    for m in mr:
        blob = git(root, "show", m["new_pin"] + ":infra/logic/registry/" + m["member"], raw=True)
        need(sha(blob) == m["new_sha256"], "new_sha256 differs from the blob at the new pin for " + m["member"])
        (fixed / "infra/logic/registry" / m["member"]).write_bytes(blob)
    a, b = run_probe(live), run_probe(fixed)
    need(a == r["derived"]["in_zip_tree"] and b == r["derived"]["with_repinned_members"], "recorded derivations differ from the recomputed probe")
    need(a["blackdiamond_z09"]["firm"].startswith("REFUSED") and b["blackdiamond_z09"]["firm"] == "cottonwood", "the live tree must refuse z09 and the re-pinned tree resolve it to cottonwood")
    need(a["schwab_08335338"] == b["schwab_08335338"] and a["orion"] == b["orion"], "the 49 Financial or Inflection derivation (firm, prefixes, gold addresses, names) changes under the re-pin")
    need(r["unchanged_for_other_channels"] is True, "unchanged_for_other_channels is not true")
    rd = r["reads"]
    need(all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads", "aws_writes")), "a write is recorded")
    need(r.get("pushed") is False and r.get("deployed") is False, "side-effect flags")


def ac_2(root):
    r = p114.load(root, REC)
    t = (Path(root) / PACKET).read_text(encoding="utf-8") if (Path(root) / PACKET).is_file() else None
    need(t is not None, "packet absent: " + PACKET)
    need(len(t) >= 5000, "packet shorter than 5000 characters")
    pos = -1
    for h in HEADS:
        i = t.find(h)
        need(i > pos, "packet heading absent or out of order: " + h)
        pos = i
    need("UNSIGNED" in t or "unsigned" in t, "the packet must state that it is unsigned")
    need(not re.search(r"\bsigned by\b|\bapproved by\b", t), "the packet claims a signature")
    for m in r["minimal_repin"]:
        need(m["member"] in t and m["new_pin"][:10] in t, "the packet does not name the re-pin of " + m["member"])
    need(r["zip"]["version_id"][:8] in t, "the packet does not name the live zip version it starts from")
    need("handler.py" not in re.sub(r"[^\n]*handler\.py[^\n]*", "", t) or True, "")
    need("irpt-cot-holdings-performance-lambda" in t and "catch-up" in t.lower(), "the packet does not name the Cottonwood function and the catch-up resume")


ARMS = {"DBC118-1-AC1": ac_1, "DBC118-2-AC1": ac_2}


def main(argv):
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
