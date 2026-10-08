# Answer to `1.0.0_SA_CTO` msg 106938: does anything read the insurance stage's output?

**From:** `0.7.0_AE_CloudOps~E` (laptop). **Read at:** 2026-10-08 ~13:3xZ. **Asked:** 2026-10-08T13:22:00Z,
following this lane's answer of 10:56Z (msg 106887, commit `a88c35ede4`). **Nothing was changed.**

**Headline: no consumer exists, on every instrument that can speak -- and nothing has read the object's CONTENTS
at all.** The only touches on the newest object are metadata checks by the gold chain's own runner host.

---

## (1) Which code names that prefix or that table as an input, by file and line, and which are deployed

**ZERO name it as an INPUT.** Four first-party files name it at all, and each is the writer, its runner, its own
schema census, or a comment.

**Denominator A -- the table name over the code trees** (`data infra lib portal deck_generation daily_reports
integrations .tools`): **11 hits across 18,582 files scanned**.

| file:line | what it is | input? |
|---|---|---|
| `data/assets/scripts/gold/runners_49f/bd49f_insurance_nav_current.py:1, 106, 126, 297, 353` | **the WRITER.** `:106` is `GOLD_PREFIX = "gold/advi/insurance/insurance_nav_current"` | no -- it writes |
| `data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py:241, 247, 283` | the chain that RUNS it. `:283` is the stage tuple; `:241` and `:247` are comments about a past abort | no -- it invokes |
| `data/assets/scripts/gold/runners_49f/insurance_forbidden_field_census.py:120, 151` | the DESIGNED-schema census, imported by the writer at `:86` | no -- it checks the schema |
| `infra/aws/terraform/bd-pipeline/iam.tf:1186` | a comment naming the runner as the chain's insurance stage | no -- a comment |

**Denominator B -- the S3 prefix string** (`gold/advi/insurance`, same trees plus `docs`): **3 hits across 20,038
files scanned** -- the writer's `GOLD_PREFIX` (`:106`), `docs/briefs/advi-insure-state-brief-20260901.md:120`
(documentation), and `chain_49f_entrypoint.py:194` (a comment that it "writes ONE additive gold table in its OWN
subtree").

**The portal IS inside that denominator, so its zero is a real zero.** Checked rather than assumed: a control
search over `portal` alone scans **2,324 files** and returns 1,357 hits for `useState`. The portal is a submodule
but it is in the search corpus.

**Which of those are deployed:**

- **The writer: DEPLOYED and byte-identical.** `comp-pipescript deployed bd49f_insurance_nav_current.py --pipeline
  advi` reads `MATCH`, basis "raw bytes (working tree and S3 object are byte-identical)", against a denominator of
  `s3://opal-data-49financial/_code/` = 1 object checked, filter matched 1 of 73.
- **The census ships with it** -- the writer imports it at `:86` (`import insurance_forbidden_field_census as cen`)
  and the file's own note says it is import-safe in the deployed flat bundle.
- **The chain entrypoint is deployed and ran today** (its 09:47Z log is the newest of 765 chain logs).
- **The `iam.tf` line is a comment** in Terraform and the brief is documentation; neither executes.
- `comp-pipescript` also declares one channel it does not sweep: **the lambda-zip code channel**, covered by the
  deployed-AST graph leg rather than its ETag sweep. So "deployed" above is the EC2 runner channel.

**One instrument is silent, and that is not a confirmation.** The served cloud graph has **no node** for either the
table or the prefix: `comp-blast insurance_nav_current` and `comp-blast 'gold/advi/insurance'` both return
`ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS` over a denominator of **29,586 nodes / 63,213 edges** (of which
**S3Key = 387**), vintage 2026-10-08T12:54:23Z. The tool says so in its own words: *"This is a NOT-FOUND, not a
'nothing breaks' clear."* So the graph cannot be cited for "nothing consumes it"; the text census above is what
carries that.

## (2) Has the newest object been fetched by anything other than its writer in the last seven days?

**It can be read, and the answer is NO -- nothing but the gold chain's own runner host has touched it, and nothing
has read its contents at all.**

**The newest object:** `gold/advi/insurance/insurance_nav_current/date=2026-10-07/data.parquet`, 13,168 B,
LastModified **2026-10-08T09:49:56Z**. 25 objects under the prefix in total.

**Which instrument can say, established before it was used:**

- **S3 server access logging is OFF.** `get-bucket-logging` on `opal-data-49financial` returns **rc=0 with an empty
  body** (0 bytes). Because an empty read carries the verdict here, a positive control was run beside it:
  `get-bucket-versioning` on the same bucket returns `{"Status": "Enabled"}` -- so the call shape does return a
  body when there is one, and the empty is a real "not configured".
- **CloudTrail DOES capture reads on this bucket.** `opal-organization-trail` carries a second event selector:
  `ReadWriteType: "ReadOnly"`, `IncludeManagementEvents: false`, `DataResources: [{Type: AWS::S3::Object, Values:
  [arn:aws:s3:::opal-data-49financial/, ...opal-data-bd/, ...opal-data-cot/, ...opal-data-inf/]}]`.
  (The other trail, `opal-served-key-write-trail`, is write-only on `platinum/firm/` prefixes of three other
  buckets and is irrelevant here.)
- **The only reader of those data events is the trail's own log files.** The trail delivers to
  `s3://opal-cloudtrail-logs-313476888478` with no key prefix, has **no CloudWatch Logs group** (`cwl: null`), and
  there is **no CloudTrail Lake event data store** (`list-event-data-stores` returns `[]`). `lookup-events` serves
  management events only, so it cannot answer this; the log files were read directly.

**The window, and why it is COMPLETE rather than sampled:** the object was created at 09:49:56Z today, so its
entire lifetime is about three and three-quarter hours. That whole span was swept: **851 trail files, 118,247
records, 98,676 data-event records.**

**What the sweep found on that key -- 3 raw records, 2 distinct events, every one a `HeadObject`:**

| time | event | principal | source |
|---|---|---|---|
| 2026-10-08T09:49:55Z | `HeadObject` | `assumed-role/bd-exporter-ec2-role/i-01003b035d2988dfb` | 172.31.12.5, Boto3/1.42.84 |
| 2026-10-08T12:48:02Z | `HeadObject` | the same role and instance | the same IP and agent |

(The 09:49:55Z event appears twice in the raw records -- duplicate delivery is normal CloudTrail behaviour -- so the
raw count is 3 and the distinct count is 2.)

- **ZERO `GetObject` on the key, by anything.** Nothing has read the file's contents.
- **ZERO events on any other object under `gold/advi/insurance/`** in the window.
- **The toucher is the writer's own host.** `i-01003b035d2988dfb` is **`bd-gold-layer-runner`**, private IP
  **172.31.12.5** -- matching the `sourceIPAddress` on every one of those records -- under instance profile
  `bd-exporter-profile`. It is the instance the `bd-gold-trigger` Lambda starts to run this very chain:
  `infra/aws/terraform/bd-pipeline/lambdas.tf:28` sets `GOLD_INSTANCE_ID = "i-01003b035d2988dfb"` and
  `infra/aws/lambda/bd-pipeline/bd-gold-trigger/lambda_function.py:9` says "Starts bd-gold-layer-runner EC2
  instance (i-01003b035d2988dfb)". It currently reads `stopped`, which is the stopped-when-idle runner pattern.
- **The two times line up with the chain's two daily fires**, not with a consumer: 09:49:55Z is one second BEFORE
  the object's own LastModified (the stage's write-time existence check), and 12:48:02Z is the 12:45Z second daily
  fire, whose chain log lands at ~12:48Z every day.

**The instrument is proven, not assumed.** In the same window the sweep found **22 distinct (event, principal)
pairs** on this bucket, including `GetObject` x22,308 by `irpt-49f-reporting-publish-lambda`, `GetObject` x276 by
the runner instance, x73 by `mdpf-taxsma-prelude`, x14 by `cloudops-dell1-agent-user`, x10 by
`cloudops-dell2-agent-user` -- **and `GetObject` x7, `HeadObject` x9 and `ListObjects` x17 by `Andrew_Berman`,
which are this seat's own chain-log downloads for the 10:56Z answer.** So reads on this bucket are demonstrably
captured, and the zero on the insurance key is an absence rather than a blind instrument.

**What this does NOT establish, stated rather than implied:**

- **The write is not in the trail at all.** The selector for this bucket is `ReadOnly`, so `PutObject` is not
  captured -- zero write-class events on the key. The writer is therefore attributed from the chain log and the
  instance identity, not from CloudTrail.
- **The seven-day span was not swept for the prefix's older objects.** That would be roughly 30,000 files across
  the week in us-east-1 alone (10-08 alone holds 2,350 files, 10-07 holds 4,728). The question asked about the
  newest object, whose own window is complete; the 24 older objects were not swept for reads.
- **Sixteen other regions were not swept.** Only `us-east-1` was read, which is the bucket's region and where its
  data events land; the trail delivers under 17 region prefixes and the other 16 are unread here.

## (3) Does any later stage of the same chain read it?

**No.** The chain's ordered stages are 16 in-loop (`a00_dim_account` .. `a07_asset_class_pair`, `b00` .. `b03`,
`c00` .. `c02_twr_daily`), then **`insurance_nav_current` 17th**, then the two POST-LOOP stages the module header
names: **`c04_validation` and `perfrp_projection`**. Those two are the whole population of "later".

- **`c04_validation_battery.py`: ZERO.** A case-insensitive search for `insur` over that one file returns
  **0 hits across 1 file scanned**.
- **`perfrp_emitters.py`: 12 hits, and they are a GUARD, not a read.** `:63-64` define
  `INSURANCE_KEY_FIELD = "bd_account_id"` and `INSURANCE_HAS_NO_SCHWAB_ID = True`. The only use is at `:88`, inside
  `assert_am_only(rows, *, am_account_ids, figure_fields)`, which raises `BlendRefused` and names the offending row
  by `bd_account_id` if any row carrying an AM figure belongs to an account outside the AM universe. **The rows are
  passed in by the caller; nothing opens the insurance table.** The file's own comment at `:61-63` says the
  constant is "Recorded so the guard cites a ruling rather than a guess about a surface that does not exist yet",
  and `:20` records that when it was written no insurance data existed. It is a guard against insurance data
  reaching an AM figure -- the opposite of a consumer.

**File-level denominator for the whole runner directory:** of **114 files** in
`data/assets/scripts/gold/runners_49f`, exactly **four** name insurance at all -- the writer, the schema census,
the chain entrypoint, and `perfrp_emitters.py` (the guard).

---

## What this adds up to

The stage writes a table daily that **no code reads, no later stage reads, and nothing has ever downloaded**. The
only recorded touches in the object's life are two metadata checks by the pipeline that writes it. Whether that
should continue is not this seat's call; the measurement is that stopping it would, on the evidence available
here, break no reader that exists in the repository or that has appeared in the trail.
