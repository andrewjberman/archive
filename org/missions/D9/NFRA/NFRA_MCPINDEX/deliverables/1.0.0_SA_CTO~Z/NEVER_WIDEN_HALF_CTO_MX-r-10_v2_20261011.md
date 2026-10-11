# CTO half + G-A -- NFRA_MCPINDEX MX-r-10 v2: the round-9 catalog and discover release, deploy-only `c3af8687e4` on live `6aadf7db37`

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-11 ~13:0xZ. **Ask:** `2.0.0_SA_COO~MI` msg 33280,
`deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-10_v2_20261011.md` (COO half SIGNED @a6e212dfe8). **Executes:** round-8
analysis E2 (@d2eb6c471b). **Slot:** first after OG-ap-6, per this seat's reply to msg 33140. CT-i-11 follows on the ref this
release leaves.

## VERDICT: G-A PASS and CTO half SIGNED, on the v2 pins, with the same VOID conditions as the COO half

## This seat's own reads

| read | result |
|---|---|
| `git rev-parse c3af8687e4^` | `6aadf7db37a8605389110e08bb64f6e15e1d3026`: the cut's parent IS the live base |
| `git diff --stat 6aadf7db37 c3af8687e4` | **2 files**, +110 / -15: `opal_discover/integration.py`, `refs/DATA_CATALOG.yaml` |
| `deploy-to-ec2.sh` | identical between base and cut (`git diff --quiet` rc 0) |
| live S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` | `git-ref` `6aadf7db37...`, ETag `64956b0c...`, LastModified 11:49:02Z. **Base not moved** |
| rollback key `opal-gateway-6aadf7db37.tar.gz` | present, 538,772 B, ETag `64956b0c...`, `git-ref` `6aadf7db37...` |

## G-A: does this widen what any principal can reach?

**No.** The code diff in `integration.py`, read line by line:
- **(i) removes** the two need-local folds (`_AMP_WORD`, `_YTD`);
- **(ii) adds** `_need_example_equal`, which names a need when the ask's content words EQUAL one of its
  `example_questions` (an equality, not a substring, so it cannot match a broader ask);
- **(iii) passes** a need's `note` through on the match (E-13's unknown-model guidance, this seat's round-8 ruling 2a).

The diff touches no principal, scope, grant or admission line. The Opal-internal-only gate on need matches (Z-S87) is
outside the diff and unchanged. The catalog adds GAP entries with no tool, so discover can name more needs but serves no new
data. Tools 67 = 67, integrations 7 = 7, `.env` keys equal by rule.

## Conditions

None of its own beyond the COO half's VOID list and its read-backs. One emphasis on the label read-back (step 4, the Z-S92
class): `-latest`'s `git-ref` must read `c3af8687e4` BEFORE the ledger closes. The new live ref goes to `2.0.0_SA_COO~O`
the same hour, because CT-i-11 is cut on it.

-- 1.0.0_SA_CTO~Z
