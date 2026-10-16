"""AR380-y-AC2: builds the users item and the partner item for a fixed date and checks their attribute sets.

Prints ITEMS-OK users=<n> partner=<m> only when the users item has exactly the thirteen attributes and the partner item
exactly the eight; otherwise ITEMS-BAD <why> and exit 1. Expected attribute sets are written here, independently of the helper.
"""
import sys

import fwd1_advisor as fa

DATE = "20261016"
NOW = 1792000000
USER_EXPECTED = ("PK", "SK", "email", "firmId", "status", "name", "role", "tier", "allowedFirmIds",
                 "createdAt", "createdBy", "updatedAt", "exp")
PARTNER_EXPECTED = ("email", "advisorKey", "advisorName", "advisorRole", "firmRole", "createdAt", "createdBy", "updatedAt")


def bad(why):
    print("ITEMS-BAD " + why)
    return 1


def main():
    addr = fa.address_for(DATE)
    users = fa.user_item(addr, NOW)
    partner = fa.partner_item(addr, DATE, NOW)
    if set(users) != set(USER_EXPECTED) or len(users) != 13:
        return bad("users attributes %s" % sorted(users))
    if set(partner) != set(PARTNER_EXPECTED) or len(partner) != 8:
        return bad("partner attributes %s" % sorted(partner))
    if users["allowedFirmIds"] != {"L": [{"S": "49financial"}]}:
        return bad("allowedFirmIds is not the explicit one-firm list")
    if users["status"] != {"S": "active"} or users["firmId"] != {"S": "49financial"}:
        return bad("users row is not active at 49financial")
    if not users["exp"].get("N", "").isdigit():
        return bad("exp is not a number")
    if any(k in users or k in partner for k in ("passwordHash", "password", "hash")):
        return bad("a credential key is present")
    if not addr.endswith("@opal.invalid"):
        return bad("address is not @opal.invalid")
    print("ITEMS-OK users=%d partner=%d" % (len(users), len(partner)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
