#!/usr/bin/env bash
# OPLGTW OG-yr-1 AC1 (round-37 YEARINREVIEW, PHASE A): the one-file release carries exactly the CRO's final page.
#  - W/yr_release.json base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - base..release differs in exactly three files: the page, app/yearinreview_view.py (A2: any non-guest Opal identity may view) and its test file;
#  - the page's bytes at the release equal the CRO's page at pin 947fc522a8 in LF form (md5 3bbd5ab2d325657020357003c3ea387d; the pin blob is CRLF);
#  - the view gate and the three named tests are in the release.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/yr_release.json"
SRC="org/tier1_exec/4.0.0_SA_CRO/deliverables/BRIEF1_YEAR_ONE_20261004/YEAR_ONE_ONE_PAGER.html"
ONE="infra/aws/ec2/opal-gateway/app/static/yearinreview/index.html"
[ -f "$REC" ] || { echo "yr_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" || { echo "release_sha ${rel:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); n=$(printf '%s\n' "$files" | grep -c .)
VIEW="infra/aws/ec2/opal-gateway/app/yearinreview_view.py"; TST="infra/aws/ec2/opal-gateway/tests/test_yearinreview_view.py"
want=$(printf '%s\n' "$ONE" "$VIEW" "$TST" | sort); got=$(printf '%s\n' "$files" | sort)
one=no; [ "$want" = "$got" ] && one=yes
LFMD5=3bbd5ab2d325657020357003c3ea387d
m_src=$(MSYS_NO_PATHCONV=1 git show "947fc522a8:$SRC" | tr -d '\r' | md5sum | cut -c1-32)
m_rel=$(MSYS_NO_PATHCONV=1 git show "$rel:$ONE" | md5sum | cut -c1-32)
eq=no; [ "$m_src" = "$LFMD5" ] && [ "$m_src" = "$m_rel" ] && eq=yes
gate=no; MSYS_NO_PATHCONV=1 git show "$rel:$VIEW" | tr -d '\r' | grep -q "_is_opal_user(email) or (bool(roster) and email in roster)" && gate=yes
nt=$(MSYS_NO_PATHCONV=1 git show "$rel:$TST" | tr -d '\r' | grep -cE "^def (test_yr1_opal_admitted_on_empty_roster|test_yr1_guest_refused|test_yr1_outside_domain_refused)\(")
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}"
echo "files differing $n (want 3); they are the page, the view gate and its test file: $one; release page equals the CRO page at 947fc522a8 in LF form: $eq (md5 $m_src / $m_rel); the gate admits Opal users on an empty roster: $gate; tests defined $nt of 3"
[ "$base" = "$live" ] && [ "$n" = 3 ] && [ "$one" = yes ] && [ "$eq" = yes ] && [ "$gate" = yes ] && [ "$nt" = 3 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
