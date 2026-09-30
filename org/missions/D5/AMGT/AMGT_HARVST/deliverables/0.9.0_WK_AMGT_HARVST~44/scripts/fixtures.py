"""The HVST-c-1 planted fixture (variants 1 and 2, copied from ac2_burst_shape_census.py ~:149-200, which is read
only) plus a planted CONTROL. Every row carries `match_forms` ["Zorbex"], as every real mention row does."""
import datetime


def mk(i, pub, tier, month, dayn, hour, title, forms=("Zorbex",)):
    return {"security_key": "FIXT_US_Equity", "composite_figi": "FIXTURE", "article_key": "%s:fixture-%d" % (pub, i),
            "publisher": pub, "signal_tier": tier, "match_forms": list(forms),
            "published_utc": datetime.datetime(2026, month, dayn, hour, 0, tzinfo=datetime.timezone.utc), "title": title}


def variant1():
    return [
        mk(1, "wsj", "A", 9, 10, 9, "Zorbex Unveils Quantum Battery Plant in Ohio"),
        mk(2, "bbg", "A", 9, 10, 12, "Zorbex Breaks Ground on Quantum Battery Plant"),
        mk(3, "wsj", "A", 9, 11, 9, "Quantum Battery Plant Zorbex Announced Adds Jobs"),
        mk(4, "bbg", "A", 9, 11, 14, "Zorbex Quantum Battery Plant Draws State Subsidy"),
        mk(5, "ft", "A", 9, 12, 8, "Ohio Quantum Battery Plant Zorbex Faces Local Opposition"),
        mk(6, "sa", "B", 9, 12, 10, "Zorbex Quantum Battery Plant: Analyst Roundup"),
    ]


def variant2():
    bg = [
        mk(11, "wsj", "A", 9, 1, 9, "Zorbex Names New Chief Financial Officer"),
        mk(12, "bbg", "A", 9, 3, 9, "Zorbex Shares Fall on Analyst Downgrade"),
        mk(13, "sa", "A", 9, 5, 9, "Zorbex Board Approves Share Buyback"),
        mk(14, "ft", "A", 9, 7, 9, "Zorbex Settles Patent Suit With Rival"),
        mk(15, "wsj", "A", 9, 15, 9, "Zorbex Opens Office in Singapore"),
        mk(16, "bbg", "A", 9, 17, 9, "Zorbex Raises Prices on Enterprise Plans"),
    ]
    return variant1() + bg


def control():
    """Two UNRELATED multi-day stories of one security, no other coverage. Story X 09-10..09-11 (battery plant),
    story Y 09-13..09-14 (pension lawsuit): within the day-gap window of each other, disjoint in words."""
    return [
        mk(21, "wsj", "A", 9, 10, 9, "Zorbex Unveils Quantum Battery Plant in Ohio"),
        mk(22, "bbg", "A", 9, 10, 12, "Zorbex Breaks Ground on Quantum Battery Plant"),
        mk(23, "wsj", "A", 9, 11, 9, "Quantum Battery Plant Zorbex Adds Jobs"),
        mk(24, "bbg", "A", 9, 11, 14, "Zorbex Quantum Battery Plant Draws State Subsidy"),
        mk(25, "ft", "A", 9, 13, 8, "Zorbex Faces Pension Fund Lawsuit Over Retirees"),
        mk(26, "sa", "A", 9, 13, 10, "Retirees Sue Zorbex Pension Fund in Federal Court"),
        mk(27, "wsj", "A", 9, 14, 9, "Zorbex Pension Fund Lawsuit Hearing Set"),
        mk(28, "bbg", "A", 9, 14, 12, "Judge Schedules Zorbex Retirees Pension Lawsuit Hearing"),
    ]
