# OG-rl-1 AC1 inputs -- the four message and attachment ids the issuer supplies (rl.AC1.sh)

By `2.0.0_SA_COO~O`, 2026-10-01 ~10:2xZ, read through the Opal gateway's own mail tools (`search_email`,
`list_email_attachments`) as the gateway's identity. Ids only; no body, address or content is recorded here.

| env var | arm | message (and attachment) | why it fits |
|---|---|---|---|
| `OG_RL_OFF_TABLE_MSG` | off-table sender refused | `AAMkAGJlNzJkOTQ2LTUxNzAtNGMwOC1hMmMwLWNmMjRiOWY1MWE3ZABGAAAAAABeGHeU_OH-RYG7MWQVnyDJBwB3I0IU-OYZSpxdEFzb-njIAAAAAAEMAAB3I0IU-OYZSpxdEFzb-njIAADhoKmrAAA=` | sender is an Opal colleague, not on `DEFAULT_AUTHORS` |
| `OG_RL_THREAD_MSG` | off-table sender in a table sender's thread refused | `AAMkAGJlNzJkOTQ2LTUxNzAtNGMwOC1hMmMwLWNmMjRiOWY1MWE3ZABGAAAAAABeGHeU_OH-RYG7MWQVnyDJBwB3I0IU-OYZSpxdEFzb-njIAAAAAAEMAAB3I0IU-OYZSpxdEFzb-njIAADaBU4oAAA=` | an external advisor's message that opened a conversation a table sender replied in (reply id `...ADaBU4qAAA=`) |
| `OG_RL_NONPDF_MSG` | non-PDF attachment returns metadata only | `AAMkAGJlNzJkOTQ2LTUxNzAtNGMwOC1hMmMwLWNmMjRiOWY1MWE3ZABGAAAAAABeGHeU_OH-RYG7MWQVnyDJBwB3I0IU-OYZSpxdEFzb-njIAAAAAAEMAAB3I0IU-OYZSpxdEFzb-njIAACniYutAAA=` | a TABLE sender's message (the route checks the sender first, so the attachment arm must sit on an admitted message) |
| `OG_RL_NONPDF_ATT` | (same arm) | `AAMkAGJlNzJkOTQ2LTUxNzAtNGMwOC1hMmMwLWNmMjRiOWY1MWE3ZABGAAAAAABeGHeU_OH-RYG7MWQVnyDJBwB3I0IU-OYZSpxdEFzb-njIAAAAAAEMAAB3I0IU-OYZSpxdEFzb-njIAACniYutAAABEgAQABv-3HqMt-ZFn3gKXUwpYNE=` | `image/png`, `isInline: false`, 570,082 bytes: a non-inline, non-PDF file attachment |

The same table message also carries a non-inline PDF (`...AHv2WjIjaH5Bm2B2LBRLNQw=`, 582,940 bytes, under the 10,000,000
cap): the POSITIVE arm (bytes with sha256) for the NFRA_TRNSPT laptop order 103564 ("one admitted message's bytes land
with a hash"), run after AC1 by the issuer, not graded by this order.
