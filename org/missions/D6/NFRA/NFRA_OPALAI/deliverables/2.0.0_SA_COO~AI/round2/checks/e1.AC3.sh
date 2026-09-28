#!/usr/bin/env bash
# OA-e-1 AC3 (R-5, row Z-W8-S1; a NO-REGRESSION BOUND): tests/test_data_entitlement_guard.py COLLECTS with moto importable
# from the G-MOTO scratch target C:/tmp/moto-target (G-MOTO GIVEN, record @f8d1103a38; never the system Python), passes
# >= 10, errors 0, and the failed set is EXACTLY the TWO measured at the round-2 cut (c8df03c408, moto 5.2.3: 10 passed, 2 failed -- test_ogz1_ac05 KeyError
# 'unclassified' and test_ogz1_ac08 the route-class set; row NFRA_OPALAI-Z-S36 @3c61dbe4d3; neither is this cell's). A NEW
# failure is a regression and FAILS; so does a changed failed set.
. "$(dirname "$0")/_root.sh"
G=infra/aws/ec2/opal-gateway
T="C:/tmp/moto-target"
ALLOWED=" test_ogz1_ac05 test_ogz1_ac08 "
mv=$(PYTHONPATH="$T" timeout 30 python -c "import moto;print(moto.__version__)" 2>&1 | tr -d '\r' | tail -1)
out=$(cd "$G" && PYTHONPATH="$T;." timeout 115 python -m pytest tests/test_data_entitlement_guard.py -q -rfE -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -v '^[[:space:]]*$')
summ=$(printf '%s\n' "$out" | tail -1)
passed=$(printf '%s\n' "$summ" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
errs=$(printf '%s\n' "$summ" | grep -cE '[0-9]+ error')
failed=$(printf '%s\n' "$out" | grep -E '^FAILED ' | sed -E 's/^FAILED [^:]*::([A-Za-z0-9_]+).*/\1/' | sort -u)
new=""
for f in $failed; do case "$ALLOWED" in *" $f "*) ;; *) new="$new $f";; esac; done
echo "moto from $T: $mv; guard suite: $summ; passed=$passed; failed=[$(echo $failed)]; new failures=[${new# }]"
fs=$(echo $failed)
if [ "$passed" -ge 10 ] && [ "$errs" = 0 ] && [ -z "$new" ] && [ "$fs" = "test_ogz1_ac05 test_ogz1_ac08" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
