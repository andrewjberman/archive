# PLAN NOTE -- TO-CT-d-5 amendment: sqs:SetQueueAttributes added to DenyResourcePolicyWrites

By reading of the diff, not a plan run (no terraform plan was made against the backend).

1. WHAT THE APPLY SHOWS: one managed policy updated in place (`aws_iam_policy.dell_agent_respol`, the file `dell_respol_policy.json` goes from 74 to 75 actions, one added entry `sqs:SetQueueAttributes`), a new default policy version, nothing added or destroyed. The edit to `iam.tf` is a comment only and shows no change.
2. WHO LOSES WHAT: both Dell users (group member of the Dell group) lose any later change to a queue's attributes, its access policy included, and cannot apply a root that declares an `aws_sqs_queue_policy` (globgrph, inf-pipeline, nfra-agentbus, nfra-agentbus-alyssa01, opal-gateway, partner-etl-ops-alerts). Creating a queue (`sqs:CreateQueue`, attributes in the call), tagging (`sqs:TagQueue`) and `sns:SetTopicAttributes` stay allowed (simulation arms).
3. ROLLBACK: IAM keeps the prior policy version; set the earlier version as default, or revert this commit and apply (the apply is the issuer's route).

Basis of the ruling's assumption (measured, `tests/queue_attribute_writers.json`): region us-east-1 only, 90 days; 18 Terraform creates, all carried attributes inside the create call; 3 were followed by a set, all three in roots that declare a separate queue policy resource.
