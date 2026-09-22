# IRPT_BCKEND.TO-IB-rtj-4 -- the source-map note, corrected -- result

**Assignee:** `0.9.0_WK_IRPT_BCKEND~14` | **Cell:** `IB-rtj-4` | **Row:** `IRPT_BCKEND-W10-S3`

## (a) READ THE CURRENT NOTE (verbatim, before)

File: `infra/aws/lambda/ci/lambda-source-map.json`, entry `functions["irpt-ycharts-generate"]`.

`_staged_from_note` (before):
```
IRPT_BCKEND IB-rte-4 (row W1-S20's class, generalised): 8 of this function's members share the _authz/_scope/_keys/_ids/_gate frontier plus the terraform-core firm_destination_policy.json, all staged at build time with each blob's sha256 verified. firm_registry.json is ALSO declared in files[] above and genuinely served, but its exact content does NOT exist as a git blob anywhere in this repository's reachable history (content-addressed blob lookup, row IRPT_BCKEND-W4-S34) -- no true source is declared for it and none is invented here; this function's build still fails on that one member.
```

`staged_from` (verbatim, unchanged by this cell) already carries, at the tail of the array, the two entries `IB-rti-2` (`0.9.0_WK_IRPT_BCKEND~10`, commit `63b5a913a2`) added:
```json
{
  "repo_path": "data/firm_registry.json",
  "pin": "1f54e16dfd39971faec8e7ba20a9d4364596e37d",
  "packaged_as": "firm_registry.json",
  "sha256": "38ad04b2c25e96387b2614e9f4caba4316978924d5647d0e8d229093cdefd539"
},
{
  "repo_path": "infra/aws/lambda/investor-reporting/intake/settings.json",
  "pin": "dc5d119b84b8f8ff6fdacc8b190b5d60a3faea11",
  "packaged_as": "settings.json",
  "sha256": "c493ea6edd6ee7c38c0044feda1440865532e0fbc86d30b2dfe2c0e34ec1eefd"
}
```
So `staged_from` already declared true sources for both members (per `IB-rti-2`'s battery, row `IRPT_BCKEND-W10-S1`: both resolve to tracked blobs, CRLF-only difference from the live zip member), but `_staged_from_note` (a separate free-text field) still claimed firm_registry.json's content "does NOT exist as a git blob anywhere in this repository's reachable history" -- stale, per this order's premise and row `IRPT_BCKEND-W10-S3`.

## (b) CORRECT THE NOTE ONLY (after)

`_staged_from_note` (after):
```
IRPT_BCKEND IB-rte-4 (row W1-S20's class, generalised): 8 of this function's members share the _authz/_scope/_keys/_ids/_gate frontier plus the terraform-core firm_destination_policy.json, all staged at build time with each blob's sha256 verified. firm_registry.json and settings.json are ALSO declared in files[] above and genuinely served; both now have declared staged_from pins (firm_registry.json -> data/firm_registry.json @1f54e16dfd; settings.json -> infra/aws/lambda/investor-reporting/intake/settings.json @dc5d119b84), resolving row IRPT_BCKEND-W10-S1: each pin resolves to a tracked git blob with a CRLF-only difference from the live zip member, never claimed byte-identical to a HEAD-generated view.
```

Nothing else in the entry (`staged_from`, `files[]`, `runtime`, `note`, `artifact_sha256`, etc.) or in the file was touched. The replacement was done by an exact-substring `str.replace()` in Python asserting `count(old) == 1` before writing, and the file was written back with `newline=''` to preserve its original CRLF line endings byte-for-byte outside the one changed line.

## (c) VERIFY NOTHING ELSE CHANGED

```
$ git diff HEAD~1 -- infra/aws/lambda/ci/lambda-source-map.json
diff --git a/infra/aws/lambda/ci/lambda-source-map.json b/infra/aws/lambda/ci/lambda-source-map.json
index 7739bbd996..125cfb0c82 100644
--- a/infra/aws/lambda/ci/lambda-source-map.json
+++ b/infra/aws/lambda/ci/lambda-source-map.json
@@ -3493,7 +3493,7 @@
           "sha256": "c493ea6edd6ee7c38c0044feda1440865532e0fbc86d30b2dfe2c0e34ec1eefd"
         }
       ],
-      "_staged_from_note": "IRPT_BCKEND IB-rte-4 (row W1-S20's class, generalised): 8 of this function's members share the _authz/_scope/_keys/_ids/_gate frontier plus the terraform-core firm_destination_policy.json, all staged at build time with each blob's sha256 verified. firm_registry.json is ALSO declared in files[] above and genuinely served, but its exact content does NOT exist as a git blob anywhere in this repository's reachable history (content-addressed blob lookup, row IRPT_BCKEND-W4-S34) -- no true source is declared for it and none is invented here; this function's build still fails on that one member.",
+      "_staged_from_note": "IRPT_BCKEND IB-rte-4 (row W1-S20's class, generalised): 8 of this function's members share the _authz/_scope/_keys/_ids/_gate frontier plus the terraform-core firm_destination_policy.json, all staged at build time with each blob's sha256 verified. firm_registry.json and settings.json are ALSO declared in files[] above and genuinely served; both now have declared staged_from pins (firm_registry.json -> data/firm_registry.json @1f54e16dfd; settings.json -> infra/aws/lambda/investor-reporting/intake/settings.json @dc5d119b84), resolving row IRPT_BCKEND-W10-S1: each pin resolves to a tracked git blob with a CRLF-only difference from the live zip member, never claimed byte-identical to a HEAD-generated view.",
       "runtime": "python3.12",
       "memory_size": 512,
       "timeout": 900,
$ git diff --stat HEAD~1 -- infra/aws/lambda/ci/lambda-source-map.json
 infra/aws/lambda/ci/lambda-source-map.json | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

**Denominator:** 1 of 1 files changed (`infra/aws/lambda/ci/lambda-source-map.json`), 1 of 3789 lines in that file changed (`_staged_from_note`'s line, `git diff --stat` reports `1 insertion(+), 1 deletion(-)` = one line replaced), 1 of 1 JSON entries touched (`functions["irpt-ycharts-generate"]`), 1 of the entry's fields touched (`_staged_from_note`; `staged_from`, `files[]` and every other sibling field byte-identical). File re-parses as valid JSON after the edit (`json.load` succeeded).

`IBR104-NOTE-CORRECTED-NOTHING-ELSE-CHANGED`: the diff touches exactly one field (`_staged_from_note`) in exactly one entry (`irpt-ycharts-generate`); the new text names both members' true sources (`firm_registry.json -> data/firm_registry.json @1f54e16dfd`; `settings.json -> infra/aws/lambda/investor-reporting/intake/settings.json @dc5d119b84`) and does not claim byte-identity (states "CRLF-only difference from the live zip member, never claimed byte-identical to a HEAD-generated view"); every other line in the file is unchanged.

## Declared exclusions
- `staged_from`, `files[]` and every other field/entry in the file: untouched by design (order clause (b)).
- No served bytes copied into the repo; no deploy or rebuild attempted (out of this cell's bound).
- Whether the note's stale "8 of this function's members" count (a separate, pre-existing number unrelated to firm_registry.json/settings.json) is itself still accurate is NOT evaluated here -- the order named one correction (the firm_registry.json/settings.json claim) and this cell makes exactly that one, nothing wider.

## Surprises
None encountered outside the order's mandate; no row filed.
