"""OG-rl-2 AC3 read: the SHIPPED deploy template takes MAIL_SENDER_TABLE host-side from the artifact's
deploy/mail_sender_table.txt (row Z-S36's durable fix, CTO msg 27843) and refuses an empty table before any .env write.
Prints booleans and counts only, never an address.

usage: python _rl2.py <deploy_template_path>
Last line: RESULT: PASS|FAIL
"""
import re
import subprocess
import sys

s = open(sys.argv[1], encoding="utf-8").read()
reads_file = "deploy/mail_sender_table.txt" in s
needs_shell = "${OG_MAIL_SENDER_TABLE" in s or "$OG_MAIL_SENDER_TABLE" in s
refuse = [ln for ln in s.splitlines() if "REFUSED" in ln and "MAIL_SENDER_TABLE" in ln and "empty" in ln.lower()]
print("template reads deploy/mail_sender_table.txt host-side: %s" % reads_file)
print("template still takes OG_MAIL_SENDER_TABLE from the deploying shell: %s" % needs_shell)
print("empty-table refusal lines naming MAIL_SENDER_TABLE: %d" % len(refuse))
render = [ln for ln in s.splitlines() if "/.env >/dev/null" in ln and "printf" in ln]
ok = reads_file and not needs_shell and len(refuse) >= 1
if len(render) == 1:
    fmt = re.search(r"printf '([^']*)'", render[0]).group(1)
    args = render[0][render[0].index(fmt) + len(fmt) + 1:].split("|")[0]
    n_fmt, n_args = fmt.count("%s"), len(re.findall(r'"[^"]*"', args))
    print(".env render: %%s %d, args %d; MAIL_SENDER_TABLE line %s" % (n_fmt, n_args, "MAIL_SENDER_TABLE=" in fmt))
    ok &= n_fmt == n_args and "MAIL_SENDER_TABLE=" in fmt
else:
    print(".env render lines: %d (expected 1)" % len(render))
    ok = False
b = subprocess.run(["bash", "-n", sys.argv[1]], capture_output=True, text=True)
print("bash -n rc=%d" % b.returncode)
ok &= b.returncode == 0
print("RESULT: %s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
