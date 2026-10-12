"""IB-pr-456 replay driver: for each BUILT function, the LIVE package against the BUILT package, offline. From the worktree root:
    python <this file> <scratch_dir> <out_replay_json>
<scratch_dir> (OUTSIDE the worktree) holds live/<fn>.zip, zips/<fn>.1.zip and reg/firm_registry.json (one synthetic firm). Each zip is
extracted to <scratch>/x/<fn>/<side>; negative-control trees are the BUILT tree with ONE member put back to its LIVE bytes. Each tree runs
probe_456.py in its own `python -I` process (boto3 never imported, every socket connect refused, no AWS call, synthetic ids only). The
verdict of an arm is computed here from the probe outputs; a comparison that does not come out as stated reads UNEXPECTED. ASCII only."""
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
scratch, out_path = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
FNS = ["irpt-ycharts-generate", "irpt-status", "irpt-commentary-draft-store-lambda", "irpt-commentary-composition-read-lambda"]
REG = scratch / "reg" / "firm_registry.json"
WRONG = ["member_string_true", "member_int_1", "member_none", "member_list"]
ACTOR = "acting_principal_id"


def extract(zip_path, dest):
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest)


def probe(tree, label, fn):
    o = scratch / "out" / ("%s.%s.json" % (fn, label))
    o.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", str(HERE / "probe_456.py"), str(tree), label, str(REG), str(o)], capture_output=True, timeout=180)
    if r.returncode:
        raise SystemExit("probe failed %s %s: %s" % (fn, label, (r.stderr + r.stdout).decode("utf-8", "replace")[-500:]))
    return json.loads(o.read_text(encoding="utf-8"))


def strip_actor(view):
    """a record view without the AR-y-37 member, so the commentary_requested comparison is not masked by it"""
    if isinstance(view, dict):
        return {k: (sorted(x for x in v if x != ACTOR) if k == "keys" else strip_actor(v)) for k, v in view.items()}
    if isinstance(view, list):
        return [strip_actor(x) for x in view]
    return view


def code(o):
    return o.get("raised") or ("returned" if "returned" in o else "?")


arms = []


def arm(fn, name, verdict, detail, members, neg=False, without=False, extra=None):
    a = {"function": fn, "name": "%s: %s" % (fn, name), "verdict": verdict, "negative_control": neg, "members": members, "detail": detail}
    if without:
        a["submission_without_the_member"] = True
    a.update(extra or {})
    arms.append(a)


trees = {}
for fn in FNS:
    live, built = scratch / "x" / fn / "live", scratch / "x" / fn / "built"
    extract(scratch / "live" / (fn + ".zip"), live)
    extract(scratch / "zips" / (fn + ".1.zip"), built)
    P = {"live": probe(live, "live", fn), "built": probe(built, "built", fn)}
    for ctl, member in (("ctl_submission", "submission.py"), ("ctl_acceptance", "acceptance.py"), ("ctl_service", "submission_service.py")):
        if not (live / member).is_file():
            continue
        d = scratch / "x" / fn / ctl
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(built, d)
        shutil.copyfile(str(live / member), str(d / member))
        P[ctl] = probe(d, ctl, fn)
    trees[fn] = P

for fn in FNS:
    L, B = trees[fn]["live"], trees[fn]["built"]
    pair = "service_pair" in B
    # 1 -- a submission WITHOUT the member
    la, ba = L["accept_new"]["without_member"], B["accept_new"]["without_member"]
    same = strip_actor(la) == strip_actor(ba) and la["transactions_written"] == ba["transactions_written"] == 2 and "commentary_requested" not in json.dumps(ba).replace('"commentary_requested": "<absent>"', "")
    detail = "DynamoAcceptance.accept over an in-memory store: live and built both write %d transactions (one request row, one job row) and both records carry no commentary_requested (read back through get: identical). Compared with the AR-y-37 member %s removed from the key list (the next arm shows it)." % (ba["transactions_written"], ACTOR)
    if pair:
        ls, bs = L["service_pair"]["without_member"], B["service_pair"]["without_member"]
        same = same and strip_actor(ls) == strip_actor(bs) and bs["queue_sends"] == ls["queue_sends"] == 1 and bs["calls"] == ls["calls"]
        detail += " Through the real SubmissionService (submit -> lookup -> accept -> dispatch): calls %s, queue sends %d / %d, transactions %d / %d, stored record identical." % (
            [code(c) for c in bs["calls"]], ls["queue_sends"], bs["queue_sends"], ls["transactions_written"], bs["transactions_written"])
    arm(fn, "a submission WITHOUT commentary_requested is accepted and recorded identically (live vs built)", "identical" if same else "UNEXPECTED", detail,
        ["submission.py", "acceptance.py"] + (["submission_service.py"] if pair else []), without=True)
    lk, bk = set(la["accept"]["returned"]["keys"]), set(ba["accept"]["returned"]["keys"])
    arm(fn, "full record of a submission WITHOUT the member: the one key built adds is acting_principal_id (AR-y-37, commit 2f7cc7be42, earlier than IB-pr-455)",
        "expected-diff" if bk - lk == {ACTOR} and lk - bk == set() else "UNEXPECTED",
        "live record keys %s; built record keys %s. Built passes acting_principal_id when its tree's accept takes it (the keyword is REQUIRED in the built acceptance.py)." % (sorted(lk), sorted(bk)),
        ["acceptance.py"], without=True)
    # 2 -- a submission WITH the member
    ok = True
    parts = []
    for nm, val in (("member_true", True), ("member_false", False)):
        lo, bo = L["accept_new"][nm], B["accept_new"][nm]
        step = (code(lo["accept"]) == "SubmissionRefused:UNKNOWN_OR_SERVER_OWNED_FIELD" and lo["transactions_written"] == 0 and code(bo["accept"]) == "returned"
                and bo["accept"]["returned"]["commentary_requested"] is val and bo["read_back_get"]["returned"]["commentary_requested"] is val and bo["transactions_written"] == 2)
        ok = ok and step
        parts.append("%s: live %s (0 writes); built accepted, record carries commentary_requested=%s as sent, read back through get the same (2 writes)" % (nm, code(lo["accept"]), val))
    if pair:
        for nm in ("member_true", "member_false"):
            ls, bs = L["service_pair"][nm], B["service_pair"][nm]
            ok = ok and code(ls["calls"][0]) == "SubmissionRefused:UNKNOWN_OR_SERVER_OWNED_FIELD" and ls["queue_sends"] == 0 and code(bs["calls"][0]) == "returned" and bs["queue_sends"] == 1
        parts.append("through the real SubmissionService the same: live refuses before any write or send; built accepts and sends the queue message once")
    arm(fn, "a submission WITH commentary_requested (true, false) is refused by live and accepted by built", "expected-diff" if ok else "UNEXPECTED", "; ".join(parts) + ".",
        ["submission.py", "acceptance.py"])
    # 3 -- wrong type
    ok, codes_l, codes_b = True, set(), set()
    for nm in WRONG:
        lo, bo = L["accept_new"][nm], B["accept_new"][nm]
        ok = ok and "raised" in lo["accept"] and "raised" in bo["accept"] and lo["transactions_written"] == 0 == bo["transactions_written"]
        codes_l.add(code(lo["accept"]))
        codes_b.add(code(bo["accept"]))
    arm(fn, "a wrong-typed commentary_requested (string, integer, null, list) is refused by BOTH, nothing written; the reason code differs", "expected-diff" if ok else "UNEXPECTED",
        "live refuses all 4 as %s (the member is unknown to it); built refuses all 4 as %s. Neither writes anything." % (sorted(codes_l), sorted(codes_b)), ["submission.py"],
        extra={"refused_by_both": ok})
    # 4 -- replay of the same body
    r_l, r_b = L["replay_same_request_id"]["same_body_twice_without_member"], B["replay_same_request_id"]["same_body_twice_without_member"]
    same = strip_actor(r_l) == strip_actor(r_b) and r_b["transactions_after_second"] == r_b["transactions_after_first"]
    arm(fn, "the same submission WITHOUT the member sent twice: the replay returns the prior record and writes nothing (live vs built)", "identical" if same else "UNEXPECTED",
        "first and second call: live %s / %s, built %s / %s; transactions after the replay %d / %d (unchanged)." % (code(r_l["first"]), code(r_l["second"]), code(r_b["first"]), code(r_b["second"]),
                                                                           r_l["transactions_after_second"], r_b["transactions_after_second"]),
        ["submission.py", "acceptance.py"], without=True)
    # 5 -- AMENDMENT 1 (b): same request id, a different member
    RL, RB = L["replay_same_request_id"], B["replay_same_request_id"]
    cases = [("same_request_id_member_added", "first call without the member, second with it"),
             ("same_request_id_member_dropped", "first call with the member, second without it"),
             ("same_request_id_member_true_then_false", "first call with true, second with false")]
    for key, words in cases:
        rl, rb = RL[key], RB[key]
        ok = (code(rb["second"]) == "IdempotencyConflict:CHANGED_INPUTS_SAME_REQUEST_ID" and rb["transactions_after_second"] == rb["transactions_after_first"] == 2
              and code(rl["second"] if key == "same_request_id_member_added" else rl["first"]) == "SubmissionRefused:UNKNOWN_OR_SERVER_OWNED_FIELD")
        arm(fn, "same_request_id_different_member (%s)" % key.replace("same_request_id_", ""), "expected-diff" if ok else "UNEXPECTED",
            "%s. LIVE: first call %s, second call %s (the member is refused outright whenever it is sent); BUILT: first call %s, second call %s, transactions %d after the first and %d after the second (the second writes nothing)." % (
                words, code(rl["first"]), code(rl["second"]), code(rb["first"]), code(rb["second"]), rb["transactions_after_first"], rb["transactions_after_second"]),
            ["submission.py", "acceptance.py"])
    ra, rbb = L["record_accepted_before"], B["record_accepted_before"]
    ok = (code(rbb["lookup_body_with_member"]) == "IdempotencyConflict:CHANGED_INPUTS_SAME_REQUEST_ID" and code(ra["lookup_body_with_member"]) == "SubmissionRefused:UNKNOWN_OR_SERVER_OWNED_FIELD"
          and strip_actor(ra["get_old_record"]) == strip_actor(rbb["get_old_record"]) and strip_actor(ra["lookup_same_body"]) == strip_actor(rbb["lookup_same_body"]))
    arm(fn, "same_request_id_different_member against a record accepted BEFORE any release (no member stored): get and lookup of the same body identical; lookup with the member differs",
        "expected-diff" if ok else "UNEXPECTED",
        "stored record without the member, read through get and through lookup(same body): identical on live and built; lookup(body WITH the member): live %s, built %s." % (
            code(ra["lookup_body_with_member"]), code(rbb["lookup_body_with_member"])), ["submission.py", "acceptance.py"], without=True)
    if pair:
        for key in ("same_request_id_member_added", "same_request_id_member_dropped"):
            ls, bs = L["service_pair"][key], B["service_pair"][key]
            ok = code(bs["calls"][1]) == "IdempotencyConflict:CHANGED_INPUTS_SAME_REQUEST_ID" and bs["queue_sends"] == 1 and bs["transactions_written"] == 2
            arm(fn, "same_request_id_different_member through the real SubmissionService (%s): what a caller sees" % key.replace("same_request_id_", ""), "expected-diff" if ok else "UNEXPECTED",
                "live calls %s (queue sends %d); built calls %s (queue sends %d, transactions %d): the second call is refused CHANGED_INPUTS_SAME_REQUEST_ID (an IdempotencyConflict, public_reason_code INVALID_INPUT) and sends nothing." % (
                    [code(c) for c in ls["calls"]], ls["queue_sends"], [code(c) for c in bs["calls"]], bs["queue_sends"], bs["transactions_written"]), ["submission.py", "acceptance.py", "submission_service.py"])
    # 6 -- readers the function holds
    for rname in sorted(B["readers"]):
        if isinstance(B["readers"][rname], bool):
            continue
        lv, bv = L["readers"][rname], B["readers"][rname]
        same_member = all(bv[k] == bv["record_without_member"] for k in bv) and all(lv[k] == lv["record_without_member"] for k in lv)
        across = lv == bv
        arm(fn, "reader %s over a stored record WITHOUT the member and WITH it (true, false): the answer is the same, live and built" % rname,
            "identical" if (same_member and across) else "UNEXPECTED",
            "answers: %s. The answer does not depend on the member, and live and built answer alike." % json.dumps(bv["record_without_member"], sort_keys=True)[:260],
            [rname.split(".")[0] + ".py"], without=True)
    if "resident_worker.has_send_ready_if_ticketed" in B["readers"]:
        arm(fn, "the zip's resident_worker.py is the OLD one (no send_ready_if_ticketed, no producer_for): the worker gate IB-pr-455 merged is not in this package, live or built",
            "identical" if (L["readers"]["resident_worker.has_send_ready_if_ticketed"] is False and B["readers"]["resident_worker.has_send_ready_if_ticketed"] is False
                            and L["readers"]["resident_worker.has_producer_for"] is False and B["readers"]["resident_worker.has_producer_for"] is False) else "UNEXPECTED",
            "hasattr(resident_worker, 'send_ready_if_ticketed') and hasattr(..., 'producer_for') are False on both trees: the staged row pins resident_worker.py at the live bytes, so this release does not move the gate.",
            ["resident_worker.py"])
    # 7 -- the packaged contract
    if "schema" in B:
        ok = (L["schema"]["properties_has_commentary_requested"] is False and B["schema"]["properties_has_commentary_requested"] is True and B["schema"]["commentary_requested_type"] == "boolean"
              and B["schema"]["additionalProperties"] is False and L["ingestion_revision_rule_digest"] != B["ingestion_revision_rule_digest"])
        arm(fn, "the packaged AnalysisSubmissionRequest.schema.json: the member is declared (boolean) on built and absent on live; the schemas digest the function stamps as ingestion_gate_revision moves",
            "expected-diff" if ok else "UNEXPECTED",
            "live properties lack commentary_requested; built declares it as boolean, additionalProperties false on both. The rule generate_installed.ingestion_revision_for hashes contracts/*.schema.json: live %s, built %s, so every request accepted after a release carries the new ingestion_gate_revision." % (
                L["ingestion_revision_rule_digest"][:20], B["ingestion_revision_rule_digest"][:20]), ["contracts/AnalysisSubmissionRequest.schema.json"])
    # 8 -- negative controls
    C = trees[fn]["ctl_submission"]
    ok = code(C["accept_new"]["member_true"]["accept"]) == "SubmissionRefused:UNKNOWN_OR_SERVER_OWNED_FIELD" and C["accept_new"]["member_true"]["transactions_written"] == 0
    arm(fn, "NEGATIVE CONTROL: the built tree with submission.py put back to the LIVE bytes -- a submission WITH the member is refused again", "expected-diff" if ok else "UNEXPECTED",
        "control: member_true -> %s, 0 writes (the live answer): submission.py is the member that admits it." % code(C["accept_new"]["member_true"]["accept"]), ["submission.py"], neg=True)
    C = trees[fn]["ctl_acceptance"]
    cm = C["accept_new"]["member_true"]
    sub_admits = C["submission"]["validate_public_request"]["member_true"].get("returned") is not None
    ok = sub_admits and "returned" in cm["accept"] and cm["accept"]["returned"]["commentary_requested"] == "<absent>" if not pair else sub_admits and "raised" in cm["accept"]
    if pair:
        cs = C["service_pair"]["member_true"]
        ok = sub_admits and code(cs["calls"][0]).startswith("TypeError") and cs["transactions_written"] == 0
        detail = "control: built submission.py admits the member (validate_public_request returns it), but with the LIVE acceptance.py the real SubmissionService raises %s and writes %d transactions (the built service passes acting_principal_id; the live accept takes no such keyword): the pair cannot be split." % (
            code(cs["calls"][0])[:90], cs["transactions_written"])
    else:
        detail = "control: the built submission.py admits the member but the live acceptance.py (no copy line) records a record with commentary_requested %s: acceptance.py is the member that writes it." % cm["accept"].get("returned", {}).get("commentary_requested")
    arm(fn, "NEGATIVE CONTROL: the built tree with acceptance.py put back to the LIVE bytes", "expected-diff" if ok else "UNEXPECTED", detail, ["acceptance.py"], neg=True)
    if pair:
        C = trees[fn]["ctl_service"]
        cs = C["service_pair"]["without_member"]
        ok = code(cs["calls"][0]).startswith("TypeError") and cs["transactions_written"] == 0
        arm(fn, "NEGATIVE CONTROL: the built tree with submission_service.py put back to the LIVE bytes (built acceptance.py, live service) -- every new submission, WITH or WITHOUT the member", "expected-diff" if ok else "UNEXPECTED",
            "control: the live service calls accept without acting_principal_id, which the built acceptance.py requires: %s, %d transactions written. This is the pairing the one-tree census stated; it holds here because this function packages its only caller of accept." % (
                code(cs["calls"][0])[:110], cs["transactions_written"]), ["acceptance.py", "submission_service.py"], neg=True, without=True)

doc = {"arms": arms, "arm_count": len(arms), "functions": FNS,
       "harness": "replay/run_replay_456.py + probe_456.py; offline: no boto3, in-memory fakes, every socket connect refused, AWS never called; one tree per process (python -I); synthetic ids only",
       "unexpected": [a["name"] for a in arms if a["verdict"] not in ("identical", "expected-diff")]}
out_path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
for a in arms:
    print(a["verdict"], "NEG" if a["negative_control"] else "   ", a["name"][:140])
print("arms=%d unexpected=%d" % (len(arms), len(doc["unexpected"])))
