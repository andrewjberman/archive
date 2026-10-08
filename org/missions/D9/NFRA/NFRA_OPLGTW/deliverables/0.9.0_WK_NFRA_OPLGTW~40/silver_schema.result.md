# Silver schema measurement (OG-sc-1)

Measured 2026-10-08T22:45:41Z. Footer only; no row content, no statistics.

Name flags are by column NAME only (account number, name/title, tax id, mailing address, email, phone); nothing is classified.

## fact_acc

- 08242234: newest 2026-10-07, 686 partitions, 95 columns
- 08335338: newest 2026-10-07, 567 partitions, 95 columns

Only in 08242234: none

Only in 08335338: none

Type differs: none

Name-flagged: account_id, account_mailing_city, account_title_line_1, account_title_line_2, account_title_line_3, acct_mail_zip, acct_mailing_ctry_code, acct_regis, acct_type, alias_name, bank_sweep_display_name, email_address, mailing_address_line_1, mailing_address_line_2, mailing_address_line_3, master_account_name, mngdacct_pltfrmcd, mobile_phone_number, mstracct_number, organization_primary_name, phone_nbr, ssn_tin_number, taxpayer_first_name, taxpayer_last_name, taxpayer_middle_name, txpyr_title

| # | 08242234 name | type | 08335338 name | type |
|---|---|---|---|---|
| 1 | custdian_id | string | custdian_id | string |
| 2 | mstracct_number | string | mstracct_number | string |
| 3 | master_account_name | string | master_account_name | string |
| 4 | business_date | date32[day] | business_date | date32[day] |
| 5 | account_id | string | account_id | string |
| 6 | account_title_line_1 | string | account_title_line_1 | string |
| 7 | account_title_line_2 | string | account_title_line_2 | string |
| 8 | account_title_line_3 | string | account_title_line_3 | string |
| 9 | account_status | string | account_status | string |
| 10 | acct_regis | string | acct_regis | string |
| 11 | acct_type | string | acct_type | string |
| 12 | txpyr_title | string | txpyr_title | string |
| 13 | taxpayer_first_name | string | taxpayer_first_name | string |
| 14 | taxpayer_middle_name | string | taxpayer_middle_name | string |
| 15 | taxpayer_last_name | string | taxpayer_last_name | string |
| 16 | txpyr_suff | string | txpyr_suff | string |
| 17 | wh_cd | string | wh_cd | string |
| 18 | primary_contact | string | primary_contact | string |
| 19 | alias_name | string | alias_name | string |
| 20 | mailing_address_line_1 | string | mailing_address_line_1 | string |
| 21 | mailing_address_line_2 | string | mailing_address_line_2 | string |
| 22 | mailing_address_line_3 | string | mailing_address_line_3 | string |
| 23 | account_mailing_city | string | account_mailing_city | string |
| 24 | ac_st | string | ac_st | string |
| 25 | acct_mail_zip | string | acct_mail_zip | string |
| 26 | acct_mailing_ctry_code | string | acct_mailing_ctry_code | string |
| 27 | email_address | string | email_address | string |
| 28 | phone_nbr | string | phone_nbr | string |
| 29 | business_ph | string | business_ph | string |
| 30 | date_opened | date32[day] | date_opened | date32[day] |
| 31 | schwab_br_cd | string | schwab_br_cd | string |
| 32 | s_s | string | s_s | string |
| 33 | ac_cs | string | ac_cs | string |
| 34 | ac_ma | string | ac_ma | string |
| 35 | m_a | string | m_a | string |
| 36 | a_r | string | a_r | string |
| 37 | a_m | string | a_m | string |
| 38 | nr_am | string | nr_am | string |
| 39 | a_o | string | a_o | string |
| 40 | b_f | string | b_f | string |
| 41 | nr_bn | string | nr_bn | string |
| 42 | p_c | string | p_c | string |
| 43 | p_d | string | p_d | string |
| 44 | p_b | string | p_b | string |
| 45 | u_m | string | u_m | string |
| 46 | f_a | string | f_a | string |
| 47 | intbr_cd | string | intbr_cd | string |
| 48 | intbr_mm_cd | string | intbr_mm_cd | string |
| 49 | intbearing_ticker_symbol | string | intbearing_ticker_symbol | string |
| 50 | intbearing_feat_is_id | string | intbearing_feat_is_id | string |
| 51 | int_sf | string | int_sf | string |
| 52 | p_v | string | p_v | string |
| 53 | p_m | string | p_m | string |
| 54 | statemnt_pref | string | statemnt_pref | string |
| 55 | a_t | string | a_t | string |
| 56 | dflt_ltsel | string | dflt_ltsel | string |
| 57 | c_m | string | c_m | string |
| 58 | cbm_mf | string | cbm_mf | string |
| 59 | cbm_nmf | string | cbm_nmf | string |
| 60 | cb_mthd_date | date32[day] | cb_mthd_date | date32[day] |
| 61 | versmrkr_1 | string | versmrkr_1 | string |
| 62 | custtype_code | string | custtype_code | string |
| 63 | organization_primary_name | string | organization_primary_name | string |
| 64 | versmrkr_2 | string | versmrkr_2 | string |
| 65 | rstr_rsn1 | string | rstr_rsn1 | string |
| 66 | rstr_rsn2 | string | rstr_rsn2 | string |
| 67 | rstr_rsn3 | string | rstr_rsn3 | string |
| 68 | rstr_rsn4 | string | rstr_rsn4 | string |
| 69 | rstr_rsn5 | string | rstr_rsn5 | string |
| 70 | versmrkr_3 | string | versmrkr_3 | string |
| 71 | schwab_bank_ic_account | string | schwab_bank_ic_account | string |
| 72 | versmrkr_4 | string | versmrkr_4 | string |
| 73 | ssn_tin_number | string | ssn_tin_number | string |
| 74 | versmrkr_5 | string | versmrkr_5 | string |
| 75 | p_e | string | p_e | string |
| 76 | mngdacct_pltfrmcd | string | mngdacct_pltfrmcd | string |
| 77 | managed_account_money_manager | string | managed_account_money_manager | string |
| 78 | managed_account_investment_strategy | string | managed_account_investment_strategy | string |
| 79 | versmrkr_6 | string | versmrkr_6 | string |
| 80 | bank_sweep_display_name | string | bank_sweep_display_name | string |
| 81 | versmrkr_7 | string | versmrkr_7 | string |
| 82 | o_l | string | o_l | string |
| 83 | versmrkr_8 | string | versmrkr_8 | string |
| 84 | date_of_birth | date32[day] | date_of_birth | date32[day] |
| 85 | coy_cd | string | coy_cd | string |
| 86 | st_cd | string | st_cd | string |
| 87 | versmrkr_9 | string | versmrkr_9 | string |
| 88 | s_i | string | s_i | string |
| 89 | m_t | string | m_t | string |
| 90 | mobile_phone_number | string | mobile_phone_number | string |
| 91 | _source_file | string | _source_file | string |
| 92 | _source_as_of | string | _source_as_of | string |
| 93 | _master_observed | string | _master_observed | string |
| 94 | _section | string | _section | string |
| 95 | _schema_version | string | _schema_version | string |

## fact_uln

- 08242234: newest 2026-10-07, 687 partitions, 61 columns
- 08335338: newest 2026-10-07, 567 partitions, 61 columns

Only in 08242234: none

Only in 08335338: none

Type differs: none

Name-flagged: account_id, master_account_name, mstracct_number, tax_code

| # | 08242234 name | type | 08335338 name | type |
|---|---|---|---|---|
| 1 | custdian_id | string | custdian_id | string |
| 2 | mstracct_number | string | mstracct_number | string |
| 3 | master_account_name | string | master_account_name | string |
| 4 | business_date | date32[day] | business_date | date32[day] |
| 5 | account_id | string | account_id | string |
| 6 | prod_code | string | prod_code | string |
| 7 | prodcatg_code | string | prodcatg_code | string |
| 8 | tax_code | string | tax_code | string |
| 9 | ticker_symbol | string | ticker_symbol | string |
| 10 | cusip | string | cusip | string |
| 11 | schwab_sec_nbr | string | schwab_sec_nbr | string |
| 12 | item_issue_id | string | item_issue_id | string |
| 13 | isin | string | isin | string |
| 14 | sedol | string | sedol | string |
| 15 | options_display_symbol | string | options_display_symbol | string |
| 16 | underlying_ticker_symbol | string | underlying_ticker_symbol | string |
| 17 | underlyng_cusip | string | underlyng_cusip | string |
| 18 | underly_schwab | string | underly_schwab | string |
| 19 | underlying_itm_iss_id | string | underlying_itm_iss_id | string |
| 20 | underlying_isin | string | underlying_isin | string |
| 21 | underly_sedol | string | underly_sedol | string |
| 22 | current_quantity | decimal128(16, 6) | current_quantity | decimal128(16, 6) |
| 23 | l_s | string | l_s | string |
| 24 | trans_code | string | trans_code | string |
| 25 | current_market_value | decimal128(17, 4) | current_market_value | decimal128(17, 4) |
| 26 | accrued_interest | decimal128(15, 2) | accrued_interest | decimal128(15, 2) |
| 27 | acquired_date | date32[day] | acquired_date | date32[day] |
| 28 | orgpurch_date | date32[day] | orgpurch_date | date32[day] |
| 29 | org_purchase_price | decimal128(19, 8) | org_purchase_price | decimal128(19, 8) |
| 30 | yield_tomaturity | decimal128(11, 9) | yield_tomaturity | decimal128(11, 9) |
| 31 | cost_basis_unamortized | decimal128(15, 2) | cost_basis_unamortized | decimal128(15, 2) |
| 32 | cost_per_share | decimal128(19, 8) | cost_per_share | decimal128(19, 8) |
| 33 | adjusted_cost_basis_amortized | decimal128(15, 2) | adjusted_cost_basis_amortized | decimal128(15, 2) |
| 34 | adjusted_cost_per_share | decimal128(23, 12) | adjusted_cost_per_share | decimal128(23, 12) |
| 35 | unrealized_gain_loss | decimal128(17, 4) | unrealized_gain_loss | decimal128(17, 4) |
| 36 | days_held | string | days_held | string |
| 37 | h_t | string | h_t | string |
| 38 | c_b | string | c_b | string |
| 39 | c_t | string | c_t | string |
| 40 | a_t | string | a_t | string |
| 41 | c_f | string | c_f | string |
| 42 | original_face | decimal128(15, 5) | original_face | decimal128(15, 5) |
| 43 | dflot_selct | string | dflot_selct | string |
| 44 | w_s | string | w_s | string |
| 45 | versmrkr_1 | string | versmrkr_1 | string |
| 46 | disallowed_loss_amount | decimal128(17, 4) | disallowed_loss_amount | decimal128(17, 4) |
| 47 | transaction_cost | decimal128(15, 2) | transaction_cost | decimal128(15, 2) |
| 48 | transaction_cost_per_share | decimal128(23, 12) | transaction_cost_per_share | decimal128(23, 12) |
| 49 | versmrkr_2 | string | versmrkr_2 | string |
| 50 | g_i | string | g_i | string |
| 51 | original_cost_basis | decimal128(15, 2) | original_cost_basis | decimal128(15, 2) |
| 52 | versmrkr_3 | string | versmrkr_3 | string |
| 53 | adjusted_cost_incldg_unpd_amort | decimal128(15, 2) | adjusted_cost_incldg_unpd_amort | decimal128(15, 2) |
| 54 | versmrkr_4 | string | versmrkr_4 | string |
| 55 | event_id | string | event_id | string |
| 56 | c_v | string | c_v | string |
| 57 | _source_file | string | _source_file | string |
| 58 | _source_as_of | string | _source_as_of | string |
| 59 | _master_observed | string | _master_observed | string |
| 60 | _section | string | _section | string |
| 61 | _schema_version | string | _schema_version | string |

## fact_ult

- 08242234: newest 2026-10-07, 687 partitions, 61 columns
- 08335338: newest 2026-10-07, 567 partitions, 61 columns

Only in 08242234: none

Only in 08335338: none

Type differs: none

Name-flagged: account_id, master_account_name, mstracct_number, tax_code

| # | 08242234 name | type | 08335338 name | type |
|---|---|---|---|---|
| 1 | custdian_id | string | custdian_id | string |
| 2 | mstracct_number | string | mstracct_number | string |
| 3 | master_account_name | string | master_account_name | string |
| 4 | business_date | date32[day] | business_date | date32[day] |
| 5 | account_id | string | account_id | string |
| 6 | prod_code | string | prod_code | string |
| 7 | prodcatg_code | string | prodcatg_code | string |
| 8 | tax_code | string | tax_code | string |
| 9 | ticker_symbol | string | ticker_symbol | string |
| 10 | cusip | string | cusip | string |
| 11 | schwab_sec_nbr | string | schwab_sec_nbr | string |
| 12 | item_issue_id | string | item_issue_id | string |
| 13 | isin | string | isin | string |
| 14 | sedol | string | sedol | string |
| 15 | options_display_symbol | string | options_display_symbol | string |
| 16 | underlying_ticker_symbol | string | underlying_ticker_symbol | string |
| 17 | underlyng_cusip | string | underlyng_cusip | string |
| 18 | underly_schwab | string | underly_schwab | string |
| 19 | underlying_itm_iss_id | string | underlying_itm_iss_id | string |
| 20 | underlying_isin | string | underlying_isin | string |
| 21 | underly_sedol | string | underly_sedol | string |
| 22 | current_quantity | decimal128(16, 6) | current_quantity | decimal128(16, 6) |
| 23 | l_s | string | l_s | string |
| 24 | trans_code | string | trans_code | string |
| 25 | current_market_value | decimal128(17, 4) | current_market_value | decimal128(17, 4) |
| 26 | accrued_interest | decimal128(15, 2) | accrued_interest | decimal128(15, 2) |
| 27 | acquired_date | date32[day] | acquired_date | date32[day] |
| 28 | orgpurch_date | date32[day] | orgpurch_date | date32[day] |
| 29 | org_purchase_price | decimal128(19, 8) | org_purchase_price | decimal128(19, 8) |
| 30 | yield_tomaturity | decimal128(11, 9) | yield_tomaturity | decimal128(11, 9) |
| 31 | cost_basis_unamortized | decimal128(15, 2) | cost_basis_unamortized | decimal128(15, 2) |
| 32 | cost_per_share | decimal128(19, 8) | cost_per_share | decimal128(19, 8) |
| 33 | adjusted_cost_basis_amortized | decimal128(15, 2) | adjusted_cost_basis_amortized | decimal128(15, 2) |
| 34 | adjusted_cost_per_share | decimal128(23, 12) | adjusted_cost_per_share | decimal128(23, 12) |
| 35 | unrealized_gain_loss | decimal128(17, 4) | unrealized_gain_loss | decimal128(17, 4) |
| 36 | days_held | string | days_held | string |
| 37 | h_t | string | h_t | string |
| 38 | c_b | string | c_b | string |
| 39 | c_t | string | c_t | string |
| 40 | a_t | string | a_t | string |
| 41 | c_f | string | c_f | string |
| 42 | original_face | decimal128(15, 5) | original_face | decimal128(15, 5) |
| 43 | dflot_selct | string | dflot_selct | string |
| 44 | w_s | string | w_s | string |
| 45 | versmrkr_1 | string | versmrkr_1 | string |
| 46 | disallowed_loss_amount | decimal128(17, 4) | disallowed_loss_amount | decimal128(17, 4) |
| 47 | transaction_cost | decimal128(15, 2) | transaction_cost | decimal128(15, 2) |
| 48 | transaction_cost_per_share | decimal128(23, 12) | transaction_cost_per_share | decimal128(23, 12) |
| 49 | versmrkr_2 | string | versmrkr_2 | string |
| 50 | g_i | string | g_i | string |
| 51 | original_cost_basis | decimal128(15, 2) | original_cost_basis | decimal128(15, 2) |
| 52 | versmrkr_3 | string | versmrkr_3 | string |
| 53 | adjusted_cost_incldg_unpd_amort | decimal128(15, 2) | adjusted_cost_incldg_unpd_amort | decimal128(15, 2) |
| 54 | versmrkr_4 | string | versmrkr_4 | string |
| 55 | event_id | string | event_id | string |
| 56 | c_v | string | c_v | string |
| 57 | _source_file | string | _source_file | string |
| 58 | _source_as_of | string | _source_as_of | string |
| 59 | _master_observed | string | _master_observed | string |
| 60 | _section | string | _section | string |
| 61 | _schema_version | string | _schema_version | string |

## fact_rld

- 08242234: newest 2026-10-07, 936 partitions, 86 columns
- 08335338: newest 2026-10-07, 815 partitions, 86 columns

Only in 08242234: none

Only in 08335338: none

Type differs: none

Name-flagged: account_id, federal_tax_withholding, master_account_name, mstracct_number, state_tax_withholding, tax_code

| # | 08242234 name | type | 08335338 name | type |
|---|---|---|---|---|
| 1 | custdian_id | string | custdian_id | string |
| 2 | mstracct_number | string | mstracct_number | string |
| 3 | master_account_name | string | master_account_name | string |
| 4 | business_date | date32[day] | business_date | date32[day] |
| 5 | account_id | string | account_id | string |
| 6 | security_type | string | security_type | string |
| 7 | prod_code | string | prod_code | string |
| 8 | prodcatg_code | string | prodcatg_code | string |
| 9 | tax_code | string | tax_code | string |
| 10 | ticker_symbol | string | ticker_symbol | string |
| 11 | cusip | string | cusip | string |
| 12 | schwab_sec_nbr | string | schwab_sec_nbr | string |
| 13 | item_issue_id | string | item_issue_id | string |
| 14 | isin | string | isin | string |
| 15 | sedol | string | sedol | string |
| 16 | options_display_symbol | string | options_display_symbol | string |
| 17 | underlying_ticker_symbol | string | underlying_ticker_symbol | string |
| 18 | underlyng_cusip | string | underlyng_cusip | string |
| 19 | underly_schwab | string | underly_schwab | string |
| 20 | underlying_itm_iss_id | string | underlying_itm_iss_id | string |
| 21 | underlying_isin | string | underlying_isin | string |
| 22 | underly_sedol | string | underly_sedol | string |
| 23 | closing_date | date32[day] | closing_date | date32[day] |
| 24 | closing_quantity | decimal128(16, 6) | closing_quantity | decimal128(16, 6) |
| 25 | l_s | string | l_s | string |
| 26 | trans_code | string | trans_code | string |
| 27 | proceeds | decimal128(17, 4) | proceeds | decimal128(17, 4) |
| 28 | proceeds_per_share | decimal128(17, 4) | proceeds_per_share | decimal128(17, 4) |
| 29 | acquired_date | date32[day] | acquired_date | date32[day] |
| 30 | orgpurch_date | date32[day] | orgpurch_date | date32[day] |
| 31 | original_purchase_price | decimal128(19, 8) | original_purchase_price | decimal128(19, 8) |
| 32 | cost_basis_unamortized | decimal128(15, 2) | cost_basis_unamortized | decimal128(15, 2) |
| 33 | cost_per_share | decimal128(19, 8) | cost_per_share | decimal128(19, 8) |
| 34 | adjusted_cost_basis_amortized | decimal128(15, 2) | adjusted_cost_basis_amortized | decimal128(15, 2) |
| 35 | adjusted_cost_per_share | decimal128(23, 12) | adjusted_cost_per_share | decimal128(23, 12) |
| 36 | days_held | string | days_held | string |
| 37 | h_t | string | h_t | string |
| 38 | gain_loss_dollars | decimal128(17, 4) | gain_loss_dollars | decimal128(17, 4) |
| 39 | gain_loss_percentage | decimal128(17, 12) | gain_loss_percentage | decimal128(17, 12) |
| 40 | adjusted_gain_loss_dollars | decimal128(17, 4) | adjusted_gain_loss_dollars | decimal128(17, 4) |
| 41 | adjusted_gain_loss_percentage | decimal128(17, 12) | adjusted_gain_loss_percentage | decimal128(17, 12) |
| 42 | c_f | string | c_f | string |
| 43 | c_t | string | c_t | string |
| 44 | a_t | string | a_t | string |
| 45 | c_f_2 | string | c_f_2 | string |
| 46 | g_f | string | g_f | string |
| 47 | p_f | string | p_f | string |
| 48 | original_face | decimal128(15, 5) | original_face | decimal128(15, 5) |
| 49 | lot_selct | string | lot_selct | string |
| 50 | c_m | string | c_m | string |
| 51 | w_s | string | w_s | string |
| 52 | disallowed_loss_amount | decimal128(17, 4) | disallowed_loss_amount | decimal128(17, 4) |
| 53 | adj_disallowed_loss_amount | decimal128(17, 4) | adj_disallowed_loss_amount | decimal128(17, 4) |
| 54 | publication_timestamp | string | publication_timestamp | string |
| 55 | cbm | string | cbm | string |
| 56 | versmrkr_1 | string | versmrkr_1 | string |
| 57 | federal_tax_withholding | decimal128(15, 2) | federal_tax_withholding | decimal128(15, 2) |
| 58 | state_tax_withholding | decimal128(15, 2) | state_tax_withholding | decimal128(15, 2) |
| 59 | wh_st | string | wh_st | string |
| 60 | ytd_amortization | decimal128(17, 12) | ytd_amortization | decimal128(17, 12) |
| 61 | c_i | string | c_i | string |
| 62 | settle_date | date32[day] | settle_date | date32[day] |
| 63 | r_u | string | r_u | string |
| 64 | versmrkr_2 | string | versmrkr_2 | string |
| 65 | transaction_cost | decimal128(15, 2) | transaction_cost | decimal128(15, 2) |
| 66 | transaction_cost_per_share | decimal128(23, 12) | transaction_cost_per_share | decimal128(23, 12) |
| 67 | transaction_gain_loss_dollars | decimal128(17, 4) | transaction_gain_loss_dollars | decimal128(17, 4) |
| 68 | transaction_gain_loss_pct | decimal128(17, 12) | transaction_gain_loss_pct | decimal128(17, 12) |
| 69 | versmrkr_3 | string | versmrkr_3 | string |
| 70 | employee_option_original_cost | decimal128(17, 4) | employee_option_original_cost | decimal128(17, 4) |
| 71 | employee_option_realized_gain_loss | decimal128(17, 4) | employee_option_realized_gain_loss | decimal128(17, 4) |
| 72 | versmrkr_4 | string | versmrkr_4 | string |
| 73 | g_i | string | g_i | string |
| 74 | versmrkr_5 | string | versmrkr_5 | string |
| 75 | trancode_expanded | string | trancode_expanded | string |
| 76 | order_number | string | order_number | string |
| 77 | versmrkr_6 | string | versmrkr_6 | string |
| 78 | close_event_id | string | close_event_id | string |
| 79 | close_open_event_id | string | close_open_event_id | string |
| 80 | versmrkr_7 | string | versmrkr_7 | string |
| 81 | schwab_order_id | string | schwab_order_id | string |
| 82 | _source_file | string | _source_file | string |
| 83 | _source_as_of | string | _source_as_of | string |
| 84 | _master_observed | string | _master_observed | string |
| 85 | _section | string | _section | string |
| 86 | _schema_version | string | _schema_version | string |

## fact_rly

- 08242234: newest 2026-09-30, 45 partitions, 87 columns
- 08335338: newest 2026-09-30, 39 partitions, 87 columns

Only in 08242234: none

Only in 08335338: none

Type differs: none

Name-flagged: account_id, federal_tax_withholding, master_account_name, mstracct_number, state_tax_withholding, tax_code

| # | 08242234 name | type | 08335338 name | type |
|---|---|---|---|---|
| 1 | custdian_id | string | custdian_id | string |
| 2 | mstracct_number | string | mstracct_number | string |
| 3 | master_account_name | string | master_account_name | string |
| 4 | business_date | date32[day] | business_date | date32[day] |
| 5 | account_id | string | account_id | string |
| 6 | security_type | string | security_type | string |
| 7 | prod_code | string | prod_code | string |
| 8 | prodcatg_code | string | prodcatg_code | string |
| 9 | tax_code | string | tax_code | string |
| 10 | ticker_symbol | string | ticker_symbol | string |
| 11 | cusip | string | cusip | string |
| 12 | schwab_sec_nbr | string | schwab_sec_nbr | string |
| 13 | item_issue_id | string | item_issue_id | string |
| 14 | isin | string | isin | string |
| 15 | sedol | string | sedol | string |
| 16 | options_display_symbol | string | options_display_symbol | string |
| 17 | underlying_ticker_symbol | string | underlying_ticker_symbol | string |
| 18 | underlyng_cusip | string | underlyng_cusip | string |
| 19 | underly_schwab | string | underly_schwab | string |
| 20 | underlying_itm_iss_id | string | underlying_itm_iss_id | string |
| 21 | underlying_isin | string | underlying_isin | string |
| 22 | underly_sedol | string | underly_sedol | string |
| 23 | closing_date | date32[day] | closing_date | date32[day] |
| 24 | closing_quantity | decimal128(16, 6) | closing_quantity | decimal128(16, 6) |
| 25 | l_s | string | l_s | string |
| 26 | trans_code | string | trans_code | string |
| 27 | proceeds | decimal128(17, 4) | proceeds | decimal128(17, 4) |
| 28 | proceeds_per_share | decimal128(17, 4) | proceeds_per_share | decimal128(17, 4) |
| 29 | acquired_date | date32[day] | acquired_date | date32[day] |
| 30 | orgpurch_date | date32[day] | orgpurch_date | date32[day] |
| 31 | original_purchase_price | decimal128(19, 8) | original_purchase_price | decimal128(19, 8) |
| 32 | cost_basis_unamortized | decimal128(15, 2) | cost_basis_unamortized | decimal128(15, 2) |
| 33 | cost_per_share | decimal128(19, 8) | cost_per_share | decimal128(19, 8) |
| 34 | adjusted_cost_basis_amortized | decimal128(15, 2) | adjusted_cost_basis_amortized | decimal128(15, 2) |
| 35 | adjusted_cost_per_share | decimal128(23, 12) | adjusted_cost_per_share | decimal128(23, 12) |
| 36 | days_held | string | days_held | string |
| 37 | h_t | string | h_t | string |
| 38 | gain_loss_dollars | decimal128(17, 4) | gain_loss_dollars | decimal128(17, 4) |
| 39 | gain_loss_percentage | decimal128(17, 12) | gain_loss_percentage | decimal128(17, 12) |
| 40 | adjusted_gain_loss_dollars | decimal128(17, 4) | adjusted_gain_loss_dollars | decimal128(17, 4) |
| 41 | adjusted_gain_loss_percentage | decimal128(17, 12) | adjusted_gain_loss_percentage | decimal128(17, 12) |
| 42 | c_f | string | c_f | string |
| 43 | c_t | string | c_t | string |
| 44 | a_t | string | a_t | string |
| 45 | c_f_2 | string | c_f_2 | string |
| 46 | g_f | string | g_f | string |
| 47 | p_f | string | p_f | string |
| 48 | original_face | decimal128(15, 5) | original_face | decimal128(15, 5) |
| 49 | lot_selct | string | lot_selct | string |
| 50 | c_m | string | c_m | string |
| 51 | w_s | string | w_s | string |
| 52 | disallowed_loss_amount | decimal128(17, 4) | disallowed_loss_amount | decimal128(17, 4) |
| 53 | adj_disallowed_loss_amount | decimal128(17, 4) | adj_disallowed_loss_amount | decimal128(17, 4) |
| 54 | versmrkr_1 | string | versmrkr_1 | string |
| 55 | publication_timestamp | string | publication_timestamp | string |
| 56 | cbm | string | cbm | string |
| 57 | versmrkr_2 | string | versmrkr_2 | string |
| 58 | federal_tax_withholding | decimal128(15, 2) | federal_tax_withholding | decimal128(15, 2) |
| 59 | state_tax_withholding | decimal128(15, 2) | state_tax_withholding | decimal128(15, 2) |
| 60 | wh_st | string | wh_st | string |
| 61 | ytd_amortization | decimal128(17, 12) | ytd_amortization | decimal128(17, 12) |
| 62 | c_i | string | c_i | string |
| 63 | settle_date | date32[day] | settle_date | date32[day] |
| 64 | r_u | string | r_u | string |
| 65 | versmrkr_3 | string | versmrkr_3 | string |
| 66 | transaction_cost | decimal128(15, 2) | transaction_cost | decimal128(15, 2) |
| 67 | transaction_cost_per_share | decimal128(23, 12) | transaction_cost_per_share | decimal128(23, 12) |
| 68 | transaction_gain_loss_dollars | decimal128(17, 4) | transaction_gain_loss_dollars | decimal128(17, 4) |
| 69 | transaction_gain_loss_pct | decimal128(17, 12) | transaction_gain_loss_pct | decimal128(17, 12) |
| 70 | versmrkr_4 | string | versmrkr_4 | string |
| 71 | employee_option_original_cost | decimal128(17, 4) | employee_option_original_cost | decimal128(17, 4) |
| 72 | employee_option_realized_gain_loss | decimal128(17, 4) | employee_option_realized_gain_loss | decimal128(17, 4) |
| 73 | versmrkr_5 | string | versmrkr_5 | string |
| 74 | g_i | string | g_i | string |
| 75 | versmrkr_6 | string | versmrkr_6 | string |
| 76 | trancode_expanded | string | trancode_expanded | string |
| 77 | order_number | string | order_number | string |
| 78 | versmrkr_7 | string | versmrkr_7 | string |
| 79 | close_event_id | string | close_event_id | string |
| 80 | close_open_event_id | string | close_open_event_id | string |
| 81 | versmrkr_8 | string | versmrkr_8 | string |
| 82 | schwab_order_id | string | schwab_order_id | string |
| 83 | _source_file | string | _source_file | string |
| 84 | _source_as_of | string | _source_as_of | string |
| 85 | _master_observed | string | _master_observed | string |
| 86 | _section | string | _section | string |
| 87 | _schema_version | string | _schema_version | string |

## fact_rty

- 08242234: newest 2026-09-30, 45 partitions, 75 columns
- 08335338: newest 2026-09-30, 39 partitions, 75 columns

Only in 08242234: none

Only in 08335338: none

Type differs: none

Name-flagged: account_id, federal_tax_withholding, master_account_name, mstracct_number, state_tax_withholding, tax_code

| # | 08242234 name | type | 08335338 name | type |
|---|---|---|---|---|
| 1 | custdian_id | string | custdian_id | string |
| 2 | mstracct_number | string | mstracct_number | string |
| 3 | master_account_name | string | master_account_name | string |
| 4 | business_date | date32[day] | business_date | date32[day] |
| 5 | account_id | string | account_id | string |
| 6 | security_type | string | security_type | string |
| 7 | prod_code | string | prod_code | string |
| 8 | prodcatg_code | string | prodcatg_code | string |
| 9 | tax_code | string | tax_code | string |
| 10 | ticker_symbol | string | ticker_symbol | string |
| 11 | cusip | string | cusip | string |
| 12 | schwab_sec_nbr | string | schwab_sec_nbr | string |
| 13 | item_issue_id | string | item_issue_id | string |
| 14 | isin | string | isin | string |
| 15 | sedol | string | sedol | string |
| 16 | options_display_symbol | string | options_display_symbol | string |
| 17 | underlying_ticker_symbol | string | underlying_ticker_symbol | string |
| 18 | underlyng_cusip | string | underlyng_cusip | string |
| 19 | underly_schwab | string | underly_schwab | string |
| 20 | underlying_itm_iss_id | string | underlying_itm_iss_id | string |
| 21 | underlying_isin | string | underlying_isin | string |
| 22 | underly_sedol | string | underly_sedol | string |
| 23 | closing_date | date32[day] | closing_date | date32[day] |
| 24 | closing_quantity | decimal128(16, 6) | closing_quantity | decimal128(16, 6) |
| 25 | l_s | string | l_s | string |
| 26 | trans_code | string | trans_code | string |
| 27 | proceeds | decimal128(17, 4) | proceeds | decimal128(17, 4) |
| 28 | proceeds_per_share | decimal128(17, 4) | proceeds_per_share | decimal128(17, 4) |
| 29 | acquired_date | date32[day] | acquired_date | date32[day] |
| 30 | cost_basis_unamortized | decimal128(15, 2) | cost_basis_unamortized | decimal128(15, 2) |
| 31 | cost_per_share | decimal128(19, 8) | cost_per_share | decimal128(19, 8) |
| 32 | adjusted_cost_basis_amortized | decimal128(15, 2) | adjusted_cost_basis_amortized | decimal128(15, 2) |
| 33 | adjusted_cost_per_share | decimal128(23, 12) | adjusted_cost_per_share | decimal128(23, 12) |
| 34 | days_held | string | days_held | string |
| 35 | h_t | string | h_t | string |
| 36 | gain_loss_dollars | decimal128(17, 4) | gain_loss_dollars | decimal128(17, 4) |
| 37 | gain_loss_percentage | decimal128(17, 12) | gain_loss_percentage | decimal128(17, 12) |
| 38 | adjusted_gain_loss_dollars | decimal128(17, 4) | adjusted_gain_loss_dollars | decimal128(17, 4) |
| 39 | adjusted_gain_loss_percentage | decimal128(17, 12) | adjusted_gain_loss_percentage | decimal128(17, 12) |
| 40 | c_b | string | c_b | string |
| 41 | c_t | string | c_t | string |
| 42 | a_t | string | a_t | string |
| 43 | c_f | string | c_f | string |
| 44 | g_f | string | g_f | string |
| 45 | p_f | string | p_f | string |
| 46 | original_face | decimal128(15, 5) | original_face | decimal128(15, 5) |
| 47 | lot_selct | string | lot_selct | string |
| 48 | c_m | string | c_m | string |
| 49 | w_s | string | w_s | string |
| 50 | disallowed_loss_amount | decimal128(17, 4) | disallowed_loss_amount | decimal128(17, 4) |
| 51 | adj_disallowed_loss_amount | decimal128(17, 4) | adj_disallowed_loss_amount | decimal128(17, 4) |
| 52 | versmrkr_1 | string | versmrkr_1 | string |
| 53 | publication_timestamp | string | publication_timestamp | string |
| 54 | cbm | string | cbm | string |
| 55 | versmrkr_2 | string | versmrkr_2 | string |
| 56 | federal_tax_withholding | decimal128(15, 2) | federal_tax_withholding | decimal128(15, 2) |
| 57 | state_tax_withholding | decimal128(15, 2) | state_tax_withholding | decimal128(15, 2) |
| 58 | wh_st | string | wh_st | string |
| 59 | ytd_amortization | decimal128(17, 12) | ytd_amortization | decimal128(17, 12) |
| 60 | c_i | string | c_i | string |
| 61 | settle_date | date32[day] | settle_date | date32[day] |
| 62 | versmrkr_3 | string | versmrkr_3 | string |
| 63 | transaction_cost | decimal128(15, 2) | transaction_cost | decimal128(15, 2) |
| 64 | transaction_cost_per_share | decimal128(23, 12) | transaction_cost_per_share | decimal128(23, 12) |
| 65 | transaction_gain_loss_dollars | decimal128(17, 4) | transaction_gain_loss_dollars | decimal128(17, 4) |
| 66 | transaction_gain_loss_pct | decimal128(17, 12) | transaction_gain_loss_pct | decimal128(17, 12) |
| 67 | versmrkr_4 | string | versmrkr_4 | string |
| 68 | trancode_expanded | string | trancode_expanded | string |
| 69 | versmrkr_5 | string | versmrkr_5 | string |
| 70 | close_event_id | string | close_event_id | string |
| 71 | _source_file | string | _source_file | string |
| 72 | _source_as_of | string | _source_as_of | string |
| 73 | _master_observed | string | _master_observed | string |
| 74 | _section | string | _section | string |
| 75 | _schema_version | string | _schema_version | string |

## fact_trn

- 08242234: newest 2026-10-07, 686 partitions, 140 columns
- 08335338: newest 2026-10-07, 567 partitions, 140 columns

Only in 08242234: none

Only in 08335338: none

Type differs: none

Name-flagged: account_id, account_title_line_1, account_title_line_2, account_title_line_3, accounting_rule_code, acct_regis, acct_type, bank_name_part_1, bank_name_part_2, broker_name, intermediary_name, master_account_name, mstracct_number, recipient_maker_acct_number, recipient_maker_name_line_1, recipient_maker_name_line_2, recipient_maker_name_line_3, retirement_fed_income_tax, retirement_state_income_tax, state_tax_withholding, tax_cd, tax_code

| # | 08242234 name | type | 08335338 name | type |
|---|---|---|---|---|
| 1 | custdian_id | string | custdian_id | string |
| 2 | mstracct_number | string | mstracct_number | string |
| 3 | master_account_name | string | master_account_name | string |
| 4 | business_date | date32[day] | business_date | date32[day] |
| 5 | account_id | string | account_id | string |
| 6 | account_title_line_1 | string | account_title_line_1 | string |
| 7 | account_title_line_2 | string | account_title_line_2 | string |
| 8 | account_title_line_3 | string | account_title_line_3 | string |
| 9 | acct_regis | string | acct_regis | string |
| 10 | acct_type | string | acct_type | string |
| 11 | prod_code | string | prod_code | string |
| 12 | prodcatg_code | string | prodcatg_code | string |
| 13 | tax_code | string | tax_code | string |
| 14 | ly_st | string | ly_st | string |
| 15 | ticker_symbol | string | ticker_symbol | string |
| 16 | industry_ticker_symbol | string | industry_ticker_symbol | string |
| 17 | cusip | string | cusip | string |
| 18 | schwab_sec_nbr | string | schwab_sec_nbr | string |
| 19 | item_issue_id | string | item_issue_id | string |
| 20 | rulst_sufid | string | rulst_sufid | string |
| 21 | isin | string | isin | string |
| 22 | sedol | string | sedol | string |
| 23 | options_display_symbol | string | options_display_symbol | string |
| 24 | underlying_ticker_symbol | string | underlying_ticker_symbol | string |
| 25 | underlying_industry_ticker_symbol | string | underlying_industry_ticker_symbol | string |
| 26 | underlyng_cusip | string | underlyng_cusip | string |
| 27 | underly_schwab | string | underly_schwab | string |
| 28 | underlying_itm_iss_id | string | underlying_itm_iss_id | string |
| 29 | unrul_sufid | string | unrul_sufid | string |
| 30 | underlying_isin | string | underlying_isin | string |
| 31 | underly_sedol | string | underly_sedol | string |
| 32 | mnymk_code | string | mnymk_code | string |
| 33 | tr_cd | string | tr_cd | string |
| 34 | sb_cd | string | sb_cd | string |
| 35 | transaction_category | string | transaction_category | string |
| 36 | tran_srcde | string | tran_srcde | string |
| 37 | transaction_source_code_description | string | transaction_source_code_description | string |
| 38 | transaction_detail_description | string | transaction_detail_description | string |
| 39 | trade_typcd | string | trade_typcd | string |
| 40 | t_c | string | t_c | string |
| 41 | trade_date | date32[day] | trade_date | date32[day] |
| 42 | settlmnt_date | date32[day] | settlmnt_date | date32[day] |
| 43 | tran_date | date32[day] | tran_date | date32[day] |
| 44 | exdivdnd_date | date32[day] | exdivdnd_date | date32[day] |
| 45 | quantity | decimal128(15, 5) | quantity | decimal128(15, 5) |
| 46 | price | decimal128(15, 5) | price | decimal128(15, 5) |
| 47 | gross_amount | decimal128(15, 2) | gross_amount | decimal128(15, 2) |
| 48 | debit_credit | string | debit_credit | string |
| 49 | net_amount | decimal128(15, 2) | net_amount | decimal128(15, 2) |
| 50 | commission | decimal128(15, 2) | commission | decimal128(15, 2) |
| 51 | exchange_processing_fee | decimal128(15, 2) | exchange_processing_fee | decimal128(15, 2) |
| 52 | broker_service_fee | decimal128(15, 2) | broker_service_fee | decimal128(15, 2) |
| 53 | prime_broker_fee | decimal128(15, 2) | prime_broker_fee | decimal128(15, 2) |
| 54 | trade_away_fee | decimal128(15, 2) | trade_away_fee | decimal128(15, 2) |
| 55 | redemption_fee | decimal128(15, 2) | redemption_fee | decimal128(15, 2) |
| 56 | other_fee | decimal128(15, 2) | other_fee | decimal128(15, 2) |
| 57 | federal_tefra_withholding | decimal128(15, 2) | federal_tefra_withholding | decimal128(15, 2) |
| 58 | state_tax_withholding | decimal128(15, 2) | state_tax_withholding | decimal128(15, 2) |
| 59 | st_tx | string | st_tx | string |
| 60 | accrued_interest | decimal128(15, 2) | accrued_interest | decimal128(15, 2) |
| 61 | accounting_rule_code | string | accounting_rule_code | string |
| 62 | ordr_srcd | string | ordr_srcd | string |
| 63 | order_number | string | order_number | string |
| 64 | trade_order_entry_tm_stmp | string | trade_order_entry_tm_stmp | string |
| 65 | trade_order_exectn_tm_stmp | string | trade_order_exectn_tm_stmp | string |
| 66 | broker_code | string | broker_code | string |
| 67 | broker_name | string | broker_name | string |
| 68 | swb_from_account | string | swb_from_account | string |
| 69 | swb_to_account | string | swb_to_account | string |
| 70 | s1_check_number | string | s1_check_number | string |
| 71 | s_i | string | s_i | string |
| 72 | stock_exchg | string | stock_exchg | string |
| 73 | i_e | string | i_e | string |
| 74 | distribution_rate | decimal128(15, 8) | distribution_rate | decimal128(15, 8) |
| 75 | cash_in_lieu_share_quantity | decimal128(15, 5) | cash_in_lieu_share_quantity | decimal128(15, 5) |
| 76 | dividend_interest_share_quantity | decimal128(15, 5) | dividend_interest_share_quantity | decimal128(15, 5) |
| 77 | cash_in_lieu_rate | decimal128(15, 8) | cash_in_lieu_rate | decimal128(15, 8) |
| 78 | asset_backed_factor | decimal128(15, 12) | asset_backed_factor | decimal128(15, 12) |
| 79 | sr_sy | string | sr_sy | string |
| 80 | jn_tp | string | jn_tp | string |
| 81 | d_m | string | d_m | string |
| 82 | schwab_cashiering_unique_id | string | schwab_cashiering_unique_id | string |
| 83 | recipient_maker_name_line_1 | string | recipient_maker_name_line_1 | string |
| 84 | recipient_maker_name_line_2 | string | recipient_maker_name_line_2 | string |
| 85 | recipient_maker_name_line_3 | string | recipient_maker_name_line_3 | string |
| 86 | frequency | string | frequency | string |
| 87 | disburse_check_number | string | disburse_check_number | string |
| 88 | federal_bank_reference_number | string | federal_bank_reference_number | string |
| 89 | recipient_maker_acct_number | string | recipient_maker_acct_number | string |
| 90 | bank_act_typ | string | bank_act_typ | string |
| 91 | bank_name_part_1 | string | bank_name_part_1 | string |
| 92 | bank_name_part_2 | string | bank_name_part_2 | string |
| 93 | bank_aba | string | bank_aba | string |
| 94 | intermediary_name | string | intermediary_name | string |
| 95 | transaction_check_memo_1 | string | transaction_check_memo_1 | string |
| 96 | transaction_check_memo_2 | string | transaction_check_memo_2 | string |
| 97 | retirement_fed_income_tax | decimal128(15, 2) | retirement_fed_income_tax | decimal128(15, 2) |
| 98 | retirement_state_income_tax | decimal128(15, 2) | retirement_state_income_tax | decimal128(15, 2) |
| 99 | rt_tx | string | rt_tx | string |
| 100 | publication_time_stamp | string | publication_time_stamp | string |
| 101 | versmrkr_1 | string | versmrkr_1 | string |
| 102 | tips_factor | decimal128(18, 9) | tips_factor | decimal128(18, 9) |
| 103 | closing_price | decimal128(16, 5) | closing_price | decimal128(16, 5) |
| 104 | versmrkr_2 | string | versmrkr_2 | string |
| 105 | transaction_memo | string | transaction_memo | string |
| 106 | versmrkr_3 | string | versmrkr_3 | string |
| 107 | closing_price_unfactored | decimal128(16, 5) | closing_price_unfactored | decimal128(16, 5) |
| 108 | factor | decimal128(15, 12) | factor | decimal128(15, 12) |
| 109 | factor_date | date32[day] | factor_date | date32[day] |
| 110 | versmrkr_4 | string | versmrkr_4 | string |
| 111 | step_in_fee | decimal128(18, 4) | step_in_fee | decimal128(18, 4) |
| 112 | markupmarkdown | decimal128(18, 4) | markupmarkdown | decimal128(18, 4) |
| 113 | research_fee | decimal128(18, 4) | research_fee | decimal128(18, 4) |
| 114 | exec_brok_comm | decimal128(18, 4) | exec_brok_comm | decimal128(18, 4) |
| 115 | versmrkr_5 | string | versmrkr_5 | string |
| 116 | order_id | string | order_id | string |
| 117 | record_date | date32[day] | record_date | date32[day] |
| 118 | payable_date | date32[day] | payable_date | date32[day] |
| 119 | accstart_date | string | accstart_date | string |
| 120 | accrend_date | string | accrend_date | string |
| 121 | d_f | string | d_f | string |
| 122 | versmrkr_6 | string | versmrkr_6 | string |
| 123 | yield_to_call | decimal128(8, 7) | yield_to_call | decimal128(8, 7) |
| 124 | yield_to_maturity | decimal128(8, 7) | yield_to_maturity | decimal128(8, 7) |
| 125 | trust_princ | decimal128(5, 2) | trust_princ | decimal128(5, 2) |
| 126 | trust_income | decimal128(5, 2) | trust_income | decimal128(5, 2) |
| 127 | tax_cd | string | tax_cd | string |
| 128 | r_dc | string | r_dc | string |
| 129 | r_cc | string | r_cc | string |
| 130 | r_cy | string | r_cy | string |
| 131 | cycle_id | string | cycle_id | string |
| 132 | tran_randm | decimal128(5, 0) | tran_randm | decimal128(5, 0) |
| 133 | tranproc_date | date32[day] | tranproc_date | date32[day] |
| 134 | cashiering_transaction_identifier | string | cashiering_transaction_identifier | string |
| 135 | transaction_memo_or_wire_instructions | string | transaction_memo_or_wire_instructions | string |
| 136 | _source_file | string | _source_file | string |
| 137 | _source_as_of | string | _source_as_of | string |
| 138 | _master_observed | string | _master_observed | string |
| 139 | _section | string | _section | string |
| 140 | _schema_version | string | _schema_version | string |
