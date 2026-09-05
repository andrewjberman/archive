# RUNBOOK -- blocked addresses: how to unblock one, and why never to edit the IP set

**Owner:** `0.7.0_AE_CloudOps~T` (NFRA_OPSEC202609, cells `OP-s-15` + `OP-s-19`)
**Audience:** anyone with account administration who is looking at a blocked address --
which, measured, is `Andrew_Berman`, `Andrew_Berman_Console` and `Opal_Terminal`.

---

## READ THIS FIRST IF YOU WERE ABOUT TO EDIT AN IP SET

**You almost certainly can.** Account administration includes `wafv2:UpdateIPSet` on all four
blocked-ip sets, so the console will let you add or remove an address and it will appear to work.

**DO NOT. Your change will be silently erased and nobody will tell you.**

The DynamoDB table `opal-suspicious-addresses` is the source of truth. The four WAF IP sets are a
**projection** of it. A reconciler recomputes the sets from the table -- on the table's stream within
about a minute, and again on a daily full pass. So:

```
  you add an address to the IP set by hand
      -> the table does not know about it
      -> the next reconcile computes the desired set FROM THE TABLE
      -> your address is not in that computation
      -> it is removed
      -> no error, no alert, no notification, and the console shows success at every step
```

The same in reverse: **remove a blocked address from the set by hand and the reconciler puts it
back**, because the table still says BLOCKED. You will have spent the effort and the address will
still be blocked minutes later.

**THIS IS THE DESIGN WORKING, NOT A BUG.** The invariant (C-2) is that the table is truth and
nothing but the reconciler writes the sets. A convenience path that writes a set directly makes the
table a lie, and the reconcile that erases it is what keeps the two honest. The cost is that the
erasure is **completely invisible to the person it happens to** -- which is why this page exists.

**AND IT IS RECORDED EVEN THOUGH IT IS NOT ALARMED.** A console `UpdateIPSet` is a management write
event and the organization trail captures it (`opal-organization-trail`, `IsLogging` true,
`ReadWriteType` All, management events included -- measured by `0.7.0_AE_CloudOps~W`). So a direct
edit is *auditable after the fact*; it simply is not *prevented*, and nothing watches for it in real
time. Deliberately: building a detector would be a monitor, and the estate's moratorium stands.

---

## THE SANCTIONED PATH

```bash
.tools/opal-ipblock status <address>                      # read the row first
.tools/opal-ipblock allow  <address> --reason "<why>"     # lift the block
```

`--reason` is mandatory and is recorded. The tool:

1. **edits the ROW only** -- sets `status = ALLOW`, `unblocked_by`, `unblocked_at`, `notes`;
2. **never touches an IP set** -- it is denied `wafv2:UpdateIPSet` at the IAM layer, not merely
   declining to call it, so the property survives a future edit by someone who has not read this;
3. **appends to `org/opal-ipblock-audit.log`** (append-only) so repeat unblocks keep their history,
   which a row alone would lose because a row holds only the LATEST unblock.

**The set is UNCHANGED at the instant the command returns.** That is expected and is the proof the
CLI is not a second writer. The reconciler picks the row change off the stream and the address
reaches you again typically within a minute. Confirm with `aws wafv2 get-ip-set`.

### Addresses are stored NORMALIZED

The partition key is a CIDR: IPv4 as `/32`, IPv6 as `/64`. `203.0.113.7` is stored as
`203.0.113.7/32`. The CLI normalizes for you, but if a lookup says the address is absent when you
expect it, check the normalization before concluding the row is missing.

### A row can read BLOCKED and not be blocking

DynamoDB TTL deletion is best-effort and can lag `expires_at` by up to ~48 hours. The reconciler
treats a row past its `expires_at` as **not blocking**, so an expired block is already lifted even
though the row is still there and still says `BLOCKED`. `opal-ipblock status` prints a `lapsed`
line for exactly this reason -- read it before lifting something that has already lapsed.

---

## IF THE RECONCILER IS DOWN

Then the sets are frozen at their last reconciled state, and a row edit will not take effect until
it recovers. **Editing the set by hand is still the wrong move** -- it will be erased the moment the
reconciler returns, which is the worst possible timing. Escalate instead; a stale block that a
human knows about is better than a correct block that silently reverts.

---

## WHAT WOULD MAKE THIS PAGE UNNECESSARY, and why it was not done

Denying `wafv2:UpdateIPSet` to `AdministratorAccessOpalCapital` would make the direct edit
impossible rather than merely inadvisable. It was **ruled against** (`2.0.0_SA_COO~Z`, row
`NFRA_OPSEC202609-Z-S125`): that group governs far more than this project, and an operator locked
out of the edge during an incident is a worse estate than this one. An administrator who can delete
the four sets outright is not meaningfully constrained by being denied update on them anyway -- the
capability just moves one API call sideways.

So the guard here is **knowing**, not permission. Hence this page.
