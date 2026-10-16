# CLIENT_NOTICE_CONTACT_MAP: where a firm's notice contact could come from (read 2026-10-16; no address recorded here)

**Owed by:** `2.0.0_SA_COO~V2`, confirmed by `1.0.0_SA_CTO~DELL2`, before the Ticket Center opens to clients (CTO ruling msg 9120, row `d33f`). Not before the combined release, which ships the map as `{}`.
**What the map needs:** `CLIENT_NOTICE_CONTACT_MAP` = `{"<firm id>": ["<address>", ...]}` for each client firm the Ticket Center serves. The first address is the default recipient; the stored requester's own address is used only if it is in the list (`_client_recipients`, built by `TO-R19-L1`).

## What the estate holds (measured)

| source | what it holds | what it lacks |
|---|---|---|
| `data/firm_registry.json` (the one firm enumeration; read through `_keys.load_firm_ids`) | five firms: `49financial`, `inflection`, `cottonwood` (`kind` client, enabled) and `mockadv` (test), `demo` (demo); a firm-level `email_domain` for each client firm | **no contact person and no address**: only a domain. The two non-client firms need no contact |
| the estate's tool catalog (`comp-which`, asked for the firm contact people) | nothing: "no curated rule matched; the catalog does not cover it" | **no CRM or contacts source is cataloged** |
| `opal-users-v2` PROFILE rows with `firmId` = a client firm (a count read, no address read) | 30 active people with logins: **`49financial` 13** (12 `user`, 1 `advisor`), **`inflection` 8** (all `user`), **`cottonwood` 9** (1 `admin`, 7 `user`, 1 `advisor`); the scan was complete (86 rows scanned, no continuation) | which of them should receive a ticket notice: a login is not a designated contact |

## The gap, stated

The ruling expected the registry or a CRM to supply the contact. **Neither names a person.** The registry gives the domain; the estate has no cataloged CRM; the users table has people but not a designation. Choosing who at each client firm receives ticket notices is a business decision (and the addresses are real external ones), so it is not a lookup this seat can complete, and it is not typed into Terraform or any file until named.

## Options (for the CTO to choose; the issuer's recommendation first)

1. **Andrew names one notice contact per client firm** (three names), at or before the client opening. The issuer then writes the `main.tf` row (a literal list per firm, no code) in its own cell, with a pair, and the after-read of the release is re-run. Clean, and the choice is made by the person who knows the firms.
2. **Derive from the users table:** the firm's `admin`-role user where one exists. Only `cottonwood` has one; `49financial` and `inflection` have none, so this leaves two firms unresolved.
3. **A firm-level shared address on the registry's `email_domain`** (for example a role mailbox). Needs the firm to create it; invents an address no one has confirmed.

**Recommendation: option 1.** It is the only one that yields a confirmed recipient for all three firms.
