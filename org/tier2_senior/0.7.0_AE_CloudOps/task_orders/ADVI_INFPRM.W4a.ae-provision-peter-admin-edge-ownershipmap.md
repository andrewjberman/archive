<task_order>
<metadata>
  <to_id>ADVI_INFPRM.W4a</to_id>
  <project>ADVI_INFPRM</project>
  <title>AE: provision Peter firmRole=admin (IMMEDIATE Segment-403 unblock) + confirm edge admin-path + the inflection ownership_map need (produce if required)</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>DISPATCHED — IMMEDIATE (gates Andrew's Segment-drill re-smoke). W4(a)+(c)+(d) of the access-model. CTO scoped DT for (a) but DT OFFLINE -> routed to AE (DynamoDB = CloudOps domain; AE traced the exact record). CC DT for lane-awareness.</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct; (a) is the smallest/highest-leverage fix + gates the Segment relationship-drill re-smoke.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFPRM.md sec.3.W4 (a/c/d) + AC4 (d2c96bb1b)</ref>
    <ref type="record">opal-users-v2 PK=USER#peter@inflectionwealth.com SK=PROFILE (currently role=user, firmRole=null, advisorId=null, tier=advisor, firmId=inflection)</ref>
    <ref type="edge">auth-validator-edge:312 (admins EXEMPT from advisorId requirement; non-admin + empty advisorId -> 403)</ref>
    <ref type="ownership_map">platinum/inflection/ownership_map.json (AE flagged ABSENT -> getOwnershipMap 503 fail-closed)</ref>
  </references>
</metadata>

<scope>
Andrew ruled: admins (Peter) see the full Books/ tab (advisor list + Firm Overview + BI + relationship drills); non-admins (Patrick/Joe) = Profile-tab-only (W4b, RD~C). The Segment "No relationship-level data" 403 root = Peter is provisioned NON-admin (firmRole=null) + edge requires advisorId for non-admins. THREE AE legs:

## (a) PROVISION Peter firmRole=admin [IMMEDIATE]
Update opal-users-v2 PK=USER#peter@inflectionwealth.com SK=PROFILE -> set firmRole=admin (single-field add; role/tier/firmId unchanged; advisorId stays null — admins are edge-exempt from it). This makes isFirmAdmin=true (inflection/index.tsx:128) + passes the edge admin-path -> his relationship/client/account drills stop 403'ing. Do NOT set advisorId=peter_lee (that's the wrong fix per the access-model). Patrick/Joe stay firmRole=null (non-admin) — do NOT touch their records. If opal-users-v2 has a provisioning process/script (vs raw PutItem) DT normally runs, use it / flag if AE shouldn't raw-write; else a scoped single-field UpdateItem is fine (low-risk, CTO-traced).

## (c) CONFIRM edge admin-path + ownership_map need
After (a): confirm Peter-as-admin passes auth-validator-edge:312 (admin-exempt) for the relationship-drill endpoints (getPlatinumClientSummary / relationship platinum-summary). AND determine: does the admin relationship-drill ALSO need the inflection ownership_map.json (you flagged it ABSENT -> getOwnershipMap 503 fail-closed)? Test the actual drill path for admin Peter end-to-end (does it 200 with data, or 503 on the missing ownership_map?).

## (d) PRODUCE ownership_map IF (c) needs it
If the admin relationship-drill requires platinum/inflection/ownership_map.json + it's absent -> produce it (or route DS if it's a data-production artifact, not a config). Gated on (c)'s finding.
</scope>

<acceptance>
- [ ] AC-W4a — Peter opal-users-v2 firmRole=admin (verified record read-back); isFirmAdmin=true. Patrick/Joe untouched (non-admin).
- [ ] AC-W4c — edge admin-path confirmed: Peter-as-admin's relationship/client drills pass the 312 gate (no 403); ownership_map need determined (needed/not-needed, with the live-drill evidence).
- [ ] AC-W4d (conditional) — if needed, inflection ownership_map.json produced + the admin drill 200s with data.
- Deploy/data per CLAUDE.md rules; RAVC2 to CTO+COO+CVO. This is the IMMEDIATE Segment-drill unblock for Andrew's re-smoke — report the moment (a) lands so Andrew can re-smoke the Segment relationship-data.
</acceptance>

<notes>
Decomposed by COO from CTO PRD §3.W4 (Andrew-direct d2c96bb1b). (a) is the immediate highest-leverage unblock. (b) FE non-admin-Profile-only -> RD~C (separate TO). RD~B's earlier Segment :1951 firmId-add is HELD/likely-subsumed by (a). DT offline -> AE owns the DynamoDB provisioning (its domain); CC DT. Coordinate with RD~C (W4b) — together (a)+(b) deliver Andrew's full admin/non-admin model. CC DT + RD~C + DS + CTO + CVO.
</notes>
</task_order>
