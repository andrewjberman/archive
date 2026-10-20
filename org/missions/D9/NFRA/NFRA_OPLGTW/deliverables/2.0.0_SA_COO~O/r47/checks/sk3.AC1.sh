#!/usr/bin/env bash
# OPLGTW OG-sk-3 AC1 (round 47; the Schwab 0840 move to schwab/49financial/, the CTO's conditions 17:49Z and 20:18Z): the reader IAM's LOCALS evaluate to exactly the new, FILE-NAME-fenced grants.
# The check copies the `locals { ... }` block of infra/aws/terraform/opal-gateway/schwab_reader_iam.tf into a scratch module (the one line that references a resource is dropped) and EVALUATES it with `terraform console`:
#  schwab_state_bucket == "opal-data-49financial"; schwab_state_bucket_arn == "arn:aws:s3:::opal-data-49financial";
#  schwab_firm_silver_object_arns == the 4 ARNs  arn:aws:s3:::opal-data-assets/schwab/49financial/silver/<t>/date=*/08403355.parquet  (t in dim_position, dim_balance, dim_asset, dim_transaction) -- the master in the FILE NAME;
#  schwab_firm_silver_prefix_forms == the 4 prefixes  schwab/49financial/silver/<t>/*  ;
#  schwab_state_complete_object_arns == ["arn:aws:s3:::opal-data-49financial/schwab/49financial/state/complete/date=*/08403355.complete.json"]; schwab_state_complete_prefix_form == ["schwab/49financial/state/complete/*"];
#  schwab_data_object_arns == the OLD 12 (unchanged, in order) followed by the 4 firm ARNs; schwab_data_prefix_forms == the OLD 12 then the 4 firm forms;
#  schwab_catalog_object_arns == the OLD 3 then the 1 state ARN; schwab_catalog_prefix_form == the OLD 3 (UNCHANGED: it conditions listing on the OLD bucket only).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F=infra/aws/terraform/opal-gateway/schwab_reader_iam.tf
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo "terraform absent"; echo "RESULT: FAIL"; exit 1; }
SD=$(mktemp -d 2>/dev/null) || SD="${TMPDIR:-/tmp}/sk3_$$"; mkdir -p "$SD"
res=$(python3 -I - "$(native "$F")" "$(native "$SD")" <<'PYEOF'
import json, os, subprocess, sys
F, SD = sys.argv[1], sys.argv[2]
t = open(F, encoding="utf-8").read()
i = t.index("locals {"); j = t.index("\n}\n", i) + 3
blk = "\n".join(l for l in t[i:j].splitlines() if "aws_secretsmanager_secret_version" not in l)
open(os.path.join(SD, "main.tf"), "w", encoding="utf-8", newline="\n").write(blk + "\n")
init = subprocess.run(["terraform", "init", "-backend=false", "-input=false"], cwd=SD, capture_output=True, text=True)
names = ["schwab_state_bucket", "schwab_state_bucket_arn", "schwab_firm_silver_object_arns", "schwab_firm_silver_prefix_forms", "schwab_state_complete_object_arns",
         "schwab_state_complete_prefix_form", "schwab_data_object_arns", "schwab_data_prefix_forms", "schwab_catalog_object_arns", "schwab_catalog_prefix_form"]
vals = {}
for n in names:
    r = subprocess.run(["terraform", "console"], cwd=SD, input="jsonencode(local.%s)\n" % n, capture_output=True, text=True)
    out = (r.stdout or "").strip()
    try:
        v = json.loads(json.loads(out.splitlines()[-1])) if out else None
    except Exception:
        v = None
    vals[n] = v
OLDM = ["08242234", "08335338", "08403355"]
T = ["dim_position", "dim_balance", "dim_asset", "dim_transaction"]
A = "arn:aws:s3:::opal-data-assets/"
old_data_arns = [A + "schwab/%s/silver/%s/*" % (m, t_) for m in OLDM for t_ in T]
old_data_forms = ["schwab/%s/silver/%s/*" % (m, t_) for m in OLDM for t_ in T]
firm_arns = [A + "schwab/49financial/silver/%s/date=*/08403355.parquet" % t_ for t_ in T]
firm_forms = ["schwab/49financial/silver/%s/*" % t_ for t_ in T]
old_cat = [A + "schwab/%s/meta/complete/*" % m for m in OLDM]
old_cat_forms = ["schwab/%s/meta/complete/*" % m for m in OLDM]
state_arn = ["arn:aws:s3:::opal-data-49financial/schwab/49financial/state/complete/date=*/08403355.complete.json"]
ok = True


def say(label, cond, got=None):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NOT OK", ("" if cond else " (got %s)" % (json.dumps(got)[:240]))))


say("terraform console evaluated all ten locals (a name that does not evaluate reads null)", all(v is not None for v in vals.values()), [k for k, v in vals.items() if v is None])
say("state bucket and its ARN", vals["schwab_state_bucket"] == "opal-data-49financial" and vals["schwab_state_bucket_arn"] == "arn:aws:s3:::opal-data-49financial", [vals["schwab_state_bucket"], vals["schwab_state_bucket_arn"]])
say("firm silver object ARNs: four, the master in the FILE NAME (date=*/08403355.parquet), no folder wildcard", vals["schwab_firm_silver_object_arns"] == firm_arns, vals["schwab_firm_silver_object_arns"])
say("firm silver listing forms: the four table prefixes", vals["schwab_firm_silver_prefix_forms"] == firm_forms, vals["schwab_firm_silver_prefix_forms"])
say("state completion: one object ARN naming 08403355.complete.json, one listing form", vals["schwab_state_complete_object_arns"] == state_arn and vals["schwab_state_complete_prefix_form"] == ["schwab/49financial/state/complete/*"], [vals["schwab_state_complete_object_arns"], vals["schwab_state_complete_prefix_form"]])
say("data role: the OLD 12 object ARNs unchanged and in order, then the 4 firm ARNs; the listing forms the same", vals["schwab_data_object_arns"] == old_data_arns + firm_arns and vals["schwab_data_prefix_forms"] == old_data_forms + firm_forms, [len(vals["schwab_data_object_arns"] or []), len(vals["schwab_data_prefix_forms"] or [])])
say("catalog role: the OLD 3 completion ARNs then the 1 state ARN; the listing form for the OLD bucket is UNCHANGED (3)", vals["schwab_catalog_object_arns"] == old_cat + state_arn and vals["schwab_catalog_prefix_form"] == old_cat_forms, [vals["schwab_catalog_object_arns"], vals["schwab_catalog_prefix_form"]])
flat = json.dumps(vals)
say("no bucket-wide or folder-wide grant on the new bucket or the firm folder (no ARN ends in /*, or in 49financial/*, on opal-data-49financial; none names another master's file)",
    not any(x.startswith("arn:aws:s3:::opal-data-49financial") and x.endswith("/*") for x in (vals["schwab_state_complete_object_arns"] or [])) and "08242234.parquet" not in flat and "08335338.parquet" not in flat, None)
print("OK" if ok else "NO")
PYEOF
)
rm -rf "$SD"
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
