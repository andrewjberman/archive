set -u
# TO-APPLY-MODELGRANT G4 (read only): a real get-object of the two keys with the host's own role, in the service host's environment.
# Prints sizes, return codes and closed facts only; no body is printed; the temp folder is removed at the end.
export AWS_DEFAULT_REGION=us-east-1
echo "G4 identity: $(aws sts get-caller-identity --query Arn --output text 2>&1 | sed -n 's#.*assumed-role/\([^/]*\)/.*#assumed-role=\1#p')"
T=$(mktemp -d)
B=opal-data-portal-v2
K1=json/benchmarks/model_portfolio_timeseries.json
K2=json/positioning/positioning_data.json
for k in "$K1" "$K2"; do
  f="$T/$(echo "$k" | tr '/' '_')"
  aws s3api get-object --bucket "$B" --key "$k" "$f" > "$f.meta" 2> "$f.err"
  rc=$?
  code=$(grep -o -E 'AccessDenied|NoSuchKey|NoSuchBucket' "$f.err" | head -1)
  echo "G4 get-object $k rc=$rc bytes=$(stat -c %s "$f" 2>/dev/null || echo 0) sse=$(grep -o -E '"ServerSideEncryption": "[A-Za-z0-9:]+"' "$f.meta" | head -1 | cut -d'"' -f4) error=${code:-none}"
done
F1="$T/$(echo "$K1" | tr '/' '_')"
F2="$T/$(echo "$K2" | tr '/' '_')"
python3 -m json.tool "$F1" > /dev/null 2>&1; echo "G4 series json-parse rc=$?"
echo "G4 positioning first-two-bytes=$(head -c2 "$F2" | od -An -tx1 | tr -d ' \n')"
gzip -dc "$F2" 2>/dev/null | python3 -m json.tool > /dev/null 2>&1; echo "G4 positioning gunzip-then-json rc=$?"
rm -rf "$T"
echo "G4 temp-removed=$(test -e "$T" && echo no || echo yes)"
