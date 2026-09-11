"""Proof-of-concept: the Trending / Breakout ranking math over a rolling 7-day chatter-volume
window. Uses a synthetic dataset (since a real 7-day history can't exist yet) to prove the
ALGORITHM is sound -- specifically that it correctly separates 'consistently loud' tickers from
'suddenly spiking' ones, and handles the zero-baseline edge case without letting pure noise
dominate the Breakout list."""
import random

random.seed(7)

TICKERS = ["NVDA", "RTX", "KHC", "AAPL", "XYZQ", "SLEEPY", "GME", "SMALLCO"]

# Simulate 7 days of daily chatter volume (organic-result count with a recency marker) per ticker.
# NVDA: consistently high (mega-cap, always in the news) -> should win TRENDING.
# GME: was quiet, spikes hard on day 7 (meme-stock event) -> should win BREAKOUT.
# SLEEPY/SMALLCO: near-zero baseline, one noisy blip -> must NOT dominate BREAKOUT off noise alone.
history = {
    "NVDA":    [9, 8, 9, 10, 9, 8, 9],
    "RTX":     [4, 3, 4, 5, 4, 4, 5],
    "KHC":     [3, 4, 3, 3, 4, 3, 4],
    "AAPL":    [7, 7, 6, 7, 8, 7, 7],
    "XYZQ":    [1, 1, 0, 1, 1, 0, 1],
    "SLEEPY":  [0, 0, 0, 0, 0, 0, 1],   # tiny blip off a zero baseline -- must not win breakout
    "GME":     [1, 1, 1, 1, 1, 2, 9],   # real spike on the last day
    "SMALLCO": [0, 0, 1, 0, 0, 0, 0],
}

TOP_N = 3
MIN_ABSOLUTE_JUMP = 3      # a breakout must ALSO gain at least this many raw mentions today
BASELINE_SMOOTHING = 1.0   # Laplace-style smoothing so a zero baseline isn't a divide-by-zero


def trending(history):
    """Highest ABSOLUTE chatter volume today."""
    today = {t: h[-1] for t, h in history.items()}
    return sorted(today.items(), key=lambda kv: kv[1], reverse=True)[:TOP_N]


def breakout(history):
    """Largest PERCENTAGE jump vs. the trailing 6-day baseline (today excluded from its own
    baseline), with two guards against noise dominating the list:
      1. BASELINE_SMOOTHING avoids a divide-by-zero / infinite-percent result for a ticker with a
         zero baseline -- a real behavior difference from a naive (today-avg)/avg formula.
      2. MIN_ABSOLUTE_JUMP requires the spike to also be a real, non-trivial absolute increase --
         a 0 -> 1 change is technically "infinite percent" but is noise, not a breakout."""
    scored = []
    for t, h in history.items():
        today, baseline_days = h[-1], h[:-1]
        baseline = sum(baseline_days) / len(baseline_days)
        pct_jump = (today - baseline) / (baseline + BASELINE_SMOOTHING)
        abs_jump = today - baseline
        if abs_jump < MIN_ABSOLUTE_JUMP:
            continue
        scored.append((t, pct_jump, today, round(baseline, 2)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:TOP_N]


if __name__ == "__main__":
    print("TRENDING (top absolute volume today):")
    for t, v in trending(history):
        print(f"  {t}: {v}")

    print("\nBREAKOUT (top % jump vs 6-day baseline, min absolute jump >= {}):".format(MIN_ABSOLUTE_JUMP))
    for t, pct, today, baseline in breakout(history):
        print(f"  {t}: +{pct*100:.0f}% (today={today}, baseline={baseline})")

    trending_set = {t for t, _ in trending(history)}
    breakout_set = {t for t, *_ in breakout(history)}
    union = trending_set | breakout_set
    print(f"\nACTIVE MONITOR SET (union, gets daily platform refresh): {sorted(union)} -- {len(union)} of {len(TICKERS)} tickers")
    print(f"Noise check: SLEEPY/SMALLCO (near-zero baseline, tiny blips) excluded from breakout: "
          f"{'SLEEPY' not in breakout_set and 'SMALLCO' not in breakout_set}")
