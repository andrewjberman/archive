# WILDCARD_CENSUS -- TO-IAM-z-4 (READ-ONLY), account 313476888478, read 2026-10-11

Source: iam get-account-authorization-details (35.7 MB, saved at C:/tmp/z4_auth.json). Allow statements with an
arn:aws:s3:::<bucket> Resource whose bucket part starts with "opal" and contains "*". Patterns found: opal*, opal-*,
opal-data-*. No other opal-prefixed wildcard pattern exists. No non-opal S3 wildcard Resource exists
(arn:aws:s3:::* style) in any Allow; no NotResource S3 statement was graded as a grant.
Account buckets (s3api list-buckets): 40 total; opal*=40, opal-*=39, opal-data-*=24 (opal* also matches opalinvest-portal).

WILDCARD: opal* principal=cloudops-dell-agent-create-policy write=yes ours_matching=40 addressed=0
  attached (customer-managed) to group cloudops-dell-agents-group; members: cloudops-dell1-agent-user, cloudops-dell2-agent-user (IAM users).
  Actions: s3:CreateBucket, PutBucketTagging/Versioning/PublicAccessBlock/OwnershipControls/CORS/Logging/Notification,
  PutEncryptionConfiguration, PutLifecycleConfiguration, PutObjectTagging. No object Get/Put/Delete. Resources opal* and opal*/*.
  Note: write=yes by the Put* rule; these are bucket-configuration writes plus CreateBucket (an outsider-style new bucket
  named opal* is creatable and then configurable by this holder).
  Addressed buckets: none observed. CloudTrail management events (90-day window, oldest 2026-07-13) for CreateBucket and
  PutBucket{Cors,Logging,Notification,OwnershipControls,PublicAccessBlock,Tagging,Versioning,Encryption,Lifecycle*}: no event
  by either cloudops-dell user (0 of 11 event-name lookups).
  Planes READ: IAM policy/attachments; group membership; CloudTrail management-event lookup (11 event names, 90 days).
  Planes NOT READ (named, not zero): s3:PutObjectTagging use (S3 data event, not in the trails for these buckets);
  any workstation-held access-key use; repo code that runs under the two users (they are interactive agent users, no Lambda/ECS/EC2 binding).

WILDCARD: opal-* principal=cloudops-dell-agent-deploy-policy write=yes ours_matching=39 addressed=4
  attached (customer-managed) to group cloudops-dell-agents-group; members: cloudops-dell1-agent-user, cloudops-dell2-agent-user.
  Actions: s3:GetObject, GetObjectVersion, PutObject (WRITE), ListBucket, GetBucketLocation, ListBucketVersions, GetBucket*.
  Resources opal-* and opal-*/*. The same policy carries an explicit Deny of s3:DeleteBucket*, s3:DeleteObject*,
  s3:PutLifecycleConfiguration on opal-data-* (and /*), so the holder cannot delete in the 24 opal-data-* buckets.
  Addressed (floor, from a 2000-event CloudTrail sample of cloudops-dell1-agent-user, 2026-10-11 11:24-14:51 local, more pages
  existed): opal-data-49financial, opal-data-assets, opal-data-bd, opal-data-harvest. All four are in our account.
  Planes READ: IAM; CloudTrail management events (sample above only). Planes NOT READ (named, not zero): S3 object-level data
  events for this principal (trail opal-organization-trail logs ReadOnly data events for only opal-data-49financial/bd/cot/inf;
  no write data events for these users; opal-served-key-write-trail covers only platinum/firm/ writes); full 90-day
  management history of both users (throttled; only 2000 of >2000 events of dell1 read, dell2 not read); repo code that
  deploys under these users (open-ended Terraform/CLI operations, no single code unit named). The addressed count is a floor.

WILDCARD: opal-data-* principal=partners-lambda-role write=no ours_matching=24 addressed=6
  Inline policy partners-lambda-permissions on role partners-lambda-role. Actions: s3:GetObject, s3:ListBucket (read only).
  Resources opal-data-* and opal-data-*/*. No instance profile on the role; no ECS task or execution role is this role
  (9 task definitions in us-east-1 checked, cluster opal-globgrph; us-east-2 has no cluster).
  Lambda on the role: opal-partners-data only (us-east-1: 237 functions listed, 1 on this role; us-east-2: 1 function listed, 0 on this role).
  Environment of opal-partners-data: USERS_TABLE=opal-users-v2 (no bucket variable).
  Addressed buckets:
    opal-data-bd         (DynamoDB opal-users-v2 FIRM#*/META s3Bucket; also PIPELINE_BUCKET in served_seam.py)
    opal-data-cot        (DynamoDB s3Bucket)
    opal-data-demo       (DynamoDB s3Bucket)
    opal-data-inf        (DynamoDB s3Bucket)
    opal-data-portal-v2  (DynamoDB s3Bucket)
    opal-data-49financial (platinum_dest_view.py / served_seam.py literal in infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data)
  All six are in our account.
  Planes READ: IAM; Lambda config both regions; Lambda Environment; ECS task definitions us-east-1; EC2 instance profiles; DynamoDB
  scan of opal-users-v2 (SK=META with s3Bucket: 6 of 88 scanned items, 5 distinct buckets); repo code of opal-partners-data (all .py + deploy.sh).
  Planes NOT READ (named, not zero): runtime key-level GetObject use (no data-event trail for opal-data-demo/portal-v2); the
  Lambda zip contents as deployed (repo code only, deployed bytes not diffed).

DENOMINATOR: principals=314 documents=652 wildcard_grants=3

Denominator notes: principals = 303 roles + 9 users + 2 groups (all in the authorization-details dump). documents = every
role/user/group inline policy document plus the default version of every customer-managed policy (57) plus every attached
AWS-managed policy (scanned if attached to any principal), 652 scanned in total. Two of the three grants arise from customer-managed
policies attached to one group, so they are attributed to the policy name; the group's members hold them transitively.
Addressed buckets outside our account: NONE found on any plane read.
