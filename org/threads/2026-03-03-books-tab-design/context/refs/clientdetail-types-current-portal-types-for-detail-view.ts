/**
 * Client Detail Page Types
 * Matches output from 09_generate_client_detail.py
 */

/** Tax exposure breakdown */
export interface TaxExposure {
  taxable: number
  tax_deferred: number
  tax_free: number
  taxable_pct: number
  tax_deferred_pct: number
  tax_free_pct: number
}

/** Portfolio exposure data */
export interface PortfolioExposure {
  tax: TaxExposure
}

/** Time series data point */
export interface ClientTimeSeriesPoint {
  date: string            // "2025-01"
  period: string          // "Jan '25"
  total_aua: number
  inflows: number
  outflows: number
  net_flows: number
}

/** Time series data */
export interface ClientTimeSeries {
  description: string
  start_date: string
  end_date: string
  data: ClientTimeSeriesPoint[]
}

/** AI-generated portfolio summary */
export interface PortfolioSummary {
  summary: string
  characteristics?: string[]
  risk_profile?: 'conservative' | 'moderate' | 'aggressive' | 'unknown'
  objectives?: string[]
  generated_at?: string
}

/** Point-in-time snapshot */
export interface PortfolioSnapshot {
  date: string
  label: string
  total_aua: number
  account_count: number
  exposure?: PortfolioExposure
}

/** Full client detail response */
export interface ClientDetailResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  architect_key: string
  architect_name: string
  client_key: string
  client_name: string

  summary: {
    total_aua: number
    account_count: number
    relationship_start_date?: string
    last_activity_date?: string
  }

  portfolio_summary?: PortfolioSummary
  exposure: PortfolioExposure

  snapshots?: {
    current: PortfolioSnapshot
    q1?: PortfolioSnapshot
    q2?: PortfolioSnapshot
    q3?: PortfolioSnapshot
  }

  timeseries: ClientTimeSeries
}
