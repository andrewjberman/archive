"""AR-y-311 step 2: derive the r29 host script from the r28 host script by line-exact replacements (ASCII only).

Every replacement must match exactly once; any miss refuses.
usage: python -I make_host_r29.py <r28 script> <r29 script>
"""
import sys

SRC, DST = sys.argv[1], sys.argv[2]
text = open(SRC, "rb").read().decode("ascii")
lines = text.split("\n")

REPL = {
    2: "# Ledger irpt-resident-r29-20261014: resident root 0485393f3a-r28 -> 0485393f3a-r29 (the r28 member set with the trunk HEAD blobs of",
    3: "# intake/uploads.py and ops/status.py replaced (AR-y-308 Shares words; the rest of the r28 member set unchanged, base pin 0485393f3a, package pin f812980d12),",
    4: "# and the 0485393f3a-r28 root and its library stay on the host for rollback.",
    5: "# Copy of the r28 script with NEW, OLD, WANT_TAR, the two moved member checks, the ledger and this header changed; written by 0.9.0_WK_IRPT_ANLREQ~125",
    6: "# for 2.0.0_SA_COO~Y2 (AR-y-311, build only); operator 0.7.0_AE_CloudOps~YC2. Authoring this script uploaded, installed and applied nothing.",
    7: "NEW=0485393f3a-r29",
    8: "OLD=0485393f3a-r28",
    15: "WANT_TAR=2de2adce622f8bb9bbd5ebc071e862446b056303c0d9ffd7d41b050bd17f51a4",
    46: 'check "intake/uploads.py" f85e8c9bb5af6ceddc6ccd513e511368447966d21f805a09306ef8f3cda81494',
    48: 'check "ops/status.py" 87048c7f4d00ba33c87de1a223a36b53e3487ed7414d613ee744984bcaef6030',
    76: '          "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ledger": "irpt-resident-r29-20261014"})',
}

old_lines = list(lines)
for n, new in REPL.items():
    i = n - 1
    if i >= len(lines):
        raise SystemExit("REFUSE: line %d beyond file" % n)
    print("OLD %3d: %s" % (n, lines[i]))
    print("NEW %3d: %s" % (n, new))
    lines[i] = new

out = "\n".join(lines)
open(DST, "wb").write(out.encode("ascii"))
print("replaced lines:", sorted(REPL))
