# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-390: the _authz served.py release (IB-pr-385 svc-custody-statement + IB-pr-387 internal-caller allowedFirmIds narrowing + "ALL" never admits) on 6 of 8 hosts

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~06:5xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~201/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-390.md`, **blob be15b61188**
(drained into box/dell2; verified SAME at HEAD) | **Code pin:** `74a62fb46c` | **Census pin:** `71e9aacf27` | **Released now on Andrew's word**
(~V2 msg 2536); CTO msg 2539 commits to signing the 385+387 packet.

## Blast radius signed

Six functions, each built twice byte-identical at the REAL source map. Their `served.py` staged rows are restaged to `74a62fb46c`; the six
pins are verified intact at box/dell2 HEAD.

| function | built sha256 | live_before (rollback target) |
|---|---|---|
| irpt-49f-reporting-read-lambda | `8ySmTtYXTqZgnpFY/cnFKnbsGGO/qm6qLCxGLXhIVCI=` | `cou/Td9ydDrn9rQPT4hfa1n04eb54VXqnWaq4+N4FTI=` |
| irpt-directory-search | `RwgwXI5+xiss9h7OmVPqk6EujzQalXYCciQkvTBGj+c=` | `IV7P2AL43cGo9VfyY2ku0zEFAhQWq9BPxge754UynM8=` |
| irpt-export-render | `c7jOyysB/zo6OjtzCNdUZiu0o4fxNE9XeCM1FxXIHhk=` | `7T29wPhzbU/FlJpeT3MNSJ5jFWcEmi7bvHiSKECkyns=` |
| irpt-performance-adapter | `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=` | `NU6YVERLJ0i6qmazBYWUF+1xVDPGHwdMKqQ5vgjmVc4=` |
| irpt-status | `E7VKvhg3E9D5euWO+S649/iyAJ05xUmFPqHEAKDTFxA=` | `jhGc2J4Q5EesJgnLq8EzdE5ErrZLbyqnJ8m00R7CgdE=` |
| irpt-ycharts-generate | `ZA0QJ5Wt/7JcwmuzVfHOeNAdFk6th4H5IEeqQStDYm8=` | `5FRkux2oSNN1jB4xJEibio+F9F2ofl9mgcuH9jN/JrY=` |

No IAM, route, schedule, env or other function change. `irpt-holdings` and `irpt-narrative` are held out: their routes stay NOT YET
NARROWED, and IB-pr-394 is their follow-up cell, in flight.

## Measured by this seat

- `p97_release.py`: IB97-3-AC1 PASS (6 artifacts) and IB97-3-AC2 PASS (10 arms, 4 negative controls). The arms cover:
  - `svc-custody-statement` admitted on its 3 routes through built and refused through live;
  - `[cottonwood]` selecting inflection refused FIRM_BINDING on 21 of 21;
  - an `ALL` row, string or list, refused on 21 of 21;
  - a no-row Opal caller identical on 21 of 21.
- The `_authz` suite passes 304 of 304 at the code pin (worker run). A live census of `opal-users-v2` profile rows finds that no row holds
  `ALL`, so this release changes no live caller's reach today.
- `svc-custody-statement` stays inert until its mint lands; no such token exists yet.

## Branch A and Branch B

- **A:** the six functions run the built code.
  - An internal caller with a non-empty profile list is narrowed to it.
  - A non-list value, a lookup error or `ALL` fails closed.
  - `svc-custody-statement` is admitted cottonwood-only on its 3 routes.
- **B:** redeploy each function's prior artifact, by the S3 rollback versions recorded in the packet's table, through the Terraform or
  build path, never by console. There is no data or state to undo.

## Sequencing

ONE apply order to an applier lane. It lands the six functions through the Terraform path, reads each live CodeSha256 back equal to its
built value, and reads one admitted and one refused route call per host. It opens a ledger that **states the pin** (ccbe8b8be1 rule: blob
`be15b61188`, code `74a62fb46c`) and closes it.

**Verdict: GIVEN** for exactly these six artifacts at this packet blob.

-- 2.0.0_SA_COO~P2
