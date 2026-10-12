"""IB-pr-460 replay driver: the LIVE package against the BUILT package of irpt-commentary-draft-store-lambda, offline. From the worktree root:
    python <this file> <scratch_dir> <out_replay_json>
<scratch_dir> (OUTSIDE the worktree) holds live/<fn>.zip and zips/<fn>.1.zip. Each zip is extracted to <scratch>/x/<side>; the negative control
is the BUILT tree with commentary_draft_store.py put back to its LIVE bytes. Each tree runs probe_460.py in its own `python -I` process
(boto3 never imported, every socket connect refused, no AWS call, synthetic ids only). The verdict of an arm is computed here from the probe
outputs; a comparison that does not come out as stated reads UNEXPECTED. ASCII only."""
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
scratch, out_path = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
FN = "irpt-commentary-draft-store-lambda"
TICKET = "TCK-20261011-0a1b2c3d"
REFKEYS = {"artifact_id", "sha256", "version_id"}
MEMBER = "commentary_draft_store.py"
SIX_REFUSALS = ["refusal_other_tenant", "refusal_reserved_tenant", "refusal_unknown_op", "refusal_extra_key", "refusal_missing_draft", "refusal_absent_record"]


def wipe(d):
    """remove a scratch tree file by file (no recursive delete command)"""
    if d.exists():
        for root, dirs, files in os.walk(str(d), topdown=False):
            for f in files:
                os.unlink(os.path.join(root, f))
            for x in dirs:
                os.rmdir(os.path.join(root, x))
        os.rmdir(str(d))


def extract(zip_path, dest):
    wipe(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest)


def probe(tree, label):
    o = scratch / "out" / ("%s.json" % label)
    o.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", str(HERE / "probe_460.py"), str(tree), label, str(o)], capture_output=True, timeout=180)
    if r.returncode:
        raise SystemExit("probe failed %s: %s" % (label, (r.stderr + r.stdout).decode("utf-8", "replace")[-500:]))
    return json.loads(o.read_text(encoding="utf-8"))


live, built, ctl = scratch / "x" / "live", scratch / "x" / "built", scratch / "x" / "ctl_store"
extract(scratch / "live" / (FN + ".zip"), live)
extract(scratch / "zips" / (FN + ".1.zip"), built)
wipe(ctl)
shutil.copytree(built, ctl)
shutil.copyfile(str(live / MEMBER), str(ctl / MEMBER))
L, B, C = probe(live, "live"), probe(built, "built"), probe(ctl, "ctl_store")

arms = []


def arm(name, verdict, detail, ticket, neg=False, members=(MEMBER,)):
    arms.append({"function": FN, "name": name, "verdict": verdict, "record_has_ticket_id": ticket, "negative_control": neg, "members": list(members), "detail": detail})


def v(ok, expected):
    return expected if ok else "UNEXPECTED"


# 1 -- a first persist for a record with NO ticket id: byte-identical
for key, words in (("no_ticket_key", "no ticket_id key"), ("ticket_empty_string", "ticket_id is the empty string"), ("ticket_none", "ticket_id is null"),
                   ("ticket_int", "ticket_id is an integer"), ("ticket_list", "ticket_id is a list")):
    lf, bf = L[key]["first_persist"], B[key]["first_persist"]
    ok = (json.dumps(lf, sort_keys=True) == json.dumps(bf, sort_keys=True) and lf["status"] == "OK" and set(bf) == {"status", "commentary_ref"} and set(bf["commentary_ref"]) == REFKEYS)
    arm("first persist, record with %s (no usable ticket id): the answer is byte-identical on live and built" % words, v(ok, "identical"),
        "live and built answer %s members %s; the serialized answers are equal." % (sorted(bf), sorted(bf["commentary_ref"])), False)
# 2 -- with one: built adds ticket_id
lf, bf = L["ticket"]["first_persist"], B["ticket"]["first_persist"]
ok = (set(lf) == {"status", "commentary_ref"} and set(bf) == {"status", "commentary_ref", "ticket_id"} and bf["ticket_id"] == TICKET and lf["commentary_ref"] == bf["commentary_ref"] and bf["status"] == lf["status"] == "OK")
arm("first persist, record WITH a ticket id: live answers today's two members, built adds ticket_id equal to the record's", v(ok, "expected-diff"),
    "live members %s; built members %s; ticket_id equals the planted synthetic id: %s; commentary_ref equal on both." % (sorted(lf), sorted(bf), bf.get("ticket_id") == TICKET), True)
# 3 -- reads of the record per persist
ok = all(X[k]["requests_get_calls_for_the_first_persist"] == 1 for X in (L, B) for k in ("ticket", "no_ticket_key"))
arm("requests.get is called exactly once for a first persist, live and built, with and without a ticket id (no second read)", v(ok, "identical"),
    "calls: live %s / %s, built %s / %s." % (L["ticket"]["requests_get_calls_for_the_first_persist"], L["no_ticket_key"]["requests_get_calls_for_the_first_persist"],
                                              B["ticket"]["requests_get_calls_for_the_first_persist"], B["no_ticket_key"]["requests_get_calls_for_the_first_persist"]), True)
# 4 -- the writes
ok = all(L[k]["artifact_puts"] == B[k]["artifact_puts"] == 1 and L[k]["ref_sets"] == B[k]["ref_sets"] == 1 for k in ("ticket", "no_ticket_key"))
arm("writes: one artifact put and one commentary_ref set per request, live and built, with and without a ticket id", v(ok, "identical"), "artifact puts 1 / 1 and ref sets 1 / 1 on both sides in both cases.", True)
# 5 -- a replay
for key, has in (("ticket", True), ("no_ticket_key", False)):
    ok = L[key]["replay"] == B[key]["replay"] == {"status": "REFUSED", "reason": "ALREADY_WRITTEN"}
    arm("replay (second put of the same request), record %s a ticket id: ALREADY_WRITTEN on both, no ticket_id" % ("WITH" if has else "WITHOUT"), v(ok, "identical"),
        "live %s, built %s." % (json.dumps(L[key]["replay"], sort_keys=True), json.dumps(B[key]["replay"], sort_keys=True)), has)
# 6 -- every refusal
for key, has in (("ticket", True), ("no_ticket_key", False)):
    ok = all(L[key][r] == B[key][r] and set(B[key][r]) == {"status", "reason"} for r in SIX_REFUSALS)
    arm("refusals (%s), record %s a ticket id: identical on live and built, each exactly {status, reason}" % (", ".join(r.replace("refusal_", "") for r in SIX_REFUSALS), "WITH" if has else "WITHOUT"), v(ok, "identical"),
        "reason codes built: %s." % ", ".join("%s=%s" % (r.replace("refusal_", ""), B[key][r]["reason"]) for r in SIX_REFUSALS), has)
# 7 -- get_ref
for key, has in (("ticket", True), ("no_ticket_key", False)):
    ok = (L[key]["get_ref_before"] == B[key]["get_ref_before"] and L[key]["get_ref_after"] == B[key]["get_ref_after"] and "ticket_id" not in B[key]["get_ref_after"]
          and B[key]["get_ref_before"] == {"status": "OK", "commentary_ref": None})
    arm("get_ref before and after a first persist, record %s a ticket id: identical, no ticket_id" % ("WITH" if has else "WITHOUT"), v(ok, "identical"),
        "built before %s; after members %s." % (json.dumps(B[key]["get_ref_before"], sort_keys=True), sorted(B[key]["get_ref_after"])), has)
# 8 -- the crash-recovery branch
lc, bc = L["crash_recovery_with_ticket"]["healed"], B["crash_recovery_with_ticket"]["healed"]
ok = set(lc) == {"status", "commentary_ref"} and set(bc) == {"status", "commentary_ref", "ticket_id"} and bc["ticket_id"] == TICKET and lc["commentary_ref"] == bc["commentary_ref"]
arm("crash-recovery branch (artifact exists, commentary_ref never set), record WITH a ticket id: built carries ticket_id, live does not; the first artifact's ref is returned on both", v(ok, "expected-diff"),
    "live members %s; built members %s; refs equal." % (sorted(lc), sorted(bc)), True)
lc, bc = L["crash_recovery_no_ticket"]["healed"], B["crash_recovery_no_ticket"]["healed"]
arm("crash-recovery branch, record WITHOUT a ticket id: identical", v(lc == bc and set(bc) == {"status", "commentary_ref"}, "identical"), "members %s on both." % sorted(bc), False)
# 9 -- resolve_request keeps its two-value return
ok = L["resolve_request_arity"] == B["resolve_request_arity"] == {"returned": 2} and L["resolve_request"] == B["resolve_request"]
arm("resolve_request(requests, tenant_hint, request_id) still returns exactly (tenant, owner): arity 2 on live and built", v(ok, "identical"),
    "live %s, built %s; the built tree adds _resolve_record: %s (live: %s)." % (L["resolve_request_arity"], B["resolve_request_arity"], B["tree_has_resolve_record"], L["tree_has_resolve_record"]), True)
# 10 -- negative controls
cf = C["ticket"]["first_persist"]
ok = set(cf) == {"status", "commentary_ref"} and C["ticket"]["first_persist"] == L["ticket"]["first_persist"] and cf != B["ticket"]["first_persist"]
arm("NEGATIVE CONTROL: the built tree with commentary_draft_store.py put back to the LIVE bytes -- the first persist for a record WITH a ticket id answers today's two members again", v(ok, "expected-diff"),
    "control answer members %s equal live's and differ from built's: commentary_draft_store.py is the member that adds ticket_id, and this comparison can tell an answer with the member from one without." % sorted(cf), True, neg=True)
cn = C["no_ticket_key"]["first_persist"]
arm("NEGATIVE CONTROL: the same control tree, record WITHOUT a ticket id -- equal to built's answer (the comparison reads identical when nothing differs)", v(cn == B["no_ticket_key"]["first_persist"], "identical"),
    "control answer members %s, equal to built's." % sorted(cn), False, neg=True)

doc = {"arms": arms, "arm_count": len(arms), "function": FN,
       "harness": "replay/run_replay_460.py + probe_460.py; offline: no boto3, in-memory fakes, every socket connect refused, AWS never called; one tree per process (python -I); synthetic ids only",
       "unexpected": [a["name"] for a in arms if a["verdict"] not in ("identical", "expected-diff")]}
out_path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
for a in arms:
    print(a["verdict"], "NEG" if a["negative_control"] else "   ", "T=%s" % a["record_has_ticket_id"], a["name"][:130])
print("arms=%d unexpected=%d" % (len(arms), len(doc["unexpected"])))
