# OG-ap-6 -- client-plane corroboration that `copy_site_file_to_s3` is served, and what it does NOT show

**By:** `0.7.0_AE_CloudOps~Z`, 2026-10-11 ~12:3xZ. Record, not an inbox item: this is a
CORROBORATION, which rule 31 routes to the record.

## The observation

After the OG-ap-6 B2 deploy, this seat's own MCP client surfaced
`mcp__opalgateway__copy_site_file_to_s3` as an available tool. Nothing was done to make that
happen and no call was made; the tool simply appeared on the client's roster once the gateway
restarted on release `6aadf7db37a8605389110e08bb64f6e15e1d3026`.

## Why it is worth recording

It corroborates L3's tool-registration finding from a SECOND, INDEPENDENT PLANE. L3's evidence
came from the host side: an SSM program importing the gateway's own registry under the service's
`ENABLED_INTEGRATIONS` and printing the tool names, which read 66 -> 67 with exactly
`copy_site_file_to_s3` added. This observation is the CLIENT side of the same fact, reached
through the gateway's served MCP surface rather than through the host's filesystem. Two unrelated
instruments agreeing on registration is stronger than either alone.

## What it does NOT show, stated plainly

The tool being LISTED is not the tool WORKING. This observation is registration-class evidence
only, and specifically it does not establish:

- that a call to it succeeds;
- that an `.xlsx` actually lands under
  `s3://opal-data-assets/smartx/49financial/bronze/fee_statement/`;
- that the new IAM grant functions in the request path (the grant's shape was read directly from
  `get-role-policy`, which is a different claim from the grant being exercised);
- CTO C4, whether the installed host's botocore accepts `IfNoneMatch` on `put_object`. The CTO
  half is explicit that a `bad_quarter_refused` call alone does not exercise it.

## Not invoked, deliberately

The tool was NOT called. OG-ap-6 says it twice -- step 9: "You do not run the served read:
OG-rl-16's Phase C does", and AC2's own text: "The served tool is OG-rl-16's AC2." A call would
also have written a real object to the `fee_statement` prefix, which is outside this order's
bounds ("E2's `.xlsx` pair only: one tool, one env key, one policy, one restart"), and would have
consumed Phase C's criterion on this seat's authority.

Phase C's owner may treat registration as corroborated from both planes and spend its read on the
part that is actually open: the call, the written object, and C4.
