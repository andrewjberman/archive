# IRPT_ANLREQ FWD-5 -- the owner rule the report-side readers apply, and which identity it admits as the control (issuer 2.0.0_SA_COO~T2, 2026-10-17)

Asked by the CTO (msg 10096, ruling (a)): before cutting the fourth sitting, "read the owner rule (served.py:987-997) and name in the packet the identity that rule admits, the owner or the on-behalf filer." Claim levels: *measured* = read from the named lines at HEAD `cdfc85ba12`; *inferred* = reasoned from those lines and the third sitting's reports, not read live.

## 1. The rule (measured)

`infra/aws/lambda/investor-reporting/_authz/served.py:960-1003` (`_handle_owner_read`) builds `guard_owner_read(...)` (`_scope/owner_reads.py:14-48`) with, for a caller whose verified subject is INTERNAL (`served.py:988`), the authorizer `InteractiveAccess(...).authorize_current` (`_scope/interactive_access.py:101-121`). On each owned read, `owner_reads.py:26-34` loads the retained record owner and REFUSES (`ProspectOwnershipRefused`, answered `NOT_AUTHORIZED`, `served.py:1001`) unless ALL of:

1. the retained owner is a dict whose `firm_id` equals the request's tenant (`49financial` here), for EVERY caller, `OPAL_GLOBAL` included (`owner_reads.py:28`);
2. the caller is `OPAL_GLOBAL`, OR the caller's `firm_id` equals the owner's `firm_id` AND the caller's `principal_id` equals the owner's `principal_id` (`owner_reads.py:29-31`);
3. the authorizer returns True: for an `OPAL_GLOBAL` caller `authorize_current` returns True whatever the owner (`interactive_access.py:115-116`, "a view filter never narrows verified Opal authority"); for any other caller it requires the same firm and principal id and the ordinary authorizer.

The `selected_tenant` of a request is checked BEFORE this (`served.py:1234-1260`): a caller that is not internal is refused `FIRM_BINDING` for a tenant other than its own; an internal caller is narrowed by its profile row's `allowedFirmIds`.

## 2. Who the rule admits (measured from the lines, applied to the retained owner)

- **The retained OWNER of the request**, when its `firm_id` is the tenant: the same firm and `principal_id`. For a request filed ON BEHALF of an advisor (window 5's design), the retained owner is the ADVISOR (the on-behalf subject), not the filing staff user.
- **Any `OPAL_GLOBAL` caller**, when the retained owner's `firm_id` equals the tenant. The on-behalf FILER (staff) is neither the owner nor needs to be: a staff caller of class `OPAL_GLOBAL` is admitted by clause 3 alone. The third sitting's synthetic target shows exactly this (inferred): the staff control (`opal-capital`, `allowedFirmIds` [49financial]) was served `original-upload`, `opal-report`, `request-read` and `job-status` on a request filed by a different synthetic user.
- **Nobody**, when the retained owner's `firm_id` is not the tenant (clause 1): the packaged R28 ticket of the third sitting (`TCK-20261014-2965a5e0`, request `REQ-28a5ca6b...`) answered the same staff control `NOT_AUTHORIZED` on the file routes, `opal-report`, `request-read` and `job-status`. INFERRED cause: its retained owner (a service-made request) does not carry `firm_id` = `49financial`, so no caller at tenant `49financial` is admitted, the control or an owner alike. This is a reading of the rule against the reports, not a read of the retained record.

## 3. What this means for the control of the fourth sitting (the identity to name)

- **The control = the staff control already used** (`fwd5-control-r60`, firm `opal-capital`, `allowedFirmIds` [49financial], class `OPAL_GLOBAL` by the interactive-access reading), minted with a sitting-only credential and removed after, **provided the retained owner of window 5's packaged request carries `firm_id` = `49financial`** (clause 1). The on-behalf FILER is not required as the control; the OWNER (the synthetic advisor) would also be admitted, but is a second mint with no gain.
- **To measure before the packet is signed:** the retained owner of window 5's request (its `firm_id` and `principal_id`, read-only, names of the keys and the firm only) equals the tenant; and the request carries `original_ref`, `pdf_ref` and `commentary_ref`. If the retained owner's `firm_id` is not the tenant, no control at tenant `49financial` can be served, and the sitting would need the packaged request re-owned (a window-5 matter), not a different control.
- **Also to settle (open, from the third sitting):** the staff control read `UNEXPECTED` on `request-history` and on the no-selection call for BOTH targets (row filed); a control that cannot read the history route says nothing about the fence there.

## 4. Not done

No retained record was read for this memo; no sitting is cut before window 5 (CTO msg 10096).
