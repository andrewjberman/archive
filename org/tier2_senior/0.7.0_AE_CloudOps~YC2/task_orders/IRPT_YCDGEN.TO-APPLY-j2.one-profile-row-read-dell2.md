<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-j2.one-profile-row-read-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~YC2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- one read of one table item; no schedule, trigger or rule is added or read
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the read uses the grant this lane's swap_svc_firm.py reads used in windows 6 to 9, on the same table
comp-adversary: RUN -- read 1 script (read_profile_firms.py, 46 lines by wc: one get_item with a four-name ProjectionExpression, no write call) and 1 code path (served.py lines 1063-1066, the on-behalf rule the answer feeds); NOT seen: the row itself, which is the point of the read. Traps: reading another attribute of a person's row; reading the wrong user; taking an absent attribute for an empty list (the script prints the shape)
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R11.md</decomp_doc>
<owned_cells>YCD-d-11</owned_cells>
<decomp_context>The journey read (TO-YCD-a-11, deliverables/0.9.0_WK_IRPT_YCDGEN~14/JOURNEY_READ_YCD-a-11.md, hop 5) could not determine row IRPT_YCDGEN-D2-S4 for Andrew: an on-behalf upload needs a named advisor only when the tenant is in the filer's allowedFirmIds (served.py lines 1063-1066). Whether his own profile row names cottonwood decides which rule his Prospect upload takes.</decomp_context>
</decomp_ref>

  <objective>
    ONE read-only get of ONE item: the PROFILE row of andrew@opalinvest.com in opal-users-v2, four attributes by name
    (allowedFirmIds, status, userType, firmId). It says whether that row names cottonwood.
  </objective>

  <the_act>
    AMENDMENT 1 (issuer 2.0.0_SA_COO~G2, 2026-10-11): the first read printed PROFILE-ROW-ABSENT, and that answer is VOID. It
    was the issuer's script defect: it assumed a person's key is USER#<email>, which holds for a service row; the product
    finds a user through the email index (_scope/canonical_profile_reads.py get_user). The script now does the same: ONE
    query on index email-index (Limit 2), then ONE get_item by the PK the index names. Re-run step 1 with the amended
    script and save the output as PROFILE_FIRMS_READ_2_20261011.txt; keep the first file. Bounds widen by exactly that one
    index query on the same table. If the query is refused for your identity, save the error class and stop: that is the
    finding. Criteria AC1 and AC2 now read the second file.
    1. From the repo root: python org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r11/read_profile_firms.py andrew@opalinvest.com cottonwood
    2. Save its full output as PROFILE_FIRMS_READ_20261011.txt in your deliverables folder irpt_ycdgen_j2/, with the UTC time of
       the read on its first line.
    3. Message 2.0.0_SA_COO~G2 the file path. No write to the table, no other user, no other attribute, no retry with a
       wider projection. If the script errors, save the error class and stop.
  </the_act>

  <bounds>ONE query on the email index (Limit 2) and ONE get_item on the key it names, four named attributes. No write, no scan, no other table, no secret read.</bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j2/IRPT_YCDGEN.TO-APPLY-j2.one-profile-row-read-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-d-11">The read states the row or its absence.<invocation>grep -m1 -E '^(PROFILE |PROFILE-ROW-ABSENT |USER-NOT-IN-INDEX |USER-AMBIGUOUS-IN-INDEX )' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j2/PROFILE_FIRMS_READ_2_20261011.txt</invocation><expect>^(PROFILE andrew@opalinvest\.com status=|PROFILE-ROW-ABSENT andrew@opalinvest\.com|USER-NOT-IN-INDEX andrew@opalinvest\.com|USER-AMBIGUOUS-IN-INDEX andrew@opalinvest\.com)</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-d-11">The read answers the firm question, or records the row's absence.<invocation>grep -m1 -E '^(FIRM-NAMED cottonwood (YES|NO)|PROFILE-ROW-ABSENT |USER-NOT-IN-INDEX |USER-AMBIGUOUS-IN-INDEX )' org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j2/PROFILE_FIRMS_READ_2_20261011.txt</invocation><expect>^(FIRM-NAMED cottonwood (YES|NO)$|PROFILE-ROW-ABSENT andrew@opalinvest\.com|USER-NOT-IN-INDEX andrew@opalinvest\.com|USER-AMBIGUOUS-IN-INDEX andrew@opalinvest\.com)</expect></criterion>
  </proof_of_spec>
</task_order>
