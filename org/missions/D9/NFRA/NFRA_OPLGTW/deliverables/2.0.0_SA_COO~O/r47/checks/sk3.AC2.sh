#!/usr/bin/env bash
# OPLGTW OG-sk-3 AC2 (statements and bounds), on infra/aws/terraform/opal-gateway/schwab_reader_iam.tf and its pinned blob 95427d8edc:
#  (a) `terraform fmt -check` accepts the file (syntax and style);
#  (b) the CATALOG role's policy block holds, besides its six existing statements, exactly TWO new ones on the STATE bucket: a Deny on s3:ListBucket with Resource local.schwab_state_bucket_arn and StringNotLike s3:prefix local.schwab_state_complete_prefix_form,
#      and an Allow on s3:ListBucket with Resource local.schwab_state_bucket_arn and StringLike s3:prefix local.schwab_state_complete_prefix_form; its `DenyListingOtherBuckets` NotResource names BOTH bucket ARNs (a list);
#  (c) the DATA role's policy block keeps its six statements and names no state bucket;
#  (d) no new action: the words s3:Put, s3:Delete, s3:* and sts: do not appear in any added line; no added line names "*" as the whole Resource;
#  (e) the file differs from the pin by at most 70 added lines and 12 removed lines.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F=infra/aws/terraform/opal-gateway/schwab_reader_iam.tf
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
fmt=no; terraform fmt -check "$F" >/dev/null 2>&1 && fmt=yes
res=$(python3 -I - "$(native "$F")" "$fmt" <<'PYEOF'
import difflib, re, subprocess, sys
F, fmt = sys.argv[1], sys.argv[2]
t = open(F, encoding="utf-8").read()
pin = subprocess.run(["git", "show", "95427d8edc1450c4172f37bd43045d590eae0dc2"], capture_output=True).stdout.decode("utf-8")
ok = True


def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NOT OK", (" (%s)" % extra) if extra else ""))


say("terraform fmt -check accepts the file", fmt == "yes")


def block(name):
    i = t.index('resource "aws_iam_role_policy" "%s"' % name)
    j = t.index("\n}\n", i)
    return t[i:j]


cat, dat = block("schwab_catalog_read_policy"), block("schwab_data_read_policy")
nstate_cat = len(re.findall(r"local\.schwab_state_bucket_arn", cat))
deny = re.search(r'Effect\s*=\s*"Deny"\s*\n\s*Action\s*=\s*"s3:ListBucket"\s*\n\s*Resource\s*=\s*local\.schwab_state_bucket_arn\s*\n\s*Condition\s*=\s*\{\s*StringNotLike\s*=\s*\{\s*"s3:prefix"\s*=\s*local\.schwab_state_complete_prefix_form', cat)
allow = re.search(r'Effect\s*=\s*"Allow"\s*\n\s*Action\s*=\s*"s3:ListBucket"\s*\n\s*Resource\s*=\s*local\.schwab_state_bucket_arn\s*\n\s*Condition\s*=\s*\{\s*StringLike\s*=\s*\{\s*"s3:prefix"\s*=\s*local\.schwab_state_complete_prefix_form', cat)
other = re.search(r'Sid\s*=\s*"DenyListingOtherBuckets"[\s\S]*?NotResource\s*=\s*\[([^\]]*)\]', cat)
both = bool(other) and "local.schwab_bucket_arn" in other.group(1) and "local.schwab_state_bucket_arn" in other.group(1)
sids_cat = len(re.findall(r"\bSid\s*=", cat))
say("catalog policy: 8 statements (6 old + 2 new), the new Deny and Allow on the state bucket's prefix form, DenyListingOtherBuckets names both bucket ARNs", sids_cat == 8 and bool(deny) and bool(allow) and both, "statements %d, deny %s, allow %s, both %s" % (sids_cat, bool(deny), bool(allow), both))
sids_dat = len(re.findall(r"\bSid\s*=", dat))
say("data policy: still 6 statements and no mention of the state bucket", sids_dat == 6 and "state_bucket" not in dat and "49financial" not in dat, "statements %d" % sids_dat)
d = list(difflib.unified_diff(pin.splitlines(), t.splitlines(), lineterm="", n=0))
added = [x[1:] for x in d if x.startswith("+") and not x.startswith("+++")]
removed = [x for x in d if x.startswith("-") and not x.startswith("---")]
bad = [x for x in added if re.search(r"s3:Put|s3:Delete|s3:\*|sts:|Resource\s*=\s*\"\*\"", x)]
say("added lines carry no write, delete, wildcard-action or sts action, and no bare \"*\" Resource", not bad, bad[:2])
say("diff against the pin: %d added, %d removed (want 1 to 70 and at most 12)" % (len(added), len(removed)), 1 <= len(added) <= 70 and len(removed) <= 12)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
