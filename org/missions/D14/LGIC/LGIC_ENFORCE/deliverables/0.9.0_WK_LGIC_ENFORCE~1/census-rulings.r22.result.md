# EN-ab-1 (round 22) -- the census reads name_rulings.json

Run from the worktree root at 4d6ca219e0 (branch wk-LGIC_ENFORCE-1). Registry `name_rulings.json`: 119 rows.

## The check, whole (`check_en_r22.py ruled`, rc=0)

```
A: CENSUS RULED names IAM_GROUP calculated-group -- name_rulings.json#2 none_owed
A: CENSUS RULED names SECRET astn/kimi/api-key -- name_rulings.json#3 none_owed
A: CENSUS RULED names IAM_POLICY restricted-prefix-get-put-list -- name_rulings.json#118 cloudops-49f-restricted-breakglass-policy
A: CENSUS CARDED names LAMBDA zzqx-unruled-r22-lambda -- NOT-JUDGED (R-29)
B: rc=3 last="CENSUS: STOPPED on the first RAISE after 0 judged (0 carded, ruled=3): names LAMBDA 'zzqx-unruled-r22-lambda'"
PASS-R22-RULED
```

## One `--live --repo` census run (`python lib/opal_naming.py census --live --repo`, rc=3)

- RULED: **0**. The live plane is judged first and stopped on its first uncarded RAISE
  (`live API_GW sentiment-query-api`, R1.f: 'sentiment' is in no vocabulary) after 3 judged; the repo plane was not judged.
- STALE: **0 of 119** ruling rows (STALE is computed over every item the run carried, not only those judged before a stop).
- Final line: `CENSUS: STOPPED on the first RAISE after 3 judged (0 carded, ruled=0): live API_GW 'sentiment-query-api'`.

## The repo plane alone (`python lib/opal_naming.py census --repo`, rc=3)

- RULED: **17** (rows #96-#101, #102-#110, #63, #66 among them).
- STALE: **7 of 119** -- #68 SCHEDULE irpt-intake-poll, #91 S3_BUCKET opal-data-imo, #94 S3_BUCKET_POLICY opal-data-security,
  #95 S3_BUCKET_POLICY opal-data-security-access-logs, #111-#113 SECRET astn/brightdata/residential-proxy, astn/ft/credentials,
  astn/ft/session (the live plane carries these; a repo-only run does not).
- Final line: `CENSUS: STOPPED on the first RAISE after 703 judged (0 carded, ruled=17): repo S3Key 'config/mdpf/route_bindings.yaml'`.

Both stops are uncarded RAISEs in today's estate; the loud stop is the behaviour the order keeps. Row `LGIC_ENFORCE-D1-W1-S2`.

## Test bar

`python -m pytest lib/tests -q -p no:cacheprovider`: 199 passed, 1 skipped (base 196 + 3 new arms).
