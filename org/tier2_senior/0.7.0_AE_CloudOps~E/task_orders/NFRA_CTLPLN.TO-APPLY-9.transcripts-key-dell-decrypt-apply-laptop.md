<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-9.transcripts-key-dell-decrypt-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-07</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc> (workstream ACCESS, round 1): the apply leg of cell `CT-a-1` as amended (AMENDMENT 3, the transcripts key; complete as a build, merged @5d321bfc0a).
<owned_cells>CT-a-1</owned_cells>
</decomp_ref>

  <objective>
    Apply ONE targeted update of ONE key policy so the two Dell box users can DECRYPT objects in the meeting-transcripts store.
    Their own policies already allow the object read; today only the key stops them. After this act both can read the whole
    store, the raw tier included. That width is signed by both halves on Andrew's recorded answer.
  </objective>

  <context>
    Root `infra/aws/terraform/transcripts/`, resource `aws_kms_key.transcripts`. The change is one statement in the key policy,
    Sid `DellAgentUsersDecryptOnly`: `kms:Decrypt` and `kms:DescribeKey` for the two Dell agent users (commit 74320c91b2). The
    existing reader statement is untouched.
    TWO FACTS ABOUT THIS ROOT, both measured by the issuer at ~18:2xZ, both in both halves:
    (1) UNTARGETED, the root plans `9 to add, 4 to change, 0 to destroy`: another project's unapplied pull function with its
        role, policy, rule, target, log group, permission and grant, and four updates. NONE of it is yours to apply.
    (2) In the shared tree `terraform init` fails with "Backend configuration changed": the root's own `.terraform` directory
        holds a backend record that differs from the backend block in `main.tf`. Do NOT run `init -reconfigure` or
        `init -migrate-state` in that directory: it is another project's root. The issuer planned with the environment variable
        `TF_DATA_DIR` set to a scratch directory outside the repository, which initialises against the backend `main.tf`
        declares and leaves the root's own `.terraform` untouched.
    Targeted at the key, the issuer's plan read `0 to add, 1 to change, 0 to destroy`, 11 added lines, 0 removed.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED and each binds on the plan shape below. ONE go, no second message.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_TRANSCRIPTS_KEY_DELL_DECRYPT_20261007.md (@e18f0f8d3f)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_TRANSCRIPTS_KEY_DELL_DECRYPT_20261007.md (@091b68b282)
    Read both in full first and carry every condition of both (six, and the CTO's 7 to 9). "An untargeted apply voids the half."

    COO CONDITION 6, BEFORE THE APPLY: both Dells are told, in one line, what they may now read and how the raw tier is handled.
    `1.0.0_SA_CTO` asked `0.0.0_AB_MSTR` to relay it (msg 106494). You do not message a Dell. Before step 5, show from the fabric
    manager's relay record under `org/tier0_exec/0.0.0_AB_MSTR/deliverables/`, or by asking `0.0.0_AB_MSTR` once, that the line
    reached both Dells' managers. If you cannot show it, STOP before the apply and report.

    THE COMMIT: the shared tree at its HEAD on CLOUD. `git diff --stat 5d321bfc0a HEAD -- infra/aws/terraform/transcripts/main.tf`
    prints nothing and the file is unmodified in the working tree. A difference is a STOP.

    1. Load /cloud-ops. Run `python infra/aws/terraform/transcripts/tests/check_transcripts_dell_decrypt.py` immediately before the
       plan; record its last line (expect `dell_decrypt=2/2 dell_write_refused=10/10 reader_unchanged=True unlisted_refused=True statements_added=1 ok=True`).
       A failing check is a STOP.
    2. Set `TF_DATA_DIR` to a NEW scratch directory outside every git tree and run `terraform -chdir=infra/aws/terraform/transcripts
       init -input=false`. If `init` asks to migrate or reconfigure state, or reports any backend other than the one `main.tf`
       declares, STOP. Print the backend bucket and key it initialised against. Every later Terraform call in this order uses
       the same `TF_DATA_DIR`. Confirm afterwards that the root's own `.terraform` directory is byte-unchanged (hash its
       `terraform.tfstate` before and after).
    3. BEFORE: save the LIVE key policy (`kms get-key-policy` on the key behind the bucket's alias) with its SHA-256: the
       rollback reference. List nothing in the bucket.
    4. Plan TARGETED at exactly `aws_kms_key.transcripts` (echo the argument back), with the state lock taken (no `-lock=false`).
       - EXACTLY `0 to add, 1 to change, 0 to destroy`, that one address; the diff is ONE added statement, Sid
         `DellAgentUsersDecryptOnly`, Effect Allow, actions exactly `kms:Decrypt` and `kms:DescribeKey`, principals exactly the
         two Dell agent users' ARNs, Resource `*`; ZERO removed lines; the `NamedReadersUseTheKey` statement unchanged -> go to 5.
       - ANY other resource, action, principal, removed line or count -> apply NOTHING; report the plan as read and stop.
    5. Open ONE NEVER-2 ledger entry naming the laptop, the saved key policy by path and hash, both halves, and the rollback (put
       the saved policy back, or revert the statement and the same targeted apply; never an empty principal list).
    6. ONE apply through `.tools/safe-apply.sh`, TARGETED at the same one address, with the same `TF_DATA_DIR`. If the wrapper
       cannot be made to use the scratch data directory or the target, STOP and report rather than apply any other way.
    7. Read-back LIVE: the live key policy equals the saved one plus exactly the one statement (parsed, with a planted-mutant
       control); the check script's arms against the LIVE policy, both its readings printed (under the key rule and raw); a
       targeted re-plan reads no changes; an UNTARGETED plan (read-only, `-lock=false`) still reads `9 to add` and now
       `3 to change`: report its counts, apply none of it. Close the entry.
       You read NO transcript object, list NO key of the bucket and make NO decrypt call. The exercised read is a Dell's own, by
       another route; until it runs the grant is APPLIED, not EXERCISED: say so in those words.
  </the_act>

  <bounds>
    - This one resource only. NEVER an untargeted apply of this root. No `init -reconfigure`, no `init -migrate-state`, no write
      to the root's own `.terraform` directory, no edit to any file of the root.
    - `safe-apply` only. No push of a shared branch. No object read, no bucket listing, no decrypt.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's check on the rendered key policy (decrypt allowed for both Dell users; ten write and administration arms refused under the key rule, six of ten on the raw simulator, both printed; an unlisted user refused; a mutant with encrypt added fails) and re-run by the applier immediately before the plan; step 7 repeats it against the LIVE policy.
comp-adversary: RUN -- another project's nine additions and four changes applied by accident (targeted plan and targeted apply only; an untargeted apply voids both halves; the untargeted count is re-read after and must be unchanged but for the key); a state migration triggered in another project's root (a scratch data directory; any migrate or reconfigure prompt is a stop; the root's own record hashed before and after); a wider statement than signed (the plan's statement classified field by field); no way back (the live key policy saved before); a Dell surprised by what it can now read (the line shown before the apply); BLIND: a real decrypt, live grants on the key, and whether a Dell put fails at the key in practice (the Dell's own exercised read; the CTO's ninth condition restores on a put that succeeds).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/transcripts/tests/check_transcripts_dell_decrypt.py</invocation><expect>dell_decrypt=2/2 dell_write_refused=10/10 reader_unchanged=True unlisted_refused=True</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1" judgment="true"/>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): how condition 6 was shown; the check line;
    the backend initialised against and the proof the root's own `.terraform` is unchanged; the saved key policy's path and hash;
    the targeted plan's count and the statement as read, field by field; how the apply was targeted through the wrapper; the
    live comparison and both simulator readings; the targeted re-plan's result and the untargeted plan's counts (the judgment
    criterion AC2 is the issuer's and the CVO's to grade from these: do not mark it PASS or FAIL); the ledger entry's path and
    close; the proof-of-spec instance path (genre DEPLOY) and its check result; commit hashes and the measured push state. Leave
    the status flip to the issuer.
  </report>
</task_order>
