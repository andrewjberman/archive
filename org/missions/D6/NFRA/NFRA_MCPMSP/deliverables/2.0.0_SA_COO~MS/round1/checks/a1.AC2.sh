#!/usr/bin/env bash
# MS-a-1 AC2 (A1n arms 1 and 2, LIVE on the IAM plane): iam simulate-principal-policy on the applied role
# name('gateway','inflection','firm-reader','role') for s3:GetObject, one call per resource, reads
#   opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json  allowed      (the positive arm: its own prefix)
#   opal-data-inf/platinum/firm/x.json                            allowed      (its own bucket)
#   opal-data-cot/platinum/firm/x.json                            NOT allowed  (the other firm's bucket)
#   opal-data-portal-v2/platinum/mdpf/cottonwood/aum-metrics.json NOT allowed  (the other firm's prefix)
. "$(dirname "$0")/_root.sh"
nm=$(opal_name gateway inflection firm-reader role); A=$(acct); R="arn:aws:iam::${A}:role/${nm}"
p=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/inflection/aum-metrics.json")
i=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-inf/platinum/firm/x.json")
c=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-cot/platinum/firm/x.json")
x=$(sim "$R" s3:GetObject "arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/cottonwood/aum-metrics.json")
ok() { case "$1" in allowed|implicitDeny|explicitDeny) return 0;; *) return 1;; esac; }
echo "role $nm: own-prefix=${p:-NONE} own-bucket=${i:-NONE} cot-bucket=${c:-NONE} cot-prefix=${x:-NONE}"
if [ "$p" = allowed ] && [ "$i" = allowed ] && ok "$c" && [ "$c" != allowed ] && ok "$x" && [ "$x" != allowed ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
