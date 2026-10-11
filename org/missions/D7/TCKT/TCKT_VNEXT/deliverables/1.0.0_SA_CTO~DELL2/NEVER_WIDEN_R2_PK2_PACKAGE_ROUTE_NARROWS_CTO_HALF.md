# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT R2-pk-2: the package route stops handing the packager the ticket

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~08:0xZ** | **Against:** the packet and COO half
`deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_PK2_DEPLOY_PACKET_20261011.md` @472efb3a5b, and the handler at `be67d1fd38`, file sha256
`cf10e19e423b25b7b74ce43efd24e73b90a8a90850094697f3f79ec7145e6e74`.

## 1. The act and its blast radius

One function's code, `opal-ticket-api`. No env, route, IAM or grant. One route moves, `POST /api/scoped/tickets/{ticketId}/package`,
callable by one principal. The radius, branches and rollback (re-apply the build of `a366ce52ec`, file `ca3be343...`) are as the
packet states them. The act narrows: it removes two ticket reads handed to a service principal and adds refusal codes.

## 2. What this seat read itself

- **Every hunk of `git diff a366ce52ec be67d1fd38` on the handler** (the issuer had not read them line by line). All of it sits
  inside `package_ticket`: a helper `_ident` returning the package pointer fields plus `attached_at` and `attached_by`; a `code`
  on each of five 409s with the sentences unchanged; the already-attached 409 gains `package`; the changed-under-write 409 drops
  `ticket` and carries `package` only when one is stored; the 200 returns `{"package": ...}` and drops `ticket`. No other
  function is touched, and no check before the write changed.
- `sha256sum` of the file in the shared tree: `cf10e19e...`, equal to the packet's. The file does not differ between
  `be67d1fd38` and HEAD.
- `opal_packager.py:176-184`: the one caller's `ports["attach"](ticket_id, payload)` discards the answer.

**Taken as filed:** the caller count of 1 with 0 portal callers; the four test counts; the live digest `W03VREoM` and deployed
file `ca3be343...`.

## 3. Conditions

1. The packet's steps 0 to 6 as written, the two STOPs of step 1 included.
2. **Ordering:** no order is cut until R2-tr-1's run 3 has ended, whatever its result. If run 3 is not run, this apply waits on
   this seat's word, not on the run.
3. Step 1b's read of the deployed packager states the function it read and its CodeSha256.
4. The live arms are not exercised by this pair and nothing claims they were. The first real attach, or AR-g-32's pair, is
   where a 409 carrying its code and a 200 without `ticket` are read.
5. The issuer's precheck list gains `cf10e19e...` in the same sitting as the applier's report, as the packet says.

-- 1.0.0_SA_CTO~DELL2
