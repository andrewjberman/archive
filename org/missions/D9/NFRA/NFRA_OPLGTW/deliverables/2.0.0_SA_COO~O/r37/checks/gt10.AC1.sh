#!/usr/bin/env bash
# OPLGTW OG-gt-10 AC1 (round-37, FWD-22): the gateway modules import on a HOST-SHAPED path and find the staged calendar.
# The host path is /opt/opal-gateway/app/<module>.py (4 parents); `Path(__file__).parents[5]` raised IndexError there.
# This check copies app/ to a shallow path (C:/tmp/gt10host.<pid>/opal-gateway/app), stages lib/trading_calendar.py beside it
# the way the artifact does (<root>/lib/trading_calendar.py), and imports both portal modules in a fresh interpreter.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D="/c/tmp/gt10host.$$"
rm -rf "$D"; mkdir -p "$D/opal-gateway/lib" || { echo "ERROR: cannot make $D"; exit 9; }
cp -R "$GW/app" "$D/opal-gateway/app"
cp lib/trading_calendar.py "$D/opal-gateway/lib/trading_calendar.py"
find "$D" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null   # rail-checked: scratch copy under C:/tmp
out=$(cd "$D/opal-gateway" && timeout 100 python -c "
import sys
sys.path.insert(0, '.')
res = {}
for name in ('portal_models', 'portal_macro'):
    try:
        m = __import__('app.' + name, fromlist=['_calendar'])
        cal = m._calendar()
        res[name] = (True, cal is not None)
    except Exception as e:
        res[name] = (False, type(e).__name__)
ok_imp = all(v[0] for v in res.values())
ok_cal = all(v[0] and v[1] is True for v in res.values())
t1 = None
if ok_cal:
    import datetime as dt
    t1 = sys.modules['app.portal_models']._t1_date()
print('host-shaped import: portal_models %s, portal_macro %s; calendar importable %s; T-1 computable %s' % (
    'OK' if res['portal_models'][0] else 'FAIL(' + str(res['portal_models'][1]) + ')',
    'OK' if res['portal_macro'][0] else 'FAIL(' + str(res['portal_macro'][1]) + ')',
    'yes' if ok_cal else 'no', 'yes' if t1 is not None else 'no'))
sys.exit(0 if (ok_imp and ok_cal and t1 is not None) else 1)
" 2>&1 | tr -d '\r' | tail -3); rc=$?
echo "$out"
rm -rf "$D"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
