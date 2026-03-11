# Task Order: ADVI_PSCFIX A3 — Script 09 Certified AUA Override

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-advi-pscfix-a3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-11</date>
    <status>complete</status>
  </metadata>

  <objective>
    Add certified_aua override to 09_generate_partner_analytics.py so that the
    current-period donut totals for the aua, geo, and adv views in
    partner_analytics/header_metrics_{gran}.json reflect certified_aua rather
    than gold-derived totals. This is the final unimplemented item from
    ADVI_PSCFIX PRD Deliverable 3 Acceptance Criterion 5.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/09_generate_partner_analytics.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add _load_aua_certification() helper to 09_generate_partner_analytics.py.
      Identical non-blocking pattern to 05d and the publisher Lambda:

        def _load_aua_certification(s3_client, bucket: str, today_str: str):
            key = f"gold/aua_certification/{today_str}.json"
            try:
                resp = s3_client.get_object(Bucket=bucket, Key=key)
                data = json.loads(resp['Body'].read())
                print(f"  OK: aua_certification loaded: certified_aua={data.get('certified_aua'):,.2f}")
                return data
            except Exception as e:
                print(f"  OK: aua_certification absent ({e}) -- using gold totals")
                return None

      Load it once near the top of the main run function, before the period loop:
        cert = _load_aua_certification(s3, S3_BUCKET, today.strftime('%Y-%m-%d'))
    </requirement>

    <requirement id="2">
      In the period loop (around line 1538), after aua/geo/adv views are built for
      EACH period, apply the cert override ONLY to the CURRENT (in-progress) period.
      The current period is the last iteration — identifiable by its date being the
      latest perf snapshot date.

      After the three view assignments (aua, geo, adv) inside the loop:

        # ADVI_PSCFIX: override current-period donut totals with certified_aua
        if cert and is_current_period:
            certified = cert['certified_aua']
            views['aua'][period_key]['donut']['total'] = round(certified, 2)
            views['geo'][period_key]['donut']['total'] = round(certified, 2)
            views['adv'][period_key]['donut']['total'] = round(certified, 2)
            print(f"  OK: cert override applied to {period_key} -- "
                  f"donut totals set to certified_aua={certified:,.2f}")

      How to identify is_current_period: the loop already has access to the period
      snapshot date (ts / period_info['date']). The current period is the one where
      ts == the maximum snapshot date available. Add a simple flag:
        is_current_period = (ts == max(period_dates))
      where period_dates is the list of dates being iterated. Confirm the right
      variable name by reading the loop structure before implementing.

      Historical periods: NOT overridden. Only the current in-progress period.
    </requirement>

    <requirement id="3">
      Deploy to EC2 using safe-ec2-deploy.sh for the bd-gold-layer-runner service.
      Same deploy path as A1 (05d). Upload script 09 to S3:
        s3://opal-data-bd/code/gold/09_generate_partner_analytics.py
      Then trigger or wait for the next gold pipeline run to verify.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      partner_analytics/header_metrics_{gran}.json for the current period:
        views.aua.current.donut.total == certified_aua
        views.geo.current.donut.total == certified_aua
        views.adv.current.donut.total == certified_aua
      Verify with:
        aws s3 cp s3://opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json - \
          | python -c "import sys,json; d=json.load(sys.stdin); print(d['views']['aua']['current']['donut']['total'])"
    </criterion>
    <criterion id="2">
      Historical period donut totals unchanged — only current period overridden.
    </criterion>
    <criterion id="3">
      When gold/aua_certification/{today}.json is absent: script runs normally,
      gold-derived totals used, no error.
    </criterion>
    <criterion id="4">
      EC2_MANIFEST.json updated by safe-ec2-deploy.sh after upload.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Non-blocking: cert load must not raise. Wrap in try/except, return None on any failure.</constraint>
    <constraint>Override applies to current period ONLY. Historical periods are untouched.</constraint>
    <constraint>Do NOT override segment-level aua values in donut segments — only the top-level
    donut.total field on each view.</constraint>
    <constraint>Deploy via S3 artifact model — repo -> S3 -> EC2 pull. Never edit on EC2 directly.</constraint>
    <constraint>No emojis in code or log output. Use OK:, SKIP:, WARN:, ERROR: prefixes.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL"
                task="ADVI_PSCFIX.A1.aua-certification-script.md"
                status="complete"
                note="05d is live and producing gold/aua_certification/{date}.json after each
                nightly run. A3 depends on those JSONs existing to activate the override.
                Override is non-blocking so A3 can be deployed before a cert JSON exists."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">09_generate_partner_analytics.py — _load_aua_certification + current-period donut override</deliverable>
    <deliverable type="deploy">Script deployed to S3, EC2_MANIFEST.json updated</deliverable>
    <deliverable type="verify">header_metrics_quarterly.json current-period donut totals spot-checked</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_PSCFIX_PRD.md — Deliverable 3, Acceptance Criterion 5</ref>
    <ref type="precedent">data/black_diamond/scripts/gold/05d_write_aua_certification.py — cert load pattern</ref>
    <ref type="source">data/black_diamond/scripts/gold/09_generate_partner_analytics.py — period loop ~line 1530</ref>
  </references>
</task_order>
```
