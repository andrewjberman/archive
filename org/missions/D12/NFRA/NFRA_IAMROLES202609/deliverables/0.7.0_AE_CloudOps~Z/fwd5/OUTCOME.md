# FWD-5 OUTCOME -- narrowing `secretsmanager:DescribeSecret` off `smartx-assets-pull-role`

**By:** `0.7.0_AE_CloudOps~Z`, 2026-10-09, under `NFRA_IAMROLES202609.TO-IAM-v-4` (cell `IAM-v-4`, outcome
`FWD-5`). Prediction under test: `deliverables/0.9.0_WK_NFRA_IAMROLES202609~13/PREDICTION.json`.

> **STATUS: steps 1-4 complete. Step 5 (the observation window) is NOT yet read, so the
> `MATCHES-PREDICTION` line is deliberately ABSENT from this file rather than guessed.** The window waits for
> the first scheduled `smartx-assets-daily-pull` run that STARTS after the apply. The apply completed at
> ~10:4xZ on 2026-10-09, before that day's `cron(2 13 * * ? *)` fire, so by PREDICTION.json's own rule D =
> 2026-10-09 and the earliest sound read is 13:30Z. Writing `MATCHES-PREDICTION: yes` now would be a
> prediction about a prediction; the whole point of FWD-5 is that the check was believed BEFORE and then
> READ AFTER.

## 1. The act

One action, one statement, one file. `infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf` line 101:

```
-        Action = ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"]
+        Action = ["secretsmanager:GetSecretValue"]
```

Applied from worker ~13's own `narrowing.patch` via `git apply` (not retyped; `--check` first), planned with
`-target` on the one policy, graded from `terraform show -json`, and applied from the SAVED plan through
`safe-apply`. Commit `e02476796b`. Ledger `iamroles-fwd5-narrowing` opened before the act at `f07f3dcc87`.

The plan was graded by DECOMPOSING the policy document per `Sid` rather than diffing it as a string, because
an IAM role policy is ONE opaque `policy` attribute in the plan: `0 add, 1 change, 0 destroy` would read
identically if the change had dropped a resource or widened a different statement.

| Sid | before | after |
|---|---|---|
| `ReadAuthBundle` | `GetSecretValue`, `DescribeSecret` | **`GetSecretValue`** |
| `WriteBackRefreshedToken` | `PutSecretValue` | unchanged |
| `WriteMonolithSmartx` | `PutObject`, `GetObject` | unchanged |
| `ListMonolithSmartx` | `ListBucket` | unchanged |

`REMOVED {'ReadAuthBundle': ['secretsmanager:DescribeSecret']}`, `ADDED {}`, and the resource sets are
identical across all four statements. Live read-back after the apply: `ReadAuthBundle` carries
`['secretsmanager:GetSecretValue']` alone over its 5 resources, 4 statements intact, and the targeted
re-plan reads `No changes. Your infrastructure matches the configuration.`

## 2. Step 4 -- the removed action on the live role: `implicitDeny` 5 of 5

Raw `simulate-principal-policy` results, quoted verbatim. **One `--resource-arns` per invocation**, because
two or more in a single call flips the HELD ones to `implicitDeny` and would manufacture this very result.

```json
[
  {
    "name": "smartx/credentials/username",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-9mrtlN",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:DescribeSecret",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-9mrtlN",
      "EvalDecision": "implicitDeny",
      "MatchedStatements": [],
      "MissingContextValues": [
        "s3:prefix"
      ],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-9mrtlN",
          "EvalResourceDecision": "implicitDeny",
          "MissingContextValues": [
            "s3:prefix"
          ]
        }
      ]
    }
  },
  {
    "name": "smartx/credentials/password",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-hChc3R",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:DescribeSecret",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-hChc3R",
      "EvalDecision": "implicitDeny",
      "MatchedStatements": [],
      "MissingContextValues": [
        "s3:prefix"
      ],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-hChc3R",
          "EvalResourceDecision": "implicitDeny",
          "MissingContextValues": [
            "s3:prefix"
          ]
        }
      ]
    }
  },
  {
    "name": "smartx/jwt/current",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:DescribeSecret",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
      "EvalDecision": "implicitDeny",
      "MatchedStatements": [],
      "MissingContextValues": [
        "s3:prefix"
      ],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
          "EvalResourceDecision": "implicitDeny",
          "MissingContextValues": [
            "s3:prefix"
          ]
        }
      ]
    }
  },
  {
    "name": "smartx/cookie/current",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:DescribeSecret",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI",
      "EvalDecision": "implicitDeny",
      "MatchedStatements": [],
      "MissingContextValues": [
        "s3:prefix"
      ],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI",
          "EvalResourceDecision": "implicitDeny",
          "MissingContextValues": [
            "s3:prefix"
          ]
        }
      ]
    }
  },
  {
    "name": "smartx/credentials/yaliu-bundle",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:DescribeSecret",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S",
      "EvalDecision": "implicitDeny",
      "MatchedStatements": [],
      "MissingContextValues": [
        "s3:prefix"
      ],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S",
          "EvalResourceDecision": "implicitDeny",
          "MissingContextValues": [
            "s3:prefix"
          ]
        }
      ]
    }
  }
]
```

## 3. The control, in its OWN invocations: the retained action is `allowed` 5 of 5

A positive control is only a control if it is run in ISOLATION from the target, so each of these is a
separate call against the same principal and the same resource. This is what makes section 2's denies a
fact about the ACTION rather than about the call: the same principal, same resource and same call shape
returns `allowed` for the action that stayed.

```json
[
  {
    "name": "smartx/credentials/username",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-9mrtlN",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:GetSecretValue",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-9mrtlN",
      "EvalDecision": "allowed",
      "MatchedStatements": [
        {
          "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
          "SourcePolicyType": "IAM Policy",
          "StartPosition": {
            "Line": 1,
            "Column": 38
          },
          "EndPosition": {
            "Line": 1,
            "Column": 564
          }
        }
      ],
      "MissingContextValues": [],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/username-9mrtlN",
          "EvalResourceDecision": "allowed",
          "MatchedStatements": [
            {
              "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
              "SourcePolicyType": "IAM Policy",
              "StartPosition": {
                "Line": 1,
                "Column": 38
              },
              "EndPosition": {
                "Line": 1,
                "Column": 564
              }
            }
          ]
        }
      ]
    }
  },
  {
    "name": "smartx/credentials/password",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-hChc3R",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:GetSecretValue",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-hChc3R",
      "EvalDecision": "allowed",
      "MatchedStatements": [
        {
          "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
          "SourcePolicyType": "IAM Policy",
          "StartPosition": {
            "Line": 1,
            "Column": 38
          },
          "EndPosition": {
            "Line": 1,
            "Column": 564
          }
        }
      ],
      "MissingContextValues": [],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/password-hChc3R",
          "EvalResourceDecision": "allowed",
          "MatchedStatements": [
            {
              "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
              "SourcePolicyType": "IAM Policy",
              "StartPosition": {
                "Line": 1,
                "Column": 38
              },
              "EndPosition": {
                "Line": 1,
                "Column": 564
              }
            }
          ]
        }
      ]
    }
  },
  {
    "name": "smartx/jwt/current",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:GetSecretValue",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
      "EvalDecision": "allowed",
      "MatchedStatements": [
        {
          "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
          "SourcePolicyType": "IAM Policy",
          "StartPosition": {
            "Line": 1,
            "Column": 38
          },
          "EndPosition": {
            "Line": 1,
            "Column": 564
          }
        }
      ],
      "MissingContextValues": [],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
          "EvalResourceDecision": "allowed",
          "MatchedStatements": [
            {
              "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
              "SourcePolicyType": "IAM Policy",
              "StartPosition": {
                "Line": 1,
                "Column": 38
              },
              "EndPosition": {
                "Line": 1,
                "Column": 564
              }
            }
          ]
        }
      ]
    }
  },
  {
    "name": "smartx/cookie/current",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:GetSecretValue",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI",
      "EvalDecision": "allowed",
      "MatchedStatements": [
        {
          "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
          "SourcePolicyType": "IAM Policy",
          "StartPosition": {
            "Line": 1,
            "Column": 38
          },
          "EndPosition": {
            "Line": 1,
            "Column": 564
          }
        }
      ],
      "MissingContextValues": [],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/cookie/current-UOdUCI",
          "EvalResourceDecision": "allowed",
          "MatchedStatements": [
            {
              "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
              "SourcePolicyType": "IAM Policy",
              "StartPosition": {
                "Line": 1,
                "Column": 38
              },
              "EndPosition": {
                "Line": 1,
                "Column": 564
              }
            }
          ]
        }
      ]
    }
  },
  {
    "name": "smartx/credentials/yaliu-bundle",
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:GetSecretValue",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S",
      "EvalDecision": "allowed",
      "MatchedStatements": [
        {
          "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
          "SourcePolicyType": "IAM Policy",
          "StartPosition": {
            "Line": 1,
            "Column": 38
          },
          "EndPosition": {
            "Line": 1,
            "Column": 564
          }
        }
      ],
      "MissingContextValues": [],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/credentials/yaliu-bundle-ILu23S",
          "EvalResourceDecision": "allowed",
          "MatchedStatements": [
            {
              "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
              "SourcePolicyType": "IAM Policy",
              "StartPosition": {
                "Line": 1,
                "Column": 38
              },
              "EndPosition": {
                "Line": 1,
                "Column": 564
              }
            }
          ]
        }
      ]
    }
  }
]
```

A second control on a different statement -- the write path on the jwt secret -- confirms nothing else moved:

```json
[
  {
    "arn": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
    "EvaluationResult": {
      "EvalActionName": "secretsmanager:PutSecretValue",
      "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
      "EvalDecision": "allowed",
      "MatchedStatements": [
        {
          "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
          "SourcePolicyType": "IAM Policy",
          "StartPosition": {
            "Line": 1,
            "Column": 564
          },
          "EndPosition": {
            "Line": 1,
            "Column": 836
          }
        }
      ],
      "MissingContextValues": [],
      "EvalDecisionDetails": {},
      "ResourceSpecificResults": [
        {
          "EvalResourceName": "arn:aws:secretsmanager:us-east-1:313476888478:secret:smartx/jwt/current-jk8FRu",
          "EvalResourceDecision": "allowed",
          "MatchedStatements": [
            {
              "SourcePolicyId": "role_smartx-assets-pull-role_smartx-assets-pull-access",
              "SourcePolicyType": "IAM Policy",
              "StartPosition": {
                "Line": 1,
                "Column": 564
              },
              "EndPosition": {
                "Line": 1,
                "Column": 836
              }
            }
          ]
        }
      ]
    }
  }
]
```

## 4. Against `predicted_post_state`, clause by clause

| predicted | observed | met |
|---|---|---|
| `DescribeSecret` on each of the 5 `ReadAuthBundle` resources reads `implicitDeny` | implicitDeny on 5 of 5 | YES |
| `GetSecretValue` on the same 5 stays `allowed` | allowed on 5 of 5 | YES |
| `PutSecretValue` on `smartx/jwt/current-jk8FRu` stays `allowed` | allowed | YES |
| `grants_revoked_by_instrument_count` 5 | 5 resource patterns lost the capability | YES |

`predicted_breaks` is `[]`. **That half is NOT yet tested**: section 2 shows the CAPABILITY is gone, which
is not the same claim as no CONSUMER breaking. Only the observation window tests the second claim, and the
five ARNs were RESOLVED from `list-secrets` (100 listed) rather than typed as patterns, so each decision
above is about an object that exists -- an `allowed` against a pattern that matches nothing would prove
nothing.

## 5. Two instrument limits I am not papering over

1. **A nonexistent action also returns `implicitDeny`**, so a typo is indistinguishable from a removed
   grant. `accessanalyzer validate-policy`, the tool that would settle it, is BARRED here
   (`C-ANALYZER-PRICED-FIRST`, `G-25`). Corroboration instead: AWS accepted this exact action string inside
   this role's policy until this morning (the live BEFORE read shows it), and `GetSecretValue` -- same
   service, same call shape, same principal -- returns `allowed`, so the call is well-formed.
2. **`implicitDeny` is the right verdict here and `explicitDeny` would be wrong**: the narrowing removed an
   Allow, it did not add a Deny. A reader expecting `explicitDeny` would misread this as the narrowing
   having failed.

## 6. What remains

Step 5, at or after **13:30Z on 2026-10-09**, against PREDICTION.json's four falsifiers: F1 any
`AccessDenied` in the D log stream; F2 any CloudTrail event for `smartx-assets-daily-pull` on D with
`AccessDenied`/`UnauthorizedOperation` or `eventName=DescribeSecret` at all; F3 zero `GetSecretValue`
events on D (baseline about 6/day) -- the auth path did not run; F4 an ERROR signature other than the
standing `DirtyRunError` baseline, which 30 of 30 prior daily runs carry. Then the `MATCHES-PREDICTION`
line, and leg `OBS` closes. A mismatch is a finding and gets rolled back per PREDICTION.json's
`exact_revert`; it does not get hidden.
