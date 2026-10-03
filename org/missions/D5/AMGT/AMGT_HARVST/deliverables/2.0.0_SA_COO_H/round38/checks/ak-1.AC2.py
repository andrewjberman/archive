"""HVST-ak-1 AC2 (issuer, LIVE PROBE, NO WRITE): the scorer module calls the real FinBERT Lambda `opal-news-ai-sentiment`
(FWD-16; CTO fold ruling 6, reuse; build ladder rung 2) and returns a label, a confidence and a signed score.

Calls `finbert_sentiment.score_text(text)` with NO invoke override, so the module's own boto3 path calls the Lambda, on
3 fixed texts. PASS requires:
- `SCORER == "opal-news-ai-sentiment"`;
- each result's label is in {positive, negative, neutral} and its confidence is a float in [0, 1];
- the signed score follows the label: +confidence for positive, -confidence for negative, 0.0 for neutral;
- the 3 labels are not all the same, which a constant stub would produce.
Nothing is written anywhere.
"""
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)

TEXTS = [
    "Shares surged after the company reported record quarterly profit that beat every analyst estimate.",
    "Shares plunged as losses widened, the company cut its full-year outlook and warned of layoffs.",
    "The company will hold its annual shareholder meeting on Tuesday at its headquarters.",
]


def main():
    failures = []
    try:
        from lib.research.harvest import finbert_sentiment as fs
    except Exception as exc:  # the module does not exist yet at the base
        print("IMPORT FAILED: %s: %s" % (type(exc).__name__, exc))
        print("AC2 RESULT: FAIL (1 failure(s))")
        return 1
    if getattr(fs, "SCORER", None) != "opal-news-ai-sentiment":
        failures.append("SCORER is %r" % getattr(fs, "SCORER", None))
    labels = []
    for i, text in enumerate(TEXTS):
        try:
            r = fs.score_text(text)
        except Exception as exc:
            failures.append("text %d raised %s: %s" % (i, type(exc).__name__, str(exc)[:160]))
            continue
        label, conf, score = r.get("label"), r.get("confidence"), r.get("score")
        print("TEXT %d -> label=%s confidence=%s score=%s" % (i, label, conf, score))
        labels.append(label)
        if label not in ("positive", "negative", "neutral"):
            failures.append("text %d label %r" % (i, label))
            continue
        if not isinstance(conf, float) or not 0.0 <= conf <= 1.0:
            failures.append("text %d confidence %r" % (i, conf))
            continue
        expected = {"positive": conf, "negative": -conf, "neutral": 0.0}[label]
        if score != expected:
            failures.append("text %d score %r != %r for label %s" % (i, score, expected, label))
    if len(labels) == len(TEXTS) and len(set(labels)) == 1:
        failures.append("all %d labels are %r (a constant would read the same)" % (len(labels), labels[0]))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    sys.exit(main())
