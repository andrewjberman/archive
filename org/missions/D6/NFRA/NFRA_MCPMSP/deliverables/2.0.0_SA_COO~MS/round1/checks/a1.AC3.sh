#!/usr/bin/env bash
# MS-a-1 AC3 (A1n arm 3 as ruled in PRD v0.3, and the gateway's one new grant, LIVE on the IAM plane): simulate on the
# gateway role opal-gateway-role, one call per resource, reads sts:AssumeRole on the Inflection firm role ALLOWED,
# while s3:GetObject on opal-data-inf/* and on opal-data-cot/* is NOT allowed (its opal-data-portal-v2 read is the
# accepted residual, C5 v0.3).
. "$(dirname "$0")/_root.sh"
nm=$(opal_name gateway inflection firm-reader role); A=$(acct); S="arn:aws:iam::${A}:role/${GW_ROLE}"
as=$(sim "$S" sts:AssumeRole "arn:aws:iam::${A}:role/${nm}")
i=$(sim "$S" s3:GetObject "arn:aws:s3:::opal-data-inf/platinum/firm/x.json")
c=$(sim "$S" s3:GetObject "arn:aws:s3:::opal-data-cot/platinum/firm/x.json")
ok() { case "$1" in allowed|implicitDeny|explicitDeny) return 0;; *) return 1;; esac; }
echo "gateway role $GW_ROLE: AssumeRole($nm)=${as:-NONE}; GetObject opal-data-inf=${i:-NONE} opal-data-cot=${c:-NONE}"
if [ "$as" = allowed ] && ok "$i" && [ "$i" != allowed ] && ok "$c" && [ "$c" != allowed ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
