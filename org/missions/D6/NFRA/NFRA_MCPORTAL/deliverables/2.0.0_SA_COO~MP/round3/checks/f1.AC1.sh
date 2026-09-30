#!/usr/bin/env bash
# MP-f-1 AC1 (R-8, disarms row Z-W2-S3): the gateway tests that reach the audit path -- tests/test_owner_gate.py,
# tests/test_admin_grants.py, tests/test_admin_round2.py -- run green and leave the TRACKED
# infra/aws/ec2/opal-gateway/audit.jsonl byte-identical (md5 before == md5 after, and `git status --porcelain` on it
# empty). POSITIVE CONTROL beside it: a planted one-line append to the same file IS seen by the same two probes, then
# the file is put back from the byte copy taken before the run (never `git restore`, which would clobber a peer's edit).
# Bounded: the three files run in ~10 s; the full collectable suite is the COO's drain check, not this criterion.
. "$(dirname "$0")/_root.sh"
G="infra/aws/ec2/opal-gateway"; A="$G/audit.jsonl"
T="${TMPDIR:-/tmp}/mp_f1_ac1_$$"; mkdir -p "$T"; cp "$A" "$T/audit.before"
md5b=$(md5sum "$A" | cut -d' ' -f1); pre=$(git status --porcelain -- "$A" | wc -l)
out=$(cd "$G" && timeout 100 python -m pytest -q -p no:cacheprovider tests/test_owner_gate.py tests/test_admin_grants.py tests/test_admin_round2.py 2>&1 | tr -d '\r' | tail -1)
md5a=$(md5sum "$A" | cut -d' ' -f1); post=$(git status --porcelain -- "$A" | wc -l)
passed=$(printf '%s' "$out" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+' || echo 0)
failed=$(printf '%s' "$out" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1 || true); failed=${failed:-0}
# the positive control, on the restored bytes
cp "$T/audit.before" "$A"
echo '{"planted":"mp-f-1 positive control"}' >> "$A"
ctl_md5=$(md5sum "$A" | cut -d' ' -f1); ctl_st=$(git status --porcelain -- "$A" | wc -l)
cp "$T/audit.before" "$A"; restored=$(md5sum "$A" | cut -d' ' -f1); rm -rf "$T"
ctl=no; [ "$ctl_md5" != "$md5b" ] && [ "$ctl_st" -ge 1 ] && ctl=yes
echo "pytest: $out"
echo "audit.jsonl: md5 before=$md5b after=$md5a; porcelain before=$pre after=$post; control seen=$ctl; restored=$([ "$restored" = "$md5b" ] && echo yes || echo NO)"
if [ "${passed:-0}" -ge 1 ] && [ "$failed" = 0 ] && [ "$md5a" = "$md5b" ] && [ "$post" = "$pre" ] && [ "$pre" = 0 ] && [ "$ctl" = yes ]; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
