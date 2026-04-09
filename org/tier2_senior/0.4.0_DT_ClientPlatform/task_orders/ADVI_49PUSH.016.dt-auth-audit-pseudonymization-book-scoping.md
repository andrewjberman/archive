<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-016-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>4</wave>
    <phase>P4</phase>
  </metadata>

  <objective>
    Two audits in one TO:
    1. Pseudonymization field path audit: diff gold vs platinum JSON structures for every
       PII-containing file. Verify the HMAC function in opal-partners-data targets the
       correct fields in the new platinum schemas.
    2. Book scoping audit: for every platinum path, determine if it's S3-direct (no
       server-side scoping) or Lambda-routed (scoped). Flag any S3-direct paths that
       contain book-specific data without server-side filtering.
  </objective>

  <context>
    PRDs:
    - docs/architecture/ADVI_49PUSH_P4_PRD.md (sections: What Changed with Platinum, Known Risk Areas)
    - docs/architecture/ADVI_ANONYM_PRD.md (HMAC pseudonymization details)

    DT route mapping from .011 defines which paths are S3-direct vs Lambda:
    - S3-direct (shared-advisor-router): all /platinum/ paths
    - Lambda (opal-partners-data): mix-timeseries, concentration-timeseries

    Key risk from P4 PRD: platinum JSON may nest client names differently than gold JSON.
    If the HMAC function misses fields, cleartext PII leaks to external users.

    Key risk: S3-direct paths serve unfiltered files. If a 49F advisor requests another
    advisor's platinum/advisors/{id}/summary.json directly, it's served without book scoping.
  </context>

  <compiler_tools_mandate>
    1. comp-routes auth-map
       -- which paths have edge-only vs double auth vs Lambda scoping

    2. comp-routes trace platinum/advisors --direction both
       -- serving chain for advisor summaries (S3-direct = no book scoping)

    3. comp-routes trace platinum/clients --direction both
       -- serving chain for client summaries

    4. comp-trace opal-partners-data --direction both
       -- what the Lambda handles (these routes have server-side scoping)
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      PSEUDONYMIZATION AUDIT:
      For every platinum file that contains PII (names), produce a diff table:

      | Platinum File | PII Field Path (platinum) | Equivalent Gold Field Path | HMAC Function Covers? |
      |---|---|---|---|
      | firm/dashboard.json | leaderboard[].name | employee_leaderboard.json advisors[].name | ? |
      | advisors/{id}/summary.json | book.clients[].client_name | advisors/{id}/book.json clients[].name | ? |
      | ... | | | |

      Read the pseudonymization function in opal-partners-data/lambda_function.py (or
      pseudonymizer.py). Check if it walks the JSON looking for specific field names or
      uses a path-based approach. Verify it handles platinum field names.
    </requirement>

    <requirement id="2">
      BOOK SCOPING AUDIT:
      For every platinum path from .011 route mapping, classify:

      | Platinum Path | Serving | Auth Layers | Book Scoped? | Risk |
      |---|---|---|---|---|
      | platinum/firm/dashboard.json | S3-direct | Edge JWT only | No (firm-level, OK) | None |
      | platinum/advisors/{id}/summary.json | S3-direct | Edge JWT only | NO | HIGH -- advisor can request other advisor's summary |
      | platinum/clients/{rel_id}/summary.json | S3-direct | Edge JWT only | NO | HIGH -- advisor can request other's clients |
      | platinum/clients/{rel_id}/mix_timeseries.json | Lambda | Edge + API GW + Lambda | Yes | Low |
      | ... | | | | |

      For HIGH risk paths, recommend mitigation (per P4 PRD Known Risk Areas section 2).
    </requirement>

    <requirement id="3">
      Produce a single deliverable covering both audits with clear PASS/FAIL/RISK ratings.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>docs/briefs/ADVI_49PUSH_P4_auth_audit.md -- pseudonymization diff + book scoping risk matrix</deliverable>
    <deliverable>Message to COO with risk summary: how many HIGH risk paths, recommended mitigations</deliverable>
  </deliverables>
</task_order>
