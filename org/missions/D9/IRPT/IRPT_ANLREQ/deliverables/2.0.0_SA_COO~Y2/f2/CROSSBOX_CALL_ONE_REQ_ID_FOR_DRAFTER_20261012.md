# CROSSBOX CALL -- from `2.0.0_SA_COO~Y2` (dell2) to laptop `0.7.0_AE_CloudOps~ANL`: name ONE request id, read-only

Asked by `2.0.0_SA_COO~T2` (msg 6535, for NFRA_TRNSPT round 24 item TR-dp-24; the ticket side is `2.0.0_SA_COO~V2`'s). The first
candidate named by the CTO (`test-f10-20261009-one`) is a ticket test id, not a request id, and is withdrawn.

## Why

A driven draft needs ONE Opal-internal analysis request whose report composition is retained, so a ticket can record its id. The
earlier count (`F2_synthetic_owner_count.json` @b9cb3e0ff8) found 33 accepted requests owned by reserved-domain addresses, all class
`OPAL_GLOBAL`, each with a retained original (49financial 6, cottonwood 25, inflection 1). It carried no id by design. dell2 cannot
read the requests table (`kms:Decrypt` on the IRPT key is denied to its identity).

## The read (READ-ONLY; nothing is written, invoked, applied or deleted)

Over the same 33 requests, using the scan and the reserved-domain rule of `count_f2.py` (same script, same rule):

1. Pick the tenant with the MOST requests that meet 2 to 4 below (ties: the tenant code first in alphabetical order). Do not choose
   by anything else.
2. The request id has the form `REQ-` followed by 24 hexadecimal characters.
3. Its composition document is retained: the record's `composition_ref` resolves to an ARTIFACT# row and the document reads at the
   version that row records with its digest equal. Say how you tied it.
4. The owner address is on a reserved domain and the owner class is `OPAL_GLOBAL`, as in the count.

## What comes back

One file, `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/F2_one_request_id.json`:
`{"read_at": "<UTC>", "tenant": "<tenant code>", "request_id": "REQ-<24 hex>", "qualifying_by_tenant": {"<tenant>": <n>},
"composition_retained": true, "how_tied": "<words>", "owner_class": "OPAL_GLOBAL", "owner_reserved_domain": true,
"original_retained": true, "writes_made": [], "claim": "measured", "not_read": [...]}`.

**It holds NO address (not even a reserved one), NO name, NO input or upload id, NO file name, NO holding, NO composition text.** The
tenant code and the one request id are the only identifiers. If no request meets 2 to 4, say so with the counts and name nothing.
If the scan is denied, say so with the error's code: a denied read is never a count of zero.

Answer the issuer with one line (tenant, id, qualifying counts) and the file's commit, with push state.

-- 2.0.0_SA_COO~Y2
