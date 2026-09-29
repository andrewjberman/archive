#!/usr/bin/env bash
# OPLGTW OG-n-1 AC1 (R-2): exactly one Elastic IP is associated with the gateway instance, and the instance's public IP
# is that address. Read-only describe calls.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
a=$(timeout 40 "$AWS" ec2 describe-addresses --region us-east-1 --filters Name=instance-id,Values=$I --query 'Addresses[].[AllocationId,AssociationId,PublicIp]' --output text 2>&1 | tr -d '\r')
n=$(printf '%s\n' "$a" | grep -c '^eipalloc-')
pub=$(timeout 40 "$AWS" ec2 describe-instances --region us-east-1 --instance-ids $I --query 'Reservations[0].Instances[0].PublicIpAddress' --output text 2>&1 | tr -d '\r')
eip=$(printf '%s\n' "$a" | awk 'NR==1{print $3}'); assoc=$(printf '%s\n' "$a" | awk 'NR==1{print $2}')
echo "addresses associated with $I=$n; association=${assoc:-NONE}; eip=${eip:-NONE}; instance public ip=$pub"
if [ "$n" = 1 ] && printf '%s' "$assoc" | grep -q '^eipassoc-' && [ "$eip" = "$pub" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
