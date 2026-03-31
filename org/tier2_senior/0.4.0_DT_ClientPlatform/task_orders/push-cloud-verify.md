# Task Order: Push and Verify CLOUD Branch

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-push-verify</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <!-- Verified 2026-03-26: origin/CLOUD at 6df73d10, all TICKID+GLDRST commits present. AE completed combined gold run. -->
  </metadata>

  <objective>
    Verify that all CLOUD commits are on origin. As of COO check, origin/CLOUD
    matches local CLOUD at 1f69d98f. Confirm this is still true, then notify AE
    that code is ready for S3 upload.

    NOTE: If origin/CLOUD is behind local, push. If already at parity, just
    confirm and message AE.
  </objective>

  <requirements>
    <requirement id="1">
      Check push state:
        git log --oneline origin/CLOUD..CLOUD

      If empty: origin is up to date. Proceed to Req 3.
      If commits listed: push them:
        git push origin CLOUD
    </requirement>

    <requirement id="2">
      Verify these key commits are on origin:
        git log --oneline origin/CLOUD | grep -E "(TICKID|GLDRST|exclusions|ghost)"

      Expected commits (at minimum):
      - 0253186a TICKID.007
      - da272777 TICKID.006
      - 76c26f33 TICKID.005
      - 8d04e167 GLDRST.001
      - 54d1f988 ghost_account_ids fix
    </requirement>

    <requirement id="3">
      Send go signal to AE:

      send_message(
        from="0.4.0_DT_ClientPlatform",
        to="0.6.0_AE_PartnerETL",
        subject="CLOUD push verified -- proceed with GLDRST.002 combined run",
        body="origin/CLOUD confirmed at {commit}. All TICKID + GLDRST commits present.
              You are clear to upload scripts to S3 and begin the combined run."
      )
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">origin/CLOUD contains all TICKID + GLDRST commits</criterion>
    <criterion id="2">AE notified via send_message</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT commit or push any uncommitted working tree changes. The " M" files in gold/silver scripts are GLDRST P3 prep and must NOT be pushed yet.</constraint>
    <constraint>This is a verification + notification task only. No code changes.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="message">GO message to AE confirming push state</deliverable>
  </deliverables>
</task_order>
