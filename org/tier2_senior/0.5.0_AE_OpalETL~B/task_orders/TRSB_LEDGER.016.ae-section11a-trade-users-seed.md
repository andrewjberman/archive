<task_order>
  <metadata>
    <id>TRSB_LEDGER.016</id>
    <slug>ae-section11a-trade-users-seed</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GATE CLEARED + GO'd 2026-05-20 by COO~B. TRSB_LEDGER.015 probe COMPLETE -- P1 finding: the andrew@opalinvest.com trade-users row carries exactly 6 attributes -- active (BOOL), created_at (S), email (S), groups (L = [approvers, executors]), name (S), role (S = dev). §11-A replicates this 6-attribute shape for menachem@, substituting only the identity fields (email, name, and a fresh created_at); groups + role + active identical to andrew@. Use 0.5~B's .015 verbatim capture (session log org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-05-20/trsb_ledger_015_section11_menachem_probe.md) as the authoritative shape -- do not hand-construct.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P2 -- TRSB §11-A. Seeds menachem@opalinvest.com into trade-users with andrew@-mirror authority. Together with §11-B (.017) it discharges §11; TRSB_LEDGER then needs only .012 (Andrew :5175 gate) to 3-step-close.</priority>
    <sla>~0.5-1h AE wall -- a single direct DDB write replicating a captured row shape.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md §11.2-A + §11.1 (privilege baseline) + §11.3 (SoD consequence -- recorded decision of record, not an oversight) + §11.4 (scope notes -- direct write, does NOT revive the dropped TO-7 productized-management path).</prd>
    <gate_input>TRSB_LEDGER.015 probe P1 output -- the verbatim andrew@opalinvest.com trade-users row shape.</gate_input>
  </references>

  <context>
    Andrew directive 2026-05-20: menachem@opalinvest.com gets the same trade authority as andrew@. §11-A is the trade-users seed: one direct-write record for menachem@ mirroring andrew@ exactly -- groups = ['approvers','executors'], role = 'dev'. The dev role confers the segregation-of-duties bypass (§11.3) -- intentional and explicit per the "same privileges as andrew@" directive; recorded as a decision of record.
  </context>

  <scope>
    <step>P1 -- construct the menachem@ record from the .015 probe's verbatim andrew@ row shape. Replicate EVERY attribute andrew@ carries (groups, role, and any others), substituting only the identity fields (the email / user-id key). Do NOT hand-construct or guess the shape -- use the probe's captured read. groups = ['approvers','executors'], role = 'dev' confirmed against §11.1.</step>
    <step>P2 -- direct-write the menachem@opalinvest.com record to the trade-users DynamoDB table (the §11.2-A / §11.4 "seeded by direct write" path -- this does NOT revive the dropped TO-7 productized-management UI). A targeted put_item for the single new row; do not touch andrew@'s row.</step>
    <step>P3 -- verify: read back the menachem@ row, confirm it matches the intended shape attribute-for-attribute; confirm andrew@'s row is byte-unchanged (no collateral write).</step>
    <step>P4 -- RAVC2 to 2.0.0_SA_COO~B (CC 1.0.0_SA_CTO~B): the written row, the read-back verification transcript, the andrew@-unchanged confirmation. Session log with Compiler Tools section.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">A trade-users record for menachem@opalinvest.com exists, mirroring andrew@'s row shape exactly (every attribute replicated from the .015 probe read), groups = ['approvers','executors'], role = 'dev'.</ac>
    <ac id="AC2">Read-back verification transcript captured -- the written row matches intent attribute-for-attribute.</ac>
    <ac id="AC3">andrew@'s trade-users row is unchanged (no collateral write).</ac>
    <ac id="AC4">No emoji. Session log with Compiler Tools section. RAVC2 to COO~B CC CTO~B.</ac>
  </acceptance_criteria>

  <out_of_scope>
    Email-recipient changes (§11-B / .017). Portal-auth account (§11-D). Productized trade-users management UI (dropped TO-7 -- §11.4 explicitly does NOT revive it). Any change to andrew@'s row or other trade-users rows.
  </out_of_scope>

  <deliverables>
    - menachem@opalinvest.com trade-users row seeded by direct write; read-back + andrew@-unchanged verification; RAVC2 to COO~B CC CTO~B; session log.
  </deliverables>
</task_order>
