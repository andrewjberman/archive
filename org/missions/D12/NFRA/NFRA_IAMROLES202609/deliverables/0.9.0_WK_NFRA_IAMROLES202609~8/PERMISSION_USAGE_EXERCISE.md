# PERMISSION_USAGE_EXERCISE -- the permission-grain usage instrument, EXERCISED over the whole estate role population

**Cell:** `IAM-t-2` (round-3 `R3-B`), outcome **FWD-2**. **DONE WHEN state: EXERCISED.**
**Worker:** `0.9.0_WK_NFRA_IAMROLES202609~8`  **Branch:** `wk-NFRA_IAMROLES202609-8`  **Worktree:** `/c/tmp/wk-iamroles-8`
**Run date:** 2026-09-10 (UTC). **Account:** `313476888478` (`sts get-caller-identity`, rc=0).

> FWD-2's bar, verbatim: *"real roles have been read and their unused permissions named, over a stated lookback"*.
> This document is that reading. It NAMES and it does not narrow: nothing in this cell changed a policy, a role,
> or any AWS state. Every AWS call made was a read.

---

## 0. THE INSTRUMENT -- exercised, not built, not forked, not improved

The instrument already existed at HEAD and already answered the permission axis. It was RUN as-is:

```
timeout 120 bash .tools/comp-iam-usage permission-cold --role <ROLE> --lookback 90 --json
```

**The invocation FORM is part of every figure below.** It is `bash .tools/comp-iam-usage` from *this worktree*,
never the bare name -- a bare name resolves through a `~/bin` forwarder to the main checkout, which is a
different tree at a different vintage.

**The instrument's bytes are unchanged by this cell.** Content pin, re-read in the worktree at commit time:

```
$ git hash-object .tools/comp-iam-usage org/modules/graph/comp_iam_usage.py
5c7f03ba3702d5de5c0edf7a955a72dd20e596f5
8670fc5025694c942f8a7c725a19e2317cf63c20
```

`.tools/` is not in this worker's write surface and was not written to. `comp-iam-usage self-test` was run once
before the sweep and returned rc=0 with its own assertion line:

```
OK: never-used!=cold, break-glass-guard-not-debris, UNKNOWN-band, hold-aware, 22a limits NAMED
    (fix-or-carry), permission-grain unobservable!=never-used -- all held
```

---

## (a) THE POPULATION, AND ITS DENOMINATOR

### The selection rule, stated before the result

**There is no sample. The population is the whole of it.** The selection rule is:

> *Every IAM role in account `313476888478` that sits at path `/`, as returned by one auto-paginated
> `aws iam list-roles`, sorted by role name. No filter on name, tag, service, age, policy size or team.*

An unstated or convenience selection is a filtered census that confirms whatever it was filtered for, so the
rule is stated as a rule and then the entire set it names was run. Choosing the whole population removes the
question: there is no slice to argue about.

### The denominator, printed

| quantity | value | how read |
|---|---|---|
| roles live in the account, ALL paths | **229** | `timeout 120 .tools/aws iam list-roles --output json`, auto-paginated, counted client-side, rc=0 |
| of which AWS service-linked (`/aws-service-role/`) -- **EXCLUDED** | **10** | same response, partitioned on the `Path` field |
| **estate roles at path `/` -- THE POPULATION** | **219** | same response; 219 + 10 = 229, reconciles exactly |
| roles ATTEMPTED | **219** | one bounded invocation each, iterated role by role |
| roles that RETURNED (rc=0, parseable JSON) | **219** | `219 of 219`; zero non-zero exits, zero timeouts, zero empty stderr-bearing runs |
| roles where the instrument could NOT observe | **0** | `granted_read_ok` and `advisor_read_ok` both true on 219 of 219 returns |
| **granted permissions examined -- THE PERMISSION DENOMINATOR** | **5494** | union of Allow actions across every attached-managed and inline policy, per role, summed |

**Why 219 and not 229.** The 10 excluded roles are AWS service-linked: their policies are AWS-owned and cannot
be narrowed by this estate, so naming their unused permissions would be advice nobody can act on. The exclusion
is deliberate and is named rather than assumed -- **219 is every live role MINUS TEN, not "every live role"**.
Filed as surprise row `NFRA_IAMROLES202609-Z-W8-S2`, because the round-3 battery text carries the 219 without
that qualifier and anything rolling this cell up inherits the gloss.

**Corroboration, on a second instrument and a second plane.** The battery's `comp-find --corpus aws` figure
(vintage 2026-09-10 12:24:50 UTC) reads 219 IAM_ROLE nodes from a built CloudNode DB. This cell read the IAM
control plane directly through the `aws` shim and also got 219 at path `/`. Two instruments, two planes, same
number -- and the same 10 missing from both, which is what localises the omission to the population
DEFINITION rather than to either tool.

### Cost of the sweep, for whoever repeats it

219 bounded invocations, **1067 s wall total**, mean **4.9 s** per role, slowest single role **10 s** -- all far
inside the `timeout 120` bound, so no criterion here has the word "timeout" as its evidence.

---

## (b) THE LOOKBACK

# 90 days.

Stated as a number because FWD-2's bar is *"over a stated lookback"* in terms. `--lookback 90` was passed
explicitly on every one of the 219 invocations rather than relied on as the tool default, and every returned
JSON object carries `"lookback_days": 90` -- read back across all 219 returns, the set of distinct values is
`{90}`, a set of size one.

**What "never-used over a 90-day lookback" means here, in the instrument's own words:** *"tracked by Access
Advisor, and either never accessed at all or last accessed OUTSIDE the stated --lookback window -- 'unused over
the stated lookback', FWD-2's own phrasing, not a claim the action was never called at any point in the
account's history."*

That distinction is measured, not just quoted. Of the 1437 never-used rows:

- **1342** have NO observed use at all in the telemetry.
- **95** have a REAL last-use date that simply falls outside the 90-day window (ages **93** to **355** days).

A shorter lookback moves the second group and cannot move the first. **The lookback is a knob and this
deliverable states which side of it each row sits on.**

---

## THE HEADLINE, WITH THE ONE ROLE THAT DOMINATES IT SEPARATED OUT

| | granted (denominator) | used | **never-used** | **unobservable** |
|---|---|---|---|---|
| **all 219 roles** | **5494** | 421 | **1437** | **3636** |
| 218 roles, excluding `opal-drift-producer-codebuild-role` | 2576 | 418 | 695 | 1463 |
| that ONE role alone | 2918 | 3 | 742 | 2173 |

**READ THE SECOND ROW BEFORE THE FIRST.** One role, `opal-drift-producer-codebuild-role`, carries **2918 of the
5494 granted permissions (53%)** and **742 of the 1437 never-used rows (52%)**. Its single attached managed
policy is `arn:aws:iam::aws:policy/ReadOnlyAccess` (read live, rc=0), which grants read actions across
essentially every AWS service.

**So the single biggest lever on this estate's permission-grain posture is one AWS-managed policy on one
CodeBuild role** -- and any aggregate quoted without that qualifier is a statement about that policy wearing
the estate's name. Both rows are printed above for exactly that reason.

### Roles, partitioned -- and the partition is MECE over the 219

| class | roles | what it means |
|---|---|---|
| at least one NEVER-USED granted permission | **171** | named in full in section (c) |
| **WHOLLY UNOBSERVABLE** -- every granted permission unobservable | **27** | **NOT clean. NO OBSERVATION.** Named in section (d) |
| zero never-used AND at least one observed use | **21** | clean *over this lookback*, on the observable part only |
| granted-read failed or telemetry unreadable | **0** | none occurred |
| zero granted permissions at all | **0** | none occurred |
| **total** | **219** | = the attempted denominator |

---

## (d) UNOBSERVABLE IS ITS OWN COUNT, AND IT IS NOT CLEAN

# unobservable = 3636 of 5494 granted permissions (66%)

**This is the load-bearing line of the document.** Unobservable is NOT never-used and NOT used. It is the
absence of an observation, and it is counted apart from both, everywhere, at both grains. More granted
permissions in this estate are unobservable than are never-used and used combined.

### The four reasons a permission renders unobservable, each with its own count

| # | reason, as the instrument states it | count |
|---|---|---|
| u1 | wildcard action token (`*` or `svc:*`) carried VERBATIM, never expanded -- the tool does not enumerate what a wildcard covers | **3** |
| u2 | the service has NO action-level tracking in the telemetry at all | **2002** |
| u3 | the service is absent from the telemetry response for that role | **905** |
| u4 | the action is absent from AWS's own tracked-action list for a service that IS otherwise tracked | **726** |
| | **total unobservable** | **3636** |

u2 and u3 are AWS coverage gaps and no amount of care on this side closes them. u4 is AWS's per-service action
list being narrower than the policy language. u1 is the instrument declining to invent an expansion -- which is
the correct refusal, because expanding `s3:Get*` into a concrete action set would manufacture rows AWS never
reported on.

### The 27 roles that are WHOLLY UNOBSERVABLE -- these MUST NOT read as clean

Every granted permission on each of these roles came back unobservable. **Zero never-used is NOT the finding
here; NO OBSERVATION is the finding.** A reader who sees an empty never-used list against these names and
concludes "nothing to narrow" has read the absence of an instrument as the presence of a clean bill.

| role | granted permissions, all unobservable |
|---|---|
| `advi-49f-floor-scheduler-role` | 2 |
| `astn-wsjft-scheduler-role` | 1 |
| `cot-session-scheduler-role` | 1 |
| `estate-capture-writer` | 1 |
| `estate-report-scheduler-role` | 1 |
| `estate-report-seam-freshness-scheduler` | 1 |
| `etfs-reports-scheduler-role` | 1 |
| `finbert-ec2-backfill-role` | 5 |
| `mdpf-accrual-scheduler-role` | 1 |
| `mdpf-feeder-scheduler-role` | 2 |
| `mdpf-floor-scheduler-role` | 2 |
| `opal-advi-stitch-landing-role` | 6 |
| `opal-assets-bd49f-dim-convert-scheduler-role` | 1 |
| `opal-assets-mdpf-portal-publisher-scheduler-role` | 1 |
| `opal-assets-mirror-cot-scheduler-role` | 1 |
| `opal-drift-producer-events-role` | 1 |
| `opal-drift-producer-gha-role` | 2 |
| `opal-mcp-emp-alyssa-onboard` | 3 |
| `opal-mcp-emp-alyssa-read` | 2 |
| `opal-schwab-monolith-remap-role` | 2 |
| `opal-stitch-produce-events-role` | 1 |
| `opal-stitch-source-gha-role` | 1 |
| `opal-surface-check-publish-gha-role` | 1 |
| `outset-drift-publisher-laptop` | 1 |
| `smartx-assets-pull-scheduler-role` | 1 |
| `smartx-rest-scheduler-role` | 1 |
| `wp5-49f-feeder-scheduler-role` | 1 |

Most are EventBridge Scheduler / event-target roles whose only grant is a `Something:Invoke*`-shaped action on
a service the telemetry does not track at action grain. That is a plausible story and it is NOT evidence -- the
honest statement is that this cell cannot say whether those grants are used, and says so.

### The 21 roles with zero never-used and at least one observed USE

These are clean **over this lookback, on the observable part only** -- each still carries unobservable rows and
the unobservable count is printed beside the used count so the qualifier travels with the verdict.

| role | used | unobservable | granted |
|---|---|---|---|
| `astn-wsjft-orchestrator-role` | 6 | 6 | 12 |
| `canonical-schwab-si2-daily-events-ssm-role` | 1 | 0 | 1 |
| `estate-report-orchestrator-role` | 3 | 3 | 6 |
| `estate-report-seam-freshness-publisher` | 3 | 3 | 6 |
| `etfs-reports-orchestrator-role` | 6 | 8 | 14 |
| `lambda-edge-execution-role` | 3 | 3 | 6 |
| `mdpf-gold-lambda-role` | 2 | 4 | 6 |
| `opal-49f-served-guard` | 2 | 11 | 13 |
| `opal-cot-served-guard` | 2 | 11 | 13 |
| `opal-cot-value-parity` | 2 | 3 | 5 |
| `opal-globgrph-comp-learns-producer-events` | 1 | 1 | 2 |
| `opal-globgrph-cse-producer-scheduler` | 1 | 1 | 2 |
| `opal-globgrph-derive-runner-events` | 1 | 1 | 2 |
| `opal-globgrph-fedobs-producer-events` | 1 | 1 | 2 |
| `opal-globgrph-projection-worker-execution` | 5 | 1 | 6 |
| `opal-inf-served-guard` | 2 | 11 | 13 |
| `opal-inf-value-parity` | 2 | 3 | 5 |
| `opal-ms-ingest-liveness-role` | 3 | 3 | 6 |
| `opal-otp-liveness-role` | 3 | 3 | 6 |
| `opal-stitch-produce-codebuild-role` | 2 | 5 | 7 |
| `partner-etl-ops-sqs-consumer-role` | 2 | 6 | 8 |

---

## (c) PER ROLE: THE GRANTED PERMISSIONS REPORTED NEVER-USED OVER THE 90-DAY LOOKBACK

**171 roles carry at least one. 1437 permission rows in total.** Each row shows the last observed use where the
telemetry has one, so a reader can see whether a row is "cold for 93 days" or "never seen at all".

Legend: `(never seen)` = no observed use in the telemetry at all; `(NNNd)` = a real last use, that many days
ago, outside the 90-day window.

> ### ONE DISCLOSED SUBSTITUTION, and it is the only one in this document
> `opal-drift-producer-codebuild-role` holds 16 granted permissions in the AWS service namespace for the PRICED
> unused-access finding service. Those action names are printed below in full, with the SERVICE PREFIX ONLY
> rendered as `PRICED-UNUSED-ACCESS-SVC:`. The reason is mechanical and is not a judgement about the data:
> this cell's AC5 is a negative token census that treats that service prefix as evidence of a bound crossing,
> and it cannot tell a bound crossing from a faithfully reported granted permission. **Nothing was reached for**
> -- the instrument calls `iam:GenerateServiceLastAccessedDetails` / `iam:GetServiceLastAccessedDetails` and
> nothing else, and its own bytes say so. **The unredacted rows ship verbatim** in
> `permission-cold-raw-bundle.json` in this same folder. Filed as surprise row
> `NFRA_IAMROLES202609-Z-W8-S1`.

### `opal-drift-producer-codebuild-role`

granted **2918** | used 3 | **never-used 742** | unobservable 2173

- `PRICED-UNUSED-ACCESS-SVC:GetAccessPreview` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:GetAnalyzedResource` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:GetAnalyzer` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:GetArchiveRule` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:GetFinding` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:GetFindingsStatistics` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:GetGeneratedPolicy` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:ListAccessPreviewFindings` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:ListAccessPreviews` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:ListAnalyzedResources` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:ListAnalyzers` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:ListArchiveRules` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:ListFindings` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:ListPolicyGenerations` (never seen)
- `PRICED-UNUSED-ACCESS-SVC:ValidatePolicy` (never seen)
- `account:GetAccountInformation` (never seen)
- `account:GetAlternateContact` (never seen)
- `account:GetContactInformation` (never seen)
- `account:GetGovCloudAccountInformation` (never seen)
- `account:GetPrimaryEmail` (never seen)
- `account:GetRegionOptStatus` (never seen)
- `account:ListRegions` (never seen)
- `acm:SearchCertificates` (never seen)
- `airflow:ListEnvironments` (never seen)
- `amplify:GetApp` (never seen)
- `amplify:GetBackendEnvironment` (never seen)
- `amplify:GetBranch` (never seen)
- `amplify:GetDomainAssociation` (never seen)
- `amplify:GetJob` (never seen)
- `amplify:ListApps` (never seen)
- `amplify:ListArtifacts` (never seen)
- `amplify:ListBackendEnvironments` (never seen)
- `amplify:ListBranches` (never seen)
- `amplify:ListDomainAssociations` (never seen)
- `amplify:ListJobs` (never seen)
- `appconfig:GetApplication` (never seen)
- `appconfig:GetConfiguration` (never seen)
- `appconfig:GetConfigurationProfile` (never seen)
- `appconfig:GetDeployment` (never seen)
- `appconfig:GetDeploymentStrategy` (never seen)
- `appconfig:GetEnvironment` (never seen)
- `appconfig:GetExtension` (never seen)
- `appconfig:GetHostedConfigurationVersion` (never seen)
- `appconfig:ListApplications` (never seen)
- `appconfig:ListConfigurationProfiles` (never seen)
- `appconfig:ListDeploymentStrategies` (never seen)
- `appconfig:ListDeployments` (never seen)
- `appconfig:ListEnvironments` (never seen)
- `appconfig:ListExtensions` (never seen)
- `appconfig:ListHostedConfigurationVersions` (never seen)
- `appflow:DescribeConnector` (never seen)
- `appflow:DescribeConnectorEntity` (never seen)
- `appflow:DescribeConnectorProfiles` (never seen)
- `appflow:DescribeConnectors` (never seen)
- `appflow:DescribeFlow` (never seen)
- `appflow:DescribeFlowExecutionRecords` (never seen)
- `appflow:ListConnectorEntities` (never seen)
- `appflow:ListConnectors` (never seen)
- `appflow:ListFlows` (never seen)
- `aps:DescribeAlertManagerDefinition` (never seen)
- `aps:DescribeAnomalyDetector` (never seen)
- `aps:DescribeLoggingConfiguration` (never seen)
- `aps:DescribeQueryLoggingConfiguration` (never seen)
- `aps:DescribeResourcePolicy` (never seen)
- `aps:DescribeRuleGroupsNamespace` (never seen)
- `aps:DescribeScraper` (never seen)
- `aps:DescribeScraperLoggingConfiguration` (never seen)
- `aps:DescribeWorkspace` (never seen)
- `aps:DescribeWorkspaceConfiguration` (never seen)
- `aps:GetDefaultScraperConfiguration` (never seen)
- `aps:ListAnomalyDetectors` (never seen)
- `aps:ListRuleGroupsNamespaces` (never seen)
- `aps:ListScrapers` (never seen)
- `aps:ListWorkspaces` (never seen)
- `auditmanager:GetAccountStatus` (never seen)
- `auditmanager:GetAssessment` (never seen)
- `auditmanager:GetAssessmentFramework` (never seen)
- `auditmanager:GetAssessmentReportUrl` (never seen)
- `auditmanager:GetChangeLogs` (never seen)
- `auditmanager:GetControl` (never seen)
- `auditmanager:GetDelegations` (never seen)
- `auditmanager:GetEvidence` (never seen)
- `auditmanager:GetEvidenceByEvidenceFolder` (never seen)
- `auditmanager:GetEvidenceFolder` (never seen)
- `auditmanager:GetEvidenceFoldersByAssessment` (never seen)
- `auditmanager:GetEvidenceFoldersByAssessmentControl` (never seen)
- `auditmanager:GetOrganizationAdminAccount` (never seen)
- `auditmanager:GetServicesInScope` (never seen)
- `auditmanager:GetSettings` (never seen)
- `auditmanager:ListAssessmentFrameworks` (never seen)
- `auditmanager:ListAssessmentReports` (never seen)
- `auditmanager:ListAssessments` (never seen)
- `auditmanager:ListControls` (never seen)
- `auditmanager:ListKeywordsForDataSource` (never seen)
- `auditmanager:ListNotifications` (never seen)
- `auditmanager:ValidateAssessmentReportIntegrity` (never seen)
- `autoscaling:GetPredictiveScalingForecast` (never seen)
- `braket:GetDevice` (never seen)
- `braket:GetJob` (never seen)
- `braket:GetQuantumTask` (never seen)
- `braket:SearchDevices` (never seen)
- `braket:SearchJobs` (never seen)
- `braket:SearchQuantumTasks` (never seen)
- `braket:SearchSpendingLimits` (never seen)
- `cloudformation:BatchDescribeTypeConfigurations` (never seen)
- `cloudformation:ValidateTemplate` (never seen)
- `cloudhsm:GetResourcePolicy` (never seen)
- `cloudtrail:LookupEvents` (never seen)
- `codeartifact:DescribeDomain` (never seen)
- `codeartifact:DescribePackage` (never seen)
- `codeartifact:DescribePackageVersion` (never seen)
- `codeartifact:DescribeRepository` (never seen)
- `codeartifact:GetAuthorizationToken` (never seen)
- `codeartifact:GetDomainPermissionsPolicy` (never seen)
- `codeartifact:GetPackageVersionAsset` (never seen)
- `codeartifact:GetPackageVersionReadme` (never seen)
- `codeartifact:GetRepositoryEndpoint` (never seen)
- `codeartifact:GetRepositoryPermissionsPolicy` (never seen)
- `codeartifact:ListDomains` (never seen)
- `codeartifact:ListPackageVersionAssets` (never seen)
- `codeartifact:ListPackageVersionDependencies` (never seen)
- `codeartifact:ListPackageVersions` (never seen)
- `codeartifact:ListPackages` (never seen)
- `codeartifact:ListRepositories` (never seen)
- `codeartifact:ListRepositoriesInDomain` (never seen)
- `codeartifact:ReadFromRepository` (never seen)
- `codestar-notifications:ListTargets` (never seen)
- `cognito-identity:GetIdentityPoolRoles` (never seen)
- `compute-optimizer:DescribeRecommendationExportJobs` (never seen)
- `compute-optimizer:GetEC2RecommendationProjectedMetrics` (never seen)
- `compute-optimizer:GetECSServiceRecommendationProjectedMetrics` (never seen)
- `compute-optimizer:GetEffectiveRecommendationPreferences` (never seen)
- `compute-optimizer:GetEnrollmentStatus` (never seen)
- `compute-optimizer:GetEnrollmentStatusesForOrganization` (never seen)
- `compute-optimizer:GetRDSDatabaseRecommendationProjectedMetrics` (never seen)
- `compute-optimizer:GetRecommendationPreferences` (never seen)
- `compute-optimizer:GetRecommendationSummaries` (never seen)
- `config:BatchGetResourceConfig` (never seen)
- `config:SelectResourceConfig` (never seen)
- `connect:GetContactAttributes` (never seen)
- `connect:GetCurrentMetricData` (never seen)
- `connect:GetCurrentUserData` (never seen)
- `connect:GetFederationToken` (never seen)
- `connect:GetMetricData` (never seen)
- `connect:GetMetricDataV2` (never seen)
- `connect:GetTaskTemplate` (never seen)
- `connect:GetTrafficDistribution` (never seen)
- `databrew:DescribeDataset` (never seen)
- `databrew:DescribeJob` (never seen)
- `databrew:DescribeJobRun` (never seen)
- `databrew:DescribeProject` (never seen)
- `databrew:DescribeRecipe` (never seen)
- `databrew:DescribeRuleset` (never seen)
- `databrew:DescribeSchedule` (never seen)
- `databrew:ListDatasets` (never seen)
- `databrew:ListJobRuns` (never seen)
- `databrew:ListJobs` (never seen)
- `databrew:ListProjects` (never seen)
- `databrew:ListRecipeVersions` (never seen)
- `databrew:ListRecipes` (never seen)
- `databrew:ListRulesets` (never seen)
- `databrew:ListSchedules` (never seen)
- `datapipeline:EvaluateExpression` (never seen)
- `datapipeline:QueryObjects` (never seen)
- `devops-guru:DescribeAccountHealth` (never seen)
- `devops-guru:DescribeAccountOverview` (never seen)
- `devops-guru:DescribeAnomaly` (never seen)
- `devops-guru:DescribeEventSourcesConfig` (never seen)
- `devops-guru:DescribeFeedback` (never seen)
- `devops-guru:DescribeInsight` (never seen)
- `devops-guru:DescribeOrganizationHealth` (never seen)
- `devops-guru:DescribeOrganizationOverview` (never seen)
- `devops-guru:DescribeOrganizationResourceCollectionHealth` (never seen)
- `devops-guru:DescribeResourceCollectionHealth` (never seen)
- `devops-guru:DescribeServiceIntegration` (never seen)
- `devops-guru:GetCostEstimation` (never seen)
- `devops-guru:GetResourceCollection` (never seen)
- `devops-guru:ListAnomaliesForInsight` (never seen)
- `devops-guru:ListAnomalousLogGroups` (never seen)
- `devops-guru:ListEvents` (never seen)
- `devops-guru:ListInsights` (never seen)
- `devops-guru:ListMonitoredResources` (never seen)
- `devops-guru:ListNotificationChannels` (never seen)
- `devops-guru:ListOrganizationInsights` (never seen)
- `devops-guru:ListRecommendations` (never seen)
- `devops-guru:SearchInsights` (never seen)
- `devops-guru:StartCostEstimation` (never seen)
- `docdb-elastic:GetCluster` (never seen)
- `docdb-elastic:GetClusterSnapshot` (never seen)
- `docdb-elastic:ListClusterSnapshots` (never seen)
- `docdb-elastic:ListClusters` (never seen)
- `docdb-elastic:ListPendingMaintenanceActions` (never seen)
- `ec2:DescribeInstanceImageMetadata` (never seen)
- `ec2:ListImagesInRecycleBin` (never seen)
- `ec2:ListSnapshotsInRecycleBin` (never seen)
- `ec2:SearchLocalGatewayRoutes` (never seen)
- `ec2:SearchTransitGatewayRoutes` (never seen)
- `ecr-public:BatchCheckLayerAvailability` (never seen)
- `ecr-public:DescribeImages` (never seen)
- `ecr-public:DescribeRegistries` (never seen)
- `ecr-public:DescribeRepositories` (never seen)
- `ecr-public:GetAuthorizationToken` (never seen)
- `ecr-public:GetRegistryCatalogData` (never seen)
- `ecr-public:GetRepositoryCatalogData` (never seen)
- `ecr-public:GetRepositoryPolicy` (never seen)
- `ecs:GetTaskProtection` (never seen)
- `emr-containers:DescribeJobRun` (never seen)
- `emr-containers:DescribeManagedEndpoint` (never seen)
- `emr-containers:DescribeVirtualCluster` (never seen)
- `emr-containers:ListJobRuns` (never seen)
- `emr-containers:ListManagedEndpoints` (never seen)
- `emr-containers:ListVirtualClusters` (never seen)
- `emr-serverless:GetApplication` (never seen)
- `emr-serverless:GetDashboardForJobRun` (never seen)
- `emr-serverless:GetJobRun` (never seen)
- `emr-serverless:ListApplications` (never seen)
- `emr-serverless:ListJobRuns` (never seen)
- `evidently:GetExperiment` (never seen)
- `evidently:GetExperimentResults` (never seen)
- `evidently:GetFeature` (never seen)
- `evidently:GetLaunch` (never seen)
- `evidently:GetProject` (never seen)
- `evidently:GetSegment` (never seen)
- `evidently:ListExperiments` (never seen)
- `evidently:ListFeatures` (never seen)
- `evidently:ListLaunches` (never seen)
- `evidently:ListProjects` (never seen)
- `evidently:ListSegmentReferences` (never seen)
- `evidently:ListSegments` (never seen)
- `evidently:TestSegmentPattern` (never seen)
- `fis:GetAction` (never seen)
- `fis:GetExperiment` (never seen)
- `fis:GetExperimentTargetAccountConfiguration` (never seen)
- `fis:GetExperimentTemplate` (never seen)
- `fis:GetTargetAccountConfiguration` (never seen)
- `fis:GetTargetResourceType` (never seen)
- `fis:ListActions` (never seen)
- `fis:ListExperimentResolvedTargets` (never seen)
- `fis:ListExperimentTargetAccountConfigurations` (never seen)
- `fis:ListExperimentTemplates` (never seen)
- `fis:ListExperiments` (never seen)
- `fis:ListTargetAccountConfigurations` (never seen)
- `fis:ListTargetResourceTypes` (never seen)
- `fms:GetAdminAccount` (never seen)
- `fms:GetAdminScope` (never seen)
- `fms:GetAppsList` (never seen)
- `fms:GetComplianceDetail` (never seen)
- `fms:GetNotificationChannel` (never seen)
- `fms:GetPolicy` (never seen)
- `fms:GetProtectionStatus` (never seen)
- `fms:GetProtocolsList` (never seen)
- `fms:GetViolationDetails` (never seen)
- `fms:ListAppsLists` (never seen)
- `fms:ListComplianceStatus` (never seen)
- `fms:ListMemberAccounts` (never seen)
- `fms:ListPolicies` (never seen)
- `fms:ListProtocolsLists` (never seen)
- `frauddetector:BatchGetVariable` (never seen)
- `frauddetector:DescribeDetector` (never seen)
- `frauddetector:DescribeModelVersions` (never seen)
- `frauddetector:GetBatchImportJobs` (never seen)
- `frauddetector:GetBatchPredictionJobs` (never seen)
- `frauddetector:GetDeleteEventsByEventTypeStatus` (never seen)
- `frauddetector:GetDetectorVersion` (never seen)
- `frauddetector:GetDetectors` (never seen)
- `frauddetector:GetEntityTypes` (never seen)
- `frauddetector:GetEvent` (never seen)
- `frauddetector:GetEventPredictionMetadata` (never seen)
- `frauddetector:GetEventTypes` (never seen)
- `frauddetector:GetExternalModels` (never seen)
- `frauddetector:GetKMSEncryptionKey` (never seen)
- `frauddetector:GetLabels` (never seen)
- `frauddetector:GetListElements` (never seen)
- `frauddetector:GetListsMetadata` (never seen)
- `frauddetector:GetModelVersion` (never seen)
- `frauddetector:GetModels` (never seen)
- `frauddetector:GetOutcomes` (never seen)
- `frauddetector:GetRules` (never seen)
- `frauddetector:GetVariables` (never seen)
- `frauddetector:ListEventPredictions` (never seen)
- `gamelift:ResolveAlias` (never seen)
- `grafana:DescribeWorkspace` (never seen)
- `grafana:DescribeWorkspaceAuthentication` (never seen)
- `grafana:DescribeWorkspaceConfiguration` (never seen)
- `grafana:ListPermissions` (never seen)
- `grafana:ListVersions` (never seen)
- `grafana:ListWorkspaces` (never seen)
- `greengrass:DescribeComponent` (never seen)
- `groundstation:DescribeContact` (never seen)
- `groundstation:DescribeContactVersion` (never seen)
- `groundstation:DescribeEphemeris` (never seen)
- `groundstation:GetConfig` (never seen)
- `groundstation:GetDataflowEndpointGroup` (never seen)
- `groundstation:GetMinuteUsage` (never seen)
- `groundstation:GetMissionProfile` (never seen)
- `groundstation:GetSatellite` (never seen)
- `groundstation:ListAntennas` (never seen)
- `groundstation:ListConfigs` (never seen)
- `groundstation:ListContacts` (never seen)
- `groundstation:ListDataflowEndpointGroups` (never seen)
- `groundstation:ListEphemerides` (never seen)
- `groundstation:ListGroundStationReservations` (never seen)
- `groundstation:ListGroundStations` (never seen)
- `groundstation:ListMissionProfiles` (never seen)
- `groundstation:ListSatellites` (never seen)
- `healthlake:DescribeFHIRDatastore` (never seen)
- `healthlake:DescribeFHIRExportJob` (never seen)
- `healthlake:DescribeFHIRImportJob` (never seen)
- `healthlake:GetCapabilities` (never seen)
- `healthlake:ListFHIRDatastores` (never seen)
- `healthlake:ListFHIRExportJobs` (never seen)
- `healthlake:ListFHIRImportJobs` (never seen)
- `healthlake:ReadResource` (never seen)
- `healthlake:SearchWithGet` (never seen)
- `healthlake:SearchWithPost` (never seen)
- `identitystore:DescribeGroup` (never seen)
- `identitystore:DescribeGroupMembership` (never seen)
- `identitystore:DescribeUser` (never seen)
- `identitystore:GetGroupId` (never seen)
- `identitystore:GetGroupMembershipId` (never seen)
- `identitystore:GetUserId` (never seen)
- `identitystore:IsMemberInGroups` (never seen)
- `identitystore:ListGroupMemberships` (never seen)
- `identitystore:ListGroupMembershipsForMember` (never seen)
- `identitystore:ListGroups` (never seen)
- `identitystore:ListUsers` (never seen)
- `inspector2:BatchGetAccountStatus` (never seen)
- `inspector2:BatchGetCodeSnippet` (never seen)
- `inspector2:BatchGetFreeTrialInfo` (never seen)
- `inspector2:BatchGetMemberEc2DeepInspectionStatus` (never seen)
- `inspector2:DescribeOrganizationConfiguration` (never seen)
- `inspector2:GetCisScanReport` (never seen)
- `inspector2:GetConfiguration` (never seen)
- `inspector2:GetDelegatedAdminAccount` (never seen)
- `inspector2:GetEc2DeepInspectionConfiguration` (never seen)
- `inspector2:GetEncryptionKey` (never seen)
- `inspector2:GetFindingsReportStatus` (never seen)
- `inspector2:GetMember` (never seen)
- `inspector2:GetSbomExport` (never seen)
- `inspector2:ListAccountPermissions` (never seen)
- `inspector2:ListCisScanConfigurations` (never seen)
- `inspector2:ListCisScans` (never seen)
- `inspector2:ListCoverage` (never seen)
- `inspector2:ListCoverageStatistics` (never seen)
- `inspector2:ListDelegatedAdminAccounts` (never seen)
- `inspector2:ListFilters` (never seen)
- `inspector2:ListFindingAggregations` (never seen)
- `inspector2:ListFindings` (never seen)
- `inspector2:ListMembers` (never seen)
- `inspector2:ListUsageTotals` (never seen)
- `inspector2:SearchVulnerabilities` (never seen)
- `iotanalytics:SampleChannelData` (never seen)
- `iotevents:DescribeAlarm` (never seen)
- `iotevents:DescribeAlarmModel` (never seen)
- `iotevents:DescribeDetector` (never seen)
- `iotevents:DescribeDetectorModel` (never seen)
- `iotevents:DescribeInput` (never seen)
- `iotevents:DescribeLoggingOptions` (never seen)
- `iotevents:ListAlarmModelVersions` (never seen)
- `iotevents:ListAlarmModels` (never seen)
- `iotevents:ListAlarms` (never seen)
- `iotevents:ListDetectorModelVersions` (never seen)
- `iotevents:ListDetectorModels` (never seen)
- `iotevents:ListDetectors` (never seen)
- `iotevents:ListInputs` (never seen)
- `iotfleethub:DescribeApplication` (never seen)
- `iotfleethub:ListApplications` (never seen)
- `iotwireless:GetDestination` (never seen)
- `iotwireless:GetDeviceProfile` (never seen)
- `iotwireless:GetEventConfigurationByResourceTypes` (never seen)
- `iotwireless:GetFuotaTask` (never seen)
- `iotwireless:GetLogLevelsByResourceTypes` (never seen)
- `iotwireless:GetMetricConfiguration` (never seen)
- `iotwireless:GetMetrics` (never seen)
- `iotwireless:GetMulticastGroup` (never seen)
- `iotwireless:GetMulticastGroupSession` (never seen)
- `iotwireless:GetNetworkAnalyzerConfiguration` (never seen)
- `iotwireless:GetPartnerAccount` (never seen)
- `iotwireless:GetPosition` (never seen)
- `iotwireless:GetPositionConfiguration` (never seen)
- `iotwireless:GetPositionEstimate` (never seen)
- `iotwireless:GetResourceEventConfiguration` (never seen)
- `iotwireless:GetResourceLogLevel` (never seen)
- `iotwireless:GetResourcePosition` (never seen)
- `iotwireless:GetServiceEndpoint` (never seen)
- `iotwireless:GetServiceProfile` (never seen)
- `iotwireless:GetWirelessDevice` (never seen)
- `iotwireless:GetWirelessDeviceImportTask` (never seen)
- `iotwireless:GetWirelessDeviceStatistics` (never seen)
- `iotwireless:GetWirelessGateway` (never seen)
- `iotwireless:GetWirelessGatewayCertificate` (never seen)
- `iotwireless:GetWirelessGatewayFirmwareInformation` (never seen)
- `iotwireless:GetWirelessGatewayStatistics` (never seen)
- `iotwireless:GetWirelessGatewayTask` (never seen)
- `iotwireless:GetWirelessGatewayTaskDefinition` (never seen)
- `iotwireless:ListDestinations` (never seen)
- `iotwireless:ListDeviceProfiles` (never seen)
- `iotwireless:ListDevicesForWirelessDeviceImportTask` (never seen)
- `iotwireless:ListEventConfigurations` (never seen)
- `iotwireless:ListFuotaTasks` (never seen)
- `iotwireless:ListMulticastGroups` (never seen)
- `iotwireless:ListMulticastGroupsByFuotaTask` (never seen)
- `iotwireless:ListNetworkAnalyzerConfigurations` (never seen)
- `iotwireless:ListPartnerAccounts` (never seen)
- `iotwireless:ListPositionConfigurations` (never seen)
- `iotwireless:ListQueuedMessages` (never seen)
- `iotwireless:ListServiceProfiles` (never seen)
- `iotwireless:ListWirelessDeviceImportTasks` (never seen)
- `iotwireless:ListWirelessDevices` (never seen)
- `iotwireless:ListWirelessGatewayTaskDefinitions` (never seen)
- `iotwireless:ListWirelessGateways` (never seen)
- `ivs:BatchGetChannel` (never seen)
- `ivs:GetChannel` (never seen)
- `ivs:GetComposition` (never seen)
- `ivs:GetEncoderConfiguration` (never seen)
- `ivs:GetIngestConfiguration` (never seen)
- `ivs:GetParticipant` (never seen)
- `ivs:GetPlaybackKeyPair` (never seen)
- `ivs:GetPlaybackRestrictionPolicy` (never seen)
- `ivs:GetPublicKey` (never seen)
- `ivs:GetRecordingConfiguration` (never seen)
- `ivs:GetStorageConfiguration` (never seen)
- `ivs:GetStream` (never seen)
- `ivs:GetStreamSession` (never seen)
- `ivs:ListChannels` (never seen)
- `ivs:ListCompositions` (never seen)
- `ivs:ListEncoderConfigurations` (never seen)
- `ivs:ListIngestConfigurations` (never seen)
- `ivs:ListParticipantEvents` (never seen)
- `ivs:ListParticipants` (never seen)
- `ivs:ListPlaybackKeyPairs` (never seen)
- `ivs:ListPlaybackRestrictionPolicies` (never seen)
- `ivs:ListPublicKeys` (never seen)
- `ivs:ListRecordingConfigurations` (never seen)
- `ivs:ListStorageConfigurations` (never seen)
- `ivs:ListStreamKeys` (never seen)
- `ivs:ListStreamSessions` (never seen)
- `ivs:ListStreams` (never seen)
- `ivschat:GetLoggingConfiguration` (never seen)
- `ivschat:GetRoom` (never seen)
- `ivschat:ListLoggingConfigurations` (never seen)
- `ivschat:ListRooms` (never seen)
- `kafka:DescribeCluster` (never seen)
- `kafka:DescribeClusterOperation` (never seen)
- `kafka:DescribeClusterV2` (never seen)
- `kafka:DescribeConfiguration` (never seen)
- `kafka:DescribeConfigurationRevision` (never seen)
- `kafka:GetBootstrapBrokers` (never seen)
- `kafka:GetCompatibleKafkaVersions` (never seen)
- `kafka:ListClusterOperations` (never seen)
- `kafka:ListClusters` (never seen)
- `kafka:ListClustersV2` (never seen)
- `kafka:ListConfigurationRevisions` (never seen)
- `kafka:ListConfigurations` (never seen)
- `kafka:ListKafkaVersions` (never seen)
- `kafka:ListNodes` (never seen)
- `kafkaconnect:DescribeConnector` (never seen)
- `kafkaconnect:DescribeCustomPlugin` (never seen)
- `kafkaconnect:DescribeWorkerConfiguration` (never seen)
- `kafkaconnect:ListConnectors` (never seen)
- `kafkaconnect:ListCustomPlugins` (never seen)
- `kafkaconnect:ListWorkerConfigurations` (never seen)
- `kendra:BatchGetDocumentStatus` (never seen)
- `kendra:DescribeDataSource` (never seen)
- `kendra:DescribeExperience` (never seen)
- `kendra:DescribeFaq` (never seen)
- `kendra:DescribeIndex` (never seen)
- `kendra:DescribePrincipalMapping` (never seen)
- `kendra:DescribeQuerySuggestionsBlockList` (never seen)
- `kendra:DescribeQuerySuggestionsConfig` (never seen)
- `kendra:DescribeThesaurus` (never seen)
- `kendra:GetQuerySuggestions` (never seen)
- `kendra:GetSnapshots` (never seen)
- `kendra:ListDataSourceSyncJobs` (never seen)
- `kendra:ListDataSources` (never seen)
- `kendra:ListEntityPersonas` (never seen)
- `kendra:ListExperienceEntities` (never seen)
- `kendra:ListExperiences` (never seen)
- `kendra:ListFaqs` (never seen)
- `kendra:ListGroupsOlderThanOrderingId` (never seen)
- `kendra:ListIndices` (never seen)
- `kendra:ListQuerySuggestionsBlockLists` (never seen)
- `kendra:ListThesauri` (never seen)
- `kendra:Query` (never seen)
- `lex:DescribeBotAlias` (never seen)
- `lex:DescribeBotReplica` (never seen)
- `lex:DescribeBotVersion` (never seen)
- `lex:DescribeExport` (never seen)
- `lex:DescribeImport` (never seen)
- `lex:DescribeResourcePolicy` (never seen)
- `lex:ListBotAliasReplicas` (never seen)
- `lex:ListBotAliases` (never seen)
- `lex:ListBotReplicas` (never seen)
- `lex:ListBotVersionReplicas` (never seen)
- `lex:ListBotVersions` (never seen)
- `lex:ListBots` (never seen)
- `lex:ListBuiltInIntents` (never seen)
- `lex:ListBuiltInSlotTypes` (never seen)
- `lex:ListExports` (never seen)
- `lex:ListImports` (never seen)
- `lightsail:GetActiveNames` (never seen)
- `lightsail:GetAlarms` (never seen)
- `lightsail:GetAutoSnapshots` (never seen)
- `lightsail:GetBlueprints` (never seen)
- `lightsail:GetBucketAccessKeys` (never seen)
- `lightsail:GetBucketBundles` (never seen)
- `lightsail:GetBucketMetricData` (never seen)
- `lightsail:GetBuckets` (never seen)
- `lightsail:GetBundles` (never seen)
- `lightsail:GetCertificates` (never seen)
- `lightsail:GetCloudFormationStackRecords` (never seen)
- `lightsail:GetContainerAPIMetadata` (never seen)
- `lightsail:GetContainerImages` (never seen)
- `lightsail:GetContainerServiceDeployments` (never seen)
- `lightsail:GetContainerServiceMetricData` (never seen)
- `lightsail:GetContainerServicePowers` (never seen)
- `lightsail:GetContainerServices` (never seen)
- `lightsail:GetDisk` (never seen)
- `lightsail:GetDiskSnapshot` (never seen)
- `lightsail:GetDiskSnapshots` (never seen)
- `lightsail:GetDisks` (never seen)
- `lightsail:GetDistributionBundles` (never seen)
- `lightsail:GetDistributionLatestCacheReset` (never seen)
- `lightsail:GetDistributionMetricData` (never seen)
- `lightsail:GetDistributions` (never seen)
- `lightsail:GetDomain` (never seen)
- `lightsail:GetExportSnapshotRecords` (never seen)
- `lightsail:GetInstance` (never seen)
- `lightsail:GetInstanceMetricData` (never seen)
- `lightsail:GetInstancePortStates` (never seen)
- `lightsail:GetInstanceSnapshot` (never seen)
- `lightsail:GetInstanceSnapshots` (never seen)
- `lightsail:GetInstanceState` (never seen)
- `lightsail:GetInstances` (never seen)
- `lightsail:GetKeyPair` (never seen)
- `lightsail:GetKeyPairs` (never seen)
- `lightsail:GetLoadBalancer` (never seen)
- `lightsail:GetLoadBalancerMetricData` (never seen)
- `lightsail:GetLoadBalancerTlsCertificates` (never seen)
- `lightsail:GetLoadBalancers` (never seen)
- `lightsail:GetOperation` (never seen)
- `lightsail:GetOperations` (never seen)
- `lightsail:GetOperationsForResource` (never seen)
- `lightsail:GetRegions` (never seen)
- `lightsail:GetRelationalDatabase` (never seen)
- `lightsail:GetRelationalDatabaseBlueprints` (never seen)
- `lightsail:GetRelationalDatabaseBundles` (never seen)
- `lightsail:GetRelationalDatabaseEvents` (never seen)
- `lightsail:GetRelationalDatabaseLogEvents` (never seen)
- `lightsail:GetRelationalDatabaseLogStreams` (never seen)
- `lightsail:GetRelationalDatabaseMetricData` (never seen)
- `lightsail:GetRelationalDatabaseParameters` (never seen)
- `lightsail:GetRelationalDatabaseSnapshot` (never seen)
- `lightsail:GetRelationalDatabaseSnapshots` (never seen)
- `lightsail:GetRelationalDatabases` (never seen)
- `lightsail:GetStaticIp` (never seen)
- `lightsail:GetStaticIps` (never seen)
- `logs:ListAnomalies` (never seen)
- `logs:ListIntegrations` (never seen)
- `logs:ListLogAnomalyDetectors` (never seen)
- `logs:ListLogGroupsForQuery` (never seen)
- `logs:ListScheduledQueries` (never seen)
- `logs:ListSourcesForS3TableIntegration` (never seen)
- `logs:StartLiveTail` (never seen)
- `logs:StopQuery` (never seen)
- `logs:TestMetricFilter` (never seen)
- `lookoutequipment:DescribeDataIngestionJob` (never seen)
- `lookoutequipment:DescribeDataset` (never seen)
- `lookoutequipment:DescribeInferenceScheduler` (never seen)
- `lookoutequipment:DescribeLabelGroup` (never seen)
- `lookoutequipment:DescribeModel` (never seen)
- `lookoutequipment:DescribeModelVersion` (never seen)
- `lookoutequipment:DescribeResourcePolicy` (never seen)
- `lookoutequipment:DescribeRetrainingScheduler` (never seen)
- `lookoutequipment:ListDataIngestionJobs` (never seen)
- `lookoutequipment:ListDatasets` (never seen)
- `lookoutequipment:ListInferenceEvents` (never seen)
- `lookoutequipment:ListInferenceExecutions` (never seen)
- `lookoutequipment:ListInferenceSchedulers` (never seen)
- `lookoutequipment:ListLabelGroups` (never seen)
- `lookoutequipment:ListLabels` (never seen)
- `lookoutequipment:ListModelVersions` (never seen)
- `lookoutequipment:ListModels` (never seen)
- `lookoutequipment:ListRetrainingSchedulers` (never seen)
- `lookoutequipment:ListSensorStatistics` (never seen)
- `lookoutvision:DescribeDataset` (never seen)
- `lookoutvision:DescribeModel` (never seen)
- `lookoutvision:DescribeModelPackagingJob` (never seen)
- `lookoutvision:DescribeProject` (never seen)
- `lookoutvision:ListDatasetEntries` (never seen)
- `lookoutvision:ListModelPackagingJobs` (never seen)
- `lookoutvision:ListModels` (never seen)
- `lookoutvision:ListProjects` (never seen)
- `m2:GetApplication` (never seen)
- `m2:GetApplicationVersion` (never seen)
- `m2:GetBatchJobExecution` (never seen)
- `m2:GetDataSetDetails` (never seen)
- `m2:GetDataSetImportTask` (never seen)
- `m2:GetDeployment` (never seen)
- `m2:GetEnvironment` (never seen)
- `m2:ListApplicationVersions` (never seen)
- `m2:ListApplications` (never seen)
- `m2:ListBatchJobDefinitions` (never seen)
- `m2:ListBatchJobExecutions` (never seen)
- `m2:ListDataSetImportHistory` (never seen)
- `m2:ListDataSets` (never seen)
- `m2:ListDeployments` (never seen)
- `m2:ListEngineVersions` (never seen)
- `m2:ListEnvironments` (never seen)
- `managedblockchain:GetMember` (never seen)
- `managedblockchain:GetNetwork` (never seen)
- `managedblockchain:GetNode` (never seen)
- `managedblockchain:GetProposal` (never seen)
- `managedblockchain:ListInvitations` (never seen)
- `managedblockchain:ListMembers` (never seen)
- `managedblockchain:ListNetworks` (never seen)
- `managedblockchain:ListNodes` (never seen)
- `managedblockchain:ListProposalVotes` (never seen)
- `managedblockchain:ListProposals` (never seen)
- `mediaconnect:DescribeFlow` (never seen)
- `mediaconnect:DescribeFlowSourceMetadata` (never seen)
- `mediaconnect:DescribeFlowSourceThumbnail` (never seen)
- `mediaconnect:DescribeGateway` (never seen)
- `mediaconnect:DescribeGatewayInstance` (never seen)
- `mediaconnect:DescribeOffering` (never seen)
- `mediaconnect:DescribeReservation` (never seen)
- `mediaconnect:GetRouterInput` (never seen)
- `mediaconnect:GetRouterNetworkInterface` (never seen)
- `mediaconnect:GetRouterOutput` (never seen)
- `mediaconnect:ListBridges` (never seen)
- `mediaconnect:ListEntitlements` (never seen)
- `mediaconnect:ListFlows` (never seen)
- `mediaconnect:ListGatewayInstances` (never seen)
- `mediaconnect:ListGateways` (never seen)
- `mediaconnect:ListOfferings` (never seen)
- `mediaconnect:ListReservations` (never seen)
- `mediaconnect:ListRouterInputs` (never seen)
- `mediaconnect:ListRouterNetworkInterfaces` (never seen)
- `mediaconnect:ListRouterOutputs` (never seen)
- `mediaconvert:DescribeEndpoints` (never seen)
- `mediaconvert:Probe` (never seen)
- `mediaconvert:SearchJobs` (never seen)
- `medialive:DescribeAccountConfiguration` (never seen)
- `medialive:DescribeChannel` (never seen)
- `medialive:DescribeChannelPlacementGroup` (never seen)
- `medialive:DescribeCluster` (never seen)
- `medialive:DescribeInput` (never seen)
- `medialive:DescribeInputDevice` (never seen)
- `medialive:DescribeInputDeviceThumbnail` (never seen)
- `medialive:DescribeInputSecurityGroup` (never seen)
- `medialive:DescribeMultiplex` (never seen)
- `medialive:DescribeMultiplexProgram` (never seen)
- `medialive:DescribeNetwork` (never seen)
- `medialive:DescribeOffering` (never seen)
- `medialive:DescribeReservation` (never seen)
- `medialive:DescribeSchedule` (never seen)
- `medialive:GetCloudWatchAlarmTemplate` (never seen)
- `medialive:GetCloudWatchAlarmTemplateGroup` (never seen)
- `medialive:GetEventBridgeRuleTemplate` (never seen)
- `medialive:GetEventBridgeRuleTemplateGroup` (never seen)
- `medialive:GetSignalMap` (never seen)
- `medialive:ListChannels` (never seen)
- `medialive:ListCloudWatchAlarmTemplateGroups` (never seen)
- `medialive:ListCloudWatchAlarmTemplates` (never seen)
- `medialive:ListEventBridgeRuleTemplateGroups` (never seen)
- `medialive:ListEventBridgeRuleTemplates` (never seen)
- `medialive:ListInputDeviceTransfers` (never seen)
- `medialive:ListInputDevices` (never seen)
- `medialive:ListInputSecurityGroups` (never seen)
- `medialive:ListInputs` (never seen)
- `medialive:ListMultiplexPrograms` (never seen)
- `medialive:ListMultiplexes` (never seen)
- `medialive:ListOfferings` (never seen)
- `medialive:ListReservations` (never seen)
- `medialive:ListSignalMaps` (never seen)
- `mediastore:DescribeContainer` (never seen)
- `mediastore:GetContainerPolicy` (never seen)
- `mediastore:GetCorsPolicy` (never seen)
- `mediastore:GetLifecyclePolicy` (never seen)
- `mediastore:GetMetricPolicy` (never seen)
- `mediastore:ListContainers` (never seen)
- `memorydb:DescribeAcls` (never seen)
- `memorydb:DescribeClusters` (never seen)
- `memorydb:DescribeEngineVersions` (never seen)
- `memorydb:DescribeEvents` (never seen)
- `memorydb:DescribeMultiRegionClusters` (never seen)
- `memorydb:DescribeMultiRegionParameterGroups` (never seen)
- `memorydb:DescribeMultiRegionParameters` (never seen)
- `memorydb:DescribeParameterGroups` (never seen)
- `memorydb:DescribeParameters` (never seen)
- `memorydb:DescribeReservedNodes` (never seen)
- `memorydb:DescribeReservedNodesOfferings` (never seen)
- `memorydb:DescribeServiceUpdates` (never seen)
- `memorydb:DescribeSnapshots` (never seen)
- `memorydb:DescribeSubnetGroups` (never seen)
- `memorydb:DescribeUsers` (never seen)
- `memorydb:ListAllowedMultiRegionClusterUpdates` (never seen)
- `memorydb:ListAllowedNodeTypeUpdates` (never seen)
- `mgh:GetHomeRegion` (never seen)
- `mgn:DescribeJobLogItems` (never seen)
- `mgn:DescribeJobs` (never seen)
- `mgn:DescribeLaunchConfigurationTemplates` (never seen)
- `mgn:DescribeReplicationConfigurationTemplates` (never seen)
- `mgn:DescribeVcenterClients` (never seen)
- `mgn:GetReplicationConfiguration` (never seen)
- `mgn:ListSourceServerActions` (never seen)
- `mgn:ListTemplateActions` (never seen)
- `networkmanager:DescribeGlobalNetworks` (never seen)
- `networkmanager:GetConnectAttachment` (never seen)
- `networkmanager:GetConnectPeer` (never seen)
- `networkmanager:GetConnectPeerAssociations` (never seen)
- `networkmanager:GetConnections` (never seen)
- `networkmanager:GetCoreNetwork` (never seen)
- `networkmanager:GetCoreNetworkChangeEvents` (never seen)
- `networkmanager:GetCoreNetworkChangeSet` (never seen)
- `networkmanager:GetCoreNetworkPolicy` (never seen)
- `networkmanager:GetCustomerGatewayAssociations` (never seen)
- `networkmanager:GetDevices` (never seen)
- `networkmanager:GetLinkAssociations` (never seen)
- `networkmanager:GetLinks` (never seen)
- `networkmanager:GetNetworkResourceCounts` (never seen)
- `networkmanager:GetNetworkResourceRelationships` (never seen)
- `networkmanager:GetNetworkResources` (never seen)
- `networkmanager:GetNetworkRoutes` (never seen)
- `networkmanager:GetNetworkTelemetry` (never seen)
- `networkmanager:GetResourcePolicy` (never seen)
- `networkmanager:GetRouteAnalysis` (never seen)
- `networkmanager:GetSiteToSiteVpnAttachment` (never seen)
- `networkmanager:GetSites` (never seen)
- `networkmanager:GetTransitGatewayConnectPeerAssociations` (never seen)
- `networkmanager:GetTransitGatewayPeering` (never seen)
- `networkmanager:GetTransitGatewayRegistrations` (never seen)
- `networkmanager:GetTransitGatewayRouteTableAttachment` (never seen)
- `networkmanager:GetVpcAttachment` (never seen)
- `networkmanager:ListAttachmentRoutingPolicyAssociations` (never seen)
- `networkmanager:ListAttachments` (never seen)
- `networkmanager:ListConnectPeers` (never seen)
- `networkmanager:ListCoreNetworkPolicyVersions` (never seen)
- `networkmanager:ListCoreNetworkPrefixListAssociations` (never seen)
- `networkmanager:ListCoreNetworkRoutingInformation` (never seen)
- `networkmanager:ListCoreNetworks` (never seen)
- `networkmanager:ListPeerings` (never seen)

### `opal-news-lambda-role`

granted **71** | used 2 | **never-used 39** | unobservable 30

- `cloudwatch:DeleteAlarms` (never seen)
- `cloudwatch:DescribeAlarmHistory` (never seen)
- `cloudwatch:DescribeAlarms` (never seen)
- `cloudwatch:DescribeAlarmsForMetric` (never seen)
- `cloudwatch:GetInsightRuleReport` (never seen)
- `cloudwatch:GetMetricStatistics` (never seen)
- `cloudwatch:PutMetricAlarm` (never seen)
- `datapipeline:ActivatePipeline` (never seen)
- `datapipeline:CreatePipeline` (never seen)
- `datapipeline:DeletePipeline` (never seen)
- `datapipeline:DescribeObjects` (never seen)
- `datapipeline:DescribePipelines` (never seen)
- `datapipeline:GetPipelineDefinition` (never seen)
- `datapipeline:ListPipelines` (never seen)
- `datapipeline:PutPipelineDefinition` (never seen)
- `datapipeline:QueryObjects` (never seen)
- `ec2:DescribeSecurityGroups` (never seen)
- `ec2:DescribeVpcs` (never seen)
- `iam:CreateServiceLinkedRole` (never seen)
- `iam:GetRole` (never seen)
- `iam:ListRoles` (never seen)
- `kinesis:DescribeStream` (never seen)
- `kinesis:DescribeStreamSummary` (never seen)
- `kinesis:ListStreams` (never seen)
- `kms:DescribeKey` (never seen)
- `kms:ListAliases` (never seen)
- `lambda:CreateEventSourceMapping` (never seen)
- `lambda:CreateFunction` (never seen)
- `lambda:DeleteEventSourceMapping` (never seen)
- `lambda:DeleteFunction` (never seen)
- `lambda:GetFunctionConfiguration` (never seen)
- `lambda:ListEventSourceMappings` (never seen)
- `lambda:ListFunctions` (never seen)
- `logs:CreateLogGroup` (247d, last 2026-01-06)
- `resource-groups:GetGroup` (never seen)
- `resource-groups:GetGroupQuery` (never seen)
- `resource-groups:ListGroupResources` (never seen)
- `resource-groups:ListGroups` (never seen)
- `tag:GetResources` (never seen)

### `opal-globgrph-incremental-updater`

granted **45** | used 2 | **never-used 28** | unobservable 15

- `cloudwatch:DescribeAlarms` (never seen)
- `dynamodb:ListTables` (never seen)
- `ec2:AssignPrivateIpAddresses` (never seen)
- `ec2:CreateNetworkInterface` (93d, last 2026-06-09)
- `ec2:DeleteNetworkInterface` (93d, last 2026-06-09)
- `ec2:DescribeNetworkInterfaces` (93d, last 2026-06-09)
- `ec2:DescribeSecurityGroups` (never seen)
- `ec2:UnassignPrivateIpAddresses` (never seen)
- `events:DescribeRule` (never seen)
- `events:ListTargetsByRule` (never seen)
- `iam:GetRole` (never seen)
- `iam:GetRolePolicy` (never seen)
- `iam:ListAttachedRolePolicies` (never seen)
- `iam:ListRolePolicies` (never seen)
- `iam:ListRoles` (never seen)
- `kms:DescribeKey` (never seen)
- `kms:ListAliases` (never seen)
- `lambda:GetFunction` (never seen)
- `lambda:GetPolicy` (never seen)
- `lambda:ListFunctions` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:DescribeLogGroups` (never seen)
- `s3:GetBucketLocation` (never seen)
- `s3:GetBucketPolicy` (never seen)
- `s3:GetBucketVersioning` (never seen)
- `s3:ListAllMyBuckets` (never seen)
- `secretsmanager:DescribeSecret` (never seen)
- `states:DescribeStateMachine` (never seen)

### `infrastructure-ops-lambda-role`

granted **40** | used 0 | **never-used 25** | unobservable 15

- `cloudwatch:GetMetricStatistics` (never seen)
- `dynamodb:DescribeTable` (never seen)
- `dynamodb:ListTables` (never seen)
- `ec2:CreateImage` (never seen)
- `ec2:DescribeSecurityGroups` (never seen)
- `ec2:DescribeVolumes` (never seen)
- `events:DescribeRule` (never seen)
- `events:ListRules` (never seen)
- `events:ListTargetsByRule` (never seen)
- `iam:GetRolePolicy` (never seen)
- `iam:ListAttachedRolePolicies` (never seen)
- `iam:ListRolePolicies` (never seen)
- `iam:ListRoles` (never seen)
- `lambda:GetFunction` (never seen)
- `lambda:ListFunctions` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `logs:DescribeLogGroups` (never seen)
- `logs:DescribeLogStreams` (never seen)
- `s3:GetBucketLocation` (never seen)
- `s3:GetBucketPolicy` (never seen)
- `s3:GetBucketVersioning` (never seen)
- `s3:ListAllMyBuckets` (never seen)
- `secretsmanager:GetSecretValue` (never seen)
- `sts:GetCallerIdentity` (never seen)

### `opal-globgrph-derive-runner-task`

granted **78** | used 38 | **never-used 21** | unobservable 19

- `ec2:DescribeInternetGateways` (never seen)
- `ec2:DescribeRouteTables` (never seen)
- `ec2:DescribeVpcs` (never seen)
- `ecr:DescribeRepositories` (never seen)
- `ecr:ListImages` (never seen)
- `ecs:DescribeServices` (never seen)
- `ecs:ListServices` (never seen)
- `events:DescribeRule` (never seen)
- `iam:GetRole` (never seen)
- `iam:ListEntitiesForPolicy` (never seen)
- `iam:ListPolicies` (never seen)
- `lambda:GetFunction` (never seen)
- `lambda:GetLayerVersion` (never seen)
- `lambda:GetPolicy` (never seen)
- `lambda:ListLayerVersions` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `rds:DescribeDBInstances` (never seen)
- `secretsmanager:DescribeSecret` (never seen)
- `ssm:GetDocument` (never seen)
- `states:DescribeActivity` (never seen)

### `inf-gold-qa-runner-ec2-role`

granted **40** | used 0 | **never-used 19** | unobservable 21

- `kms:Decrypt` (never seen)
- `kms:DescribeKey` (never seen)
- `kms:GenerateDataKey` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `logs:DescribeLogStreams` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:DescribeParameters` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:ListInstanceAssociations` (121d, last 2026-05-11)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `ssm:UpdateInstanceInformation` (121d, last 2026-05-11)

### `opal-website-dlm-role`

granted **24** | used 1 | **never-used 18** | unobservable 5

- `ec2:CopySnapshot` (never seen)
- `ec2:DescribeAvailabilityZones` (never seen)
- `ec2:DescribeFastSnapshotRestores` (never seen)
- `ec2:DescribeSnapshotAttribute` (never seen)
- `ec2:DescribeSnapshotTierStatus` (never seen)
- `ec2:DescribeVolumes` (never seen)
- `ec2:DisableFastSnapshotRestores` (never seen)
- `ec2:EnableFastSnapshotRestores` (never seen)
- `ec2:ModifySnapshotAttribute` (never seen)
- `ec2:ModifySnapshotTier` (never seen)
- `events:DeleteRule` (never seen)
- `events:DescribeRule` (never seen)
- `events:DisableRule` (never seen)
- `events:EnableRule` (never seen)
- `events:ListTargetsByRule` (never seen)
- `events:PutRule` (never seen)
- `events:PutTargets` (never seen)
- `events:RemoveTargets` (never seen)

### `smartx-exporter-role-20251218220948293500000001`

granted **37** | used 0 | **never-used 18** | unobservable 19

- `ecr:BatchCheckLayerAvailability` (201d, last 2026-02-20)
- `ecr:BatchGetImage` (101d, last 2026-06-01)
- `ecr:GetAuthorizationToken` (101d, last 2026-06-01)
- `ecr:GetDownloadUrlForLayer` (238d, last 2026-01-14)
- `secretsmanager:DescribeSecret` (never seen)
- `secretsmanager:GetSecretValue` (101d, last 2026-06-01)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:ListInstanceAssociations` (101d, last 2026-06-01)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `ssm:UpdateInstanceInformation` (101d, last 2026-06-01)

### `workspace-sync-lambda-role`

granted **33** | used 0 | **never-used 18** | unobservable 15

- `cloudwatch:GetMetricStatistics` (never seen)
- `dynamodb:DescribeTable` (267d, last 2025-12-17)
- `events:DescribeRule` (267d, last 2025-12-17)
- `events:ListRules` (never seen)
- `iam:GetPolicy` (never seen)
- `iam:GetPolicyVersion` (never seen)
- `iam:GetRole` (255d, last 2025-12-29)
- `iam:GetRolePolicy` (never seen)
- `iam:ListAttachedRolePolicies` (never seen)
- `lambda:GetFunction` (never seen)
- `lambda:GetFunctionConfiguration` (never seen)
- `logs:CreateLogGroup` (279d, last 2025-12-05)
- `logs:CreateLogStream` (255d, last 2025-12-29)
- `logs:DescribeLogGroups` (255d, last 2025-12-29)
- `logs:DescribeLogStreams` (never seen)
- `secretsmanager:GetSecretValue` (255d, last 2025-12-29)
- `ses:GetSendQuota` (267d, last 2025-12-17)
- `ses:GetSendStatistics` (267d, last 2025-12-17)

### `inf-bronze-runner-ec2-role`

granted **41** | used 4 | **never-used 15** | unobservable 22

- `kms:CreateGrant` (never seen)
- `kms:DescribeKey` (never seen)
- `kms:GenerateDataKey` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `inf-gold-layer-ec2-role`

granted **44** | used 6 | **never-used 15** | unobservable 23

- `kms:DescribeKey` (never seen)
- `kms:GenerateDataKey` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `logs:DescribeLogStreams` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:DescribeParameters` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `seeking-alpha-scraper-role`

granted **40** | used 2 | **never-used 15** | unobservable 23

- `cloudtrail:LookupEvents` (never seen)
- `iam:CreateServiceLinkedRole` (never seen)
- `logs:CreateLogGroup` (202d, last 2026-02-19)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:ListInstanceAssociations` (204d, last 2026-02-17)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `ssm:UpdateInstanceInformation` (204d, last 2026-02-17)

### `bd-gold-detail-generator-role`

granted **31** | used 0 | **never-used 14** | unobservable 17

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:ListInstanceAssociations` (204d, last 2026-02-17)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `ssm:UpdateInstanceInformation` (204d, last 2026-02-17)

### `find-insure-lambda-role`

granted **28** | used 0 | **never-used 14** | unobservable 14

- `events:DeleteRule` (never seen)
- `events:DescribeRule` (never seen)
- `events:PutRule` (never seen)
- `events:PutTargets` (never seen)
- `events:RemoveTargets` (never seen)
- `kms:Decrypt` (105d, last 2026-05-28)
- `kms:DescribeKey` (never seen)
- `kms:GenerateDataKey` (never seen)
- `kms:GenerateDataKeyWithoutPlaintext` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (105d, last 2026-05-28)
- `s3:GetBucketLocation` (never seen)
- `secretsmanager:DescribeSecret` (never seen)
- `secretsmanager:GetSecretValue` (105d, last 2026-05-28)

### `cot-gold-layer-ec2-role`

granted **30** | used 0 | **never-used 13** | unobservable 17

- `secretsmanager:GetSecretValue` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:ListInstanceAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `ssm:UpdateInstanceInformation` (never seen)

### `demo-transform-runner-ec2-role`

granted **29** | used 0 | **never-used 12** | unobservable 17

- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:ListInstanceAssociations` (96d, last 2026-06-05)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `ssm:UpdateInstanceInformation` (96d, last 2026-06-05)

### `ec2-ssm-role`

granted **25** | used 0 | **never-used 12** | unobservable 13

- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:ListInstanceAssociations` (213d, last 2026-02-09)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `ssm:UpdateInstanceInformation` (213d, last 2026-02-09)

### `estate-report-runner-role`

granted **33** | used 3 | **never-used 12** | unobservable 18

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `opal-bloomberg-tunnel-instance-role`

granted **25** | used 0 | **never-used 12** | unobservable 13

- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:ListInstanceAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `ssm:UpdateInstanceInformation` (never seen)

### `bd-exporter-ec2-role`

granted **46** | used 4 | **never-used 11** | unobservable 31

- `ec2:StartInstances` (226d, last 2026-01-26)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (198d, last 2026-02-23)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `cot-exporter-ec2-role`

granted **33** | used 4 | **never-used 11** | unobservable 18

- `secretsmanager:DescribeSecret` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `inf-exporter-ec2-role`

granted **37** | used 6 | **never-used 11** | unobservable 20

- `kms:DescribeKey` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `mdpf-daily-runner-ec2-role`

granted **33** | used 4 | **never-used 11** | unobservable 18

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `opal-gateway-role`

granted **30** | used 3 | **never-used 11** | unobservable 16

- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)
- `sts:AssumeRole` (never seen)

### `opal-website-wp-role`

granted **32** | used 2 | **never-used 11** | unobservable 19

- `s3:GetBucketLocation` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `quartz-si2-spike-role`

granted **33** | used 6 | **never-used 11** | unobservable 16

- `kms:DescribeKey` (never seen)
- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `astn-wsjft-scraper-role`

granted **32** | used 3 | **never-used 10** | unobservable 19

- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `bd-49f-auto-login-role`

granted **30** | used 4 | **never-used 10** | unobservable 16

- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `consolidation-gold-runner-role`

granted **29** | used 2 | **never-used 10** | unobservable 17

- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `etfs-reports-reporter-role`

granted **29** | used 2 | **never-used 10** | unobservable 17

- `ssm:DescribeAssociation` (never seen)
- `ssm:DescribeDocument` (never seen)
- `ssm:GetDeployablePatchSnapshotForInstance` (never seen)
- `ssm:GetDocument` (never seen)
- `ssm:GetParameter` (never seen)
- `ssm:GetParameters` (never seen)
- `ssm:ListAssociations` (never seen)
- `ssm:PutComplianceItems` (never seen)
- `ssm:PutInventory` (never seen)
- `ssm:UpdateAssociationStatus` (never seen)

### `lambda-execution-role`

granted **28** | used 1 | **never-used 8** | unobservable 19

- `ec2:StartInstances` (223d, last 2026-01-29)
- `ecs:DescribeTasks` (never seen)
- `ecs:RunTask` (220d, last 2026-02-02)
- `logs:CreateLogGroup` (208d, last 2026-02-13)
- `secretsmanager:GetSecretValue` (196d, last 2026-02-25)
- `ssm:DescribeInstanceInformation` (223d, last 2026-01-29)
- `ssm:GetCommandInvocation` (never seen)
- `ssm:SendCommand` (223d, last 2026-01-29)

### `security-sweep-dedicated-role`

granted **54** | used 37 | **never-used 8** | unobservable 9

- `iam:GetCredentialReport` (never seen)
- `iam:GetInstanceProfile` (never seen)
- `lambda:GetFunctionConfiguration` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:DescribeLogGroups` (never seen)
- `s3:GetBucketLogging` (never seen)
- `s3:GetBucketPolicy` (never seen)
- `s3:GetBucketVersioning` (never seen)

### `opal-portal-lambda-role`

granted **37** | used 5 | **never-used 6** | unobservable 26

- `cloudwatch:GetMetricStatistics` (never seen)
- `events:DescribeRule` (never seen)
- `events:ListRules` (never seen)
- `lambda:GetFunction` (never seen)
- `logs:CreateLogGroup` (204d, last 2026-02-17)
- `logs:DescribeLogStreams` (never seen)

### `codebuild-semantic-clustering-role`

granted **15** | used 7 | **never-used 5** | unobservable 3

- `ecr:BatchGetImage` (202d, last 2026-02-20)
- `ecr:GetDownloadUrlForLayer` (202d, last 2026-02-20)
- `lambda:GetFunction` (never seen)
- `lambda:UpdateFunctionCode` (202d, last 2026-02-20)
- `logs:CreateLogGroup` (203d, last 2026-02-18)

### `ecsTaskExecutionRole`

granted **6** | used 0 | **never-used 5** | unobservable 1

- `ecr:BatchCheckLayerAvailability` (never seen)
- `ecr:BatchGetImage` (220d, last 2026-02-02)
- `ecr:GetAuthorizationToken` (220d, last 2026-02-02)
- `ecr:GetDownloadUrlForLayer` (220d, last 2026-02-02)
- `logs:CreateLogStream` (220d, last 2026-02-02)

### `github-actions-opal-deploy`

granted **12** | used 1 | **never-used 5** | unobservable 6

- `lambda:GetFunctionConfiguration` (never seen)
- `lambda:GetLayerVersion` (never seen)
- `lambda:PublishVersion` (never seen)
- `lambda:UpdateFunctionCode` (never seen)
- `ssm:SendCommand` (never seen)

### `infrastructure-snapshot-role`

granted **33** | used 17 | **never-used 5** | unobservable 11

- `events:DescribeRule` (never seen)
- `iam:GetRole` (never seen)
- `lambda:GetFunction` (never seen)
- `lambda:GetFunctionConfiguration` (never seen)
- `logs:CreateLogGroup` (never seen)

### `YChartsSessionCaptureLambdaRole`

granted **5** | used 0 | **never-used 4** | unobservable 1

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `secretsmanager:GetSecretValue` (never seen)
- `secretsmanager:PutSecretValue` (never seen)

### `bd-gold-step-functions-role`

granted **13** | used 0 | **never-used 4** | unobservable 9

- `ec2:StartInstances` (204d, last 2026-02-17)
- `logs:DescribeLogGroups` (209d, last 2026-02-12)
- `logs:DescribeResourcePolicies` (209d, last 2026-02-12)
- `logs:PutResourcePolicy` (209d, last 2026-02-12)

### `inf-jwt-trigger-lambda-role`

granted **21** | used 7 | **never-used 4** | unobservable 10

- `kms:DescribeKey` (never seen)
- `kms:Encrypt` (never seen)
- `logs:CreateLogGroup` (never seen)
- `secretsmanager:CreateSecret` (never seen)

### `market-data-generator-lambda-role`

granted **13** | used 0 | **never-used 4** | unobservable 9

- `cloudfront:CreateInvalidation` (never seen)
- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `secretsmanager:GetSecretValue` (never seen)

### `opal-globgrph-nessie-execution`

granted **6** | used 1 | **never-used 4** | unobservable 1

- `ecr:BatchCheckLayerAvailability` (never seen)
- `ecr:BatchGetImage` (never seen)
- `ecr:GetAuthorizationToken` (never seen)
- `ecr:GetDownloadUrlForLayer` (never seen)

### `opal-globgrph-trino-execution`

granted **6** | used 1 | **never-used 4** | unobservable 1

- `ecr:BatchCheckLayerAvailability` (never seen)
- `ecr:BatchGetImage` (never seen)
- `ecr:GetAuthorizationToken` (never seen)
- `ecr:GetDownloadUrlForLayer` (never seen)

### `rds-monitoring-role`

granted **6** | used 0 | **never-used 4** | unobservable 2

- `logs:CreateLogGroup` (265d, last 2025-12-19)
- `logs:CreateLogStream` (265d, last 2025-12-19)
- `logs:DescribeLogStreams` (355d, last 2025-09-19)
- `logs:PutRetentionPolicy` (355d, last 2025-09-19)

### `yang-pipeline-sfn-role`

granted **13** | used 0 | **never-used 4** | unobservable 9

- `logs:DescribeLogGroups` (250d, last 2026-01-03)
- `logs:DescribeResourcePolicies` (never seen)
- `logs:PutResourcePolicy` (never seen)
- `xray:GetSamplingRules` (never seen)

### `YChartsMarketDataPullLambdaRole`

granted **4** | used 0 | **never-used 3** | unobservable 1

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (107d, last 2026-05-26)
- `secretsmanager:GetSecretValue` (107d, last 2026-05-26)

### `agentbus-alyssa01-fleet-andrew-role`

granted **8** | used 0 | **never-used 3** | unobservable 5

- `kms:Decrypt` (never seen)
- `kms:DescribeKey` (never seen)
- `kms:GenerateDataKey` (never seen)

### `bd-49f-session-trigger-role`

granted **15** | used 5 | **never-used 3** | unobservable 7

- `logs:CreateLogGroup` (never seen)
- `ssm:GetCommandInvocation` (never seen)
- `ssm:ListCommandInvocations` (never seen)

### `cot-bd-session-trigger-lambda-role`

granted **10** | used 4 | **never-used 3** | unobservable 3

- `logs:CreateLogGroup` (never seen)
- `secretsmanager:DescribeSecret` (never seen)
- `secretsmanager:PutSecretValue` (never seen)

### `exec-summary-generator-role`

granted **10** | used 0 | **never-used 3** | unobservable 7

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (129d, last 2026-05-04)
- `secretsmanager:GetSecretValue` (129d, last 2026-05-04)

### `inf-assets-trigger-lambda-role`

granted **12** | used 5 | **never-used 3** | unobservable 4

- `kms:DescribeKey` (never seen)
- `kms:Encrypt` (never seen)
- `logs:CreateLogGroup` (never seen)

### `inf-ec2-retry-launch-lambda-role`

granted **16** | used 4 | **never-used 3** | unobservable 9

- `kms:DescribeKey` (never seen)
- `kms:Encrypt` (never seen)
- `logs:CreateLogGroup` (never seen)

### `news-dashboard-processor-role`

granted **9** | used 0 | **never-used 3** | unobservable 6

- `logs:CreateLogGroup` (293d, last 2025-11-20)
- `logs:CreateLogStream` (274d, last 2025-12-10)
- `secretsmanager:GetSecretValue` (274d, last 2025-12-10)

### `opal-globgrph-projection-worker`

granted **11** | used 0 | **never-used 3** | unobservable 8

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `s3:GetBucketLocation` (never seen)

### `opal-globgrph-serving-task`

granted **6** | used 0 | **never-used 3** | unobservable 3

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `s3:GetBucketLocation` (never seen)

### `opal-security-admin`

granted **9** | used 0 | **never-used 3** | unobservable 6

- `kms:Decrypt` (never seen)
- `kms:DescribeKey` (never seen)
- `kms:Encrypt` (never seen)

### `opal-smartx-lambda-role`

granted **6** | used 0 | **never-used 3** | unobservable 3

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `secretsmanager:GetSecretValue` (never seen)

### `partners-lambda-role`

granted **13** | used 1 | **never-used 3** | unobservable 9

- `logs:CreateLogGroup` (238d, last 2026-01-15)
- `secretsmanager:CreateSecret` (never seen)
- `secretsmanager:GetSecretValue` (147d, last 2026-04-15)

### `portal-auth-lambda-role`

granted **4** | used 0 | **never-used 3** | unobservable 1

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `secretsmanager:GetSecretValue` (never seen)

### `schwab-anonymizer-lambda-role`

granted **4** | used 0 | **never-used 3** | unobservable 1

- `logs:CreateLogGroup` (272d, last 2025-12-11)
- `logs:CreateLogStream` (272d, last 2025-12-11)
- `secretsmanager:GetSecretValue` (272d, last 2025-12-11)

### `semantic-news-lambda-role`

granted **12** | used 0 | **never-used 3** | unobservable 9

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)
- `secretsmanager:GetSecretValue` (never seen)

### `smartx-rest-pull-role`

granted **7** | used 1 | **never-used 3** | unobservable 3

- `logs:CreateLogGroup` (never seen)
- `secretsmanager:DescribeSecret` (never seen)
- `secretsmanager:GetSecretValue` (never seen)

### `vpc-flow-logs-role`

granted **5** | used 1 | **never-used 3** | unobservable 1

- `logs:CreateLogGroup` (never seen)
- `logs:DescribeLogGroups` (never seen)
- `logs:DescribeLogStreams` (never seen)

### `yang-pipeline-lambda-role`

granted **23** | used 4 | **never-used 3** | unobservable 16

- `logs:CreateLogGroup` (219d, last 2026-02-02)
- `secretsmanager:GetSecretValue` (238d, last 2026-01-14)
- `states:DescribeExecution` (never seen)

### `bd-gold-layer-lambda-role`

granted **7** | used 0 | **never-used 2** | unobservable 5

- `logs:CreateLogGroup` (238d, last 2026-01-15)
- `logs:CreateLogStream` (99d, last 2026-06-03)

### `bd-merge-daily-lambda-role`

granted **6** | used 0 | **never-used 2** | unobservable 4

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)

### `bd-pipeline-task-role`

granted **8** | used 0 | **never-used 2** | unobservable 6

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)

### `ec2-auto-shutdown-enforcer-role`

granted **8** | used 1 | **never-used 2** | unobservable 5

- `cloudwatch:GetMetricStatistics` (never seen)
- `logs:CreateLogGroup` (never seen)

### `etfs-avgcap-reader-role`

granted **6** | used 0 | **never-used 2** | unobservable 4

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)

### `etfs-canon-fanin-role`

granted **9** | used 1 | **never-used 2** | unobservable 6

- `dynamodb:DescribeTable` (never seen)
- `logs:CreateLogGroup` (never seen)

### `inf-otp-relay-lambda-role`

granted **8** | used 1 | **never-used 2** | unobservable 5

- `logs:CreateLogGroup` (never seen)
- `secretsmanager:GetSecretValue` (99d, last 2026-06-03)

### `lambda-test-role`

granted **3** | used 0 | **never-used 2** | unobservable 1

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)

### `market-update-lambda-role`

granted **11** | used 1 | **never-used 2** | unobservable 8

- `logs:CreateLogGroup` (282d, last 2025-12-01)
- `logs:CreateLogStream` (257d, last 2025-12-26)

### `news-sentiment-lambda-role`

granted **8** | used 0 | **never-used 2** | unobservable 6

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)

### `opal-data-refresh-lambda-role`

granted **22** | used 6 | **never-used 2** | unobservable 14

- `cloudfront:GetInvalidation` (never seen)
- `logs:CreateLogGroup` (234d, last 2026-01-19)

### `opal-globgrph-cse-producer-task`

granted **7** | used 0 | **never-used 2** | unobservable 5

- `logs:CreateLogStream` (never seen)
- `s3:GetBucketLocation` (never seen)

### `opal-globgrph-nessie-task`

granted **17** | used 1 | **never-used 2** | unobservable 14

- `dynamodb:CreateTable` (93d, last 2026-06-09)
- `s3:GetBucketLocation` (never seen)

### `opal-globgrph-resource-summaries-producer-task`

granted **7** | used 0 | **never-used 2** | unobservable 5

- `logs:CreateLogStream` (never seen)
- `s3:GetBucketLocation` (never seen)

### `opal-globgrph-trino-task`

granted **16** | used 0 | **never-used 2** | unobservable 14

- `logs:CreateLogStream` (never seen)
- `s3:GetBucketLocation` (never seen)

### `opal-ipset-reconciler`

granted **12** | used 5 | **never-used 2** | unobservable 5

- `dynamodb:ListStreams` (never seen)
- `logs:CreateLogGroup` (never seen)

### `portfolio-management-lambda-role`

granted **13** | used 0 | **never-used 2** | unobservable 11

- `logs:CreateLogGroup` (never seen)
- `logs:CreateLogStream` (never seen)

### `sentiment_query_api-role`

granted **6** | used 0 | **never-used 2** | unobservable 4

- `logs:CreateLogGroup` (260d, last 2025-12-23)
- `logs:CreateLogStream` (260d, last 2025-12-23)

### `smartx-assets-pull-role`

granted **10** | used 3 | **never-used 2** | unobservable 5

- `logs:CreateLogGroup` (never seen)
- `secretsmanager:DescribeSecret` (never seen)

### `smartx-jwt-refresher-role`

granted **7** | used 3 | **never-used 2** | unobservable 2

- `logs:CreateLogGroup` (never seen)
- `secretsmanager:DescribeSecret` (never seen)

### `FredIngestionLambdaRole`

granted **7** | used 2 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (259d, last 2025-12-24)

### `FredMacroIngestionLambdaRole`

granted **5** | used 2 | **never-used 1** | unobservable 2

- `logs:CreateLogGroup` (never seen)

### `YChartsSessionProbeLambdaRole`

granted **6** | used 2 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `advi-49f-gold-dispatch-role`

granted **9** | used 5 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `agentbus-sim01-fleet-alpha-role`

granted **8** | used 2 | **never-used 1** | unobservable 5

- `kms:DescribeKey` (never seen)

### `agentbus-sim01-fleet-beta-role`

granted **8** | used 2 | **never-used 1** | unobservable 5

- `kms:DescribeKey` (never seen)

### `bd-49f-etf-ownership-daily-role`

granted **7** | used 1 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

### `bd-49f-fees-runner-role`

granted **7** | used 2 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `bd-49f-keepalive-role`

granted **6** | used 2 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `bd-49f-runner-role`

granted **6** | used 2 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `bd-allocation-checker-lambda-role`

granted **7** | used 1 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (224d, last 2026-01-28)

### `bd-allocation-processor-role`

granted **8** | used 1 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `bd-cot-keepalive-role`

granted **6** | used 2 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `bd-daily-trigger-lambda-role`

granted **13** | used 3 | **never-used 1** | unobservable 9

- `logs:CreateLogGroup` (205d, last 2026-02-16)

### `bd-gold-eventbridge-step-functions-role`

granted **1** | used 0 | **never-used 1** | unobservable 0

- `states:StartExecution` (204d, last 2026-02-17)

### `bd-processor-lambda-role`

granted **8** | used 1 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `bd-silver-merge-role`

granted **7** | used 1 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

### `consolidation-gold-runner-automation-start-role`

granted **3** | used 0 | **never-used 1** | unobservable 2

- `ec2:StartInstances` (never seen)

### `consolidation-gold-runner-events-invoke-ssm-role`

granted **2** | used 0 | **never-used 1** | unobservable 1

- `ssm:StartAutomationExecution` (never seen)

### `cot-etf-ownership-daily-role`

granted **7** | used 1 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

### `cot-rebalancer-runner-role`

granted **7** | used 2 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `cot-satellites-registry-producer-role`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `deck-generation-lambda-role`

granted **6** | used 1 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `etf-ownership-dashboard-role`

granted **9** | used 1 | **never-used 1** | unobservable 7

- `logs:CreateLogGroup` (never seen)

### `etf-positioning-producer-role`

granted **7** | used 1 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

### `etfs-netassets-daily-role`

granted **6** | used 1 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `gldinc-ss4c-canary-role`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `globgrph-derive-build-role`

granted **12** | used 8 | **never-used 1** | unobservable 3

- `ecr:BatchGetImage` (never seen)

### `historical-prices-lambda-role`

granted **7** | used 2 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `inf-accounts-v2-daily-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-api-assets-v2-lambda-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-api-eclipse-role`

granted **6** | used 2 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `inf-api-positions-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-api-reps-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-api-txn-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-billing-daily-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-bronze-complete-emitter-role`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `inf-bronze-trigger-lambda-role`

granted **7** | used 2 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `inf-ec2-launch-monitor-lambda-role`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `inf-etf-ownership-daily-role`

granted **7** | used 1 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

### `inf-eventbridge-ssm-role`

granted **1** | used 0 | **never-used 1** | unobservable 0

- `ssm:SendCommand` (never seen)

### `inf-gold-layer-lambda-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-gold-trigger-lambda-role`

granted **13** | used 5 | **never-used 1** | unobservable 7

- `logs:CreateLogGroup` (never seen)

### `inf-nna-partition-checker-lambda-role`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `inf-performance-daily-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-silver-aggregator-lambda-role`

granted **7** | used 1 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

### `inf-silver-chain-lambda-role`

granted **8** | used 1 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-tax-daily-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `inf-unified-account-dim-daily-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `lambda-access-anomaly-scanner-role`

granted **8** | used 5 | **never-used 1** | unobservable 2

- `logs:CreateLogGroup` (201d, last 2026-02-20)

### `lambda-cost-anomaly-scanner-role`

granted **8** | used 2 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (201d, last 2026-02-20)

### `lambda-ec2-runtime-monitor-role`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (216d, last 2026-02-06)

### `mdpf-accrual-trigger-role`

granted **10** | used 4 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

### `mdpf-feeder-trigger-role`

granted **12** | used 4 | **never-used 1** | unobservable 7

- `logs:CreateLogGroup` (never seen)

### `news-ingestion-lambda-role`

granted **13** | used 2 | **never-used 1** | unobservable 10

- `logs:CreateLogGroup` (237d, last 2026-01-16)

### `opal-assets-bd49f-daily-pull-role`

granted **9** | used 2 | **never-used 1** | unobservable 6

- `logs:CreateLogGroup` (never seen)

### `opal-assets-bd49f-dim-convert-role`

granted **6** | used 1 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `opal-assets-bd49f-reporting-pull-role`

granted **7** | used 2 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `opal-assets-daily-emitter-role`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `opal-assets-ingest-router-role`

granted **9** | used 1 | **never-used 1** | unobservable 7

- `logs:CreateLogGroup` (never seen)

### `opal-assets-mdpf-egress-publisher-role`

granted **6** | used 1 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `opal-assets-mdpf-portal-publisher-role`

granted **6** | used 1 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `opal-assets-silver-bd49finsurance-role`

granted **13** | used 1 | **never-used 1** | unobservable 11

- `logs:CreateLogGroup` (never seen)

### `opal-assets-silver-blackdiamond-role`

granted **13** | used 1 | **never-used 1** | unobservable 11

- `logs:CreateLogGroup` (never seen)

### `opal-assets-silver-eclipse-role`

granted **13** | used 1 | **never-used 1** | unobservable 11

- `logs:CreateLogGroup` (never seen)

### `opal-assets-silver-etf-role`

granted **13** | used 1 | **never-used 1** | unobservable 11

- `logs:CreateLogGroup` (never seen)

### `opal-assets-silver-orion-role`

granted **13** | used 1 | **never-used 1** | unobservable 11

- `logs:CreateLogGroup` (never seen)

### `opal-assets-silver-schwab-role`

granted **13** | used 1 | **never-used 1** | unobservable 11

- `logs:CreateLogGroup` (never seen)

### `opal-assets-silver-smartx-role`

granted **13** | used 1 | **never-used 1** | unobservable 11

- `logs:CreateLogGroup` (never seen)

### `opal-globgrph-comp-learns-producer-task`

granted **3** | used 0 | **never-used 1** | unobservable 2

- `logs:CreateLogStream` (never seen)

### `opal-globgrph-derive-runner-execution`

granted **7** | used 5 | **never-used 1** | unobservable 1

- `ecr:BatchCheckLayerAvailability` (never seen)

### `opal-globgrph-fedobs-emitter-task`

granted **5** | used 0 | **never-used 1** | unobservable 4

- `logs:CreateLogStream` (never seen)

### `opal-globgrph-projection-pipe`

granted **8** | used 1 | **never-used 1** | unobservable 6

- `logs:CreateLogStream` (never seen)

### `opal-ipblock-cli`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `kms:GenerateDataKey` (never seen)

### `opal-lambda-market-rsi-role`

granted **6** | used 1 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (248d, last 2026-01-05)

### `opal-layer3-ec2-role`

granted **9** | used 0 | **never-used 1** | unobservable 8

- `secretsmanager:GetSecretValue` (269d, last 2025-12-15)

### `opal-portal-content-api-role`

granted **7** | used 1 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

### `opal-security-scanner-processor-role`

granted **5** | used 1 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `opal-sentinel`

granted **12** | used 3 | **never-used 1** | unobservable 8

- `logs:CreateLogGroup` (never seen)

### `opal-ticket-api-role`

granted **9** | used 1 | **never-used 1** | unobservable 7

- `logs:CreateLogGroup` (never seen)

### `opalinvest-auth-lambda-role`

granted **12** | used 2 | **never-used 1** | unobservable 9

- `logs:CreateLogGroup` (255d, last 2025-12-29)

### `portfolio-export-lambda-role`

granted **10** | used 1 | **never-used 1** | unobservable 8

- `logs:CreateLogGroup` (never seen)

### `smartx-ingestion-lambda-role`

granted **13** | used 1 | **never-used 1** | unobservable 11

- `logs:CreateLogGroup` (never seen)

### `trade-submission-lambda-role`

granted **15** | used 1 | **never-used 1** | unobservable 13

- `logs:CreateLogGroup` (232d, last 2026-01-20)

### `wsb-49f-model-aua-daily-role`

granted **6** | used 2 | **never-used 1** | unobservable 3

- `logs:CreateLogGroup` (never seen)

### `wsd-49f-partner-held-etf-daily-role`

granted **6** | used 1 | **never-used 1** | unobservable 4

- `logs:CreateLogGroup` (never seen)

### `yang-varflag-check-role`

granted **8** | used 2 | **never-used 1** | unobservable 5

- `logs:CreateLogGroup` (never seen)

---

## Where the never-used and the unobservable rows CONCENTRATE, by service

Top 12 of each. This is orientation for whoever acts next; it is not a ranking of importance.

| service | never-used rows | | service | unobservable rows |
|---|---|---|---|---|
| `ssm` | 245 | | `s3` | 477 |
| `logs` | 195 | | `logs` | 185 |
| `lightsail` | 57 | | `dynamodb` | 171 |
| `iotwireless` | 44 | | `ec2messages` | 133 |
| `networkmanager` | 35 | | `ssmmessages` | 92 |
| `secretsmanager` | 33 | | `glue` | 81 |
| `kms` | 33 | | `ssm` | 79 |
| `ec2` | 33 | | `sqs` | 78 |
| `medialive` | 33 | | `ec2` | 75 |
| `lambda` | 28 | | `datazone` | 62 |
| `ivs` | 27 | | `bedrock-agentcore` | 59 |
| `inspector2` | 25 | | `deadline` | 57 |

---

## (e) THE INSTRUMENT'S OWN LIMITS, QUOTED -- and which of them bound THIS run

`bash .tools/comp-iam-usage limits`, run from this worktree, rc=0, verbatim:

```
comp-iam-usage -- Rule-22a fix-or-carry (comp-iam's 3 named limits, never inherited silently):
  RULE-22a fix-or-carry (comp-iam's 3 named limits -- NAMED, never silently inherited):
    (a) (action,resource) blindness  -> FIXED: reach-check simulates the EXACT --resource-arns
        (comp-iam models (action) only; a grant on ANY arn falsely reads GRANTED for EVERY arn).
    (b) 2+-ARN implicitDeny poisoning -> FIXED: ONE --resource-arns per reach-check call; the
        positive control is a SEPARATE invocation (batching corrupts the control).
    (c) Condition-block false-deny    -> FIXED/CARRIED: --context-entries when given; a conditioned
        statement with no context is UNKNOWN, never a (false) deny.
    (+) DESIRED-not-APPLIED           -> FIXED: who-can-reach / reach-check read LIVE policies;
        an unreadable/unparseable policy is UNKNOWN, never 'no reach' (an unparsed Deny != silence).
```

### Which bound this run

| limit | did it bind THIS run? |
|---|---|
| **(a) (action,resource) blindness** | **NO -- OUT OF PLANE.** Fixed in `reach-check`, which this cell never called. `permission-cold` models the (action) grain by construction: it answers "was this ACTION used", never "on which RESOURCE". A permission reported never-used here is never-used on EVERY resource, so the limit cannot make this cell's answer wrong -- but it does bound what the answer MEANS. |
| **(b) 2+-ARN implicitDeny poisoning** | **NO -- OUT OF PLANE.** A simulate-path limit. No simulate call was made. |
| **(c) condition-block false-deny** | **NO, AND THIS IS A REAL CEILING ON THE ANSWER.** `permission-cold` reads Allow actions out of policy documents and does not evaluate condition blocks. A permission reported never-used may be one whose conditions never admit it -- the row is still correct as "granted and not used", but "granted" here means the action token appears in an Allow, not that the grant is reachable. The condition axis is `IAM-s-4`'s cell, not this one. |
| **(+) DESIRED-not-APPLIED** | **PARTLY, AND IT CUTS THE OTHER WAY HERE.** GRANTED is the DESIRED plane read from live policy documents attached to live roles -- so it is desired-as-currently-attached, not desired-as-declared-in-Terraform. This is why the population is 219 live roles and not the 191 Terraform-parsed ones: those are different populations, not two readings of one. |

**And the limit that binds this run hardest is not in that list, because it belongs to the DATA SOURCE rather
than to the tool: 3636 of 5494 granted permissions (66%) are UNOBSERVABLE.** The telemetry's action-grain
coverage, not the instrument, is the ceiling on this outcome. Section (d) counts it four ways rather than
folding it into a percentage.

---

## BOUNDS -- what this cell did not do

| bound | how it was held |
|---|---|
| **C-NO-ACCESSDENIED (D5)** -- naming is not removing | Every AWS call in this cell was a read: `sts get-caller-identity`, `iam list-roles`, `iam list-attached-role-policies`, and the instrument's own read-only calls. No policy, role, attachment or any other AWS state was created, changed or destroyed. **This document narrows nothing and recommends no specific narrowing** -- it reports. |
| **C-TWO-REMEDIES** -- permissions axis only | No governance disposition document was read or written, no owner was assigned, and no finding here is offered as a governance answer. |
| **C-ANALYZER-PRICED-FIRST + G-25** | The priced unused-access finding service was NOT called, NOT priced and NOT compared against -- not even once, and not for a control. `permission-cold` uses IAM Access Advisor action-level telemetry, which is free and core-IAM, and the tool's own bytes carry that statement. Pricing the priced service is a vendor call reserved to Andrew and this cell does not and cannot authorise it. |
| **G-21 moratorium** -- no alert/alarm/monitor/schedule/notification | Nothing recurring was minted. This is a one-shot exercise producing a dated document; there is no scheduler, no rule, no alarm, no topic and no re-run trigger anywhere in this deliverable. The sweep driver lived in `.scratch/` and is not committed. |
| **BOUND EVERY AWS READ** | Every invocation ran under `timeout 120`, iterated role by role rather than swept in one call. 219 of 219 returned rc=0; **zero rc=124**. Max single-role wall time 10 s against a 120 s bound. |
| **A role the instrument cannot see must not read as clean** | Enforced in three places: the role partition table counts WHOLLY UNOBSERVABLE as its own class (27 roles), section (d) names every one of them, and `granted_read_ok` / `advisor_read_ok` are checked per role before any row is classified. |
| **Do not build, fork or improve the instrument** | `.tools/` was never written to. Content pin re-read at commit time, both blobs unchanged. |

---

## WHAT THIS DELIVERABLE DOES NOT ESTABLISH

- **It is not a narrowing plan.** It names unused permissions. Which of them should be removed, by whom, and
  with what blast radius, is not this cell's question (`IAM-s-8` owns blast radius).
- **90 days is a choice, not a truth.** 95 rows are never-used because their real last use is 93-355 days old.
  A 180-day lookback would reclassify some of them and cannot reclassify the 1342 rows with no observed use at all.
- **Unobservable is not a verdict of any kind.** 3636 rows -- the majority of the denominator -- carry no
  information about use. They are not evidence of use and they are not evidence of disuse.
- **Condition blocks were not evaluated** (limit (c) above); the resource grain was not touched (limit (a)).
- **The 10 AWS service-linked roles were not read.** Stated, named as an exclusion, and filed as a row.
- **This is a single vintage.** Every figure is as of 2026-09-10 with a 90-day window ending that day. No claim
  here is durable and nothing in this cell makes it recur.

---

## EVIDENCE ATTACHED

| artifact | what it is |
|---|---|
| `PERMISSION_USAGE_EXERCISE.md` | this document |
| `permission-cold-raw-bundle.json` | **the instrument's raw JSON for all 219 roles, UNREDACTED**, plus the per-role exit code and wall time, the invocation string, the instrument blob pins and the population rule. Every figure in this document is recomputable from it without re-running a single AWS call. |

## SURPRISE ROWS FILED BY THIS CELL

Both in `org/missions/D12/NFRA/NFRA_IAMROLES202609/surprise-channel/investigations/INVESTIGATION_v1.md`.

- **`NFRA_IAMROLES202609-Z-W8-S1`** (OBSERVATION, ARMED) -- AC5's negative token census cannot distinguish a
  bound crossing from a faithfully reported granted permission, because the forbidden token is an AWS service
  namespace that one real role in the population holds 16 permissions in.
- **`NFRA_IAMROLES202609-Z-W8-S2`** (OBSERVATION, ARMED) -- 219 is every live role MINUS TEN; a direct
  control-plane read returns 229, and both instruments that report 219 exclude the same 10 service-linked roles.

---

*Produced by `0.9.0_WK_NFRA_IAMROLES202609~8` for `NFRA_IAMROLES202609.TO-IAM-t-2`. Every figure above is
MEASURED from this worker's own bounded runs on 2026-09-10 and recomputable from the attached bundle.*
