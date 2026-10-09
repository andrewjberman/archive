"""NFRA_OPSWKF round 1 -- the issuer's mechanical checks (2.0.0_SA_COO~O2).

  l1-type      OW-l1-AC1  trade_request carries the four typed questions; valid create, each required answer refused, other types unchanged
  e1-token     OW-e1-AC1  the submit handler takes the initiator from the authorizer token; no context 403; a conflicting body 403
  e2-bridge    OW-e2-AC1  a submit with ticket_id binds exactly one trade_request ticket of the same filer; every refusal arm tested
  e3-writeback OW-e3-AC1  approve/reject on a ticket-born submission writes the event + status onto the ticket
  e3-fence     OW-e3-AC2  Execute on origin=ticket is refused before any write, S3 put or brokerage email; non-ticket Execute unchanged
  trade-regress OW-e-AC2  both trade handler test directories pass whole (pre-existing files included)
  i1-cond      OW-i1-AC2  (CTO half OW-d-1 cond. 1) GetItem stmt + UpdateItem stmt conditioned on dynamodb:Attributes to the 4 written attrs
  i1-grant     OW-i1-AC1  trade-pipeline Terraform grants GetItem+UpdateItem on table/opal-tickets and sets TICKETS_TABLE on both Lambdas
  k1-selftest  OW-k1-AC1  tools/ops_kit/serve.py --selftest prints both panels with source=fixture
  k1-bounds    OW-k1-AC2  the kit carries no AWS SDK or credential reference
  k1-theme     OW-k1-AC3  the kit's theme.css carries the portal colour law values (canvas, panel, hairline)
  p1-form      OW-p1-AC1  (run with --portal <portal worktree>) the trade request form tests exist and pass

Each named test must EXIST and PASS; a missing name is a FAIL, never a skip. Prints <TOKEN>-OK or <TOKEN>-FAIL <reason>,
exits 0 / 1. Run from the worktree root. Every subprocess is bounded (timeout 110 s).
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

TC_TESTS = Path("infra/aws/lambda/ticket_center/tests")
SUB_TESTS = Path("infra/aws/lambda/trade-pipeline/trade-submission-handler/tests")
WF_TESTS = Path("infra/aws/lambda/trade-pipeline/trade-workflow-handler/tests")
KIT = Path("tools/ops_kit")

NAMED = {
    "l1-type": (TC_TESTS / "test_trade_request_type.py",
                ["test_trade_request_valid_create", "test_trade_request_required_answers_refused",
                 "test_trade_request_unknown_answer_refused", "test_other_untyped_types_unchanged"]),
    "e1-token": (SUB_TESTS / "test_initiator_from_token.py",
                 ["test_initiator_is_token_email", "test_no_authorizer_context_403",
                  "test_conflicting_body_initiator_403", "test_legacy_body_without_initiator_accepted"]),
    "e2-bridge": (SUB_TESTS / "test_ticket_bridge.py",
                  ["test_bridge_links_one_ticket", "test_bridge_refuses_wrong_type", "test_bridge_refuses_other_filer",
                   "test_bridge_refuses_already_linked", "test_bridge_refuses_fund_mismatch",
                   "test_no_ticket_id_is_legacy_path"]),
    "e3-writeback": (WF_TESTS / "test_ticket_writeback_and_fence.py",
                     ["test_approve_writes_ticket_event_and_in_progress", "test_reject_writes_ticket_event_and_completed",
                      "test_non_ticket_submission_touches_no_ticket"]),
    "e3-fence": (WF_TESTS / "test_ticket_writeback_and_fence.py",
                 ["test_execute_refused_for_ticket_origin", "test_execute_refusal_sends_no_email_and_writes_nothing",
                  "test_execute_refusal_recorded_on_ticket", "test_execute_non_ticket_still_sends"]),
}


def _strip(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def _pytest(path, names=None):
    if not path.exists():
        return False, "absent: %s" % path.as_posix()
    if names:
        src = path.read_text(encoding="utf-8")
        missing = [n for n in names if not re.search(r"^\s*def %s\(" % re.escape(n), src, re.M)]
        if missing:
            return False, "missing test(s): %s" % ", ".join(missing)
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", path.as_posix()]
    if names:
        cmd += ["-k", " or ".join(names)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    out = _strip(r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) failed", out) or [0, 0])[1])
    need = len(names) if names else 1
    if r.returncode != 0 or failed or passed < need:
        tail = [ln for ln in out.splitlines() if ln.strip()][-1:] or [""]
        return False, "rc=%d passed=%d failed=%d need>=%d %s" % (r.returncode, passed, failed, need, tail[0])
    return True, "passed=%d" % passed


# test_actor_identity.py is a SCRIPT-RUN file: three tests take a fixture its own __main__ supplies, so under pytest they ERROR
# at base (row NFRA_OPSWKF-D2-S1). They are deselected from pytest and the file is run as the script it is instead.
ACTOR_SCRIPT_TESTS = ("test_jwt_resolved_actor_no_body_email", "test_matching_body_email_accepted",
                      "test_bare_authorizer_shape_resolves")


def _run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    return r, _strip(r.stdout + r.stderr)


def _trade_regress():
    for d, new in ((SUB_TESTS, "test_ticket_bridge.py"), (WF_TESTS, "test_ticket_writeback_and_fence.py")):
        if not (d / new).exists():
            return False, "absent: %s" % (d / new).as_posix()
    notes = []
    for d, extra in ((SUB_TESTS, []), (WF_TESTS, ["-k", "not (%s)" % " or ".join(ACTOR_SCRIPT_TESTS)])):
        r, out = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", d.as_posix()] + extra)
        if r is None:
            return False, "%s timeout" % d.as_posix()
        passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
        bad = int((re.search(r"(\d+) failed", out) or [0, 0])[1]) + int((re.search(r"(\d+) error", out) or [0, 0])[1])
        if r.returncode != 0 or bad or not passed:
            return False, "%s rc=%d passed=%d failed+errors=%d" % (d.as_posix(), r.returncode, passed, bad)
        notes.append("%s passed=%d" % (d.name, passed))
    r, out = _run([sys.executable, (WF_TESTS / "test_actor_identity.py").as_posix()])
    if r is None or r.returncode != 0 or "FAIL " in out:
        return False, "test_actor_identity.py as a script: %s" % ("timeout" if r is None else "rc=%d" % r.returncode)
    notes.append("test_actor_identity.py script rc=0")
    return True, "; ".join(notes)


def _grant():
    iam = Path("infra/aws/terraform/trade-pipeline/iam.tf")
    lam = Path("infra/aws/terraform/trade-pipeline/lambdas.tf")
    if not iam.exists() or not lam.exists():
        return False, "absent terraform file"
    it = iam.read_text(encoding="utf-8")
    if not re.search(r'table/opal-tickets"', it):
        return False, "iam.tf grants no table/opal-tickets"
    blk = it[max(0, it.find("table/opal-tickets") - 900):it.find("table/opal-tickets")]
    if '"dynamodb:GetItem"' not in blk or '"dynamodb:UpdateItem"' not in blk:
        return False, "opal-tickets statement lacks GetItem+UpdateItem"
    n = len(re.findall(r'TICKETS_TABLE\s*=\s*"opal-tickets"', lam.read_text(encoding="utf-8")))
    if n != 2:
        return False, "TICKETS_TABLE set on %d function(s), expected 2" % n
    tf = shutil.which("terraform")
    if tf:
        try:
            r = subprocess.run([tf, "fmt", "-check", "-list=true", "infra/aws/terraform/trade-pipeline"],
                               capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            return False, "terraform fmt timeout"
        if r.returncode != 0:
            return False, "terraform fmt -check: %s" % r.stdout.strip()[:200]
    return True, "grant+env present (2 functions); fmt %s" % ("checked" if tf else "SKIPPED: no terraform on PATH")


TICKET_WRITE_ATTRS = {"ticket_id", "linked_submission_id", "events", "status"}


def _grant_conditioned():
    """CTO half OW-d-1 condition 1: GetItem on table/opal-tickets in one statement; UpdateItem alone in another, carrying
    ForAllValues:StringEquals on dynamodb:Attributes equal to exactly the four attributes K1/K2 write. Plus the env pair."""
    iam = Path("infra/aws/terraform/trade-pipeline/iam.tf")
    lam = Path("infra/aws/terraform/trade-pipeline/lambdas.tf")
    if not iam.exists() or not lam.exists():
        return False, "absent terraform file"
    it = iam.read_text(encoding="utf-8")
    if "table/opal-tickets" not in it:
        return False, "no statement names table/opal-tickets"
    get_ok = upd_ok = False
    lines = it.splitlines()
    for i, ln in enumerate(lines):
        if not re.match(r"\s*Sid\s*=", ln):
            continue
        close = " " * (len(ln) - len(ln.lstrip()) - 2) + "}"   # the statement's own closing brace, one level out
        j = i + 1
        while j < len(lines) and not (lines[j].rstrip().rstrip(",") == close):
            j += 1
        blk = "\n".join(lines[i:j])
        if "table/opal-tickets" not in blk:
            continue
        act_line = re.search(r"^\s*Action\s*=\s*(\[[^\]]*\]|\"[^\"]*\")", blk, re.M)
        acts = set(re.findall(r'"(dynamodb:[A-Za-z]+)"', act_line.group(1))) if act_line else set()
        if acts == {"dynamodb:GetItem"}:
            get_ok = True
        elif acts == {"dynamodb:UpdateItem"}:
            if "ForAllValues:StringEquals" not in blk or "dynamodb:Attributes" not in blk:
                return False, "UpdateItem statement lacks ForAllValues:StringEquals on dynamodb:Attributes"
            listed = set(re.findall(r'"([a-z_]+)"', blk.split("dynamodb:Attributes", 1)[1].split("]", 1)[0]))
            if listed != TICKET_WRITE_ATTRS:
                return False, "dynamodb:Attributes lists %s, expected %s" % (sorted(listed), sorted(TICKET_WRITE_ATTRS))
            upd_ok = True
        else:
            return False, "a statement on table/opal-tickets carries actions %s" % sorted(acts)
    if not (get_ok and upd_ok):
        return False, "GetItem statement %s, conditioned UpdateItem statement %s" % (get_ok, upd_ok)
    n = len(re.findall(r'TICKETS_TABLE\s*=\s*"opal-tickets"', lam.read_text(encoding="utf-8")))
    if n != 2:
        return False, "TICKETS_TABLE set on %d function(s), expected 2" % n
    return True, "GetItem stmt + UpdateItem stmt conditioned to %s; env on 2 functions" % sorted(TICKET_WRITE_ATTRS)


def _kit_selftest():
    serve = KIT / "serve.py"
    if not serve.exists():
        return False, "absent: %s" % serve.as_posix()
    try:
        r = subprocess.run([sys.executable, serve.as_posix(), "--selftest"], capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    out = r.stdout + r.stderr
    rows = {m[0]: m for m in re.findall(r"PANEL (trade_rec|billing) rows=(\d+) source=(\w+)", out)}
    if r.returncode != 0:
        return False, "rc=%d" % r.returncode
    for p in ("trade_rec", "billing"):
        if p not in rows or int(rows[p][1]) < 1 or rows[p][2] != "fixture":
            return False, "panel %s line missing or wrong: %s" % (p, rows.get(p))
    return True, "trade_rec=%s billing=%s source=fixture" % (rows["trade_rec"][1], rows["billing"][1])


def _kit_bounds():
    if not KIT.exists():
        return False, "absent: %s" % KIT.as_posix()
    files = [p for p in KIT.rglob("*") if p.is_file()]
    if not files:
        return False, "empty kit"
    pat = re.compile(r"boto3|botocore|aws_access_key|aws_secret|AWS_ACCESS_KEY|AWS_SECRET", re.I)
    hits = [p.as_posix() for p in files if pat.search(p.read_text(encoding="utf-8", errors="replace"))]
    if hits:
        return False, "credential/SDK reference in %s" % hits
    return True, "0 hits across %d files" % len(files)


def _kit_theme():
    css = KIT / "static" / "theme.css"
    if not css.exists():
        return False, "absent: %s" % css.as_posix()
    t = css.read_text(encoding="utf-8").upper()
    miss = [v for v in ("#F4F6FA", "#FFFFFF", "#C4CBDB") if v not in t]
    if miss:
        return False, "missing colour-law value(s) %s" % miss
    return True, "canvas, panel, hairline present"


P1_TEST = Path("src/pages/TicketCenter/__tests__/trade-request.test.tsx")
P1_NAMES = ["submits one ticket then one engine submit carrying the ticket id",
            "sends no initiator identity in the engine body",
            "blocks submit until every required field and the attestation are filled"]


def _bun(portal):
    root = Path(portal)
    test = root / P1_TEST
    if not test.exists():
        return False, "absent: %s" % test.as_posix()
    src = test.read_text(encoding="utf-8")
    missing = [n for n in P1_NAMES if n not in src]
    if missing:
        return False, "missing test(s): %s" % missing
    bun = shutil.which("bun")
    if not bun:
        return False, "bun not on PATH"
    try:
        r = subprocess.run([bun, "test", P1_TEST.as_posix()], cwd=root, capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    out = _strip(r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) pass", out) or [0, 0])[1])
    if r.returncode != 0 or passed < len(P1_NAMES):
        return False, "rc=%d pass=%d" % (r.returncode, passed)
    return True, "pass=%d" % passed


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    sub = argv[0]
    token = "OW-" + sub.upper()
    if sub in NAMED:
        ok, why = _pytest(*NAMED[sub])
    elif sub == "trade-regress":
        ok, why = _trade_regress()
    elif sub == "i1-grant":
        ok, why = _grant()
    elif sub == "i1-cond":
        ok, why = _grant_conditioned()
    elif sub == "k1-selftest":
        ok, why = _kit_selftest()
    elif sub == "k1-bounds":
        ok, why = _kit_bounds()
    elif sub == "k1-theme":
        ok, why = _kit_theme()
    elif sub == "p1-form":
        if len(argv) < 3 or argv[1] != "--portal":
            print("%s-FAIL usage: p1-form --portal <portal worktree>" % token)
            return 1
        ok, why = _bun(argv[2])
    else:
        print("unknown check %r" % sub)
        return 2
    print("%s-%s %s" % (token, "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
