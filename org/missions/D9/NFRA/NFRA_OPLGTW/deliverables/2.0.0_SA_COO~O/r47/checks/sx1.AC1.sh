#!/usr/bin/env bash
# OPLGTW OG-sx-1 AC1 (round 47): D2 (Z-S410) the Cottonwood Black Diamond adapter parses the source's MM/DD/YYYY Trade Date, and the Z-S407 mask
# (family_depth._why) scrubs ARN, twelve-digit and instance-id shapes from an exception text. The fake identifiers are built at run time, never typed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 100 python3 -I - <<'EOF'
import sys, datetime as dt, re
sys.path.insert(0, ".")
from app import client_adapter_bdcottonwood as bd
from app import family_depth as fd
ok = True
cases = [("10/12/2026", dt.date(2026, 10, 12)), ("1/5/2026", dt.date(2026, 1, 5)), ("2026-10-12", dt.date(2026, 10, 12)),
         ("2026-10-12T04:05:06", dt.date(2026, 10, 12)), ("13/45/2026", None), ("garbage", None), (None, None), ("", None)]
good = 0
for raw, want in cases:
    got = bd._date(raw)
    hit = got == want
    good += 1 if hit else 0
    print("_date(%r) = %s (want %s): %s" % (raw, got, want, "ok" if hit else "NO"))
ok = ok and good == len(cases)
print("date cases %d of %d" % (good, len(cases)))
acct = "1" * 12
arn = "arn:aws:iam::" + acct + ":role/some-role"
iid = "i-" + "a" * 17
msg = "An error occurred (AccessDenied) when calling X: User: %s is not authorized on %s of %s and %s" % (arn, arn, acct, iid)
masked = fd._why(PermissionError(msg))
shapes = {"arn": bool(re.search(r"arn:aws[a-z-]*:", masked)), "twelve-digit": bool(re.search(r"(?<!\d)\d{12}(?!\d)", masked)),
          "instance-id": bool(re.search(r"\bi-[0-9a-f]{8,17}\b", masked))}
print("masked text: class kept %s; length %d (want <= 230); shapes left %s" % (masked.startswith("PermissionError"), len(masked), {k: v for k, v in shapes.items() if v} or "none"))
ok = ok and masked.startswith("PermissionError") and len(masked) <= 230 and not any(shapes.values())
plain = fd._why(ValueError("table not found: widgets"))
print("plain text kept: %r: %s" % (plain, "ok" if plain == "ValueError: table not found: widgets" else "NO"))
ok = ok and plain == "ValueError: table not found: widgets"
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
