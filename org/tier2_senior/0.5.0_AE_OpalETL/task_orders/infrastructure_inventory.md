# Task Order: Infrastructure Inventory

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-infrastructure-inventory</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a complete structured inventory of all AWS infrastructure in your scope.
    This is a one-time audit that becomes your permanent context for all future sessions.
    Read every Terraform file, Lambda source directory, and deployment artifact in your
    pipeline scope and document what exists.
  </objective>

  <scope>
    <terraform_dirs>
      <dir>infra/aws/terraform/yang-pipeline/</dir>
      <dir>infra/aws/terraform/news-pipeline/</dir>
      <dir>infra/aws/terraform/market-overview/</dir>
      <dir>infra/aws/terraform/smartx-pipeline/</dir>
      <dir>infra/aws/terraform/seeking-alpha/</dir>
      <dir>infra/aws/terraform/portfolio-management/</dir>
      <dir>infra/aws/terraform/causality/</dir>
    </terraform_dirs>
    <lambda_source_map>infra/aws/lambda/ci/lambda-source-map.json</lambda_source_map>
    <data_scripts>
      <dir>data/yang/</dir>
      <dir>data/seeking-alpha/</dir>
    </data_scripts>
  </scope>

  <requirements>
    <requirement id="1">For every Terraform pipeline directory in your scope: list all .tf files with a 1-line description of what each declares</requirement>
    <requirement id="2">For every Lambda function in your scope (from lambda-source-map.json and Terraform): document the function name, source directory, runtime, memory, timeout, trigger type (S3/EventBridge/API Gateway/Step Functions), and what it does</requirement>
    <requirement id="3">For every Lambda Layer used by your functions: document the layer name, S3 key, version, and what packages it provides</requirement>
    <requirement id="4">For every IAM role in your Terraform: document the role name, what services it grants access to, and key policy statements</requirement>
    <requirement id="5">For every EventBridge rule or S3 notification trigger: document the schedule/event pattern and what it invokes</requirement>
    <requirement id="6">For every S3 path your pipelines read from or write to: document the bucket, prefix, and data flow direction</requirement>
    <requirement id="7">Document the current deployment tag and any pipelines that are NOT yet Terraformed</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Output is valid XML written to org/tier2_senior/0.5.0_AE_OpalETL/deliverables/infrastructure_inventory.xml</criterion>
    <criterion id="2">Every Lambda function in your scope from lambda-source-map.json is accounted for</criterion>
    <criterion id="3">Every .tf file in your Terraform directories is referenced</criterion>
    <criterion id="4">Trigger types and schedules are actual values from the Terraform, not guesses</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify any source code or infrastructure -- this is a read-only audit</constraint>
    <constraint>Do NOT run terraform plan/apply or any AWS CLI commands</constraint>
    <constraint>Do NOT create or edit files outside your agent folder</constraint>
    <constraint>Use Glob, Grep, and Read tools only -- no Explore agent, no Task agent</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.5.0_AE_OpalETL/deliverables/infrastructure_inventory.xml
    </deliverable>
  </deliverables>
</task_order>

## Key Files to Read

### Terraform Directories
- `infra/aws/terraform/yang-pipeline/` -- all .tf files (tag: yang-v2.1.0)
- `infra/aws/terraform/news-pipeline/` -- all .tf files (tag: news-v2.4.0)
- `infra/aws/terraform/market-overview/` -- all .tf files (tag: market-overview-v1.4.0)
- `infra/aws/terraform/smartx-pipeline/` -- all .tf files (tag: smartx-v1.0.0)
- `infra/aws/terraform/seeking-alpha/` -- all .tf files (NOT yet tagged/Terraformed)
- `infra/aws/terraform/portfolio-management/` -- all .tf files (NOT yet tagged/Terraformed)
- `infra/aws/terraform/causality/` -- all .tf files (NOT yet tagged/Terraformed)

### Lambda Source Map
- `infra/aws/lambda/ci/lambda-source-map.json` -- filter to functions belonging to yang, news, market-overview, smartx, seeking-alpha, portfolio, and causality pipelines

### Lambda Source Directories
- `infra/aws/lambda/` -- all subdirectories for yang, news, smartx, market, causality, portfolio, seeking-alpha functions
- Read each function's handler file to understand what it does

### Data Scripts
- `data/yang/` -- Yang pipeline data processing scripts
- `data/seeking-alpha/` -- Seeking Alpha data processing scripts

### Deployment Tags
- yang-v2.1.0, news-v2.4.0, market-overview-v1.4.0, smartx-v1.0.0
- seeking-alpha, portfolio, causality -- NOT yet tagged or Terraformed

## Deliverable XML Schema

Write your inventory using this structure:

```xml
<infrastructure_inventory>
  <metadata>
    <agent>0.5.0_AE_OpalETL</agent>
    <scope>Yang, News, Market Overview, SmartX, Seeking Alpha, Portfolio, Causality</scope>
    <date>2026-03-02</date>
  </metadata>

  <pipelines>
    <pipeline name="{name}" terraform_dir="infra/aws/terraform/{dir}/" tag="{current_tag}">

      <lambda_functions>
        <lambda name="{function_name}"
                source_dir="infra/aws/lambda/{dir}/"
                tf_resource="{module.name.aws_lambda_function.this}"
                runtime="python3.12"
                memory_mb="256"
                timeout_s="30"
                trigger="{S3 | EventBridge | API Gateway | Step Functions | manual}"
                last_deployed="{commit_sha} @ {date}">
          One-line description of what this function does
        </lambda>
      </lambda_functions>

      <layers>
        <layer name="{layer_name}" s3_key="{key}" version="{n}">
          What packages this layer provides
        </layer>
      </layers>

      <iam_roles>
        <role name="{role_name}" tf_resource="{resource_path}">
          What this role allows -- key policy statements
        </role>
      </iam_roles>

      <triggers>
        <trigger type="{EventBridge | S3 | API Gateway}" resource="{rule/bucket/api}">
          Schedule or event pattern
        </trigger>
      </triggers>

      <s3_paths>
        <path bucket="{bucket}" prefix="{prefix}" direction="read | write">
          What data flows through this path
        </path>
      </s3_paths>

    </pipeline>
  </pipelines>

  <ec2_services>
    <service name="{service}" instance_id="{id}" manifest_entry="true | false">
      What this EC2 instance runs
    </service>
  </ec2_services>
</infrastructure_inventory>
```
