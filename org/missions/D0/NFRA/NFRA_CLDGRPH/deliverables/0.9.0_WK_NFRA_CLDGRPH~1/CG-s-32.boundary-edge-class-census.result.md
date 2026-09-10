# CG-s-32 -- THE BOUNDARY-EDGE CLASS CENSUS, COUNTED IN FACTS PER KEY

**Task order:** `NFRA_CLDGRPH.TO-CG-G-1` (cell CG-s-32, decomposition v0.10 s.1a).
**Worker:** `0.9.0_WK_NFRA_CLDGRPH~1`, branch `wk-cldgrph-7-1` from CLOUD @`f3b5f26f77`.
**Read only.** No producer was run, no ECS task started, no image act, no S3 write, nothing that
publishes to SNS. Every number below is a read of the SERVED graph through the projection service
plus arithmetic on what came back.

**INSTRUMENT** -- `projection_client.query` -> `POST <base_url>/graph/cypher`, the estate's only
laptop-side reach into the served graph. No local store was opened, named or read.
**COVERAGE** -- the whole served `CloudNode`/`CloudEdge` artifact: 27,665 nodes in 59 classes and
59,683 edges in 55 families. No sampling, no `LIMIT`, nothing filtered before the sweep. Every
count in this record prints its denominator.
**GRAIN** -- node CLASS for the population, edge FAMILY for the declared domain, and DISTINCT
SOURCE `node_id` for every fact count. A family is read as N facts over K keys, never as N successes.
**ENVIRONMENT of the stored baseline** -- round 6's closing pair (`STORED_IN_RESOLVED=135 of 137`,
`DERIVES_FROM_RESOLVED=216 of 216`) comes from the drained TO-CG-F-11 instance and is issuer-stated
at this cut. It is a PRODUCER EMIT-side pair. It was not re-derived here, because this order runs
no producer.
**VINTAGE** -- `2026-09-10T03:31:02.025931+00:00`, the service's own. Not a client clock.

---

## THE CENSUS

```json
{
  "census": "NFRA_CLDGRPH CG-s-32 -- the boundary-edge class census, counted in FACTS PER KEY",
  "task_order": "NFRA_CLDGRPH.TO-CG-G-1",
  "cell": "CG-s-32",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~1",
  "instrument": "projection_client.query -> POST <base_url>/graph/cypher (the SERVED graph; no local store is opened, named or read)",
  "coverage": "the whole served CloudNode/CloudEdge artifact; no sampling, no LIMIT",
  "grain": "node CLASS for the population; edge FAMILY for the domain; distinct SOURCE node_id for every fact count",
  "environment_of_the_stored_baseline": "round 6's closing pair from the drained TO-CG-F-11 instance (F11-AC3), issuer-stated at the cut; producer EMIT side, not re-derived here",
  "served_vintage": "2026-09-10T03:31:02.025931+00:00",
  "served_vintage_line": "VINTAGE: Built from the estate as of 2026-09-10 03:31:02 UTC.  [vintage=2026-09-10T03:31:02.025931+00:00]",
  "denominators": {
    "nodes": 27665,
    "node_classes": 59,
    "edges": 59683,
    "edge_families": 55
  },
  "arn_column_control": {
    "nodes_with_arn_column_differing_from_node_id": 0,
    "denominator": 27665,
    "reading": "the served arn column is a COPY of the key on every node that has one, so it is NOT the discriminator; node_id SHAPE plus a distinct name is"
  },
  "both_identity_population": {
    "classes": 29,
    "of_classes": 59,
    "members": {
      "API_GW": {
        "both": 5,
        "of": 5,
        "keyed_on": {
          "ARN": 5
        },
        "distinct_alt_names": 5
      },
      "API_ROUTE": {
        "both": 86,
        "of": 151,
        "keyed_on": {
          "ARN": 86,
          "OTHER": 65
        },
        "distinct_alt_names": 83
      },
      "CLOUDFRONT_DISTRIBUTION": {
        "both": 2,
        "of": 2,
        "keyed_on": {
          "ARN": 2
        },
        "distinct_alt_names": 2
      },
      "CODEBUILD_PROJECT": {
        "both": 5,
        "of": 5,
        "keyed_on": {
          "ARN": 5
        },
        "distinct_alt_names": 5
      },
      "CW_ALARM": {
        "both": 51,
        "of": 51,
        "keyed_on": {
          "ARN": 51
        },
        "distinct_alt_names": 51
      },
      "DYNAMODB_TABLE": {
        "both": 37,
        "of": 37,
        "keyed_on": {
          "ARN": 37
        },
        "distinct_alt_names": 37
      },
      "EC2_INSTANCE": {
        "both": 33,
        "of": 33,
        "keyed_on": {
          "ARN": 33
        },
        "distinct_alt_names": 24
      },
      "ECS_CLUSTER": {
        "both": 1,
        "of": 1,
        "keyed_on": {
          "ARN": 1
        },
        "distinct_alt_names": 1
      },
      "ECS_TASK_DEFINITION": {
        "both": 9,
        "of": 9,
        "keyed_on": {
          "ARN": 9
        },
        "distinct_alt_names": 9
      },
      "EVENT_RULE": {
        "both": 142,
        "of": 142,
        "keyed_on": {
          "ARN": 142
        },
        "distinct_alt_names": 142
      },
      "IAM_POLICY": {
        "both": 486,
        "of": 486,
        "keyed_on": {
          "ARN": 486
        },
        "distinct_alt_names": 391
      },
      "IAM_ROLE": {
        "both": 219,
        "of": 219,
        "keyed_on": {
          "ARN": 219
        },
        "distinct_alt_names": 219
      },
      "IAM_USER": {
        "both": 2,
        "of": 4,
        "keyed_on": {
          "ARN": 2,
          "OTHER": 2
        },
        "distinct_alt_names": 2
      },
      "INSTANCE_PROFILE": {
        "both": 18,
        "of": 18,
        "keyed_on": {
          "ARN": 18
        },
        "distinct_alt_names": 18
      },
      "KMS_KEY": {
        "both": 12,
        "of": 12,
        "keyed_on": {
          "ARN": 12
        },
        "distinct_alt_names": 12
      },
      "LAMBDA": {
        "both": 203,
        "of": 203,
        "keyed_on": {
          "ARN": 203
        },
        "distinct_alt_names": 203
      },
      "LAMBDA_LAYER": {
        "both": 15,
        "of": 15,
        "keyed_on": {
          "ARN": 15
        },
        "distinct_alt_names": 15
      },
      "LOAD_BALANCER": {
        "both": 1,
        "of": 1,
        "keyed_on": {
          "ARN": 1
        },
        "distinct_alt_names": 1
      },
      "LOG_GROUP": {
        "both": 251,
        "of": 251,
        "keyed_on": {
          "ARN": 251
        },
        "distinct_alt_names": 251
      },
      "ROUTE53_RECORD": {
        "both": 3,
        "of": 3,
        "keyed_on": {
          "ARN": 3
        },
        "distinct_alt_names": 2
      },
      "S3_BUCKET": {
        "both": 34,
        "of": 34,
        "keyed_on": {
          "ARN": 34
        },
        "distinct_alt_names": 34
      },
      "SCHEDULE": {
        "both": 19,
        "of": 19,
        "keyed_on": {
          "ARN": 19
        },
        "distinct_alt_names": 19
      },
      "SECRET": {
        "both": 87,
        "of": 87,
        "keyed_on": {
          "ARN": 87
        },
        "distinct_alt_names": 87
      },
      "SECURITY_GROUP": {
        "both": 26,
        "of": 26,
        "keyed_on": {
          "ARN": 26
        },
        "distinct_alt_names": 25
      },
      "SNS_TOPIC": {
        "both": 16,
        "of": 16,
        "keyed_on": {
          "ARN": 16
        },
        "distinct_alt_names": 16
      },
      "SQS_QUEUE": {
        "both": 19,
        "of": 19,
        "keyed_on": {
          "ARN": 19
        },
        "distinct_alt_names": 19
      },
      "SSM_DOCUMENT": {
        "both": 20,
        "of": 20,
        "keyed_on": {
          "ARN": 20
        },
        "distinct_alt_names": 20
      },
      "STATE_MACHINE": {
        "both": 1,
        "of": 1,
        "keyed_on": {
          "ARN": 1
        },
        "distinct_alt_names": 1
      },
      "VPC_ENDPOINT": {
        "both": 3,
        "of": 3,
        "keyed_on": {
          "ARN": 3
        },
        "distinct_alt_names": 3
      }
    }
  },
  "shadow_ids": {
    "count": 15,
    "classes": [
      "S3_BUCKET_POLICY"
    ],
    "ids": [
      "opal-313476888478-lambda-artifacts",
      "opal-cloudtrail-logs-313476888478",
      "opal-cur-313476888478",
      "opal-data-49financial",
      "opal-data-assets",
      "opal-data-bd",
      "opal-data-cot",
      "opal-data-demo",
      "opal-data-inf",
      "opal-data-portal-v2",
      "opal-data-security",
      "opal-data-security-access-logs",
      "opal-security-evidence",
      "opal-served-key-write-trail-logs",
      "opalinvest-portal"
    ],
    "reading": "a node whose OWN key is the second identity of a both-identity resource; an edge built onto that second identity lands here instead"
  },
  "class_probe_control": {
    "class": "S3_BUCKET",
    "fired": true,
    "both": 34,
    "of": 34
  },
  "edge_families": {
    "swept": 55,
    "of": 55,
    "included": 34,
    "excluded": 21,
    "every_family_has_a_reason": true,
    "facts_per_key": {
      "ALIAS_TO": {
        "keys": 1,
        "edges": 1,
        "dist": {
          "1": 1
        },
        "by_type": {
          "LOAD_BALANCER": 1
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) LOAD_BALANCER carry both an ARN key and a name; LIMB-A source class(es) ROUTE53_RECORD carry both an ARN key and a name"
      },
      "ASSUMES": {
        "keys": 231,
        "edges": 240,
        "dist": {
          "1": 222,
          "2": 9
        },
        "by_type": {
          "IAM_ROLE": 240
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) IAM_ROLE carry both an ARN key and a name; LIMB-A source class(es) ECS_TASK_DEFINITION,INSTANCE_PROFILE,LAMBDA,STATE_MACHINE carry both an ARN key and a name"
      },
      "CALLS": {
        "keys": 542,
        "edges": 1623,
        "dist": {
          "1": 205,
          "2": 131,
          "3": 80,
          "4": 36,
          "5": 22,
          "6": 15,
          "7": 8,
          "8": 10,
          "9": 8,
          "10": 9,
          "11": 3,
          "12": 1,
          "13": 1,
          "14": 4,
          "15": 3,
          "17": 2,
          "18": 1,
          "21": 3
        },
        "by_type": {
          "PipelineFunction": 1623
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) PipelineFunction and target class(es) PipelineFunction are all single-identity, and no endpoint node_id is a shadow id"
      },
      "CAN_ASSUME": {
        "keys": 17,
        "edges": 221,
        "dist": {
          "1": 5,
          "2": 4,
          "4": 1,
          "5": 1,
          "7": 1,
          "9": 1,
          "15": 1,
          "16": 1,
          "22": 1,
          "130": 1
        },
        "by_type": {
          "IAM_ROLE": 221
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) IAM_ROLE carry both an ARN key and a name; LIMB-A source class(es) IAM_ROLE,IAM_USER carry both an ARN key and a name"
      },
      "CLUSTERS": {
        "keys": 15,
        "edges": 91,
        "dist": {
          "1": 3,
          "2": 1,
          "3": 1,
          "4": 2,
          "5": 1,
          "6": 1,
          "7": 2,
          "8": 1,
          "11": 1,
          "13": 1,
          "18": 1
        },
        "by_type": {
          "PanelCluster": 91
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) Page and target class(es) PanelCluster are all single-identity, and no endpoint node_id is a shadow id"
      },
      "CONTAINS": {
        "keys": 7487,
        "edges": 29623,
        "dist": {
          "1": 425,
          "2": 2132,
          "3": 4440,
          "4": 79,
          "5": 73,
          "6": 54,
          "7": 34,
          "8": 32,
          "9": 39,
          "10": 15,
          "11": 18,
          "12": 20,
          "13": 12,
          "14": 4,
          "15": 9,
          "16": 6,
          "17": 8,
          "18": 5,
          "19": 3,
          "20": 4,
          "21": 6,
          "22": 5,
          "24": 3,
          "25": 3,
          "27": 3,
          "28": 5,
          "29": 3,
          "30": 2,
          "32": 1,
          "33": 3,
          "34": 1,
          "40": 1,
          "41": 1,
          "42": 1,
          "45": 1,
          "46": 1,
          "49": 1,
          "50": 1,
          "51": 1,
          "53": 1,
          "55": 1,
          "61": 2,
          "63": 2,
          "69": 1,
          "70": 1,
          "74": 2,
          "80": 1,
          "89": 1,
          "94": 1,
          "97": 1,
          "100": 1,
          "104": 1,
          "132": 1,
          "138": 1,
          "142": 1,
          "149": 1,
          "153": 1,
          "165": 2,
          "178": 1,
          "200": 1,
          "215": 1,
          "236": 1,
          "251": 1,
          "389": 1,
          "775": 1,
          "1259": 1,
          "1336": 1
        },
        "by_type": {
          "API_GW": 91,
          "API_ROUTE": 168,
          "C2Motif": 12,
          "CLOUDFRONT_DISTRIBUTION": 6,
          "CW_ALARM": 40,
          "DYNAMODB_TABLE": 199,
          "DataFetch": 100,
          "EC2_INSTANCE": 401,
          "EVENT_RULE": 225,
          "EVENT_SOURCE": 191,
          "Endpoint": 106,
          "Field": 3219,
          "IAM_POLICY": 2108,
          "IAM_ROLE": 1881,
          "INSTANCE_PROFILE": 118,
          "KMS_KEY": 185,
          "LAMBDA": 2371,
          "MS_FILE": 5065,
          "MS_FOLDER": 1088,
          "MS_LIBRARY": 1,
          "PipelineFunction": 5812,
          "PipelineScript": 2734,
          "ReactComponent": 8,
          "S3Key": 1461,
          "S3_BUCKET": 1298,
          "SERVICE_PRINCIPAL": 612,
          "STATE_MACHINE": 28,
          "ServedURL": 95
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) API_GW,API_ROUTE,CLOUDFRONT_DISTRIBUTION,CW_ALARM,DYNAMODB_TABLE,EC2_INSTANCE,EVENT_RULE,IAM_POLICY,IAM_ROLE,INSTANCE_PROFILE,KMS_KEY,LAMBDA,S3_BUCKET,STATE_MACHINE carry both an ARN key and a name; LIMB-A source class(es) S3_BUCKET carry both an ARN key and a name"
      },
      "CONTAINS_DRILLDOWN": {
        "keys": 132,
        "edges": 241,
        "dist": {
          "1": 98,
          "2": 16,
          "3": 7,
          "4": 2,
          "6": 3,
          "7": 1,
          "8": 1,
          "9": 1,
          "10": 1,
          "12": 1,
          "18": 1
        },
        "by_type": {
          "ReactComponent": 241
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) PanelCluster,ReactComponent and target class(es) ReactComponent are all single-identity, and no endpoint node_id is a shadow id"
      },
      "DEAD_LETTERS_TO": {
        "keys": 6,
        "edges": 6,
        "dist": {
          "1": 6
        },
        "by_type": {
          "SQS_QUEUE": 6
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) SQS_QUEUE carry both an ARN key and a name; LIMB-A source class(es) EVENT_RULE,SQS_QUEUE carry both an ARN key and a name"
      },
      "DECLARES": {
        "keys": 267,
        "edges": 1344,
        "dist": {
          "1": 67,
          "2": 83,
          "3": 31,
          "4": 20,
          "5": 14,
          "6": 14,
          "7": 11,
          "8": 5,
          "9": 3,
          "10": 3,
          "11": 1,
          "12": 1,
          "13": 1,
          "14": 1,
          "15": 1,
          "16": 2,
          "17": 1,
          "20": 1,
          "21": 1,
          "26": 1,
          "29": 1,
          "30": 1,
          "44": 1,
          "147": 1,
          "179": 1
        },
        "by_type": {
          "DataFetch": 106,
          "ReactComponent": 442,
          "TypeDecl": 796
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) Module and target class(es) DataFetch,ReactComponent,TypeDecl are all single-identity, and no endpoint node_id is a shadow id"
      },
      "DERIVES_FROM": {
        "keys": 121,
        "edges": 216,
        "dist": {
          "1": 84,
          "2": 20,
          "3": 13,
          "4": 1,
          "12": 1,
          "16": 1,
          "21": 1
        },
        "by_type": {
          "PipelineFunction": 127,
          "PipelineScript": 89
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) S3Key and target class(es) PipelineFunction,PipelineScript are all single-identity, and no endpoint node_id is a shadow id"
      },
      "EMITS_TO": {
        "keys": 102,
        "edges": 145,
        "dist": {
          "1": 79,
          "2": 12,
          "3": 6,
          "4": 2,
          "5": 2,
          "6": 1
        },
        "by_type": {
          "EVENT_RULE": 145
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) EVENT_RULE carry both an ARN key and a name; LIMB-A source class(es) EC2_INSTANCE,S3_BUCKET carry both an ARN key and a name"
      },
      "ENCRYPTS_WITH": {
        "keys": 45,
        "edges": 45,
        "dist": {
          "1": 45
        },
        "by_type": {
          "KMS_KEY": 45
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) KMS_KEY carry both an ARN key and a name; LIMB-A source class(es) DYNAMODB_TABLE,EC2_INSTANCE,LAMBDA,SECRET,SNS_TOPIC,SQS_QUEUE carry both an ARN key and a name"
      },
      "FETCHES": {
        "keys": 109,
        "edges": 109,
        "dist": {
          "1": 109
        },
        "by_type": {
          "Endpoint": 109
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) Hook and target class(es) Endpoint are all single-identity, and no endpoint node_id is a shadow id"
      },
      "FLOWS_TO": {
        "keys": 581,
        "edges": 961,
        "dist": {
          "1": 381,
          "2": 119,
          "3": 50,
          "4": 14,
          "5": 1,
          "6": 5,
          "7": 2,
          "8": 4,
          "9": 3,
          "10": 1,
          "18": 1
        },
        "by_type": {
          "Field": 956,
          "TypeDecl": 5
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) Field and target class(es) Field,TypeDecl are all single-identity, and no endpoint node_id is a shadow id"
      },
      "GRANTS": {
        "keys": 13,
        "edges": 20,
        "dist": {
          "1": 7,
          "2": 5,
          "3": 1
        },
        "by_type": {
          "IAM_USER": 1,
          "SERVICE_PRINCIPAL": 19
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) IAM_USER carry both an ARN key and a name; LIMB-A source class(es) IAM_POLICY carry both an ARN key and a name"
      },
      "HAS_FIELD": {
        "keys": 790,
        "edges": 4269,
        "dist": {
          "1": 43,
          "2": 106,
          "3": 141,
          "4": 141,
          "5": 99,
          "6": 66,
          "7": 39,
          "8": 39,
          "9": 31,
          "10": 21,
          "11": 9,
          "12": 8,
          "13": 9,
          "14": 6,
          "15": 1,
          "16": 6,
          "17": 3,
          "18": 6,
          "19": 2,
          "20": 1,
          "21": 2,
          "22": 6,
          "23": 1,
          "27": 1,
          "28": 1,
          "37": 1,
          "49": 1
        },
        "by_type": {
          "Field": 4269
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) TypeDecl and target class(es) Field are all single-identity, and no endpoint node_id is a shadow id"
      },
      "HAS_KEY": {
        "keys": 85,
        "edges": 85,
        "dist": {
          "1": 85
        },
        "by_type": {
          "ReactQueryKey": 85
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) Hook and target class(es) ReactQueryKey are all single-identity, and no endpoint node_id is a shadow id"
      },
      "HAS_POLICY": {
        "keys": 234,
        "edges": 625,
        "dist": {
          "1": 92,
          "2": 60,
          "3": 27,
          "4": 17,
          "5": 22,
          "6": 5,
          "7": 4,
          "8": 1,
          "9": 1,
          "13": 2,
          "17": 1,
          "18": 2
        },
        "by_type": {
          "IAM_POLICY": 625
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) IAM_POLICY carry both an ARN key and a name; LIMB-A source class(es) IAM_ROLE,S3_BUCKET carry both an ARN key and a name"
      },
      "HAS_PROFILE": {
        "keys": 31,
        "edges": 31,
        "dist": {
          "1": 31
        },
        "by_type": {
          "INSTANCE_PROFILE": 31
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) INSTANCE_PROFILE carry both an ARN key and a name; LIMB-A source class(es) EC2_INSTANCE carry both an ARN key and a name"
      },
      "HAS_PROP": {
        "keys": 116,
        "edges": 359,
        "dist": {
          "1": 26,
          "2": 27,
          "3": 26,
          "4": 17,
          "5": 10,
          "6": 5,
          "7": 2,
          "9": 1,
          "10": 1,
          "20": 1
        },
        "by_type": {
          "Prop": 359
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) ReactComponent and target class(es) Prop are all single-identity, and no endpoint node_id is a shadow id"
      },
      "HAS_PROPS_TYPE": {
        "keys": 208,
        "edges": 208,
        "dist": {
          "1": 208
        },
        "by_type": {
          "TypeDecl": 208
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) ReactComponent and target class(es) TypeDecl are all single-identity, and no endpoint node_id is a shadow id"
      },
      "HAS_ROUTE": {
        "keys": 5,
        "edges": 86,
        "dist": {
          "1": 2,
          "5": 1,
          "7": 1,
          "72": 1
        },
        "by_type": {
          "API_ROUTE": 86
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) API_ROUTE carry both an ARN key and a name; LIMB-A source class(es) API_GW carry both an ARN key and a name"
      },
      "HAS_TYPE": {
        "keys": 100,
        "edges": 100,
        "dist": {
          "1": 100
        },
        "by_type": {
          "TypeDecl": 100
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) DataFetch and target class(es) TypeDecl are all single-identity, and no endpoint node_id is a shadow id"
      },
      "INSTANTIATES": {
        "keys": 1298,
        "edges": 1298,
        "dist": {
          "1": 1298
        },
        "by_type": {
          "ReactComponent": 1298
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) JSXElement and target class(es) ReactComponent are all single-identity, and no endpoint node_id is a shadow id"
      },
      "INVOKES": {
        "keys": 12,
        "edges": 43,
        "dist": {
          "1": 8,
          "2": 2,
          "3": 1,
          "28": 1
        },
        "by_type": {
          "LAMBDA": 43
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) LAMBDA carry both an ARN key and a name; LIMB-A source class(es) LAMBDA,STATE_MACHINE carry both an ARN key and a name"
      },
      "IN_VPC": {
        "keys": 1,
        "edges": 1,
        "dist": {
          "1": 1
        },
        "by_type": {
          "SECURITY_GROUP": 1
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) SECURITY_GROUP carry both an ARN key and a name; LIMB-A source class(es) LAMBDA carry both an ARN key and a name"
      },
      "IS_ENDPOINT": {
        "keys": 106,
        "edges": 106,
        "dist": {
          "1": 106
        },
        "by_type": {
          "Endpoint": 106
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) DataFetch and target class(es) Endpoint are all single-identity, and no endpoint node_id is a shadow id"
      },
      "LOGS_TO": {
        "keys": 16,
        "edges": 16,
        "dist": {
          "1": 16
        },
        "by_type": {
          "LOG_GROUP": 16
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) LOG_GROUP carry both an ARN key and a name; LIMB-A source class(es) LAMBDA carry both an ARN key and a name"
      },
      "MONITORS": {
        "keys": 27,
        "edges": 27,
        "dist": {
          "1": 27
        },
        "by_type": {
          "CLOUDFRONT_DISTRIBUTION": 3,
          "EC2_INSTANCE": 3,
          "LAMBDA": 17,
          "S3_BUCKET": 2,
          "SQS_QUEUE": 2
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) CLOUDFRONT_DISTRIBUTION,EC2_INSTANCE,LAMBDA,S3_BUCKET,SQS_QUEUE carry both an ARN key and a name; LIMB-A source class(es) CW_ALARM carry both an ARN key and a name"
      },
      "NOTIFIES": {
        "keys": 40,
        "edges": 41,
        "dist": {
          "1": 39,
          "2": 1
        },
        "by_type": {
          "SNS_TOPIC": 40,
          "SQS_QUEUE": 1
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) SNS_TOPIC,SQS_QUEUE carry both an ARN key and a name; LIMB-A source class(es) CW_ALARM,S3_BUCKET carry both an ARN key and a name"
      },
      "ORIGIN": {
        "keys": 1,
        "edges": 5,
        "dist": {
          "5": 1
        },
        "by_type": {
          "S3_BUCKET": 5
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) S3_BUCKET carry both an ARN key and a name; LIMB-A source class(es) CLOUDFRONT_DISTRIBUTION carry both an ARN key and a name"
      },
      "OWNED_BY": {
        "keys": 6385,
        "edges": 6385,
        "dist": {
          "1": 6385
        },
        "by_type": {
          "MS_USER": 6153,
          "S3_BUCKET": 232
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) S3_BUCKET carry both an ARN key and a name"
      },
      "PROJECTS_TO": {
        "keys": 442,
        "edges": 442,
        "dist": {
          "1": 442
        },
        "by_type": {
          "Component": 442
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) ReactComponent and target class(es) Component are all single-identity, and no endpoint node_id is a shadow id"
      },
      "PROP_PASSES": {
        "keys": 483,
        "edges": 1382,
        "dist": {
          "1": 156,
          "2": 95,
          "3": 121,
          "4": 51,
          "5": 15,
          "6": 14,
          "7": 12,
          "8": 5,
          "9": 3,
          "10": 3,
          "13": 1,
          "14": 1,
          "15": 1,
          "16": 3,
          "17": 1,
          "22": 1
        },
        "by_type": {
          "Field": 965,
          "Prop": 417
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) JSXElement and target class(es) Field,Prop are all single-identity, and no endpoint node_id is a shadow id"
      },
      "PUBLISHES_TO": {
        "keys": 33,
        "edges": 35,
        "dist": {
          "1": 31,
          "2": 2
        },
        "by_type": {
          "SNS_TOPIC": 35
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) SNS_TOPIC carry both an ARN key and a name; LIMB-A source class(es) EC2_INSTANCE,LAMBDA carry both an ARN key and a name"
      },
      "READS": {
        "keys": 330,
        "edges": 1043,
        "dist": {
          "1": 150,
          "2": 43,
          "3": 36,
          "4": 38,
          "5": 12,
          "6": 3,
          "7": 17,
          "8": 2,
          "10": 16,
          "13": 12,
          "18": 1
        },
        "by_type": {
          "DYNAMODB_TABLE": 288,
          "PipelineScript": 291,
          "S3_BUCKET": 464
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) DYNAMODB_TABLE,S3_BUCKET carry both an ARN key and a name; LIMB-A source class(es) EC2_INSTANCE,LAMBDA carry both an ARN key and a name"
      },
      "READS_FIELD": {
        "keys": 169,
        "edges": 2110,
        "dist": {
          "1": 19,
          "2": 12,
          "3": 16,
          "4": 15,
          "5": 10,
          "6": 7,
          "7": 7,
          "8": 5,
          "9": 12,
          "10": 5,
          "11": 4,
          "12": 3,
          "13": 6,
          "14": 4,
          "15": 7,
          "16": 2,
          "17": 4,
          "18": 2,
          "19": 3,
          "20": 2,
          "23": 1,
          "24": 3,
          "26": 1,
          "27": 1,
          "28": 3,
          "29": 3,
          "34": 1,
          "35": 1,
          "43": 1,
          "46": 1,
          "50": 1,
          "56": 1,
          "57": 2,
          "66": 1,
          "77": 1,
          "98": 1,
          "130": 1
        },
        "by_type": {
          "Field": 2110
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) Module and target class(es) Field are all single-identity, and no endpoint node_id is a shadow id"
      },
      "READS_S3": {
        "keys": 81,
        "edges": 323,
        "dist": {
          "1": 26,
          "2": 17,
          "3": 12,
          "4": 8,
          "5": 2,
          "6": 2,
          "7": 1,
          "9": 5,
          "10": 1,
          "11": 1,
          "13": 2,
          "14": 1,
          "16": 1,
          "17": 1,
          "27": 1
        },
        "by_type": {
          "S3Key": 323
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A source class(es) LAMBDA carry both an ARN key and a name"
      },
      "READS_SECRET": {
        "keys": 101,
        "edges": 259,
        "dist": {
          "1": 43,
          "2": 8,
          "3": 20,
          "4": 15,
          "5": 14,
          "10": 1
        },
        "by_type": {
          "SECRET": 259
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) SECRET carry both an ARN key and a name; LIMB-A source class(es) EC2_INSTANCE,LAMBDA carry both an ARN key and a name"
      },
      "READS_URL": {
        "keys": 48,
        "edges": 48,
        "dist": {
          "1": 48
        },
        "by_type": {
          "ServedURL": 48
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) Endpoint and target class(es) ServedURL are all single-identity, and no endpoint node_id is a shadow id"
      },
      "REFERENCES_TYPE": {
        "keys": 261,
        "edges": 1129,
        "dist": {
          "1": 100,
          "2": 60,
          "3": 26,
          "4": 20,
          "5": 15,
          "6": 9,
          "7": 6,
          "8": 5,
          "9": 4,
          "10": 3,
          "11": 2,
          "13": 2,
          "17": 1,
          "18": 1,
          "22": 1,
          "26": 2,
          "35": 1,
          "43": 1,
          "99": 1,
          "140": 1
        },
        "by_type": {
          "TypeDecl": 1129
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) Module and target class(es) TypeDecl are all single-identity, and no endpoint node_id is a shadow id"
      },
      "RENDERS": {
        "keys": 1433,
        "edges": 2447,
        "dist": {
          "1": 1089,
          "2": 163,
          "3": 60,
          "4": 28,
          "5": 27,
          "6": 23,
          "7": 9,
          "8": 7,
          "9": 10,
          "10": 5,
          "11": 3,
          "12": 1,
          "13": 1,
          "17": 1,
          "18": 1,
          "19": 3,
          "27": 1,
          "31": 1
        },
        "by_type": {
          "Field": 2447
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) JSXRender and target class(es) Field are all single-identity, and no endpoint node_id is a shadow id"
      },
      "ROUTES_TO": {
        "keys": 86,
        "edges": 86,
        "dist": {
          "1": 86
        },
        "by_type": {
          "LAMBDA": 86
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) LAMBDA carry both an ARN key and a name; LIMB-A source class(es) API_ROUTE carry both an ARN key and a name"
      },
      "RUNS": {
        "keys": 5,
        "edges": 248,
        "dist": {
          "18": 1,
          "46": 2,
          "69": 2
        },
        "by_type": {
          "PipelineScript": 248
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A source class(es) EC2_INSTANCE carry both an ARN key and a name"
      },
      "SERVED_FROM": {
        "keys": 27,
        "edges": 27,
        "dist": {
          "1": 27
        },
        "by_type": {
          "S3_BUCKET_POLICY": 27
        },
        "decision": "INCLUDED",
        "reason": "LIMB-B target is NAME-ADDRESSED onto a both-identity resource and lands on S3_BUCKET_POLICY"
      },
      "SHARES_SOURCE": {
        "keys": 29,
        "edges": 55,
        "dist": {
          "1": 17,
          "2": 5,
          "3": 3,
          "4": 2,
          "5": 1,
          "6": 1
        },
        "by_type": {
          "PanelCluster": 55
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) PanelCluster and target class(es) PanelCluster are all single-identity, and no endpoint node_id is a shadow id"
      },
      "STORED_IN": {
        "keys": 135,
        "edges": 135,
        "dist": {
          "1": 135
        },
        "by_type": {
          "S3_BUCKET_POLICY": 135
        },
        "decision": "INCLUDED",
        "reason": "LIMB-B target is NAME-ADDRESSED onto a both-identity resource and lands on S3_BUCKET_POLICY"
      },
      "SUBSCRIBES": {
        "keys": 3,
        "edges": 3,
        "dist": {
          "1": 3
        },
        "by_type": {
          "LAMBDA": 1,
          "SQS_QUEUE": 2
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) LAMBDA,SQS_QUEUE carry both an ARN key and a name; LIMB-A source class(es) SNS_TOPIC carry both an ARN key and a name"
      },
      "TRIGGERS": {
        "keys": 160,
        "edges": 171,
        "dist": {
          "1": 155,
          "2": 3,
          "3": 1,
          "7": 1
        },
        "by_type": {
          "CODEBUILD_PROJECT": 2,
          "ECS_CLUSTER": 3,
          "LAMBDA": 161,
          "LOG_GROUP": 1,
          "SNS_TOPIC": 3,
          "SQS_QUEUE": 1
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) CODEBUILD_PROJECT,ECS_CLUSTER,LAMBDA,LOG_GROUP,SNS_TOPIC,SQS_QUEUE carry both an ARN key and a name; LIMB-A source class(es) EVENT_RULE,S3_BUCKET,SCHEDULE carry both an ARN key and a name"
      },
      "USES_LAYER": {
        "keys": 67,
        "edges": 80,
        "dist": {
          "1": 54,
          "2": 13
        },
        "by_type": {
          "LAMBDA_LAYER": 80
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) LAMBDA_LAYER carry both an ARN key and a name; LIMB-A source class(es) LAMBDA carry both an ARN key and a name"
      },
      "USES_OAC": {
        "keys": 1,
        "edges": 1,
        "dist": {
          "1": 1
        },
        "by_type": {
          "S3_BUCKET": 1
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) S3_BUCKET carry both an ARN key and a name; LIMB-A source class(es) CLOUDFRONT_DISTRIBUTION carry both an ARN key and a name"
      },
      "USES_OAI": {
        "keys": 1,
        "edges": 4,
        "dist": {
          "4": 1
        },
        "by_type": {
          "S3_BUCKET": 4
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) S3_BUCKET carry both an ARN key and a name; LIMB-A source class(es) CLOUDFRONT_DISTRIBUTION carry both an ARN key and a name"
      },
      "USES_SG": {
        "keys": 2,
        "edges": 2,
        "dist": {
          "1": 2
        },
        "by_type": {
          "SECURITY_GROUP": 2
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) SECURITY_GROUP carry both an ARN key and a name; LIMB-A source class(es) LOAD_BALANCER,VPC_ENDPOINT carry both an ARN key and a name"
      },
      "WRITES": {
        "keys": 308,
        "edges": 807,
        "dist": {
          "1": 158,
          "2": 29,
          "3": 54,
          "4": 12,
          "5": 28,
          "6": 1,
          "8": 12,
          "9": 13,
          "22": 1
        },
        "by_type": {
          "DYNAMODB_TABLE": 243,
          "S3Key": 216,
          "S3_BUCKET": 348
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A target class(es) DYNAMODB_TABLE,S3_BUCKET carry both an ARN key and a name; LIMB-A source class(es) EC2_INSTANCE,LAMBDA carry both an ARN key and a name"
      },
      "WRITES_S3": {
        "keys": 144,
        "edges": 275,
        "dist": {
          "1": 93,
          "2": 21,
          "3": 15,
          "4": 5,
          "5": 6,
          "6": 2,
          "11": 1,
          "22": 1
        },
        "by_type": {
          "S3Key": 275
        },
        "decision": "INCLUDED",
        "reason": "LIMB-A source class(es) LAMBDA carry both an ARN key and a name"
      }
    }
  },
  "round6_reconciliation": {
    "stored_in": {
      "asserted": "135 of 137 on S3_BUCKET_POLICY",
      "measured_served": {
        "keys": 135,
        "edges": 135,
        "dist": {
          "1": 135
        },
        "by_type": {
          "S3_BUCKET_POLICY": 135
        },
        "decision": "INCLUDED",
        "reason": "LIMB-B target is NAME-ADDRESSED onto a both-identity resource and lands on S3_BUCKET_POLICY"
      },
      "reproduced": true
    },
    "derives_from": {
      "asserted": "216 of 216",
      "measured_served": {
        "keys": 121,
        "edges": 216,
        "dist": {
          "1": 84,
          "2": 20,
          "3": 13,
          "4": 1,
          "12": 1,
          "16": 1,
          "21": 1
        },
        "by_type": {
          "PipelineFunction": 127,
          "PipelineScript": 89
        },
        "decision": "EXCLUDED",
        "reason": "no endpoint carries two identities: source class(es) S3Key and target class(es) PipelineFunction,PipelineScript are all single-identity, and no endpoint node_id is a shadow id"
      },
      "reproduced": true
    },
    "differences": [
      "the 137 is a PRODUCER EMIT count and cannot exist on the served plane: an unresolved edge is not a row in a REL table",
      "the served plane's own eligible key population (224 firm-prefixed canonical S3Keys over 5 present firm buckets) is a DIFFERENT grain from the producer's pre-merge 191 and from 137",
      "216 of 216 is an EDGE rate: in facts per key DERIVES_FROM is 216 edges over 121 keys, 1.79 per key",
      "the cut states 54 edge families; this read carries 55 (node classes 59 agree) -- row NFRA_CLDGRPH-W1-S36",
      "the cut names vintage 2026-09-10T03:02:00; the service reports 2026-09-10T03:31:02.025931+00:00 -- row NFRA_CLDGRPH-W1-S36"
    ]
  },
  "rows_filed": [
    "NFRA_CLDGRPH-W1-S35",
    "NFRA_CLDGRPH-W1-S36"
  ]
}
```

---

## READING THE NUMBERS

### 1. The population is wide; the seam is one class and fifteen nodes

29 of 59 node classes carry two identity strings for one resource -- an ARN-shaped `node_id` and a
distinct `name`. That is every AWS-layer class in the graph; every portal, code, MS-Graph and
pipeline class carries exactly one. On the face of it the boundary is wide.

It is not, and this is the census's central number: **only 15 nodes in the entire served graph, out
of 27,665, are keyed by the SECOND identity of a both-identity resource, and all 15 are the whole
of one class -- `S3_BUCKET_POLICY`, 15 of 15.** A bucket's `name` is the policy node's `node_id`.
Nowhere else in the estate does a resource's alternate name collide with some other node's key. So
an edge builder that reaches for a resource's second name has exactly one place to land wrong, and
it lands there silently, because the landing is a real node and the producer's dangling check sees
a resolved edge.

The `arn` COLUMN on the served table is not the discriminator and a census built on it would have
measured nothing: it is a byte-for-byte copy of `node_id` on every node that has one, 0 of 27,665
differing. `ARN_COLUMN_CONTROL` in `g1_both_identity_nodes.py` measures that rather than asserting
it. The discriminator is the SHAPE of the key plus the presence of a distinct name.

### 2. Two families land on the shadow class, and only one of them was known

Of the 34 included families, **2 resolve onto a shadow class, and both resolve onto it 100 percent
of the time**:

| family | keys | edges | per-key distribution | resolves onto |
|---|---|---|---|---|
| `STORED_IN` | 135 | 135 | `{1: 135}` | `S3_BUCKET_POLICY` 135 of 135 |
| `SERVED_FROM` | 27 | 27 | `{1: 27}` | `S3_BUCKET_POLICY` 27 of 27 |

`SERVED_FROM` was not named at the cut. It is the same defect as `STORED_IN`, built by a different
producer path: `derive_runner.py:1947-1955` forms the edge "co-keyed on the actual S3 node_id" and
targets a bucket NAME (`opal-data-portal-v2`), so all 27 ServedURL nodes assert they are served from
a bucket POLICY. **This is the answer to how wide CG-s-33's fix must reach: two families, not one,
and two producer files, not one** -- `derive_stitch.py` for `STORED_IN` and `derive_runner.py` for
`SERVED_FROM`.

The reach does not stop at the producers. Two downstream scorers already read the shape:
`debtscan_canon_scorer.py:48` and `:144` name `ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY` as the
AUTH_CANON's live shape -- the wrong-class landing has been ADOPTED AS CANON in a scored artifact --
while `canon_motif_scorer.py:131` names the dominant motif `(ServedURL)-[SERVED_FROM]->(S3)`, which
is what the edge was meant to be. The two scorers describe one edge and disagree about what it
points at. A re-point that moves `SERVED_FROM` onto `S3_BUCKET` will change `debtscan`'s dominant
shape and its outlier threshold, and that consumer must move in the same act or its census reads a
100 percent outlier rate the morning after.

### 3. `STORED_IN` is a CLASS defect now, not a cardinality one

Round 6's second cycle bought exactly what it claimed. `STORED_IN` reads `{1: 135}` -- one fact per
key, no key at 2, 764 guesses gone. Its whole remaining defect is that the one fact points at the
wrong CLASS. CG-s-33 is therefore an identity re-point (`bkt_by_name` yielding the arn rather than
the nid, both planes moving together per row W2-S70), not a re-count, and nothing in this census
suggests the fan-out can come back through that door.

**And the graph already answers the question correctly, on the correct class, for a superset of the
same keys.** `OWNED_BY` carries `S3Key -> S3_BUCKET` on 232 keys, `{1: 232}`, landing on the
ARN-keyed bucket node. Measured here: all 135 `STORED_IN` source keys also carry an `OWNED_BY` edge
(135 of 135), and in 135 of 135 cases the `OWNED_BY` bucket ARN names the same bucket as the
`STORED_IN` target name. So `STORED_IN` is not adding a fact the graph lacks; it is restating a fact
the graph already holds, onto a node that is not a bucket. Whether CG-s-33 re-points it or retires
it in favour of `OWNED_BY` is that order's call, but the census says plainly that a re-point creates
a duplicate edge family and a retirement loses nothing measurable.

### 4. Which families are healthy only by accident

Thirty-two of the 34 included families resolve onto a both-identity class by its ARN and are
correct. Their health is not luck in the sense that matters -- the builder used the key -- but two
shapes are worth flagging to a reader who might read a clean resolution rate as a clean edge:

- **Single-candidate endpoints that would fan the moment a second candidate appeared.** `ORIGIN`
  (keys=1, edges=5), `USES_OAI` (keys=1, edges=4), `USES_OAC` (keys=1, edges=1) and `HAS_ROUTE`
  (keys=5, edges=86, one key at 72) each have a source population of one to five nodes. `ORIGIN`
  already reads 5.00 edges per key from a single CloudFront distribution. These are structurally
  correct -- one distribution genuinely has several origins -- but a census that reported them as
  "5 of 5 resolved" would be reporting the same quantity the CVO warned about. Read the
  distribution, not the rate.
- **Families whose target class is a both-identity class AND whose builder does a NAME lookup.**
  `ROUTES_TO` (86 keys, 86 edges, `{1: 86}`, onto `LAMBDA`) is the one to watch: `derive_stitch`
  resolves it through `lam_by_name`, the same name-index shape that produced the bucket defect. It
  is healthy today only because a LAMBDA's `node_id` IS its arn, so `arn or nid` cannot pick the
  wrong string. If a LAMBDA node ever gained a second key -- an alias, a versioned arn, a
  name-keyed shadow -- `ROUTES_TO` would acquire the identical failure and its resolution rate
  would stay 100 percent while it did.

### 5. What a reader must NOT conclude from a resolution rate

This is the binding condition restated as a warning to the next reader of this graph.

- **A resolution rate measures DANGLING, not CORRECTNESS.** `STORED_IN` resolved 135 of 137 -- 98.5
  percent -- and 100 percent of what resolved landed on a class that is not a bucket. A rate of
  100 percent tells you every emitted edge found a node. It tells you nothing about whether it
  found the RIGHT node, and the producer's own dangling check cannot tell you either, because a
  shadow node is a real node.
- **A rate counted over EDGES hides fan-out completely.** Before the cycle-4 fix, `STORED_IN` read
  764 of 764 resolved and was four-fifths guesswork: 191 facts fanned across 4 name-keyed buckets.
  The rate was perfect and the graph was wrong. This is why every line of this census carries
  `keys=` beside `edges=`, and why `g1_facts_per_key.py` fails itself
  (`EDGES_ONLY_COUNTS_PRINTED`) if any line states an edge count without its key denominator. The
  arm is not decorative: its positive control catches a planted bare edge count, so the measured
  zero is a measurement.
- **`DERIVES_FROM 216 of 216` is an edge rate too.** In facts per key it is 216 edges over 121
  keys, `{1: 84, 2: 20, 3: 13, 4: 1, 12: 1, 16: 1, 21: 1}` -- 1.79 per key, with one key carrying
  21. The fan is legitimate (one artifact can derive from several scripts) and the rate is honest.
  But "216 of 216" and "216 facts" are different sentences and only the first one is true.
- **A both-identity population is not a defect population.** 29 of 59 classes carry two names; 1
  class is a shadow; 2 families of 55 land on it. The wide number is the exposure, the narrow
  number is the damage, and quoting either alone misdescribes the estate.

---

## SURPRISE ROWS FILED

- **`NFRA_CLDGRPH-W1-S35`** -- `DERIVES_FROM`, which the cut names as one of the two families the
  census reports among the INCLUDED set, measures OUTSIDE the both-identity population: its three
  endpoint classes (`S3Key` 0 of 381, `PipelineFunction` 0 of 1217, `PipelineScript` 0 of 167) each
  carry one identity, and no endpoint of it is a shadow id. It is reported in the identical
  facts-per-key form as the round's NAMED COMPARATOR and the seam's negative control -- a stitch
  family with no identity ambiguity -- rather than being omitted or force-fitted into a population
  it does not belong to. `OBSERVATION`, `INERT`.
- **`NFRA_CLDGRPH-W1-S36`** -- the cut states 54 distinct `edge_type` values at vintage
  `2026-09-10T03:02:00`; this read carries 55 at vintage `2026-09-10T03:31:02.025931+00:00` (the
  minute the cut names as the CVO's SIGNING time, not as the artifact's vintage). The node-class
  count, 59, agrees. No number in this deliverable is computed against the cut's 54; the census
  prints `EDGE_FAMILIES_SWEPT=55 of 55` from its own read. `OBSERVATION`, `INERT`.

## HOW TO RE-RUN THIS CENSUS

```
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g1_both_identity_nodes.py
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g1_edge_families.py
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g1_facts_per_key.py
timeout 120 python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/g1_facts_per_key.py --reconcile
```

Every one is a read. The vintage moves when the estate's own 02:00Z / 03:00Z scheduled derives fire;
nothing here fires one.
