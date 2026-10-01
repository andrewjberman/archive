#!/usr/bin/env bash
# MS-a-1 AC2 (A1n arms 1 and 2, LIVE on the IAM plane; AMENDMENT 1 -- round 1's role reads the portal prefix only):
# iam simulate-principal-policy on the applied role name('gateway','inflection','firm-reader','role') for
# s3:GetObject, one call per resource, reads
#   opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json  allowed      (the positive arm: its own prefix)
#   opal-data-portal-v2/platinum/mdpf/cottonwood/aum-metrics.json NOT allowed  (the other firm's prefix)
#   opal-data-cot/platinum/firm/x.json                            NOT allowed  (the other firm's bucket)
. "$(dirname "$0")/_root.sh"
nm=$(opal_name gateway inflection firm-reader role); A=$(acct); R="arn:aws:iam::${A}:role/${nm}"
p=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json")
x=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/cottonwood/aum-metrics.json")
c=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-cot/platinum/firm/x.json")
ok() { case "$1" in allowed|implicitDeny|explicitDeny) return 0;; *) return 1;; esac; }
echo "role $nm: own-prefix=${p:-NONE} cot-prefix=${x:-NONE} cot-bucket=${c:-NONE}"
if [ "$p" = allowed ] && ok "$x" && [ "$x" != allowed ] && ok "$c" && [ "$c" != allowed ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
