"""RB-s-9 fixture generator (scratch). Writes three ui-smoke fixture maps into
portal/.frontend-dev/testing/ -- { "<url-substring>": <response-body> }.

Deterministic (seeded) so a re-run is byte-identical. Shapes follow the typed
consumers in portal/src/api (market.ts, sentiment.ts, portal-proxy.ts,
hooks/useDataFreshness.ts). Values are illustrative, not market data.
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / ".frontend-dev" / "testing"
rng = random.Random(9)
AS_OF = "2026-09-11"
GEN = "2026-09-11T21:30:00Z"

EQ = ["S&P 500", "Dow Jones", "Nasdaq", "Russell 1000", "Russell 2000", "Russell Mid Cap",
      "Russell Mid Cap Growth", "Russell Mid Cap Value", "Russell 1000 Growth", "Russell 1000 Value",
      "MSCI ACWI", "MSCI ACWI ex US", "MSCI EAFE", "MSCI EAFE Growth", "MSCI EAFE Value",
      "MSCI Emerging Markets", "MSCI USA", "MSCI USA Growth", "MSCI USA Value",
      "MSCI USA Minimum Volatility", "MSCI USA Momentum", "MSCI USA Quality", "MSCI USA Size",
      "MSCI Australia", "MSCI Brazil", "MSCI China", "MSCI France", "MSCI Germany", "MSCI India",
      "MSCI Italy", "MSCI Japan", "MSCI Netherlands", "MSCI Saudi Arabia", "MSCI South Africa",
      "MSCI South Korea", "MSCI Spain", "MSCI Sweden", "MSCI Switzerland", "MSCI Taiwan",
      "MSCI United Kindom",
      "Energy", "Materials", "Industrials", "Consumer Discretionary", "Consumer Staples",
      "Health Care", "Financials", "Information Technology", "Communication Services",
      "Utilities", "Real Estate"]
FI = ["Bloomberg Aggregate", "Bloomberg 0-1 Year Treasury", "Bloomberg 1-3 Year Gov/Credit",
      "Bloomberg 1-5 Year Gov/Credit", "Bloomberg 20+ Year Treasury", "Bloomberg US Corporate",
      "Bloomberg High Yield", "Bloomberg 0-5 Year High Yield", "Bloomberg TIPS",
      "Bloomberg 0-5 Year TIPS", "Bloomberg Municipal"]
CM = ["S&P GSCI", "Crude Oil WTI", "Crude Oil Brent", "Natural Gas", "Gold", "Silver", "Copper",
      "Bitcoin", "Ethereum"]
PERIODS = {"1D": 1.2, "WTD": 2.0, "TTW": 2.8, "MTD": 3.0, "1M": 4.0, "QTD": 5.0, "1Q": 6.0,
           "YTD": 9.0, "1Y": 14.0}


def r(scale):
    return round(rng.uniform(-scale, scale * 1.3), 2)


def days(n):
    d0 = date(2026, 9, 11)
    return [(d0 - timedelta(days=n - 1 - i)).isoformat() for i in range(n)]


def manifest():
    src = {"data_as_of": AS_OF, "timestamp": "2026-09-11T17:00:00-04:00", "frequency": "weekly"}
    return {"generated_at": GEN, "sources": {k: dict(src) for k in
            ["yang", "data_pkl", "model_pkl", "attribution_excel", "peer_excel"]}}


# ---------------------------------------------------------------- market (populated)
def market():
    indices = []
    for names, ac in ((EQ, "Equities"), (FI, "Fixed Income"), (CM, "Commodities")):
        for n in names:
            indices.append({"ticker": n, "name": n, "entity_type": "INDEX", "asset_class": ac,
                            "latest_price": round(rng.uniform(20, 6000), 2), "latest_date": AS_OF,
                            # FRACTIONS, not percents: the heat map multiplies by 100
                            # (first render showed +254.00% from 2.54).
                            "period_returns": {p: round(r(s) / 100, 4) for p, s in PERIODS.items()}})

    def rsi_block():
        v = round(rng.uniform(35, 68), 1)
        return {"value": v, "status": "neutral", "change_7d": r(4), "change_14d": r(5),
                "change_30d": r(8), "change_90d": r(10), "change_1y": r(12), "change_3y": r(14)}

    def rsi_details(ac, names):
        hist = [{"date": d, "value": round(rng.uniform(35, 68), 1)} for d in days(60)]
        return {"generated_at": GEN, "tier": 2, "asset_class": ac,
                "indices": {n: {"current": round(rng.uniform(30, 72), 1), "change_14d": r(6),
                                "historical": hist[-20:]} for n in names},
                "aggregate": {"value": 52.4, "status": "neutral", "historical": hist,
                              "history": {"change_7d": 1.3, "change_30d": -2.1}}}

    def topic(i, bull):
        s = 0.4 if bull else -0.4
        return {"topic": ("Earnings breadth" if bull else "Rate path uncertainty") + f" {i + 1}",
                "context": "Illustrative fixture topic for layout capture.",
                "article_count": 12 + i, "sentiment_bull_bear": s, "sentiment_confidence_fear": s,
                "sentiment_risk_appetite": s, "sentiment_positive_negative": s,
                "sentiment_emotional_intensity": 0.5, "top_sources": ["Reuters", "Bloomberg"],
                "trending_rank": i + 1, "top_articles": []}

    def sig(v, lab):
        return {"value": v, "label": lab, "change": 1.5}

    regime_hist = [{"date": d, "regime": "neutral"} for d in days(30)]
    def ts():
        return [{"date": d, "value": round(rng.uniform(30, 70), 1), "raw": {}} for d in days(90)]

    fg_hist = [{"date": d, "value": int(rng.uniform(30, 70)), "description": "neutral"} for d in days(90)]
    return {
        "summary/all-returns.json": {"generated_at": GEN, "tier": 1, "page": "market-overview",
                                     "as_of_date": AS_OF, "last_updated": GEN,
                                     "count": len(indices), "indices": indices},
        "rsi-summary.json": {"generated_at": GEN, "tier": 1, "page": "market-overview",
                             "rsi_summary": {"equities": rsi_block(), "fixedIncome": rsi_block(),
                                             "commodities": rsi_block()}, "last_updated": GEN},
        "rsi-details-equities.json": rsi_details("equities", EQ[:23]),
        "rsi-details-fixedIncome.json": rsi_details("fixedIncome", FI),
        "rsi-details-commodities.json": rsi_details("commodities", CM),
        "trending/latest.json": {"generated_at": GEN, "date": AS_OF,
                                 "bullish": [topic(i, True) for i in range(3)],
                                 "bearish": [topic(i, False) for i in range(3)]},
        "market-regime.json": {"regime": "neutral", "description": "Mixed signals across momentum and volatility.",
                               "triggeredBy": "fixture", "lastUpdated": GEN, "generated_at": GEN,
                               "signals": {"momentum": sig(55, "Neutral"), "volatility": sig(61, "Calm"),
                                           "correlation": sig(48, "Neutral"), "rateRegime": sig(52, "Flat")},
                               "history": regime_hist,
                               "periodStats": {"90D": None, "1Y": None, "3Y": None}},
        "market-regime-history.json": {"generated_at": GEN,
                                       "timeSeries": {"momentum": ts(), "volatility": ts(),
                                                      "correlation": ts(), "rateRegime": ts()},
                                       "regimeHistory": regime_hist},
        "fear-greed-index.json": {"current": {"value": 54, "description": "neutral", "last_update": GEN,
                                              "previous_close": 52, "previous_1_week": 49,
                                              "previous_1_month": 44, "previous_1_year": 61},
                                  "historical": fg_hist, "generated_at": GEN, "source": "fixture"},
        "keyword-sentiments.json": {"generated_at": GEN, "keywords": [
            {"keyword": k, "sentiment": round(rng.uniform(-0.5, 0.5), 3), "count": 40 - i,
             "bullish": 10, "bearish": 8, "neutral": 12}
            for i, k in enumerate(["earnings", "inflation", "fed", "tariffs", "ai", "oil", "jobs",
                                   "housing", "china", "yields", "credit", "dollar", "gold",
                                   "consumer", "banks", "chips", "energy", "europe"])]},
        "json/latest/manifest.json": manifest(),
    }


# ---------------------------------------------------------------- positioning books
BOOKS = [("UST", "Ultra-Short Term", 0.95), ("ST", "Short Term", 0.80), ("INT", "Intermediate", 0.60),
         ("LT", "Long Term", 0.40), ("ULT", "Ultra-Long Term", 0.20)]


def alloc(fi, cash=0.05, hedge=0.0):
    return {"cash": round(cash * 100, 1), "fixed_income": round((fi - cash) * 100, 1),
            "equity": round((1 - fi - hedge) * 100, 1), "hedge": round(hedge * 100, 1)}


def positioning(holdings_per_book):
    portfolios, current = {}, {}
    for code, name, fi in BOOKS:
        hs = holdings_per_book(code)
        portfolios[code] = {
            "code": code, "name": name, "allocation": alloc(fi),
            "delta": {"cash": 0.0, "fixed_income": -0.5, "equity": 0.5, "hedge": 0.0},
            "num_holdings": len(hs), "holdings": [{"ticker": h["ticker"], "weight": h["weight"]} for h in hs],
            "as_of_date": AS_OF, "prior_date": "2026-09-04",
            "management": {"active": 35.0, "passive": 65.0},
            "characteristics": {"yield": 4.1, "cost": 0.0021, "duration": round(1 + 8 * (1 - fi), 1),
                                "beta": round(1 - fi, 2), "credit": 1.1},
            "benchmark": {"allocation": alloc(fi + 0.02),
                          "characteristics": {"yield": 4.0, "cost": 0.0018, "duration": 5.0, "beta": 0.5, "credit": 1.0},
                          "spread": {"allocation": {"cash": 0.0, "fixed_income": -2.0, "equity": 2.0, "hedge": 0.0},
                                     "characteristics": {"yield": 0.1, "cost": 0.0003, "duration": 0.2,
                                                         "beta": 0.02, "credit": 0.1}}},
        }
        current[code] = {"holdings": hs, "aum": 120.0}
    return {"generated_at": GEN, "data_as_of": AS_OF, "portfolios": portfolios, "current_holdings": current}


def holding(t, n, ac, sub, w):
    return {"ticker": t, "name": n, "asset_class": ac, "sub_asset_class": sub, "weight": w,
            "fee": 0.0005, "aum": 50000, "active": 0, "yield": 4.2, "duration": 2.0, "credit": 1.0,
            "beta": 0.1, "returns": {"QTD": 1.1, "YTD": 3.4, "1Y": 5.2, "SI": 9.8}}


def attr_holding(t, n, ac, sub, w, k):
    return {"ticker": t, "name": n, "asset_class": ac, "sub_asset_class": sub, "style_ticker": t,
            "weight": w, "fund_return": round(1.0 + k, 2), "style_return": round(0.8 + k, 2),
            "excess_return": 0.2, "fund_selection": 0.05, "policy_return": 0.7,
            "style_allocation": 0.03, "asset_allocation": 0.02, "total_attribution": 0.1}


SPARSE_ONE = holding("BIL", "SPDR Bloomberg 1-3 Month T-Bill ETF", "Fixed Income", "Treasuries", 1.0)
FULL = [("BIL", "SPDR 1-3 Month T-Bill", "Fixed Income", "Treasuries"),
        ("VGSH", "Vanguard Short-Term Treasury", "Fixed Income", "Treasuries"),
        ("VCIT", "Vanguard Intermediate Corporate", "Fixed Income", "Corporate"),
        ("JAAA", "Janus AAA CLO", "Fixed Income", "Securitized"),
        ("IVV", "iShares Core S&P 500", "Equity", "US Large Cap"),
        ("QUAL", "iShares MSCI USA Quality", "Equity", "US Factor"),
        ("IEFA", "iShares Core MSCI EAFE", "Equity", "International"),
        ("IEMG", "iShares Core MSCI EM", "Equity", "Emerging")]


def attribution_data(rows):
    out = {}
    for code, name, _ in BOOKS:
        per = {p: {"holdings": [attr_holding(*row, k * 0.1) for k, row in enumerate(rows)]}
               for p in ("qtd", "ytd", "1y", "si")}
        out[code] = {"code": code, "name": name, **per}
    return {"generated_at": GEN, "as_of_date": AS_OF, "data_as_of": AS_OF, "portfolios": out}


def ac_row(name, style, bet):
    return {"name": name, "style_weight": style, "policy_weight": round(style - bet, 1), "bet": bet,
            "asset_allocation": round(bet * 0.03, 3), "total": round(bet * 0.05, 3)}


# (fixed-income bet, equity bet) per period: each period pairs ONE narrow bar with ONE wide
# bar, and the narrow bar alternates side, so both the underweight and the overweight label
# are measured in the failing (narrow) case and the passing (wide) case.
TILTS = {"qtd": (-8.7, 0.6), "ytd": (-0.5, 9.2), "1y": (-4.0, 4.1), "si": (-0.3, 0.2)}


def allocation_summary():
    ports = {}
    for code, _, fi in BOOKS:
        per = {}
        for p, (fb, eb) in TILTS.items():
            acs = [ac_row("Fixed Income", round(fi * 100 + fb, 1), fb),
                   ac_row("Equity", round((1 - fi) * 100 + eb, 1), eb)]
            per[p] = {"asset_classes": acs, "total": {"style_weight": 100.0, "policy_weight": 100.0,
                                                      "asset_allocation": 0.05, "total": 0.12}}
        ports[code] = per
    return {"generated_at": GEN, "data_as_of": AS_OF, "portfolios": ports}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sparse = {
        "positioning/positioning_data.json": positioning(lambda c: [dict(SPARSE_ONE)]),
        "holdings_attribution_data.json": attribution_data([("BIL", "SPDR 1-3 Month T-Bill", "Fixed Income", "Treasuries", 100.0)]),
        "json/latest/manifest.json": manifest(),
    }
    full_rows = [(t, n, a, s, round(100 / len(FULL), 2)) for t, n, a, s in FULL]
    attribution = {
        "allocation_summary.json": allocation_summary(),
        "holdings_attribution_data.json": attribution_data(full_rows),
        "positioning/positioning_data.json": positioning(
            lambda c: [holding(t, n, a, s, round(1 / len(FULL), 4)) for t, n, a, s in FULL]),
        "json/latest/manifest.json": manifest(),
    }
    for fname, body in (("rb-s-9-market.json", market()), ("rb-s-9-sparse.json", sparse),
                        ("rb-s-9-attribution.json", attribution)):
        p = OUT / fname
        p.write_bytes((json.dumps(body, indent=1, ensure_ascii=True) + "\n").encode("ascii"))
        print("WROTE", p, p.stat().st_size, "bytes", len(body), "url keys")


if __name__ == "__main__":
    main()
