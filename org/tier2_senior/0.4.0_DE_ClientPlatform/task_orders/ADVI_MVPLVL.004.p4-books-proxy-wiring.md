```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-16-p4-books-firmid-fix</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-16</date>
    <status>complete</status>
    <thread_serial>ADVI_MVPLVL-004</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</thread_ref>
    <revision>REVISED 2026-03-16 — original proxy wiring delivered (deff097). This revision
    addresses the firmId naming collision discovered in DT hotfix session. 4 Lambda-routed
    functions pass wrong param name and wrong value.</revision>
  </metadata>

  <objective>
    Fix the 4 Lambda-routed Books Tab API functions to pass `?firmId={ddbFirmId}`
    instead of `?firm={bucketSuffix}`. The Lambda expects the DynamoDB partition key
    (e.g., `49financial`), not the S3 bucket suffix (`bd`). Also fix the 2 Addendum A
    functions (getMixTimeseries, getConcentrationTimeseries) which pass the same wrong value.
  </objective>

  <context>
    Two routing mechanisms exist with different parameter requirements:

    | Route type | Router | Param name | Value | Example |
    |---|---|---|---|---|
    | S3-routed (*.json) | shared-advisor-router (Lambda@Edge) | `?firm=` | S3 bucket suffix | `?firm=bd` |
    | Lambda-routed (/books/*, /partners/*) | opal-partners-data (API Gateway) | `?firmId=` | DynamoDB firm key | `?firmId=49financial` |

    The page's `selectedFirmId` is `'bd'` (S3 bucket suffix). `firmOverride` is also `'bd'`.
    The DynamoDB mapping is: `FIRM#49financial` -> `s3Bucket: opal-data-bd`.
    No mapping from bucket suffix to DynamoDB key exists in the portal.

    The `/api/partners` response returns `Partner.firmId` which IS the DynamoDB key
    (`49financial`), but the page never calls this endpoint. The firm picker hardcodes `'bd'`.
  </context>

  <scope>
    <files>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add a static firmId mapping constant in advisor-intelligence.ts:
      ```typescript
      const LAMBDA_FIRM_ID: Record&lt;string, string&gt; = { bd: '49financial' }
      ```
      This maps S3 bucket suffix -> DynamoDB firm key. Only one firm exists today.
    </requirement>

    <requirement id="2">
      Fix param name on 4 Lambda-routed functions from `?firm=` to `?firmId=`,
      and resolve the value through the mapping:

      | Function | Line | Current (BROKEN) | Required |
      |---|---|---|---|
      | getBooksRelationshipTimeseries | ~365 | `?firm=${firmOverride}` | `?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` |
      | getBooksAccountTimeseries | ~375 | `?firm=${firmOverride}` | `?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` |
      | getBooksRelationshipComposition | ~385 | `?firm=${firmOverride}` | `?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` |
      | getBooksAccountComposition | ~395 | `?firm=${firmOverride}` | `?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` |

      Keep the `firmOverride?: string` parameter signature — callers already pass it.
    </requirement>

    <requirement id="3">
      Fix the 2 Addendum A functions (getMixTimeseries, getConcentrationTimeseries)
      at lines ~410 and ~432. These already use `?firmId=` (correct param name) but
      receive `firmId` which is `'bd'` from BooksTab. Apply the same mapping:

      ```typescript
      const params = new URLSearchParams({ firmId: LAMBDA_FIRM_ID[firmId] ?? firmId })
      ```
    </requirement>

    <requirement id="4">
      In ClientsTab.tsx line 275, L3ClientDetail receives `firmId={firmOverride || firmId}`
      which is `'bd'`. L3ClientDetail passes this to getMixTimeseries and
      getConcentrationTimeseries. The mapping in requirement 3 handles this — no change
      needed in ClientsTab.tsx unless the call site sends the raw bucket suffix directly
      (verify the prop chain).
    </requirement>

    <requirement id="5">
      `bun run build` must pass clean. No type errors.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 6 Lambda-routed functions use `?firmId=` param name (not `?firm=`)</criterion>
    <criterion id="2">All 6 Lambda-routed functions resolve value through LAMBDA_FIRM_ID mapping</criterion>
    <criterion id="3">`bun run build` passes clean</criterion>
    <criterion id="4">3 S3-routed functions (getClientDetail, getAdvisorBook, getBooksClientDetail) are UNCHANGED — their `?firm=${firmOverride}` is already correct</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Commit on portal DEV branch</constraint>
    <constraint>Do NOT touch S3-routed functions — they work correctly with `?firm=bd`</constraint>
    <constraint>Do NOT change the firmOverride parameter name or type on any function signature — callers depend on it</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="partners-api-v1.0.1-hotfix" status="complete">
      API Gateway routes created and JWT authorizer attached (da5c527f)
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit with firmId mapping fix on 6 Lambda-routed functions</deliverable>
  </deliverables>
</task_order>
```
