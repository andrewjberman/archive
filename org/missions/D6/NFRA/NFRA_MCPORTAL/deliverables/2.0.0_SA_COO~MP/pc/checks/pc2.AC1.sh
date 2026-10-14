#!/usr/bin/env bash
# MP-pc-2 AC1 (FWD-21 read, F1; decomposition PC.3): tests/test_admin_people.py passes with 0 failed, and each named test
# PASSES:
#   test_people_lists_every_candidate_even_holding_nothing  a candidate admitted to no tool is listed with channels []
#   test_depth_and_freshness_carry_their_claims            tool_index claims carried through; no row -> claim absent
#   test_cadence_reads_absent_with_reason                  every tool's cadence claim absent, with the PC.3 reason
#   test_kill_switch_empties_every_person                  kill switch on -> every channels [], basis says so
#   test_people_grant_store_unreadable_is_labelled         Scan refused -> grant_store unreadable + reason, 200
#   test_people_non_owner_is_refused                       a non-owner -> 403 and zero store calls
. "$(dirname "$0")/_root.sh"
named_pytest "people tests" tests/test_admin_people.py test_people_lists_every_candidate_even_holding_nothing test_depth_and_freshness_carry_their_claims test_cadence_reads_absent_with_reason test_kill_switch_empties_every_person test_people_grant_store_unreadable_is_labelled test_people_non_owner_is_refused
