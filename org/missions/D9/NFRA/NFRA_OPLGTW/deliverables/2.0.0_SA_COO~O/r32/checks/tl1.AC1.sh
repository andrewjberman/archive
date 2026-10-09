#!/usr/bin/env bash
# OPLGTW OG-tl-1 AC1 (CTO~Z ruling @261e2c42a0, Phase A): the release candidate named in W/tl1_release.json
# ({"base_sha", "release_sha"}) differs from its base in exactly ONE file, infra/aws/ec2/opal-gateway/deploy-to-ec2.sh;
# that file sets TRANSCRIPT_MEETING_ALLOWLIST from data/transcripts/scripts/teams/meeting_allowlist.json and types none
# of the 4 ids (never retyped); the release tree carries that json byte-equal to HEAD's.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~48/tl1_release.json"
J="data/transcripts/scripts/teams/meeting_allowlist.json"
[ -f "$REC" ] || { echo "tl1_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
echo "base $base -> release $rel: files differing $n (want 1): $files"
S=$(MSYS_NO_PATHCONV=1 git show "$rel:infra/aws/ec2/opal-gateway/deploy-to-ec2.sh" | tr -d '\r')
reads=$(printf '%s\n' "$S" | grep -c 'meeting_allowlist\.json')
typed=0; for id in $(python -c "import json;print(' '.join(m['online_meeting_id'] for m in json.load(open('$J',encoding='utf-8'))['meetings']))" | tr -d '\r'); do
  printf '%s\n' "$S" | grep -qF "$id" && typed=$((typed+1)); done
same=no; [ "$(MSYS_NO_PATHCONV=1 git show "$rel:$J" | git hash-object --stdin)" = "$(git hash-object "$J")" ] && same=yes
echo "deploy-to-ec2.sh reads meeting_allowlist.json: $reads (want >=1); ids typed literally: $typed (want 0); release json equals HEAD's: $same"
[ "$n" = 1 ] && [ "$files" = "infra/aws/ec2/opal-gateway/deploy-to-ec2.sh" ] && [ "$reads" -ge 1 ] && [ "$typed" = 0 ] && [ "$same" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
