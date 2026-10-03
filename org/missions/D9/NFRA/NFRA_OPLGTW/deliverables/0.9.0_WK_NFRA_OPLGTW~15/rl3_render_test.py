"""OG-rl-3 PHASE A step 3: synthetic render test of the deploy-to-ec2.sh template edit (TEAMS_BEARER).

usage: python rl3_render_test.py <release template path> <live ref>      (run from the release tree)
Renders the template's REMOTE heredoc with bash (variables set, nothing executed), then:
  1. .env printf: live vs release, %s count, argument count, keys (48 -> 50, existing unchanged and in order).
  2. the TEAMS block extracted from the rendered text run with a stubbed `aws`: failed read, empty and 'None' each refused
     (rc 3) before the marker that stands for the first write; a value reaches it.
  3. positions: the block precedes the tar extract, the .env tee and the restart in the rendered text.
No real secret is read; the only value is the literal 'synthetic-value'."""
import re
import subprocess
import sys

TPL, LIVE = sys.argv[1], sys.argv[2]
GWT = "infra/aws/ec2/opal-gateway/deploy-to-ec2.sh"


def show_live():
    return subprocess.run(["git", "show", "%s:%s" % (LIVE, GWT)], capture_output=True).stdout.decode("utf-8")


def render(text):
    lines = text.split("\n")
    s = next(i for i, ln in enumerate(lines) if ln.startswith("REMOTE_SCRIPT=$(cat <<REMOTE"))
    e = next(i for i, ln in enumerate(lines) if i > s and ln == "REMOTE")
    body = "\n".join(lines[s + 1:e])
    # nothing in the heredoc may expand a command at render time: every $( and backtick must be escaped
    unesc = [m for m in re.finditer(r"(?<!\\)(\$\(|`)", body)]
    assert not unesc, "unescaped command substitution in the heredoc: %d" % len(unesc)
    prog = ("REGION=us-east-1\nGATEWAY_PORT=8080\nREMOTE_DIR=/opt/opal-gateway\nS3_URI=s3://x/y\nART=a.tar.gz\n"
            "OG_TAXSMA_WORKBOOK_IDENTITY=SYNTH-IDENTITY\nSVC=opal-gateway\n"
            "cat <<REMOTE\n" + body + "\nREMOTE\n")
    r = subprocess.run(["bash", "-s"], input=prog.encode("utf-8"), capture_output=True)
    assert r.returncode == 0, r.stderr.decode()[:300]
    return r.stdout.decode("utf-8")


def printf_parts(rendered):
    m = re.search(r"^printf '(MOCK_GRAPH=0.*?)' (\".*?\") \| sudo -u ec2-user tee [^\n]*/\.env", rendered, re.S | re.M)
    assert m, "printf line not found"
    fmt, args = m.group(1), m.group(2)
    keys = [x.split("=", 1)[0] for x in fmt.split("\\n") if x]
    nargs = len(re.findall(r'"[^"]*"', args))
    return fmt, keys, fmt.count("%s"), nargs


live_r, rel_r = render(show_live()), render(open(TPL, encoding="utf-8").read())
lf, lk, lp, la = printf_parts(live_r)
rf, rk, rp, ra = printf_parts(rel_r)
print("LIVE    : %%s=%d args=%d keys=%d unique=%d" % (lp, la, len(lk), len(set(lk))))
print("RELEASE : %%s=%d args=%d keys=%d unique=%d" % (rp, ra, len(rk), len(set(rk))))
ok1 = (lp == la and rp == ra and len(lk) == 48 and len(rk) == 50 and len(set(rk)) == 50 and rk[:48] == lk
       and rk[48:] == ["TEAMS_BEARER", "TEAMS_BEARER_LABELS"] and rp == lp + 1)
print("keys: existing 48 unchanged and in order: %s; added %s; %%s +1: %s" % (rk[:48] == lk, rk[48:], rp == lp + 1))
print("TEAMS_BEARER_LABELS fixed value teamsassist in the format: %s" % ("TEAMS_BEARER_LABELS=teamsassist" in rf))
ok1 = ok1 and "TEAMS_BEARER_LABELS=teamsassist" in rf
# the live format is a strict prefix of the release format up to the added keys
ok1 = ok1 and rf.startswith(lf[:-2]) and rf == lf[:-2] + "\\nTEAMS_BEARER=%s\\nTEAMS_BEARER_LABELS=teamsassist\\n"
print("release format = live format + the two lines only: %s" % (rf == lf[:-2] + "\\nTEAMS_BEARER=%s\\nTEAMS_BEARER_LABELS=teamsassist\\n"))
# the last arguments: live ends with TAXSMA identity, release adds TEAMS_BEARER
ok1 = ok1 and re.search(r'"\$TAXSMA_WORKBOOK_IDENTITY" "\$TEAMS_BEARER" \| sudo', rel_r) is not None
print("PRINTF-RENDER %s" % ("PASS" if ok1 else "FAIL"))

lines = rel_r.split("\n")
s = next(i for i, ln in enumerate(lines) if ln.startswith("TEAMS_BEARER=$(aws secretsmanager get-secret-value --secret-id gateway/teams/bearer"))
e = next(i for i, ln in enumerate(lines) if i > s and ln.startswith('echo "OK: teams bearer read host-side'))
block = "\n".join(lines[s:e + 1])
pos_teams = rel_r.index("TEAMS_BEARER=$(aws")
pos_tar = rel_r.index("tar -xzf")
pos_tee = rel_r.index("tee /opt/opal-gateway/.env")
pos_rst = rel_r.index("systemctl restart")
posok = pos_teams < pos_tar < pos_tee < pos_rst
print("positions: teams block %d < tar extract %d < .env tee %d < restart %d : %s" % (pos_teams, pos_tar, pos_tee, pos_rst, posok))


def run(mode):
    stub = {"fail": "aws() { return 255; }", "empty": "aws() { printf ''; }", "none": "aws() { echo None; }",
            "value": "aws() { echo synthetic-value; }"}[mode]
    prog = "set -euo pipefail\n%s\n%s\necho FIRST_WRITE_REACHED\n" % (stub, block)
    r = subprocess.run(["bash", "-s"], input=prog.encode("utf-8"), capture_output=True)
    return r.returncode, r.stdout.decode(), r.stderr.decode()


res = {}
for mode in ("fail", "empty", "none", "value"):
    rc, out, err = run(mode)
    reached = "FIRST_WRITE_REACHED" in out
    res[mode] = (rc, reached)
    leaked = "synthetic-value" in out + err
    print("synthetic %-5s rc=%d first-write-reached=%s value-printed=%s%s" % (mode, rc, reached, leaked, ("  stderr: " + err.strip()[:90]) if err.strip() else ""))
refused = all(res[m] == (3, False) for m in ("fail", "empty", "none")) and res["value"] == (0, True)
print("REFUSAL-TEST %s" % ("PASS" if refused and posok else "FAIL"))
print("RENDER TEST %s" % ("PASS" if ok1 and refused and posok else "FAIL"))
sys.exit(0 if ok1 and refused and posok else 1)
