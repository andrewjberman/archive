"""
Shared ETF Classification Module for Yang Pipeline Lambdas

This module provides the canonical source of truth for ETF classifications,
management styles, and sector mappings used across multiple Yang pipeline lambdas.

Usage:
    from etf_classification import (
        get_asset_class,
        is_fixed_income,
        is_equity,
        FIXED_INCOME_TICKERS,
        EQUITY_TICKERS,
        ETF_MANAGEMENT_STYLE,
    )

Why this exists:
    Previously, each lambda had its own hardcoded classification dictionaries.
    This caused inconsistencies when new ETFs were added to one lambda but not others,
    leading to bugs like UVXY being misclassified or new tickers defaulting incorrectly.

Maintenance:
    When Yang adds a new ETF to the portfolio, add it here ONCE.
    All lambdas will automatically use the updated classification.

Last updated: 2026-01-19
"""

import logging
from typing import Optional, Set, Dict

logger = logging.getLogger(__name__)

# =============================================================================
# CANONICAL ETF CLASSIFICATIONS
# =============================================================================
# This is the single source of truth for ETF asset class classification.
# Categories: 'fixed_income', 'equity', 'hedge'
#
# Note: "Cash equivalents" (T-Bills, Money Market) are classified as 'fixed_income'
# per Opal's portfolio construction methodology.

ETF_CLASSIFICATIONS: Dict[str, str] = {
    # =========================================================================
    # FIXED INCOME - Cash (Actual USD, not ETFs)
    # =========================================================================
    'CASH_USD': 'fixed_income',  # Actual USD cash position

    # =========================================================================
    # FIXED INCOME - Ultra Short-Term (T-Bills / Money Market)
    # =========================================================================
    'BIL': 'fixed_income',      # SPDR Bloomberg 1-3 Month T-Bill ETF
    'SGOV': 'fixed_income',     # iShares 0-3 Month Treasury Bond ETF
    'TFLO': 'fixed_income',     # iShares Treasury Floating Rate Bond ETF
    'XBIL': 'fixed_income',     # US Treasury 6 Month Bill ETF
    'TBIL': 'fixed_income',     # US Treasury 3 Month Bill ETF
    'BILS': 'fixed_income',     # SPDR Bloomberg 3-12 Month T-Bill ETF
    'OBIL': 'fixed_income',     # US Treasury 12 Month Bill ETF
    'IBIL': 'fixed_income',     # iShares Treasury Bill ETF

    # =========================================================================
    # FIXED INCOME - Short-Term (1-3 years)
    # =========================================================================
    'VGSH': 'fixed_income',     # Vanguard Short-Term Treasury ETF
    'VCSH': 'fixed_income',     # Vanguard Short-Term Corporate Bond ETF
    'SHY': 'fixed_income',      # iShares 1-3 Year Treasury Bond ETF
    'SCHO': 'fixed_income',     # Schwab Short-Term US Treasury ETF
    'UTWO': 'fixed_income',     # US Treasury 2 Year Note ETF
    'UTEN': 'fixed_income',     # US Treasury 10 Year Note ETF
    'BSCQ': 'fixed_income',     # Invesco BulletShares 2026 Corporate Bond ETF
    'BSCR': 'fixed_income',     # Invesco BulletShares 2027 Corporate Bond ETF
    'BSJQ': 'fixed_income',     # Invesco BulletShares 2026 High Yield Corporate Bond ETF
    'IBTF': 'fixed_income',     # iShares iBonds Dec 2026 Term Treasury ETF
    'CLIP': 'fixed_income',     # Global X 1-3 Month T-Bill ETF
    'VTES': 'fixed_income',     # Vanguard Short-Term Tax-Exempt Bond ETF

    # =========================================================================
    # FIXED INCOME - Actively Managed Short Duration
    # =========================================================================
    'MINT': 'fixed_income',     # PIMCO Enhanced Short Maturity Active ETF
    'JPST': 'fixed_income',     # JPMorgan Ultra-Short Income ETF
    'ICSH': 'fixed_income',     # BlackRock Ultra Short-Term Bond ETF
    'JAAA': 'fixed_income',     # Janus Henderson AAA CLO ETF
    'DFSD': 'fixed_income',     # Dimensional Short-Duration Fixed Income ETF
    'VUSB': 'fixed_income',     # Vanguard Ultra-Short Bond ETF
    'VNLA': 'fixed_income',     # Janus Henderson Short Duration Income ETF
    'LONZ': 'fixed_income',     # PIMCO Senior Loan Active ETF

    # =========================================================================
    # FIXED INCOME - Intermediate/Core (3-10 years)
    # =========================================================================
    'BND': 'fixed_income',      # Vanguard Total Bond Market ETF
    'AGG': 'fixed_income',      # iShares Core US Aggregate Bond ETF
    'SCHZ': 'fixed_income',     # Schwab US Aggregate Bond ETF
    'BIV': 'fixed_income',      # Vanguard Intermediate-Term Bond ETF
    'VGIT': 'fixed_income',     # Vanguard Intermediate-Term Treasury ETF
    'VCIT': 'fixed_income',     # Vanguard Intermediate-Term Corporate Bond ETF
    'IEF': 'fixed_income',      # iShares 7-10 Year Treasury Bond ETF
    'GOVT': 'fixed_income',     # iShares US Treasury Bond ETF
    'FBND': 'fixed_income',     # Fidelity Total Bond ETF
    'DFCF': 'fixed_income',     # Dimensional Core Fixed Income ETF
    'FLOT': 'fixed_income',     # iShares Floating Rate Bond ETF

    # =========================================================================
    # FIXED INCOME - Long Duration (10+ years)
    # =========================================================================
    'VGLT': 'fixed_income',     # Vanguard Long-Term Treasury ETF
    'VCLT': 'fixed_income',     # Vanguard Long-Term Corporate Bond ETF
    'TLT': 'fixed_income',      # iShares 20+ Year Treasury Bond ETF
    'LQD': 'fixed_income',      # iShares iBoxx Investment Grade Corporate Bond ETF

    # =========================================================================
    # FIXED INCOME - High Yield / Credit
    # =========================================================================
    'HYG': 'fixed_income',      # iShares iBoxx High Yield Corporate Bond ETF
    'JNK': 'fixed_income',      # SPDR Bloomberg High Yield Bond ETF
    'SPHY': 'fixed_income',     # SPDR Portfolio High Yield Bond ETF
    'SJNK': 'fixed_income',     # SPDR Bloomberg Short Term High Yield Bond ETF
    'PCHI': 'fixed_income',     # Polen High Yield ETF (NOTE: NOT MSCI China - that's MCHI)
    'QBER': 'fixed_income',     # TrueShares Structured Outcome ETF

    # =========================================================================
    # FIXED INCOME - International
    # =========================================================================
    'BNDX': 'fixed_income',     # Vanguard Total International Bond ETF
    'IAGG': 'fixed_income',     # iShares Core International Aggregate Bond ETF
    'EMB': 'fixed_income',      # iShares JP Morgan USD Emerging Markets Bond ETF
    'VWOB': 'fixed_income',     # Vanguard Emerging Markets Government Bond ETF
    'PCY': 'fixed_income',      # Invesco Emerging Markets Sovereign Debt ETF

    # =========================================================================
    # FIXED INCOME - Municipal / TIPS
    # =========================================================================
    'MUB': 'fixed_income',      # iShares National Muni Bond ETF
    'TIP': 'fixed_income',      # iShares TIPS Bond ETF
    'VTIP': 'fixed_income',     # Vanguard Short-Term Inflation-Protected Securities ETF
    'SCHP': 'fixed_income',     # Schwab US TIPS ETF

    # =========================================================================
    # EQUITY - US Large Cap
    # =========================================================================
    'SPY': 'equity',            # SPDR S&P 500 ETF Trust
    'VOO': 'equity',            # Vanguard S&P 500 ETF
    'IVV': 'equity',            # iShares Core S&P 500 ETF
    'VTI': 'equity',            # Vanguard Total Stock Market ETF
    'SPYM': 'equity',           # SPDR Portfolio S&P 500 ETF
    'QQQ': 'equity',            # Invesco QQQ Trust (Nasdaq-100)
    'QQQM': 'equity',           # Invesco Nasdaq 100 ETF

    # =========================================================================
    # EQUITY - US Mid/Small Cap
    # =========================================================================
    'IJH': 'equity',            # iShares Core S&P Mid-Cap ETF
    'IWR': 'equity',            # iShares Russell Mid-Cap ETF
    'VO': 'equity',             # Vanguard Mid-Cap ETF
    'IJR': 'equity',            # iShares Core S&P Small-Cap ETF
    'IWM': 'equity',            # iShares Russell 2000 ETF
    'VB': 'equity',             # Vanguard Small-Cap ETF
    'SPSM': 'equity',           # SPDR Portfolio S&P 600 Small Cap ETF

    # =========================================================================
    # EQUITY - US Style/Factor
    # =========================================================================
    'VUG': 'equity',            # Vanguard Growth ETF
    'VTV': 'equity',            # Vanguard Value ETF
    'QUAL': 'equity',           # iShares MSCI USA Quality Factor ETF
    'SPMO': 'equity',           # Invesco S&P 500 Momentum ETF
    'COWZ': 'equity',           # Pacer US Cash Cows 100 ETF

    # =========================================================================
    # EQUITY - US Dividend
    # =========================================================================
    'SCHD': 'equity',           # Schwab US Dividend Equity ETF
    'DVY': 'equity',            # iShares Select Dividend ETF
    'DGRO': 'equity',           # iShares Core Dividend Growth ETF
    'DIVZ': 'equity',           # TrueShares Low Volatility Equity Income ETF
    'JEPI': 'equity',           # JPMorgan Equity Premium Income ETF

    # =========================================================================
    # EQUITY - US Sector
    # =========================================================================
    'VGT': 'equity',            # Vanguard Information Technology ETF
    'XLK': 'equity',            # Technology Select Sector SPDR Fund
    'XLE': 'equity',            # Energy Select Sector SPDR Fund
    'XLF': 'equity',            # Financial Select Sector SPDR Fund
    'XLU': 'equity',            # Utilities Select Sector SPDR Fund
    'VNQ': 'equity',            # Vanguard Real Estate ETF

    # =========================================================================
    # EQUITY - International Developed
    # =========================================================================
    'VXUS': 'equity',           # Vanguard Total International Stock ETF
    'VEA': 'equity',            # Vanguard FTSE Developed Markets ETF
    'IEFA': 'equity',           # iShares Core MSCI EAFE ETF
    'EFA': 'equity',            # iShares MSCI EAFE ETF
    'SPDW': 'equity',           # SPDR Portfolio Developed World ex-US ETF
    'VSS': 'equity',            # Vanguard FTSE All-World ex-US Small-Cap ETF
    'IQLT': 'equity',           # iShares MSCI Intl Quality Factor ETF
    'IDVZ': 'equity',           # TrueShares International Equity Income ETF
    'EWJ': 'equity',            # iShares MSCI Japan ETF

    # =========================================================================
    # EQUITY - International Emerging
    # =========================================================================
    'VWO': 'equity',            # Vanguard FTSE Emerging Markets ETF
    'IEMG': 'equity',           # iShares Core MSCI Emerging Markets ETF
    'EEM': 'equity',            # iShares MSCI Emerging Markets ETF
    'INDA': 'equity',           # iShares MSCI India ETF
    'MCHI': 'equity',           # iShares MSCI China ETF

    # =========================================================================
    # EQUITY - Global
    # =========================================================================
    'ACWI': 'equity',           # iShares MSCI ACWI ETF

    # =========================================================================
    # EQUITY - Active/Specialty
    # =========================================================================
    'PFDE': 'equity',           # Pathfinder Disciplined US Equities ETF
    'PFOE': 'equity',           # Pathfinder Focused Opportunities ETF

    # =========================================================================
    # EQUITY - Volatility (per product decision 2026-01)
    # =========================================================================
    'UVXY': 'equity',           # ProShares Ultra VIX Short-Term Futures ETF
    'VXX': 'equity',            # iPath Series B S&P 500 VIX Short-Term Futures ETN

    # =========================================================================
    # HEDGE - Commodities
    # =========================================================================
    'GLD': 'hedge',             # SPDR Gold Shares
    'IAU': 'hedge',             # iShares Gold Trust
    'SLV': 'hedge',             # iShares Silver Trust
    'DBC': 'hedge',             # Invesco DB Commodity Index Tracking Fund
    'PDBC': 'hedge',            # Invesco Optimum Yield Diversified Commodity Strategy
    'GSG': 'hedge',             # iShares S&P GSCI Commodity-Indexed Trust
    'USO': 'hedge',             # United States Oil Fund

    # =========================================================================
    # HEDGE - Volatility (legacy classification, deprecated)
    # =========================================================================
    'VIXY': 'hedge',            # ProShares VIX Short-Term Futures ETF
}


# =============================================================================
# DERIVED SETS (computed from ETF_CLASSIFICATIONS)
# =============================================================================

FIXED_INCOME_TICKERS: Set[str] = {
    ticker for ticker, asset_class in ETF_CLASSIFICATIONS.items()
    if asset_class == 'fixed_income'
}

EQUITY_TICKERS: Set[str] = {
    ticker for ticker, asset_class in ETF_CLASSIFICATIONS.items()
    if asset_class == 'equity'
}

HEDGE_TICKERS: Set[str] = {
    ticker for ticker, asset_class in ETF_CLASSIFICATIONS.items()
    if asset_class == 'hedge'
}


# =============================================================================
# ETF MANAGEMENT STYLE
# =============================================================================
# Source: Yang's model PKL "Active Fund" column
# 'active' = Actively managed, 'passive' = Index/Beta tracking

ETF_MANAGEMENT_STYLE: Dict[str, str] = {
    # Passive - Index/Beta tracking
    'SPY': 'passive', 'VOO': 'passive', 'IVV': 'passive', 'VTI': 'passive',
    'QQQ': 'passive', 'QQQM': 'passive', 'IWM': 'passive', 'IJH': 'passive',
    'IJR': 'passive', 'VB': 'passive', 'VO': 'passive', 'VUG': 'passive',
    'VTV': 'passive', 'QUAL': 'passive', 'SPMO': 'passive', 'SPSM': 'passive',
    'SPYM': 'passive', 'IWR': 'passive', 'SCHD': 'passive',

    # Passive - International
    'VEA': 'passive', 'VXUS': 'passive', 'VWO': 'passive', 'IEFA': 'passive',
    'IEMG': 'passive', 'EFA': 'passive', 'EEM': 'passive', 'ACWI': 'passive',
    'SPDW': 'passive', 'VSS': 'passive', 'EWJ': 'passive',

    # Passive - Fixed Income
    'BIL': 'passive', 'SGOV': 'passive', 'TBIL': 'passive', 'XBIL': 'passive',
    'OBIL': 'passive', 'IBIL': 'passive', 'BILS': 'passive',
    'VGSH': 'passive', 'VGIT': 'passive', 'VGLT': 'passive',
    'VCSH': 'passive', 'VCIT': 'passive', 'VCLT': 'passive',
    'SHY': 'passive', 'IEF': 'passive', 'TLT': 'passive', 'GOVT': 'passive',
    'BND': 'passive', 'AGG': 'passive', 'SCHZ': 'passive', 'BIV': 'passive',
    'BNDX': 'passive', 'IAGG': 'passive',
    'BSCQ': 'passive', 'BSCR': 'passive', 'BSJQ': 'passive', 'IBTF': 'passive',
    'CLIP': 'passive', 'UTWO': 'passive', 'UTEN': 'passive', 'SCHO': 'passive',
    'SPHY': 'passive', 'SJNK': 'passive', 'HYG': 'passive', 'JNK': 'passive',
    'MUB': 'passive', 'TIP': 'passive', 'VTIP': 'passive', 'SCHP': 'passive',
    'LQD': 'passive', 'FLOT': 'passive', 'EMB': 'passive', 'VWOB': 'passive',

    # Passive - Volatility
    'UVXY': 'passive', 'VXX': 'passive', 'VIXY': 'passive',

    # Active - Actively managed
    'JEPI': 'active',
    'MINT': 'active', 'LONZ': 'active', 'JPST': 'active', 'ICSH': 'active',
    'JAAA': 'active', 'DFSD': 'active', 'DFCF': 'active', 'VUSB': 'active',
    'VNLA': 'active', 'FBND': 'active',
    'DIVZ': 'active', 'IDVZ': 'active', 'COWZ': 'active', 'IQLT': 'active',
    'PCHI': 'active', 'QBER': 'active',
    'PDBC': 'active',
    'PFDE': 'active', 'PFOE': 'active',
}


# =============================================================================
# ETF SUB-ASSET CLASS MAPPING (for attribution hierarchy)
# =============================================================================
# Granular classification for holdings attribution Excel
# Hierarchy: Asset Class → Sub-Asset Class → Ticker
#
# EQUITY Sub-Asset Classes:
#   - US Large Cap, US Mid Cap, US Small Cap (broken down from "LARGE")
#   - International (Developed markets ex-US)
#   - EM (Emerging Markets)
#   - Volatility (VIX-related products)
#
# FIXED INCOME Sub-Asset Classes:
#   - Cash (T-Bills, Money Market - top of hierarchy)
#   - Ultra Short Duration (0-1 year active)
#   - Short (1-3 years)
#   - Intermediate (3-10 years)
#   - Long (10+ years)
#   - High Yield
#   - International

ETF_SUB_ASSET_CLASS: Dict[str, str] = {
    # =========================================================================
    # FIXED INCOME → Cash (ONLY actual USD cash, not ETFs)
    # =========================================================================
    'CASH_USD': 'Cash',  # Actual USD cash position (per Yang 2026-02-02)

    # =========================================================================
    # FIXED INCOME → Ultra Short Duration (T-Bills, Money Market, 0-1 year)
    # =========================================================================
    'BIL': 'Ultra Short Duration',      # SPDR Bloomberg 1-3 Month T-Bill ETF
    'SGOV': 'Ultra Short Duration',     # iShares 0-3 Month Treasury Bond ETF
    'TFLO': 'Ultra Short Duration',     # iShares Treasury Floating Rate Bond ETF
    'XBIL': 'Ultra Short Duration',     # US Treasury 6 Month Bill ETF
    'TBIL': 'Ultra Short Duration',     # US Treasury 3 Month Bill ETF
    'BILS': 'Ultra Short Duration',     # SPDR Bloomberg 3-12 Month T-Bill ETF
    'OBIL': 'Ultra Short Duration',     # US Treasury 12 Month Bill ETF
    'IBIL': 'Ultra Short Duration',     # iShares Treasury Bill ETF
    'CLIP': 'Ultra Short Duration',     # Global X 1-3 Month T-Bill ETF
    'MINT': 'Ultra Short Duration',     # PIMCO Enhanced Short Maturity Active ETF
    'JPST': 'Ultra Short Duration',     # JPMorgan Ultra-Short Income ETF
    'ICSH': 'Ultra Short Duration',     # BlackRock Ultra Short-Term Bond ETF
    'VUSB': 'Ultra Short Duration',     # Vanguard Ultra-Short Bond ETF

    # =========================================================================
    # FIXED INCOME → Short Duration (1-3 years)
    # =========================================================================
    'VGSH': 'Short Duration',     # Vanguard Short-Term Treasury ETF
    'VCSH': 'Short Duration',     # Vanguard Short-Term Corporate Bond ETF
    'SHY': 'Short Duration',      # iShares 1-3 Year Treasury Bond ETF
    'SCHO': 'Short Duration',     # Schwab Short-Term US Treasury ETF
    'UTWO': 'Short Duration',     # US Treasury 2 Year Note ETF
    'BSCQ': 'Short Duration',     # Invesco BulletShares 2026 Corporate Bond ETF
    'BSCR': 'Short Duration',     # Invesco BulletShares 2027 Corporate Bond ETF
    'IBTF': 'Short Duration',     # iShares iBonds Dec 2026 Term Treasury ETF
    'VTES': 'Short Duration',     # Vanguard Short-Term Tax-Exempt Bond ETF
    'DFSD': 'Short Duration',     # Dimensional Short-Duration Fixed Income ETF
    'VNLA': 'Short Duration',     # Janus Henderson Short Duration Income ETF

    # =========================================================================
    # FIXED INCOME → Structured Credit (CLO, Senior Loans, Specialty)
    # =========================================================================
    'JAAA': 'Structured Credit',     # Janus Henderson AAA CLO ETF
    'LONZ': 'Structured Credit',     # PIMCO Senior Loan Active ETF
    'QBER': 'Structured Credit',     # TrueShares Structured Outcome ETF

    # =========================================================================
    # FIXED INCOME → Intermediate (3-10 years)
    # =========================================================================
    'BND': 'Intermediate',      # Vanguard Total Bond Market ETF
    'AGG': 'Intermediate',      # iShares Core US Aggregate Bond ETF
    'SCHZ': 'Intermediate',     # Schwab US Aggregate Bond ETF
    'BIV': 'Intermediate',      # Vanguard Intermediate-Term Bond ETF
    'VGIT': 'Intermediate',     # Vanguard Intermediate-Term Treasury ETF
    'VCIT': 'Intermediate',     # Vanguard Intermediate-Term Corporate Bond ETF
    'IEF': 'Intermediate',      # iShares 7-10 Year Treasury Bond ETF
    'UTEN': 'Intermediate',     # US Treasury 10 Year Note ETF
    'GOVT': 'Intermediate',     # iShares US Treasury Bond ETF
    'FBND': 'Intermediate',     # Fidelity Total Bond ETF
    'DFCF': 'Intermediate',     # Dimensional Core Fixed Income ETF
    'FLOT': 'Intermediate',     # iShares Floating Rate Bond ETF

    # =========================================================================
    # FIXED INCOME → Long Duration (10+ years)
    # =========================================================================
    'VGLT': 'Long Duration',     # Vanguard Long-Term Treasury ETF
    'VCLT': 'Long Duration',     # Vanguard Long-Term Corporate Bond ETF
    'TLT': 'Long Duration',      # iShares 20+ Year Treasury Bond ETF
    'LQD': 'Long Duration',      # iShares iBoxx Investment Grade Corporate Bond ETF

    # =========================================================================
    # FIXED INCOME → High Yield
    # =========================================================================
    'HYG': 'High Yield',      # iShares iBoxx High Yield Corporate Bond ETF
    'JNK': 'High Yield',      # SPDR Bloomberg High Yield Bond ETF
    'SPHY': 'High Yield',     # SPDR Portfolio High Yield Bond ETF
    'SJNK': 'High Yield',     # SPDR Bloomberg Short Term High Yield Bond ETF
    'PCHI': 'High Yield',     # Polen High Yield ETF
    'BSJQ': 'High Yield',     # Invesco BulletShares 2026 High Yield Corporate Bond ETF

    # =========================================================================
    # FIXED INCOME → International
    # =========================================================================
    'BNDX': 'International',     # Vanguard Total International Bond ETF
    'IAGG': 'International',     # iShares Core International Aggregate Bond ETF
    'EMB': 'International',      # iShares JP Morgan USD Emerging Markets Bond ETF
    'VWOB': 'International',     # Vanguard Emerging Markets Government Bond ETF
    'PCY': 'International',      # Invesco Emerging Markets Sovereign Debt ETF

    # =========================================================================
    # FIXED INCOME → Municipal / TIPS
    # =========================================================================
    'MUB': 'Municipal',      # iShares National Muni Bond ETF
    'TIP': 'TIPS',           # iShares TIPS Bond ETF
    'VTIP': 'TIPS',          # Vanguard Short-Term Inflation-Protected Securities ETF
    'SCHP': 'TIPS',          # Schwab US TIPS ETF

    # =========================================================================
    # EQUITY → US Large Cap (replaces ambiguous "LARGE" per Yang 2026-02-02)
    # =========================================================================
    # Note: Only mapping EQUITY sub-assets where Excel shows "LARGE".
    # All other sub-assets come from Yang's Excel directly - no override.
    'SPY': 'US Large Cap',
    'VOO': 'US Large Cap',
    'IVV': 'US Large Cap',
    'VTI': 'US Large Cap',
    'SPYM': 'US Large Cap',
    'QQQ': 'US Large Cap',
    'QQQM': 'US Large Cap',
    'VUG': 'US Large Cap',
    'VTV': 'US Large Cap',
    'QUAL': 'US Large Cap',
    'SPMO': 'US Large Cap',
    'COWZ': 'US Large Cap',
    'SCHD': 'US Large Cap',
    'DVY': 'US Large Cap',
    'DGRO': 'US Large Cap',
    'DIVZ': 'US Large Cap',
    'JEPI': 'US Large Cap',
    'VGT': 'US Large Cap',
    'XLK': 'US Large Cap',
    'XLE': 'US Large Cap',
    'XLF': 'US Large Cap',
    'XLU': 'US Large Cap',
    'VNQ': 'US Large Cap',
    'PFDE': 'US Large Cap',
    'PFOE': 'US Large Cap',

    # =========================================================================
    # EQUITY → US Mid Cap
    # =========================================================================
    'IJH': 'US Mid Cap',
    'IWR': 'US Mid Cap',
    'VO': 'US Mid Cap',

    # =========================================================================
    # EQUITY → US Small Cap
    # =========================================================================
    'IJR': 'US Small Cap',
    'IWM': 'US Small Cap',
    'VB': 'US Small Cap',
    'SPSM': 'US Small Cap',

    # =========================================================================
    # EQUITY → Developed (International Developed Markets - keep original label)
    # =========================================================================
    'VXUS': 'Developed',
    'VEA': 'Developed',
    'IEFA': 'Developed',
    'EFA': 'Developed',
    'SPDW': 'Developed',
    'IQLT': 'Developed',
    'IDVZ': 'Developed',
    'EWJ': 'Developed',

    # =========================================================================
    # EQUITY → International (ONLY VSS per Yang 2026-02-02)
    # =========================================================================
    'VSS': 'International',  # Vanguard FTSE All-World ex-US Small-Cap ETF

    # =========================================================================
    # EQUITY → EM (Emerging Markets)
    # =========================================================================
    'VWO': 'EM',
    'IEMG': 'EM',
    'EEM': 'EM',
    'INDA': 'EM',
    'MCHI': 'EM',

    # =========================================================================
    # EQUITY → Volatility
    # =========================================================================
    'UVXY': 'Volatility',
    'VXX': 'Volatility',
    'VIXY': 'Volatility',

    # =========================================================================
    # EQUITY → Global (mix of US + International)
    # =========================================================================
    'ACWI': 'Global',

    # =========================================================================
    # HEDGE → Commodities
    # =========================================================================
    'GLD': 'Gold',
    'IAU': 'Gold',
    'SLV': 'Silver',
    'DBC': 'Commodities',
    'PDBC': 'Commodities',
    'GSG': 'Commodities',
    'USO': 'Oil',
}


# =============================================================================
# ETF SECTOR MAPPING (for positioning segment breakdown)
# =============================================================================

ETF_SECTOR_MAPPING: Dict[str, str] = {
    # Government (Treasuries)
    'BIL': 'Government', 'SGOV': 'Government', 'TFLO': 'Government',
    'XBIL': 'Government', 'TBIL': 'Government', 'BILS': 'Government',
    'OBIL': 'Government', 'IBIL': 'Government',
    'SHY': 'Government', 'IEF': 'Government', 'TLT': 'Government',
    'VGSH': 'Government', 'VGIT': 'Government', 'VGLT': 'Government',
    'GOVT': 'Government', 'SCHO': 'Government', 'UTWO': 'Government',
    'UTEN': 'Government', 'CLIP': 'Government', 'IBTF': 'Government',

    # Investment Grade Corporate
    'AGG': 'Investment Grade', 'BND': 'Investment Grade',
    'VCSH': 'Investment Grade', 'VCIT': 'Investment Grade',
    'VCLT': 'Investment Grade', 'LQD': 'Investment Grade',
    'SCHZ': 'Investment Grade', 'BIV': 'Investment Grade',
    'BSCQ': 'Investment Grade', 'BSCR': 'Investment Grade',
    'FBND': 'Investment Grade', 'DFCF': 'Investment Grade',
    'FLOT': 'Investment Grade',

    # High Yield
    'HYG': 'High Yield', 'JNK': 'High Yield', 'SPHY': 'High Yield',
    'SJNK': 'High Yield', 'BSJQ': 'High Yield', 'PCHI': 'High Yield',

    # Ultra Short / Cash Management
    'MINT': 'Ultra Short', 'JPST': 'Ultra Short', 'ICSH': 'Ultra Short',
    'JAAA': 'Ultra Short', 'DFSD': 'Ultra Short', 'VUSB': 'Ultra Short',
    'VNLA': 'Ultra Short', 'LONZ': 'Ultra Short',

    # International Fixed Income
    'BNDX': 'International', 'IAGG': 'International', 'EMB': 'International',
    'VWOB': 'International', 'PCY': 'International',

    # Municipal / TIPS
    'MUB': 'Municipal', 'TIP': 'TIPS', 'VTIP': 'TIPS', 'SCHP': 'TIPS',
    'QBER': 'Structured',

    # US Large Cap Equity
    'SPY': 'US Large Cap', 'VOO': 'US Large Cap', 'IVV': 'US Large Cap',
    'VTI': 'US Large Cap', 'SPYM': 'US Large Cap',

    # US Growth
    'QQQ': 'US Growth', 'QQQM': 'US Growth', 'VUG': 'US Growth',

    # US Value
    'VTV': 'US Value',

    # US Mid/Small Cap
    'IJH': 'US Mid Cap', 'IWR': 'US Mid Cap', 'VO': 'US Mid Cap',
    'IJR': 'US Small Cap', 'IWM': 'US Small Cap', 'VB': 'US Small Cap',
    'SPSM': 'US Small Cap',

    # US Factor/Dividend
    'QUAL': 'US Factor', 'SPMO': 'US Factor', 'COWZ': 'US Factor',
    'SCHD': 'US Dividend', 'DVY': 'US Dividend', 'DGRO': 'US Dividend',
    'DIVZ': 'US Dividend', 'JEPI': 'US Dividend',

    # US Sector
    'VGT': 'Technology', 'XLK': 'Technology',
    'XLE': 'Energy', 'XLF': 'Financials', 'XLU': 'Utilities',
    'VNQ': 'Real Estate',

    # International Developed
    'VXUS': 'International Developed', 'VEA': 'International Developed',
    'IEFA': 'International Developed', 'EFA': 'International Developed',
    'SPDW': 'International Developed', 'VSS': 'International Developed',
    'IQLT': 'International Developed', 'IDVZ': 'International Developed',
    'EWJ': 'Japan',

    # Emerging Markets
    'VWO': 'Emerging Markets', 'IEMG': 'Emerging Markets',
    'EEM': 'Emerging Markets', 'INDA': 'India', 'MCHI': 'China',

    # Global
    'ACWI': 'Global',

    # Active/Specialty
    'PFDE': 'Active US', 'PFOE': 'Active US',

    # Volatility
    'UVXY': 'Volatility', 'VXX': 'Volatility', 'VIXY': 'Volatility',

    # Commodities
    'GLD': 'Gold', 'IAU': 'Gold', 'SLV': 'Silver',
    'DBC': 'Commodities', 'PDBC': 'Commodities', 'GSG': 'Commodities',
    'USO': 'Oil',
}


# =============================================================================
# ETF NAME OVERRIDES (for display purposes)
# =============================================================================

ETF_NAME_OVERRIDES: Dict[str, str] = {
    'PFDE': 'Pathfinder Disciplined US Equities ETF',
    'PFOE': 'Pathfinder Focused Opportunities ETF',
    'JAAA': 'Janus Henderson AAA CLO ETF',
    'DIVZ': 'TrueShares Low Volatility Equity Income ETF',
    'IDVZ': 'TrueShares International Equity Income ETF',
    'PCHI': 'Polen High Yield ETF',  # NOTE: NOT MSCI China (that's MCHI)
}


# =============================================================================
# ETF BETA OVERRIDES (per Yang's direction 2026-01-13)
# =============================================================================

ETF_BETA_OVERRIDES: Dict[str, float] = {
    'PFDE': 1.05,  # Pathfinder Disciplined US Equities
    'PFOE': 1.22,  # Pathfinder Focused Opportunities
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_asset_class(ticker: str, default: str = 'equity') -> str:
    """
    Get the asset class for an ETF ticker.

    Args:
        ticker: ETF ticker symbol (e.g., 'SPY', 'AGG')
        default: Default classification if ticker not found

    Returns:
        Asset class: 'fixed_income', 'equity', or 'hedge'
    """
    asset_class = ETF_CLASSIFICATIONS.get(ticker)
    if asset_class is None:
        logger.warning(f"Unknown ETF ticker '{ticker}' - defaulting to '{default}'")
        return default
    return asset_class


def is_fixed_income(ticker: str) -> bool:
    """Check if an ETF is classified as fixed income."""
    return ticker in FIXED_INCOME_TICKERS


def is_equity(ticker: str) -> bool:
    """Check if an ETF is classified as equity."""
    return ticker in EQUITY_TICKERS


def is_hedge(ticker: str) -> bool:
    """Check if an ETF is classified as hedge/alternative."""
    return ticker in HEDGE_TICKERS


def get_management_style(ticker: str, default: str = 'passive') -> str:
    """
    Get the management style for an ETF.

    Args:
        ticker: ETF ticker symbol
        default: Default style if ticker not found

    Returns:
        Management style: 'active' or 'passive'
    """
    style = ETF_MANAGEMENT_STYLE.get(ticker)
    if style is None:
        logger.debug(f"Management style unknown for '{ticker}' - defaulting to '{default}'")
        return default
    return style


def get_sub_asset_class(ticker: str, default: str = '') -> str:
    """
    Get the sub-asset class for an ETF (for attribution hierarchy).

    Args:
        ticker: ETF ticker symbol
        default: Default sub-asset class if ticker not found

    Returns:
        Sub-asset class (e.g., 'US Large Cap', 'Cash', 'EM', 'High Yield')
    """
    sub_asset = ETF_SUB_ASSET_CLASS.get(ticker)
    if sub_asset is None:
        # If not found, try to infer from asset class
        asset_class = get_asset_class(ticker, 'equity')
        if asset_class == 'equity':
            logger.warning(f"Unknown equity ticker '{ticker}' sub-asset - defaulting to 'US Large Cap'")
            return 'US Large Cap'
        elif asset_class == 'fixed_income':
            logger.warning(f"Unknown fixed income ticker '{ticker}' sub-asset - defaulting to 'Intermediate'")
            return 'Intermediate'
        else:
            return default
    return sub_asset


def get_sector(ticker: str, default: str = 'Other') -> str:
    """
    Get the sector/segment for an ETF.

    Args:
        ticker: ETF ticker symbol
        default: Default sector if ticker not found

    Returns:
        Sector name (e.g., 'Government', 'US Large Cap', 'Gold')
    """
    return ETF_SECTOR_MAPPING.get(ticker, default)


def get_display_name(ticker: str, fallback_name: Optional[str] = None) -> str:
    """
    Get the display name for an ETF.

    Args:
        ticker: ETF ticker symbol
        fallback_name: Name to use if no override exists

    Returns:
        Display name for the ETF
    """
    return ETF_NAME_OVERRIDES.get(ticker, fallback_name or ticker)


def get_beta_override(ticker: str) -> Optional[float]:
    """
    Get the beta override for an ETF if one exists.

    Args:
        ticker: ETF ticker symbol

    Returns:
        Beta override value, or None if no override
    """
    return ETF_BETA_OVERRIDES.get(ticker)


def classify_holdings(holdings_df, ticker_column: str = 'ticker') -> dict:
    """
    Classify all holdings in a DataFrame by asset class.

    Args:
        holdings_df: DataFrame with ticker column
        ticker_column: Name of the column containing tickers

    Returns:
        Dict with asset class weights and unknown tickers
    """
    unknown_tickers = []
    weights = {'fixed_income': 0.0, 'equity': 0.0, 'hedge': 0.0}

    for _, row in holdings_df.iterrows():
        ticker = row[ticker_column]
        weight = row.get('weight', 0) or row.get('allocation', 0) or 0

        asset_class = ETF_CLASSIFICATIONS.get(ticker)
        if asset_class is None:
            unknown_tickers.append(ticker)
            asset_class = 'equity'  # Default

        weights[asset_class] += float(weight)

    if unknown_tickers:
        logger.warning(f"Unknown tickers defaulted to equity: {unknown_tickers}")

    return {
        'weights': weights,
        'unknown_tickers': unknown_tickers
    }


def validate_tickers(tickers: list) -> dict:
    """
    Validate a list of tickers against the classification database.

    Args:
        tickers: List of ticker symbols to validate

    Returns:
        Dict with 'known', 'unknown', and 'coverage' stats
    """
    known = [t for t in tickers if t in ETF_CLASSIFICATIONS]
    unknown = [t for t in tickers if t not in ETF_CLASSIFICATIONS]

    return {
        'known': known,
        'unknown': unknown,
        'total': len(tickers),
        'coverage': len(known) / len(tickers) * 100 if tickers else 0
    }


# =============================================================================
# MODULE STATISTICS (for documentation)
# =============================================================================

def get_stats() -> dict:
    """Get statistics about the classification database."""
    return {
        'total_etfs': len(ETF_CLASSIFICATIONS),
        'fixed_income_count': len(FIXED_INCOME_TICKERS),
        'equity_count': len(EQUITY_TICKERS),
        'hedge_count': len(HEDGE_TICKERS),
        'management_styles': len(ETF_MANAGEMENT_STYLE),
        'sectors': len(set(ETF_SECTOR_MAPPING.values())),
    }


if __name__ == '__main__':
    # Print stats when run directly
    stats = get_stats()
    print("ETF Classification Module Statistics:")
    print(f"  Total ETFs: {stats['total_etfs']}")
    print(f"  Fixed Income: {stats['fixed_income_count']}")
    print(f"  Equity: {stats['equity_count']}")
    print(f"  Hedge: {stats['hedge_count']}")
    print(f"  Management Styles: {stats['management_styles']}")
    print(f"  Sectors: {stats['sectors']}")
