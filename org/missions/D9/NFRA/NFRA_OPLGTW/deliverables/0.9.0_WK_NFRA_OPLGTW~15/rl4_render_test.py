"""OG-rl-4 PHASE A steps 4-6: synthetic render test of the deploy-to-ec2.sh template edit.

usage: python rl4_render_test.py <release template path> <live ref> <path to _env_shape_host.py>      (run from the release tree)
Renders the template's REMOTE heredoc with bash (variables set, nothing executed), then:
  1. .env printf: live vs release -- %s count, argument count, keys (50 = 50, same order); the release format equals the live
     format plus quote characters only (the quoting edits and nothing else).
  2. MASKED SAMPLE: the printf is run with masked values into a scratch file; the issuer's `_env_shape_host.py` parse (its own
     program text, path substituted) reads the file: live must show disagreeing 4 (calibration), release disagreeing 0.
     A second release sample with a whitespace MAIL_SENDER_TABLE also reads disagreeing 0.
  3. the roster block (host side) extracted from the rendered text and run with a stubbed `aws` and `python3.11`: a valid roster
     reaches the marker and the log counts come from the parsed JSON (1 / 2, and 1 / 3 for a 3-pair roster); a roster whose
     taxsma_workbook_identity is missing, non-string, empty or malformed refuses rc 3 BEFORE the marker; an extra key is admitted.
  4. the shell variable OG_TAXSMA_WORKBOOK_IDENTITY is read nowhere in code; the identity read precedes the extract, the .env tee, the restart.
Only masked literal values appear; no real secret is read."""
import json
import os
import re
import subprocess
import sys
import tempfile

TPL, LIVE, SHAPE = sys.argv[1], sys.argv[2], sys.argv[3]
GWT = "infra/aws/ec2/opal-gateway/deploy-to-ec2.sh"
ZERO = "00000000-0000-0000-0000-000000000000"
PAIR = ZERO + "/" + ZERO
PAIR2 = "11111111-1111-1111-1111-111111111111/22222222-2222-2222-2222-222222222222"
res = []


def show_live():
    return subprocess.run(["git", "show", "%s:%s" % (LIVE, GWT)], capture_output=True).stdout.decode("utf-8")


def render(text):
    lines = text.split("\n")
    s = next(i for i, ln in enumerate(lines) if ln.startswith("REMOTE_SCRIPT=$(cat <<REMOTE"))
    e = next(i for i, ln in enumerate(lines) if i > s and ln == "REMOTE")
    body = "\n".join(lines[s + 1:e])
    unesc = [m for m in re.finditer(r"(?<!\\)(\$\(|`)", body)]
    assert not unesc, "unescaped command substitution in the heredoc: %d" % len(unesc)
    prog = ("REGION=us-east-1\nGATEWAY_PORT=8080\nREMOTE_DIR=/opt/opal-gateway\nS3_URI=s3://x/y\nART=a.tar.gz\n"
            "SVC=opal-gateway\ncat <<REMOTE\n" + body + "\nREMOTE\n")
    r = subprocess.run(["bash", "-s"], input=prog.encode("utf-8"), capture_output=True)
    assert r.returncode == 0, r.stderr.decode()[:300]
    return r.stdout.decode("utf-8")


def printf_cmd(rendered):
    m = re.search(r"^(printf 'MOCK_GRAPH=0.*?') (\".*?\") \| sudo -u ec2-user tee [^\n]*/\.env >/dev/null", rendered, re.S | re.M)
    assert m, "printf line not found"
    fmt = m.group(1)[len("printf '"):-1]
    args = m.group(2)
    keys = [x.split("=", 1)[0] for x in fmt.split("\\n") if x]
    return fmt, args, keys, fmt.count("%s"), len(re.findall(r'"[^"]*"', args))


def sample(rendered, sender_table="m1@x.test,m2@x.test,m3@x.test"):
    """Run the rendered printf with masked values into a scratch file; return the file's path."""
    fmt, args, *_ = printf_cmd(rendered)
    out = os.path.join(tempfile.mkdtemp(), "sample.env")
    prog = ("REGION=us-east-1\nGATEWAY_PORT=8080\nREMOTE_DIR=/opt/opal-gateway\n"
            "TENANT_ID=MASKED-TENANT\nCLIENT_ID=MASKED-CLIENT\nCLIENT_SECRET=MASKED-CSEC\nFERNET_KEY=MASKED-FERNET\n"
            'OTP_BEARER="MASKED-OTP-A MASKED-OTP-B"\nMS_INGEST_BEARER=MASKED-MS\nGRAPH_READ_BEARER=MASKED-GR\n'
            "MASTER_ADMIN_PRINCIPALS=%s\nWRITE_CAPABLE_PRINCIPALS=%s,%s\nTRANSCRIPT_BEARER=MASKED-TR\nMAIL_BEARER=MASKED-ML\n"
            "MAIL_SENDER_TABLE='%s'\nBD_READER_EXTERNAL_ID=MASKED-BD\nTAXSMA_WORKBOOK_BEARER=MASKED-TX\nTAXSMA_WORKBOOK_IDENTITY=%s\n"
            "TEAMS_BEARER=MASKED-TM\nsudo() { shift 2; \"$@\"; }\n"
            % (PAIR, PAIR, PAIR2, sender_table, PAIR))
    cmd = "printf '" + fmt + "' " + args + " | sudo -u ec2-user tee " + out.replace("\\", "/") + " >/dev/null\n"
    r = subprocess.run(["bash", "-s"], input=(prog + cmd).encode("utf-8"), capture_output=True)
    assert r.returncode == 0, r.stderr.decode()[:300]
    return out


def shape(path):
    src = open(SHAPE, encoding="utf-8").read()
    # execute the issuer's own PROG_LINES with the .env path pointed at the sample
    ns = {}
    code = src.split("B64 =")[0]
    exec(compile(code, SHAPE, "exec"), ns)
    prog = "\n".join(ns["PROG_LINES"]).replace("/opt/opal-gateway/.env", path.replace("\\", "/"))
    r = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True)
    line = [x for x in r.stdout.splitlines() if x.startswith("HOST env_keys")]
    keys = [x for x in r.stdout.splitlines() if x.startswith("KEY ")]
    return (line[0] if line else "UNREAD " + r.stderr[:200]), keys


live_r, rel_r = render(show_live()), render(open(TPL, encoding="utf-8").read())
lf, la_, lk, lp, la = printf_cmd(live_r)
rf, ra_, rk, rp, ra = printf_cmd(rel_r)
print("LIVE    : %%s=%d args=%d keys=%d unique=%d" % (lp, la, len(lk), len(set(lk))))
print("RELEASE : %%s=%d args=%d keys=%d unique=%d" % (rp, ra, len(rk), len(set(rk))))
def _unquote_items(fmt):
    """Strip ONE surrounding quote pair ("..." or \047...\047) from each KEY=VALUE item of the printf format."""
    out = []
    for item in fmt.split("\\n"):
        k, eq, v = item.partition("=")
        for q in ('"', "\\047"):
            if eq and v.startswith(q) and v.endswith(q) and len(v) > 2 * len(q):
                v = v[len(q):-len(q)]
                break
        out.append(k + eq + v)
    return "\\n".join(out)


stripped = _unquote_items(rf)
ok1 = (lp == la and rp == ra and lp == rp and len(lk) == 50 and rk == lk and len(set(rk)) == 50 and stripped == lf and la_ == ra_)
print("keys 50 = 50 and same order: %s; release format minus quote characters == live format: %s; args line identical: %s" % (rk == lk, stripped == lf, la_ == ra_))
print("keys TEAMS_BEARER / TEAMS_BEARER_LABELS present: %s" % (("TEAMS_BEARER" in rk) and ("TEAMS_BEARER_LABELS" in rk)))
quoted = [k for k in rk if re.search(r"(^|\\n)%s=(\"|\\047)" % k, rf)]
print("values rendered quoted (%d): %s" % (len(quoted), quoted))
ok1 = ok1 and sorted(quoted) == sorted(["OTP_BEARER", "OTP_BEARER_LABELS", "ENABLED_INTEGRATIONS", "FIRM_ROLE_ARNS", "MAIL_SENDER_TABLE"])
print("PRINTF-RENDER %s" % ("PASS" if ok1 else "FAIL"))
res.append(ok1)

sl, kl = shape(sample(live_r))
sr, kr = shape(sample(rel_r))
sr2, _ = shape(sample(rel_r, "m1@x.test, m2@x.test"))
sl2, _ = shape(sample(live_r, "m1@x.test, m2@x.test"))
print("MASKED SAMPLE live    : %s" % sl)
print("MASKED SAMPLE release : %s" % sr)
print("MASKED SAMPLE live    with a whitespace sender table (negative control): %s" % sl2)
print("MASKED SAMPLE release with a whitespace sender table: %s" % sr2)


def dis(x):
    return int(re.search(r"disagreeing (\d+)", x).group(1))


ok2 = "env_keys 50 " in sr and dis(sr) == 0 and dis(sr2) == 0 and dis(sl) == 4 and dis(sl2) == 5
print("SAMPLE-DISAGREE %s (release 0 and 0; live calibration 4 and 5)" % ("PASS" if ok2 else "FAIL"))
res.append(ok2)

# 3. the host roster block
lines = rel_r.split("\n")
s = next(i for i, ln in enumerate(lines) if ln.startswith("ROSTERS_JSON=$(aws secretsmanager get-secret-value --secret-id gateway/principals/rosters"))
e = next(i for i, ln in enumerate(lines) if i > s and ln.startswith('echo "OK: principal rosters read host-side'))
block = "\n".join(lines[s:e + 1])


def run_block(roster):
    stub = "aws() { printf '%s' \"$STUB_JSON\"; }\npython3.11() { python \"$@\"; }\n"
    prog = "set -euo pipefail\n%s%s\necho FIRST_WRITE_REACHED\n[ -n \"$TAXSMA_WORKBOOK_IDENTITY\" ] && echo IDENTITY_SET_LEN_${#TAXSMA_WORKBOOK_IDENTITY}\n" % (stub, block)
    r = subprocess.run(["bash", "-s"], input=prog.encode("utf-8"), capture_output=True, env=dict(os.environ, STUB_JSON=json.dumps(roster)))
    return r.returncode, r.stdout.decode(), r.stderr.decode()


good = {"master_admin": PAIR, "write_capable": PAIR + "," + PAIR2, "taxsma_workbook_identity": PAIR2}
cases = [
    ("valid 1/2 pairs", good, 0, True, "master_admin 1 pair; write_capable 2 pairs; taxsma_workbook_identity 1 pair"),
    ("valid 1/3 pairs", dict(good, write_capable=",".join([PAIR, PAIR2, ZERO + "/" + PAIR2.split("/")[1]])), 0, True, "write_capable 3 pairs"),
    ("extra key admitted", dict(good, note="x"), 0, True, "write_capable 2 pairs"),
    ("identity missing", {k: v for k, v in good.items() if k != "taxsma_workbook_identity"}, 3, False, None),
    ("identity non-string", dict(good, taxsma_workbook_identity=123), 3, False, None),
    ("identity empty", dict(good, taxsma_workbook_identity=""), 3, False, None),
    ("identity malformed", dict(good, taxsma_workbook_identity="not-a-pair"), 3, False, None),
    ("identity two pairs", dict(good, taxsma_workbook_identity=PAIR + "," + PAIR2), 3, False, None),
]
ok3 = True
for name, roster, want_rc, want_reach, want_text in cases:
    rc, out, err = run_block(roster)
    reached = "FIRST_WRITE_REACHED" in out
    text_ok = True if want_text is None else (want_text in out)
    leaked = PAIR2 in out + err or PAIR in out + err
    ok = rc == want_rc and reached == want_reach and text_ok and not leaked
    ok3 = ok3 and ok
    print("roster %-20s rc=%d first-write-reached=%s log-line-ok=%s value-printed=%s %s" % (name, rc, reached, text_ok, leaked, "OK" if ok else "UNEXPECTED"))
print("ROSTER-BLOCK %s" % ("PASS" if ok3 else "FAIL"))
res.append(ok3)

# 4. the shell variable is read nowhere in code; positions
code_lines = [ln for ln in open(TPL, encoding="utf-8").read().split("\n") if "OG_TAXSMA_WORKBOOK_IDENTITY" in ln and not ln.lstrip().startswith("#")]
live_code = [ln for ln in show_live().split("\n") if "OG_TAXSMA_WORKBOOK_IDENTITY" in ln and not ln.lstrip().startswith("#")]
pos_id = rel_r.index("TAXSMA_WORKBOOK_IDENTITY=$(printf")
pos_tar = rel_r.index("tar -xzf")
pos_tee = rel_r.index("tee /opt/opal-gateway/.env")
pos_rst = rel_r.index("systemctl restart")
okp = pos_id < pos_tar < pos_tee < pos_rst
print("OG_TAXSMA_WORKBOOK_IDENTITY code lines: live %d, release %d; positions identity read %d < extract %d < .env tee %d < restart %d: %s" % (len(live_code), len(code_lines), pos_id, pos_tar, pos_tee, pos_rst, okp))
ok4 = len(code_lines) == 0 and len(live_code) >= 1 and okp
print("SHELL-VARIABLE-GONE %s" % ("PASS" if ok4 else "FAIL"))
res.append(ok4)
print("RENDER TEST %s" % ("PASS" if all(res) else "FAIL"))
sys.exit(0 if all(res) else 1)
