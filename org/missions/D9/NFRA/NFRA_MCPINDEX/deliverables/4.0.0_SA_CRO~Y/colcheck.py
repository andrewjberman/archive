"""Every column each client adapter reads (the requested list) or uses (row.get on a column not requested), checked
against the live schema of the newest partition the census read. Prints one line per (adapter, table)."""
import json
import sys
t = json.load(open(sys.argv[1], encoding='utf-8'))
by = {(r['bucket'], r['prefix']): r for r in t}
A, B = 'opal-data-assets', 'opal-data-bd'
CHECKS = [
 # adapter, bucket, prefix, requested columns, extra fields read by .get() but never requested
 ('orion', A, 'orion/inflection/silver/fact_positions/', "accountNumber accountId custodian ticker name currentShares currentValue currentPrice isCustodialCash assetClass productType assetPercentOfAccount modelName sleeveType", "currency"),
 ('orion', A, 'orion/inflection/silver/fact_transactions/', "id accountId accountNumber transDate transactionDescription ticker transAmount noUnits navPrice status", "custodian"),
 ('eclipse', A, 'eclipse/inflection/silver/fact_models/', "id name nameSpace status portfolioCount", ""),
 ('eclipse', A, 'eclipse/inflection/silver/fact_model_composition/', "id name nameSpace status modelAUM portfolioCount modelDetail", ""),
 ('smartx', A, 'smartx/platform/silver/fact_model_allocation_roster/', "", "advisor_id advisor_name allocation_id model_name model_id rmid status value"),
 ('smartx', A, 'smartx/platform/silver/fact_allocation_account_map/', "", "allocation_id account_id account_number"),
 ('smartx', A, 'smartx/platform/silver/fact_allocation_positions/', "", "allocation_id ticker quantity price market_value currency"),
 ('smartx', A, 'smartx/platform/silver/fact_allocation_valuation/', "", "allocation_id cash"),
 ('smartx', A, 'smartx/platform/silver/fact_model_holdings/', "", "rmid ticker percent_of_portfolio"),
 ('schwab', A, 'schwab/08242234/silver/dim_position/', "account_id business_date cusip ticker_symbol l_s quantity_settled_unsettled market_value_settled_unsettled closing_price", "currency"),
 ('schwab', A, 'schwab/08242234/silver/dim_balance/', "account_id business_date cash_balance_settled_only net_mv_plus_cash net_mv_positions", ""),
 ('schwab', A, 'schwab/08242234/silver/dim_transaction/', "account_id business_date trade_date tran_date tr_cd transaction_category debit_credit cusip ticker_symbol quantity price gross_amount", ""),
 ('schwab', A, 'schwab/08335338/silver/dim_position/', "account_id business_date cusip ticker_symbol l_s quantity_settled_unsettled market_value_settled_unsettled closing_price", "currency"),
 ('bd49f', A, 'blackdiamond/49f/silver/dim_account_xref/', "bd_account_id bd_account_number account_is_open", ""),
 ('bd49f', B, 'silver/unrealized/', "account_id asset_id asset_name symbol ticker cusip open_date unit_cost market_value", "currency"),
 ('bd49f', B, 'silver/transactions/', "transaction_id trade_date transaction_type action market_value units asset_name cusip account_id", "currency"),
 ('bd49f', B, 'silver/fees/', "transaction_id trade_date account_id transaction_fee account_fee flat_fee fee_schedule_type fee_schedule_description", "currency"),
 ('bd49f', B, 'silver/allocations/', "account_id portfolio_id portfolio_name account_allocation cash_allocation account_market_value cash_market_value fee_schedule_type", ""),
 ('bd49f', A, 'blackdiamond/49f/silver/fact_bd_allocation/', "accountid portfolioid portfolio_name account_allocation account_market_value cash_market_value cash_allocation as_of_date", ""),
 ('bdcottonwood', A, 'blackdiamond/cottonwood/silver/fact_allocations/', "AccountID|Account Number|Custodian", ""),
 ('bdcottonwood', A, 'blackdiamond/cottonwood/silver/fact_holdings/', "AccountID|AssetID|Symbol|Ticker|CUSIP|Asset Name|Units|Market Value|Cash Equivalent", "currency"),
 ('bdcottonwood', A, 'blackdiamond/cottonwood/silver/fact_transactions/', "TransactionID|AccountID|Trade Date|Transaction Type|Transaction Sub Type|Action|Market Value|Units|Transaction Fee|Ticker|Symbol|Custodian", ""),
 ('bdcottonwood', A, 'blackdiamond/cottonwood/silver/fact_model_assignment/', "account_number account_id strategy_name program_name tax_status account_type is_sma is_rebalancer_uma can_rebalance is_closed is_managed", ""),
 ('bdcottonwood', A, 'blackdiamond/cottonwood/silver/fact_model_roster/', "model_id model_name is_opal rebalance_model_type", ""),
 ('bdcottonwood', A, 'blackdiamond/cottonwood/silver/fact_model_definition/', "model_id symbol asset_id sleeve_name component_name absolute_allocation relative_allocation", ""),
 ('bdcottonwood', A, 'blackdiamond/cottonwood/silver/fact_model_blend/', "model_id child_model_id child_model_name absolute_allocation relative_allocation", ""),
 ('commonwealth', A, 'commonwealth/cottonwood/silver/crosswalk/', "commonwealth_account status reason_code", ""),
 ('commonwealth', A, 'commonwealth/cottonwood/silver/positions/', "AccountNumber Cusip Symbol Security_Description Quantity Position_Type AsOfDate", "currency"),
 ('commonwealth', A, 'commonwealth/cottonwood/silver/account_day_value/', "account cusip quantity close value price_source blank_reason", ""),
 ('commonwealth', A, 'commonwealth/cottonwood/silver/transactions/', "Account_Number Trade_Date Transaction_Type Transaction_Description Cusip Symbol Quantity Amount AI Asset_Type CA_Event_Id", ""),
]
fails = 0
for ad, b, p, req, extra in CHECKS:
    r = by.get((b, p))
    split = (lambda s: [c for c in s.split('|') if c]) if '|' in req else (lambda s: s.split())
    req_l, extra_l = split(req), extra.split()
    if r is None or not r.get('columns'):
        print('NO-SCHEMA', ad, b, p)
        fails += 1
        continue
    cols = {c.split(':', 1)[0] for c in r['columns']}
    miss_req = [c for c in req_l if c not in cols]
    miss_extra = [c for c in extra_l if c not in cols]
    verdict = 'CRASH-RISK' if miss_req else ('SILENT-NULL' if miss_extra else 'OK')
    fails += verdict != 'OK'
    print('%-11s %-12s %-58s req=%d/%d used-not-req=%d/%d missing_req=%s missing_used=%s' % (
        verdict, ad, p, len(req_l) - len(miss_req), len(req_l), len(extra_l) - len(miss_extra), len(extra_l), miss_req, miss_extra))
print('checked:', len(CHECKS), 'non-OK:', fails)
