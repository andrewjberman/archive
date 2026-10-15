#!/usr/bin/env bash
# OPLGTW OG-ng-1 AC2 (round-37 NAMING-S3PREFIX): the gate's own self-test still passes (the fourth verdict and the catalog branch are untouched), and the real case is graded:
# the four ETF ListBucket prefix patterns of the OG-ap-20 grant (staged as a diff that also carries a path under the project home, as the real commit does) grade CONFORMANT, and a mistyped one in the same diff REFUSES.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
st=$(timeout 100 python .tools/naming-gate.py --self-test 2>&1 | tr -d '\r'); r0=$?
echo "naming-gate self-test: rc=$r0; $(printf '%s\n' "$st" | tail -1 | cut -c1-100)"
D=$(mktemp -d); cat > "$D/probe.diff" <<'EOF2'
diff --git a/infra/aws/terraform/opal-gateway/probe_s3prefix.tf b/infra/aws/terraform/opal-gateway/probe_s3prefix.tf
new file mode 100644
--- /dev/null
+++ b/infra/aws/terraform/opal-gateway/probe_s3prefix.tf
@@ -0,0 +1,10 @@
+resource "aws_iam_role_policy" "probe" {
+  name = "probe"
+  role = aws_iam_role.int_reader.id
+  policy = jsonencode({
+    Statement = [{
+      Effect = "Allow", Action = ["s3:ListBucket"], Resource = ["arn:aws:s3:::opal-data-etfs"],
+      Condition = { StringLike = { "s3:prefix" = ["gold/book/*", "gold/holding/*", "platinum/reports/*", "silver/holdings/*"] } }
+    }]
+  })
+}
diff --git a/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~99/probe_note.md b/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~99/probe_note.md
new file mode 100644
--- /dev/null
+++ b/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~99/probe_note.md
@@ -0,0 +1 @@
+probe: a path under the project home, so the clause derives the committing project (A2)
EOF2
good=$(timeout 100 python .tools/naming-gate.py --diff "$D/probe.diff" 2>&1 | tr -d '\r'); sed -i 's#"silver/holdings/\*"#"silver/holdins/*"#' "$D/probe.diff"
bad=$(timeout 100 python .tools/naming-gate.py --diff "$D/probe.diff" --enforce 2>&1 | tr -d '\r'); r1=$?
ng_good=$(printf '%s\n' "$good" | grep -cE 'REFUSE.*(gold/book|gold/holding|platinum/reports|silver/holdings)')
ng_bad=$(printf '%s\n' "$bad" | grep -cE 'REFUSE.*silver/holdins')
echo "the four registered ETF patterns refused: $ng_good (want 0); the mistyped one refused: $ng_bad (want 1+), enforce rc $r1"
rm -rf "$D"
[ "$r0" = 0 ] && [ "$ng_good" = 0 ] && [ "$ng_bad" -ge 1 ] && [ "$r1" != 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
