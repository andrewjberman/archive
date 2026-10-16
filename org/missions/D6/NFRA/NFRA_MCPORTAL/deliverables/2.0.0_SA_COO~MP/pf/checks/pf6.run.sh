#!/usr/bin/env bash
# MP-pf-6 read step (the issuer's; a worker runs it and keeps its stdout): ONE read-only SSM command on the gateway host, under the instance role (_r2_probe.py is the command).
# Prints `ssm command=<id> status=<Success|Failed|NONE>` and then the probe's single `R2 {json}` line when the read worked. Writes nothing.
. "$(dirname "$0")/../../pc/checks/_root.sh"
T="${TMPDIR:-/tmp}/mp_pf6_$$"; mkdir -p "$T"
python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/checks/_r2_probe.py "$(cygpath -m "$T")/params.json"
ssm_run "$T/params.json"; rm -rf "$T"
echo "ssm command=$SSM_CID status=$SSM_ST"
printf '%s\n' "$SSM_OUT" | grep -m1 '^R2 ' || echo "no R2 line; last output: $(printf '%s\n' "$SSM_OUT" | tail -1 | cut -c1-300)"
