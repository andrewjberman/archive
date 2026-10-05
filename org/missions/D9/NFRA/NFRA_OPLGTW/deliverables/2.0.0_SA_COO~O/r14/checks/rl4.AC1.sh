#!/usr/bin/env bash
# OPLGTW OG-rl-4 AC1 (round 14) (rows Z-S32, Z-W19-S13; analysis round 12 s.5 item 2 read-back), on the SERVED host:
#  1. .env key NAMES equal the before-set recorded at the cut (r14/RL4_ENV_KEYS_BEFORE.txt, 50): nothing lost, nothing added;
#  2. every value is read identically by a systemd-style and a bash-style (shlex) parse: disagreeing 0;
#  3. the host deploy/ contract copy's sha256 equals org/standards/NFRA_OPLGTW_CONTRACT.json at HEAD;
#  4. the Tax route keys are present and non-empty (capability stays ON with the identity now read host-side).
# Names and booleans only; .env is never sourced (row Z-S32).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_ssm.sh"
H="$(cd "$(dirname "$0")" && pwd)"
B="${RL4_ENV_KEYS_BASELINE:-$H/../RL4_ENV_KEYS_BEFORE.txt}"; n=0   # override: a release that ADDS a ruled key points this at its own set (r17/ENV_KEYS_R17B.txt, R15)
want_c=$(git show "HEAD:org/standards/NFRA_OPLGTW_CONTRACT.json" | sha256sum | cut -d' ' -f1)
ssm_run "$(python "$(native "$H/_env_shape_host.py")" | tr -d '\r')"; o1="$SSM_OUT"; echo "ssm $SSM_ID status=$SSM_STATUS"
ssm_run "$(python "$(native "$H/../../trnspt/checks/_tr_host.py")" | tr -d '\r')"; o2="$SSM_OUT"; echo "ssm $SSM_ID status=$SSM_STATUS"
before=$(grep -v '^#' "$B" | grep . | sort -u); now=$(printf '%s\n' "$o1" | sed -n 's/^KEY \([A-Z0-9_]*\) .*/\1/p' | sort -u)
lost=$(comm -23 <(printf '%s\n' "$before") <(printf '%s\n' "$now") | grep -c .)
added=$(comm -13 <(printf '%s\n' "$before") <(printf '%s\n' "$now") | grep -c .)
if [ "$lost" = 0 ] && [ "$added" = 0 ] && [ -n "$now" ]; then echo "arm 1 key names equal the before-set ($(printf '%s\n' "$now" | grep -c .)): OK"; n=$((n+1)); else echo "arm 1 key names: lost $lost added $added: FAIL"; fi
dis=$(printf '%s\n' "$o1" | sed -n 's/^HOST env_keys [0-9]* whitespace_values [0-9]* disagreeing \([0-9]*\)$/\1/p')
if [ "$dis" = 0 ]; then echo "arm 2 systemd and bash parses agree on every value: OK"; n=$((n+1)); else echo "arm 2 disagreeing values ${dis:-UNREAD}: FAIL"; fi
have_c=$(printf '%s\n' "$o1" | sed -n 's/^HOST contract_sha256 //p')
if [ "$have_c" = "$want_c" ]; then echo "arm 3 host deploy/ contract equals org/standards (${want_c:0:12}): OK"; n=$((n+1)); else echo "arm 3 host contract ${have_c:0:12} vs ${want_c:0:12}: FAIL"; fi
if printf '%s\n' "$o2" | grep -qE "^HOST env_keys [0-9]+ taxsma_keys 2 identity_empty False bearer_empty False$"; then echo "arm 4 Tax keys present and non-empty: OK"; n=$((n+1)); else echo "arm 4 Tax keys: FAIL"; fi
echo "RELEASE READ-BACK ARMS $n of 4"
[ "$n" = 4 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
