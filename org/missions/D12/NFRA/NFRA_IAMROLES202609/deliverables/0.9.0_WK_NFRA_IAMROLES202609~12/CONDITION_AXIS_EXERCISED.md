# CONDITION_AXIS_EXERCISED -- IAM-u-3 (NFRA_IAMROLES202609), FWD-3 exhibit read live and simulated

Worker: 0.9.0_WK_NFRA_IAMROLES202609~12. Date of run: 2026-10-09. Account 313476888478, us-east-1.
All AWS calls below are read-only (get-role-policy, simulate-principal-policy). The instance was not touched;
ec2:StopInstances was never executed. No policy was edited.

## (a) THE LIVE READ

Command: `.tools/aws iam get-role-policy --role-name estate-report-runner-role --policy-name estate-report-runner-selfstop --output json` (rc=0)

```json
{
    "RoleName": "estate-report-runner-role",
    "PolicyName": "estate-report-runner-selfstop",
    "PolicyDocument": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "ec2:StopInstances"
                ],
                "Effect": "Allow",
                "Resource": [
                    "arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4"
                ],
                "Sid": "SelfStopThisInstanceOnly"
            }
        ]
    }
}
```

Match against the Terraform source round 1 read (`infra/aws/terraform/estate-report/iam.tf`, resource
`aws_iam_role_policy.runner_selfstop`, lines 334-348): MATCHES on all three points. Action is
`ec2:StopInstances` (same); Resource is the single pinned ARN
`arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4` (the source computes it from
`aws_instance.estate_report_runner.id`, which resolves to that id live); there is NO `Condition` key in the live
statement, as there is none in the source. Sid `SelfStopThisInstanceOnly` is the same.

## (b) THE READER, RE-RUN UNCHANGED

Command: `python org/missions/D12/NFRA/NFRA_IAMROLES202609/deliverables/0.9.0_WK_NFRA_IAMROLES202609~2/condition-axis-reader.py --policy infra/aws/terraform/estate-report/iam.tf` (rc=0).
Reader blob pin: `git hash-object` = 62ff401ce8237a5a148e9873ce9e21e894bd256f (run, not rewritten).

Verdict line for runner_selfstop, verbatim:

```
[aws_iam_role_policy.runner_selfstop (policy)] statement 1/1 -- Sid=SelfStopThisInstanceOnly Effect=Allow
    REQUIRES-NOTHING
```

Reader denominator line: `18 statement(s) examined across 11 policy document(s)`; REQUIRES-NOTHING 16, REQUIRES 2, UNKNOWN 0.
Those counts describe one Terraform file and are quoted only for the denominator; they are not used below.

## (c) THE SIMULATE BATTERY

Role used as `--policy-source-arn`: `arn:aws:iam::313476888478:role/estate-report-runner-role`
(all calls run with `MSYS_NO_PATHCONV=1 .tools/aws iam simulate-principal-policy ... --output json`, rc=0 each).

### ARM 1 -- no context entries, ec2:StopInstances on the pinned instance ARN. Expected: allowed. Found: allowed.

Resource: `arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4`

```json
{
    "EvaluationResults": [
        {
            "EvalActionName": "ec2:StopInstances",
            "EvalResourceName": "arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4",
            "EvalDecision": "allowed",
            "MatchedStatements": [
                {
                    "SourcePolicyId": "role_estate-report-runner-role_estate-report-runner-selfstop",
                    "SourcePolicyType": "IAM Policy",
                    "StartPosition": {
                        "Line": 1,
                        "Column": 38
                    },
                    "EndPosition": {
                        "Line": 1,
                        "Column": 199
                    }
                }
            ],
            "MissingContextValues": [],
            "EvalDecisionDetails": {},
            "ResourceSpecificResults": [
                {
                    "EvalResourceName": "arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4",
                    "EvalResourceDecision": "allowed",
                    "MatchedStatements": [
                        {
                            "SourcePolicyId": "role_estate-report-runner-role_estate-report-runner-selfstop",
                            "SourcePolicyType": "IAM Policy",
                            "StartPosition": {
                                "Line": 1,
                                "Column": 38
                            },
                            "EndPosition": {
                                "Line": 1,
                                "Column": 199
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

### ARM 2 -- same, with `--context-entries ContextKeyName=aws:MultiFactorAuthPresent,ContextKeyValues=false,ContextKeyType=boolean`. Expected: allowed. Found: allowed.

```json
{
    "EvaluationResults": [
        {
            "EvalActionName": "ec2:StopInstances",
            "EvalResourceName": "arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4",
            "EvalDecision": "allowed",
            "MatchedStatements": [
                {
                    "SourcePolicyId": "role_estate-report-runner-role_estate-report-runner-selfstop",
                    "SourcePolicyType": "IAM Policy",
                    "StartPosition": {
                        "Line": 1,
                        "Column": 38
                    },
                    "EndPosition": {
                        "Line": 1,
                        "Column": 199
                    }
                }
            ],
            "MissingContextValues": [],
            "EvalDecisionDetails": {},
            "ResourceSpecificResults": [
                {
                    "EvalResourceName": "arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4",
                    "EvalResourceDecision": "allowed",
                    "MatchedStatements": [
                        {
                            "SourcePolicyId": "role_estate-report-runner-role_estate-report-runner-selfstop",
                            "SourcePolicyType": "IAM Policy",
                            "StartPosition": {
                                "Line": 1,
                                "Column": 38
                            },
                            "EndPosition": {
                                "Line": 1,
                                "Column": 199
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

### ARM 3 (optional) -- same, with `--context-entries ContextKeyName=aws:SourceIp,ContextKeyValues=203.0.113.77,ContextKeyType=ip`. Expected: allowed. Found: allowed.

(203.0.113.77 is a TEST-NET-3 documentation address, an arbitrary public-form IP.)

```json
{
    "EvaluationResults": [
        {
            "EvalActionName": "ec2:StopInstances",
            "EvalResourceName": "arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4",
            "EvalDecision": "allowed",
            "MatchedStatements": [
                {
                    "SourcePolicyId": "role_estate-report-runner-role_estate-report-runner-selfstop",
                    "SourcePolicyType": "IAM Policy",
                    "StartPosition": {
                        "Line": 1,
                        "Column": 38
                    },
                    "EndPosition": {
                        "Line": 1,
                        "Column": 199
                    }
                }
            ],
            "MissingContextValues": [],
            "EvalDecisionDetails": {},
            "ResourceSpecificResults": [
                {
                    "EvalResourceName": "arn:aws:ec2:us-east-1:313476888478:instance/i-0584e17d283fa7ef4",
                    "EvalResourceDecision": "allowed",
                    "MatchedStatements": [
                        {
                            "SourcePolicyId": "role_estate-report-runner-role_estate-report-runner-selfstop",
                            "SourcePolicyType": "IAM Policy",
                            "StartPosition": {
                                "Line": 1,
                                "Column": 38
                            },
                            "EndPosition": {
                                "Line": 1,
                                "Column": 199
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

### CONTROL -- ec2:StopInstances on a DIFFERENT instance ARN in the same account. Expected: implicitDeny. Found: implicitDeny.

Resource: `arn:aws:ec2:us-east-1:313476888478:instance/i-00000000000000000`. This is a syntactically valid instance
ARN in the same account; it was chosen as a stand-in and is not claimed to be a real instance (the simulator
evaluates policy text against the ARN string and does not look the instance up).

```json
{
    "EvaluationResults": [
        {
            "EvalActionName": "ec2:StopInstances",
            "EvalResourceName": "arn:aws:ec2:us-east-1:313476888478:instance/i-00000000000000000",
            "EvalDecision": "implicitDeny",
            "MatchedStatements": [],
            "MissingContextValues": [
                "s3:prefix"
            ],
            "EvalDecisionDetails": {},
            "ResourceSpecificResults": [
                {
                    "EvalResourceName": "arn:aws:ec2:us-east-1:313476888478:instance/i-00000000000000000",
                    "EvalResourceDecision": "implicitDeny",
                    "MissingContextValues": [
                        "s3:prefix"
                    ]
                }
            ]
        }
    ]
}
```

Observation found, not hypothesised: the control's `MissingContextValues` lists `s3:prefix`. That key comes from
OTHER statements attached to the same role (the runner policy's ListOwnPrefixes statement carries an `s3:prefix`
condition). The simulator reports the missing key for the role's whole policy set; it is unrelated to the
StopInstances decision, which has `MatchedStatements: []` and is a plain implicitDeny. Arms 1-3 report
`MissingContextValues: []`, because the matched statement has no Condition to need any context.

## (d) THE VERDICT

For the single policy `estate-report-runner-selfstop` on `estate-report-runner-role`, the claim is EXERCISED, no
longer only DESIRED. Scoping is real: the control arm returns implicitDeny for ec2:StopInstances on any instance
other than the pinned one, so the grant is exactly one action on one resource. Requirement on the caller is nil:
ARM 1 (no context), ARM 2 (aws:MultiFactorAuthPresent=false) and ARM 3 (an arbitrary aws:SourceIp) all return
`allowed`, and the live statement carries no Condition, so the policy asks nothing about who the caller is or how
they proved it. The policy is careful about what can be touched and silent about who touches it. Whether an
unconditioned self-stop on its own instance is acceptable is not assessed here; nothing is recommended or changed
(C-NO-ACCESSDENIED).

BOUND (Part VII item 5): this is ONE policy. The live read, the reader run and the simulator battery all concern
`estate-report-runner-selfstop` alone. They say nothing measured about any other policy or about the estate as a
whole; that the estate is broadly silent on this axis remains an inference from one policy, not a population claim.
The simulator also evaluates the role's identity policies with caller-supplied context, so it does not show how a
real session is established or whether the instance-profile session ever carries MFA; it shows only that the
policy text does not ask.
