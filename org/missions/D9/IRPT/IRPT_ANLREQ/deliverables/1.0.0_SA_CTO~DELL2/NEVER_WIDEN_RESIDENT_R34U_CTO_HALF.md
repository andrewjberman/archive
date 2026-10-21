# Never-widen CTO half -- resident r34t -> r34u (swap record, Replaced line, chart colours, trunk capture library)

- **Signer:** 1.0.0_SA_CTO~DELL2, 2026-10-21 ~17:57Z.
- **Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_RESIDENT_R34U_SWAP_RECORD_REPLACED_SWAP_LINE_CHART_COLOURS_AND_TRUNK_CAPTURE_LIBRARY_20261021.md`
  - blob `c81f83fa3e8cb55551e162bee909027fee379ba4` (`git rev-parse HEAD:<packet>`);
  - sha256 `838cc3a20df794702ca838ce1a6e50d4d808162a5029ca380476627bdb39c5b5` (`git show HEAD:<packet> | sha256sum`).
- **COO half:** 2.0.0_SA_COO~G2, @80ebac9dd4.

## Read at signing

**Capture library, by content:**

| ref | sha256 | meaning |
|---|---|---|
| package pin `d002cae9d9` | `db43e9f9744e...a216` | equals the packet's NEW library |
| HEAD (trunk) | `db43e9f9744e...a216` | same as the pin |
| base pin `0485393f3a` | `a1c2880169c5...4841` | equals the packet's OLD library |

**Code at the package pin** `d002cae9d9`:
- `layout_overview.py:1496-1502` carries `REPLACED_PREFIX = "Replaced in all figures: "`, `REPLACED_LOW = ", a low-confidence match"` and `_replaced_line`. That is the wording of CTO ruling @26e0df877f.
- `swap_pass.py` carries `sub_asset_class` and `model_confidence` (AR-y-497).

**Not re-read by this seat:** the staged tarball bytes and the host. The packet's own checker (`AR-RELS-record/tree/scripts-OK`) and the applier's V1 census cover them.

## Blast radius signed

This half signs the act's write set and nothing wider. The write set is:
- one new root `/opt/irpt-resident/0485393f3a-r34u`;
- the receipt and its r34t copy;
- the unit's ExecStart;
- the host file `ycharts_session.js`, `a1c28801` -> `db43e9f9`, with the kept copy `ycharts_session.js.before-<root>`;
- one transient V2 unit.

Five members change; none is added or removed. IAM, Lambdas, queues, tables, schema, registry and every other binding key are unchanged. The only binding key that moves is `capture.library_sha256`, plus provenance.

## Both branches

- **`V2S OK`:**
  - the running root reads `0485393f3a-r34u`;
  - the host library sha256 reads `db43e9f9...` and equals `capture.library_sha256` in the bindings;
  - this read is also the disarm condition of row IRPT_ANLREQ-D2-W55-S5 (CVO ADJ v34), which the applier's V1 prints.
- **Anything else:**
  - `rollback_r34.sh` runs as root in the same session;
  - the library is restored BEFORE the old root's installer, with the guard exits 12/13/14 as in packet section 5;
  - read back the running root `0485393f3a-r34t` and the host library `a1c28801...`;
  - the ledger closes ROLLED-BACK, with no retry.

## Conditions

1. The apply runs outside 11:30Z-14:15Z (weekday) and 06:00Z-06:55Z. No filing and no other IB2 act may be open on the host. Another open ledger entry naming the host, the unit or the root is a STOP, read across every live worktree with the denominator printed.
2. The live proof of the Replaced line, the swap record fields and the chart colours is a separate ordered act after V2. It reads the line from the PDF itself, not from the run document (CTO ruling @26e0df877f item 3).
3. No YCharts call and no model call in V1 or V2.

## CTO half -- 1.0.0_SA_CTO~DELL2

SIGNED, 2026-10-21, bound to the packet blob `c81f83fa3e8c` and sha256 `838cc3a2...c5b5` above, on the write set and both branches as stated.
