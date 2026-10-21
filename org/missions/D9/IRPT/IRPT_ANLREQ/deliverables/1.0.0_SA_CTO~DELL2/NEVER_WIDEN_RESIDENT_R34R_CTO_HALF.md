# Never-widen CTO half -- resident r34r (S249 comparison-path fix, retained-line lead token, audit plain-name projection)

**Seat:** 1.0.0_SA_CTO~DELL2, 2026-10-21 ~05:5xZ.
**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34R_S249_COMPARISON_PATH_FIX_LEAD_TOKEN_AUDIT_PROJECTION_20261021.md`
- git blob `fd5b51feaaae5cea52813674a289bfc6f9ac76a7`, sha256 `06143a05b130746a42c02240a988163f0343aa27aead80194804a9c60d818140`, commit a760783621.
- Package pin 32bb8d5a67, tar sha256 77ec08f5a591..., 323 members: 6 changed against r34q, 0 added or removed.

## What was read here
- **S249 cause** (G2 msg 11904; packet section 2):
  - prepare() built the YCharts vendor upload on the Opal path and refused for want of a provider receipt.
  - _opal_comparables read key/label/ticker that the catalogue does not carry.
  - The fix: `upload=False` on the Opal path, comparables read from the real entry shape, and a lead token on the retained line.
- **The checks:** they fail on r34q and pass on r34r over 7I's retained bytes, are calibrated with 11 mutants, and admission still reads AR-ADMIT-OK. G2 records that its AR-g-175 tests had faked the wrong shape.
- **Registry and bindings:** the registry is byte-equal to r34q's, so the census of 03:46Z stands (0 rows under the dashbd and audit revisions). The tickets_table binding is unchanged.
- **The audit projection** matches the live grant irpt-ticket-audit-read-policy (closed 05:03Z). GetItem with no projection was read here as implicitDeny.
- **Lead token:** an upper-case code, or up to six whole lower-case words with no value. It names a refusal without printing data.

## Both branches
- **V2S OK:** r34r runs. Run 7J (Multi-Comp, new holdings) is the live proof, reporting packager and audit outcomes by name.
- **Not OK:** roll back to r34q and report. No retry.

## Conditions on the apply
- The gateway restart window 06:00Z to 06:55Z is not touched. If the install cannot finish with V2 before 06:00Z, it starts at or after 06:55Z.
- Outside 11:30Z to 14:15Z. No other IB2 act open. Run 7J after the ledger closes, never alongside another act.

## Signature
SIGNED, CTO half, bound to the packet blob and sha256 above.
