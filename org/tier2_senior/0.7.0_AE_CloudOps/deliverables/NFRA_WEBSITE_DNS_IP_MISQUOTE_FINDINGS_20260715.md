# NFRA_WEBSITE -- the .188-vs-.186 apex-A misquote to Patricia: ROOT-CAUSED (photo-parse misread)

**archetype:** DIAGNOSE
**Agent:** 0.7.0_AE_CloudOps~A | **Date:** 2026-07-15 ~21:5xZ | **Subject:** NFRA_WEBSITE (Andrew-direct)

## Andrew-direct instruction (VERBATIM -- channel: own-terminal chat, 2026-07-15 ~21:4xZ)

> "You are going to be working on the NFRA_WEBSITE subject. I want you to check the recent message from
> Patricia. What I'm wondering is why we gave her a number ending in 8 if it was actually 6. I suspect
> maybe photo parsing issue, but want to be sure."

Scope: investigation tasking (NFRA_WEBSITE). Recorded per the Andrew-direct record+broadcast rule; I do
not adjudicate scope.

## Verdict

**Photo-parse misread CONFIRMED as the mechanism.** The `185.230.63.188` in our 2026-07-15 20:29:16Z
email to Patricia ("Re: DKIM recs + security cert") is a misread of the `185.230.63.186` apex A row in
HER OWN GoDaddy screenshot (6 -> 8, the canonical closed-glyph vision confusion). The number has no
other possible source, and the drafting pass demonstrably worked from the image.

## Evidence (each claim grounded)

1. **What we sent** (the sent message itself, read via m365 gateway): 20:29:16Z reply states
   `Value: 185.230.63.188 (the current live site - this is what confirms you are on the right row)`,
   describing "the very first record at the top, just above the two NS (nameserver) rows."
2. **True value** -- grounded THREE independent ways:
   - Live DNS (nslookup @8.8.8.8, 2026-07-15 ~21:45Z): apex `opalinvest.com` = `185.230.63.186 / .107 / .171`. No `.188`.
   - Patricia's screenshots, READ DIRECTLY (saved server-side to SharePoint `OpalCapital/Website/DNS_VERIFY_20260715/`,
     rendered via authenticated browser, pixels inspected): 25-record zone; THREE apex A rows
     (`@ -> .107`, `@ -> .171`, `@ -> .186`), `A new -> 18.208.18.213` (600s, our staging), `ns47/ns48.domaincontrol.com`,
     then CNAMEs incl. `www -> opalinvest.com`. **No row ends in .188.**
   - Estate records (RUNBOOK.md, tls-cutover.sh, TO-1/TO-2, GODADDY_DNS_REQUEST): Wix IPs recorded as `.107/.171/.186` throughout.
3. **`.188` never existed in the estate**: `comp-grep "185\.230\.63\.188"` = **0 matches / 22,119 files scanned**
   (denominator printed). It was born in the drafting step.
4. **The draft was machine-authored while reading the photo** (audit lake `s3://opal-mcp-audit/audit/dt=2026-07-15/`):
   `search_email` 20:22:59Z -> `read_email` 20:24:10Z -> `create_draft` 20:26:00Z (identity
   `andrew@opalinvest.com`, tier master_admin) -> sent 20:29:16Z. The m365 gateway has NO image-read tool
   and no attachment fetch appears in the audit -- yet the draft carries screenshot-ONLY details (all rows
   "1-hour TTL" where our estate docs recorded ~86400s; the record's position relative to the NS rows).
   The image therefore entered the drafting context directly (pasted into the chat), and the IP was read
   off the pixels. The row it identified positionally IS the `.186` row.
5. **Patricia's correction is right and no damage resulted** (her 21:28:30Z reply): *"I believe you meant
   185.230.63.186 since they isn't on that ends in 188 -- Both of these have been updated to 600 TTL."*
   Go-live meeting booked Thu Jul 16 4:00-4:30pm ET (invite received 21:29Z).

## Collateral finding -- SAME photo-parse pass, ACTIONABLE before go-live

The email represented the apex as **ONE** A record. The zone carries **THREE** apex A rows
(`@ -> .107 / .171 / .186`, all Wix). Patricia updated "both of these" = ONE A row + the www CNAME --
so `.107` and `.171` plausibly still carry 1-hour TTL. At Thursday's flip ALL THREE `@` A rows must be
replaced with `18.208.18.213`; two rows left at 3600s TTL means resolver caches can keep serving Wix for
up to an hour (that is the ROLLBACK target, so it fails soft -- but the "10-minute switch" claim in our
email holds only for the `.186` row). **Confirm all three A rows are at TTL 600 on the go-live call (or
one line to Patricia beforehand).**

## The generalizable failure mode (for the record)

A number parsed from a photo is a HYPOTHESIS (verification law: an injected column is a hypothesis --
same class, visual channel). This one was quoted to an external party with confidence while the true
value sat in five estate files and one `nslookup` away. Guard: any value quoted outward that was read
from an image gets grounded against live state or the estate record before send. 6/8 (and 3/8, 5/6, 0/8)
are closed-glyph confusion pairs at downscaled resolution -- the model reading a 2940x1912 screenshot is
not reading it at native resolution.

## Artifacts

- Screenshots preserved: SharePoint `OpalCapital / Shared Documents / Website/DNS_VERIFY_20260715/`
  (`godaddy_screenshot_31848PM.png` sha256 bf5b37ee..., `godaddy_screenshot_31908PM.png` sha256 baa13bc9...)
- Audit rows: `dt=2026-07-15/` 20:22:59 search_email / 20:24:10 read_email / 20:26:00 create_draft (master_admin)
