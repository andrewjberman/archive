# Task Order: NFRA_WEBSITE TO-2 -- cut the migrated WordPress site over to `opalinvest.com` (STAGING FIRST)

> **THIS IS THE LIVE TO FOR NFRA_WEBSITE. TO-1 (W1 platform) is COMPLETE and its cutover plan is VOID --
> it was written on `opalcapital.com`, a domain Opal DOES NOT OWN.**
>
> **The platform is built. The site is migrated and serving. Only the DNS cutover remains,
> and it is blocked on a human (GoDaddy access), not on AWS.**

```xml
<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-07-13-nfra-website-to2-opalinvest-cutover</id>
    <issued_by>0.7.0_AE_CloudOps (self-authored under Andrew-direct exclusive assignment; COO to ratify/own the GO)</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-07-13</date>
    <status>pending -- PHASE A EXECUTED + VERIFIED 2026-07-14 (A1 record added by Patricia/TWLC, verified live; A2-A5 done: blog_public=0, re-key 943/943 residual 0, LE cert to 2026-10-12, stage-wire + strict verify GREEN on-box AND external; ledger 20260714T1748Z closed 7/7). AT A6 ANDREW+TWLC SIGN-OFF GATE on https://new.opalinvest.com/ . PHASE B only on Andrew's explicit word.</status>
    <dispatch_state>ANDREW-DIRECT 2026-07-13: "You will be working exclusively on the NFRA_WEBSITE task." Andrew chose STAGING-FIRST over a direct apex cutover. Supersedes the W3 plan in TO-1.</dispatch_state>
    <gate_note>
      SOVEREIGN DOMAIN CORRECTION (Andrew-direct 2026-07-13, VERBATIM):
        "it needs to be opalinvest.com. I thought Patricia said opalcapital.com, that we were switching to
         this URL from opalinvest.com, but that was incorrect. We need to build around opalinvest.com"
        "We do not even own opalcapital.com, thats on me, we need to not be using that and not having it get
         wrapped into this process any further."
        "opalinvest.dev is my temporary url for the dashboard, the official website is opalinvest.com"
      opalcapital.com is PURGED from the estate; its SES DOMAIN SENDING IDENTITY was DELETED 2026-07-13.
    </gate_note>
  </metadata>

  <context>
    STATE (measured live 2026-07-13, not from memory):
      - Box i-0152e3fe2599fa630 (t3.small, Opal VPC), EIP 18.208.18.213. OLS + lsphp82 + MariaDB all UP.
      - It SERVES THE REAL MIGRATED SITE: WP 7.0.1, theme `bricks-opal`, title "Opal Capital | Investment
        Platform for Independent Advisors". TWLC's dev completed the content migration.
      - SES transactional email WORKS: instance-role sendmail shim, sender locked to noreply@opalinvest.dev
        by an ses:FromAddress condition. Exercised end-to-end. No stored secret.
      - Nightly DB + wp-content backup to s3://opal-website-backups is RUNNING (DB dumps through 2026-07-13).
      - certbot installed; HTTP-01 webroot armed + verified.

    >> TWO HAZARDS THAT DID NOT EXIST UNDER THE OLD (WRONG) DOMAIN. BOTH MEASURED LIVE. <<

    (1) THE APEX IS NOT AN EMPTY TARGET. opalinvest.com + www serve a LIVE Wix site ("Home | Opal")
        at 185.230.63.107 / .171 / .186. THE FLIP REPLACES OPAL'S PUBLIC WEBSITE. It is a go-live.
        ROLLBACK = point the apex A back at those Wix IPs. Wix stays up + untouched the entire time.
        (The 72.167.58.121 host TO-1 called "the rollback point" is on opalcapital.com and is NOT ours.)

    (2) opalinvest.com CARRIES OPAL'S LIVE MICROSOFT 365 EMAIL:
          MX     -> opalinvest-com.mail.protection.outlook.com
          TXT    -> v=spf1 include:mailgun.org include:spfa.cpmails.com include:spf.protection.outlook.com ~all
          CNAME  -> selector1._domainkey / selector2._domainkey  (M365 DKIM)
          CNAME  -> autodiscover -> autodiscover.outlook.com
          TXT    -> _dmarc
        >> AT GODADDY, TOUCH ONLY THE APEX `A` AND `www`. NOTHING ELSE. EVER. <<
        A well-meaning "clean up the old Wix records" KILLS COMPANY MAIL. The website records and the mail
        records are DISJOINT -- an A-record change requires touching none of them. Keep them disjoint.

    (3) apex A TTL is ~86400s (1 day). It MUST be lowered to 600 24-48h BEFORE any flip, or a rollback
        takes a day to propagate.

    (4) WORDPRESS IS KEYED TO THE RAW IP: siteurl = home = http://18.208.18.213, and 943 DB rows carry it.
        bootstrap-stack.sh ASSUMED TWLC's dev would search-replace it. THEY DID NOT. Left as-is, the moment
        the apex resolves here WP 301s every visitor to a bare IP over plain HTTP. Bricks stores absolute
        URLs inside SERIALIZED builder data -> this MUST be `wp search-replace` (re-serializes correctly),
        NEVER a raw SQL UPDATE.
  </context>

  <objective>
    Serve the migrated WordPress site at https://opalinvest.com (+ www) with a trusted, auto-renewing
    certificate, replacing the Wix site -- without a single minute of certificate-warning downtime, and
    WITHOUT disturbing Opal's company email.
  </objective>

  <blocking>
    THE CRITICAL PATH IS A HUMAN, NOT AWS. GoDaddy DNS for opalinvest.com. Andrew does NOT hold the sign-in;
    CFO AJ GRAFF does. Route via Andrew -- do NOT contact AJ directly (MSTR-directed).
    The ask: `infra/website/GODADDY_DNS_REQUEST_opalinvest.md` (written for a non-engineer; one additive
    record unblocks the entire staging phase, plus a loud do-not-touch list for the mail records).
  </blocking>

  <steps>
    PHASE A -- STAGING. Wix, the apex, and company email are ALL untouched. Nothing public changes.
      A1. [BLOCKED-EXTERNAL] GoDaddy adds ONE additive record:  A / `new` -> 18.208.18.213, TTL 600.
      A2. WP staging hygiene: set blog_public=0 (do NOT let the staging copy get crawled as duplicate content).
      A3. Re-key WP off the raw IP -> https://new.opalinvest.com  (wp search-replace, --dry-run FIRST for the
          count, then live; take a fresh backup immediately before -- 943 rows of serialized data).
      A4. `tls-cutover.sh stage-issue`  -- HTTP-01 (valid here: `new` DOES resolve to the box).
      A5. `tls-cutover.sh stage-wire`   -- wires OLS + STRICT-verifies (never -k).
      A6. Andrew + TWLC review https://new.opalinvest.com/ -- the real site, real HTTPS, real domain. SIGN-OFF GATE.

    PHASE B -- APEX CUTOVER. Only on Andrew's explicit word.
      B1. Re-key WP `new.` -> https://opalinvest.com. ASSERT zero residual `new.opalinvest.com` rows.
      B2. [ADMIN_EMAIL GATE -- CLOSED 2026-07-13, verified live] DONE. admin_email was `mike@hirst.digital`
          (external); it is now `andrew@opalinvest.com`. Verified by re-read, not by the wp-cli success line.
          >> AND THE DB HELD A LIVE RE-HIJACK SLOT: WordPress parks an UNCONFIRMED admin-email change in the
          `new_admin_email` option, and it contained `mike@hirst.digital` with an outstanding confirmation
          link. ANYONE CLICKING THAT LINK WOULD HAVE SILENTLY FLIPPED admin_email BACK to the external
          address, undoing the fix with no trace. DELETED; verified NONE. <<
          LESSON: fixing `admin_email` alone was NOT sufficient -- the setting had a SHADOW that would have
          restored the defect. A control is not closed until its shadow state is closed too.

      B2a. [ADMIN ACCESS -- ANDREW-RULED 2026-07-13, DEFERRED TO GO-LIVE ON PURPOSE. DO NOT ACT EARLY.]
          Andrew, verbatim: *"that's fine, we can cross that bridge when we get to it. The only admin that
          matters is me and patricia@whitelabelcreative.com, the rest we can add if Patricia wants it."*
          TARGET STATE AT GO-LIVE (not now):
            KEEP   opaladmin            andrew@opalinvest.com                 (Opal)
            KEEP   patricia@thewhitelabelcreative.com                         (TWLC lead)
            DROP   mike                 mike@extonwebdesign.com               (re-add ONLY if Patricia asks)
            DROP   Lindsay@thewhitelabelcreative.com                          (re-add ONLY if Patricia asks)
          WHY DEFERRED, and this is a real reason not a stall: mike + Lindsay may be MID-MIGRATION. Removing
          a working dev's admin before the site is cut over breaks their work to fix a problem that is not
          yet live. The exposure only becomes real AT THE FLIP, which is exactly when this gets actioned.
          NOTE: three distinct vendor domains are in play (@extonwebdesign.com, @thewhitelabelcreative.com,
          and the old admin_email @hirst.digital) -- confirm identities with Patricia before removing, do not
          infer from a name. DEMOTE (role -> none) before DELETE: deleting a WP user forces a content
          reassignment prompt and can orphan authored posts.
      B3. Lower apex A + www TTL -> 600. WAIT 24-48h.
      B4. `tls-cutover.sh issue` (+ `show-txt` from a SECOND SSM call) -- DNS-01, covering apex + www + new.
          HTTP-01 CANNOT work here: the apex still resolves to WIX, so LE cannot reach the box to validate it.
      B5. `tls-cutover.sh wire` -> `tls-cutover.sh verify`. Strict TLS pinned to the box + a positive control
          + SAN coverage ASSERTED for BOTH apex and www. THIS IS THE GO/NO-GO GATE. It fails closed.
      B6. FLIP the GoDaddy apex A + www -> 18.208.18.213.
      B7. ASSERT blog_public=1 (a site that launches `noindex` is invisible to Google and nobody notices
          for weeks). This is an explicit assert, not a memory item.
      B8. `tls-cutover.sh convert-renewal` -- NOT OPTIONAL. A `--manual` DNS-01 cert CANNOT AUTO-RENEW;
          left alone it expires in 90 days with NO renewal path and the site breaks with nobody watching.
          The script REFUSES to run while the apex still resolves to Wix, so it cannot be run at the wrong time.
      B9. CVO live-verify the served site (pages/Bricks render, forms submit + email, TLS, no mixed content).
  </steps>

  <acceptance_criteria>
    AC-1  https://opalinvest.com/ and https://www.opalinvest.com/ return 200 over a STRICT TLS fetch
          (NO -k / --insecure -- that flag suppresses the exact failure being tested), from a machine that
          resolves them via public DNS, and the cert is a trusted LE cert whose SANs cover BOTH names.
    AC-2  `certbot renew --dry-run` SUCCEEDS on the box (proves the cert can actually auto-renew; a manual
          cert that passes today and dies silently in 90 days is a FAIL, not a pass).
    AC-3  ZERO rows in the WP DB contain `18.208.18.213` or `new.opalinvest.com`
          (`wp search-replace <needle> x --all-tables --dry-run --format=count` -> 0, for each).
    AC-4  EMAIL UNHARMED -- the decisive one. AFTER the flip, re-read the live zone and assert BYTE-IDENTICAL
          to the pre-flip capture: MX, the SPF TXT, selector1/selector2._domainkey, autodiscover, _dmarc.
          AND exercise it: send a real mail to an @opalinvest.com mailbox and confirm receipt. A config read
          is NOT sufficient here (Rule 22a: behavior claims are EXERCISED).
    AC-5  `wp option get blog_public` -> 1.
    AC-6  `wp option get admin_email` -> `andrew@opalinvest.com` **AND** `wp option get new_admin_email`
          -> absent/empty. BOTH, not just the first -- the shadow slot silently restores the defect, so an
          AC that checks only `admin_email` PASSES on a site that is one click from reverting.
    AC-8  ADMIN ROSTER (Andrew-ruled) = exactly `opaladmin` (andrew@opalinvest.com) +
          `patricia@thewhitelabelcreative.com`. Others re-added only if Patricia asks. Demote, don't delete.
    AC-7  ROLLBACK IS REAL, NOT ASSUMED: the Wix IPs are captured in the ledger BEFORE the flip, and the
          apex TTL is <=600 at flip time (so a rollback propagates in ~10 min, not ~24h).
  </acceptance_criteria>

  <compiler_tools_mandate>
    BEFORE WRITE : comp-which for any search; `comp-iam service` if any IAM changes (NECESSARY NOT SUFFICIENT
                   -- it models (action), never (action,resource); a new ARN needs live simulate-principal-policy
                   with ONE --resource-arns and a SEPARATE positive control).
    BEFORE COMMIT: .tools/commit-gate.sh (any .py); bash -n on every shell script; terraform validate + fmt.
    AFTER COMMIT : deploy-ledger open->close for the cutover; EC2_MANIFEST parity.
    NOTE (honest gap, carried from W1/W2): NO comp-tool models SES identities, DLM policy state, DNS/zone
    records, or on-box OLS/LSPHP/wp-cli state. These ride raw `aws`/SSM with `# rail-checked:` markers.
    That is a COVERAGE GAP, not a licence -- and it is exactly the blind spot in which the unowned-domain
    defect lived undetected for two weeks.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    NONE with the data estate -- and that is LOAD-BEARING, not incidental. This is a PUBLIC marketing surface;
    its instance role holds SSM-core + its own backup bucket ONLY, with ZERO data-estate/pipeline-bucket reach
    (firm-sep). Do not widen it. Do not give this box any pipeline IAM, ever.
    SHARED SURFACE = the opalinvest.com DNS zone, which the FIRM'S EMAIL also lives in. Any zone change is
    cross-domain with company email by construction. Coordinate with Andrew/MSTR before touching SPF.
  </cross_domain_coordination>

  <explicitly_out_of_scope>
    - SES SENDER GRADUATION to @opalinvest.com. It requires EDITING the existing SPF TXT. A SECOND SPF record
      is an RFC-7208 `permerror` -- a domain with two SPF records has NONE -- which degrades M365 mail
      FIRM-WIDE. One-line change, company-email blast radius. SEPARATE WINDOW, OWN VERIFICATION, TELL MSTR
      FIRST. The form works today on opalinvest.dev; this is NOT a launch blocker and must NOT be bundled in.
    - SES production-access support case (external form-submitter confirmations). Outward-facing; Andrew's word.
      The draft previously named opalcapital.com as "our website" -- corrected, still UNSUBMITTED.
    - Anything on opalcapital.com. WE DO NOT OWN IT. It is out of the process entirely.
    - Any redesign. HARD LEASH: lift-and-shift.
  </explicitly_out_of_scope>

  <deliverables>
    - The site live at https://opalinvest.com with an auto-renewing trusted cert.
    - A deploy-ledger entry opened at cutover-start and CLOSED at completion (NEVER#6 -- a begun deploy
      finishes in-session or rolls back and escalates loud).
    - A session log with a Compiler Tools section.
    - RAVC2 to COO + MSTR with the exercised evidence (not a self-report).
  </deliverables>
</task_order>
```
