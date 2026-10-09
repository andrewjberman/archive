# EN-aa-2 result (0.9.0_WK_LGIC_ENFORCE~2, row LGIC_ENFORCE-D1-W2-S152)

Why the planted literal was skipped: NOT a call-argument exemption. py_literals() does yield the string (os.environ.get is not in
BUILDERS/EXEMPT_CALLS). The skip is in judge(): Naming.classify("investor-reporting/directory") returns (None, s), because a string
containing "/" is typed S3Key only when its first segment is a bucket, a tier, or a registered system; "investor-reporting" is none
of them, and carrier() finds no firm token. With typ None and carr None judge() returned None, so no row, so "PASS 0 graded".

The fix (.tools/naming-gate.py): where judge() would drop an untyped literal, _pattern_row() checks whether the literal is the key of a
per-firm key ruling (registry key_rulings.json, bucket_per firm). If so it asks place(value, "S3Key", root) with the root-map key that
holds the literal (longest path-prefix match) and prints the result: PATTERN -> `NAMING PATTERN <file>:<line> <name> -> <canonical>`,
counts PASS; another kind -> that kind, counts WARN; no root or the diff not in this checkout -> the ruling answers (PATTERN, PASS).
A literal that is no ruling's key is graded exactly as before. New --self-test arm: "pattern" (4 checks).

Measured on a09b284984's diff: `NAMING PATTERN infra/aws/lambda/zz-lgic-enforce-r20-s12/probe.py:4 investor-reporting/directory ->
irpt/{scope}/platinum/directory/`, `NAMING-GATE: PASS 1 graded`. Bar: pytest lib/tests 193 passed, 1 skipped; --self-test PASS.
