#!/usr/bin/env python3
"""E3-AC2 BAND CONTROL -- kuzu_db and kuzu_ac7 named ONLY in prose.

This module mentions kuzu_db and kuzu_ac7 in its module docstring, in a
function docstring, in a comment and in a prose string constant, and opens
neither. The walker must count NONE of these as a reader: if it did, the
`READERS=0` on the real scope would be a claim about text, not about behaviour.
"""


def describes_but_does_not_read():
    """Explains that kuzu_ac7 is an NFRA_GLOBGRPH.ITEM-3 artifact and that
    kuzu_db is a June-2026 scratch of the same graph. Reads neither."""
    # kuzu_db and kuzu_ac7 are named in this comment too -- comments are not in
    # the ast at all, so they cannot reach the walker by any path.
    return "the local scratch stores kuzu_db and kuzu_ac7 are described, not opened"
