#!/usr/bin/env bash
# MP-pd-3 AC2 (F2, the People rows gain `principal`; decomposition PD.3): tests/test_admin_people.py passes with 0 failed,
# and these named tests PASS (the first two are the round-1 seam tests, which must still hold):
#   test_person_holdings_equal_breakdown_holders                   THE SEAM to the breakdown, unchanged
#   test_people_lists_every_candidate_even_holding_nothing         unchanged
#   test_people_row_principal_is_set_only_for_profiled_principals  a profiled principal's row carries {tid, oid}; an email-only row carries null
#   test_people_principal_never_leaks_into_other_fields            the added key changes nothing else in the body (difference control on the row's other keys)
. "$(dirname "$0")/_root.sh"
named_pytest "people rows tests" tests/test_admin_people.py \
  test_person_holdings_equal_breakdown_holders test_people_lists_every_candidate_even_holding_nothing \
  test_people_row_principal_is_set_only_for_profiled_principals test_people_principal_never_leaks_into_other_fields
