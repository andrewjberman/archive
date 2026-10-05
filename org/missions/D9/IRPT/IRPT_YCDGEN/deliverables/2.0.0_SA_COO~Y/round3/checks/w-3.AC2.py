"""IRPT_YCDGEN round 3 check w-3.AC2 (YCD-w-3). Run from the repository root. Prints 'w-3.AC2 RESULT: PASS|FAIL <why>'."""
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
RESEARCH = ROOT / "infra/aws/lambda/investor-reporting/ycharts/research"
MAPS = ROOT / "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"


def verdict(ok, why):
    print("w-3.AC2 RESULT: %s %s" % ("PASS" if ok else "FAIL", why))
    sys.exit(0 if ok else 1)




BASE = json.loads('{"p1.e01":"BUILDER_ONLY","p1.e02":"BUILDER_ONLY","p1.e03":"BUILDER_ONLY","p1.e04":"BUILDER_ONLY","p1.e05":"BUILDER_ONLY","p10.e01":"BUILDER_ONLY","p10.e02":"BUILDER_ONLY","p11.e01":"BUILDER_ONLY","p11.e02":"BUILDER_ONLY","p12.e01":"BUILDER_ONLY","p12.e02":"BUILDER_ONLY","p12.e03":"BUILDER_ONLY","p12.e05":"BUILDER_ONLY","p13.e01":"BUILDER_ONLY","p13.e02":"BUILDER_ONLY","p13.e03":"BUILDER_ONLY","p13.e04":"BUILDER_ONLY","p13.e05":"BUILDER_ONLY","p13.e06":"BUILDER_ONLY","p14.e01":"BUILDER_ONLY","p14.e02":"BUILDER_ONLY","p14.e03":"BUILDER_ONLY","p14.e04":"BUILDER_ONLY","p14.e05":"BUILDER_ONLY","p14.e06":"BUILDER_ONLY","p15.e01":"BUILDER_ONLY","p15.e02":"BUILDER_ONLY","p16.e01":"BUILDER_ONLY","p16.e02":"BUILDER_ONLY","p17.e01":"BUILDER_ONLY","p18.e01":"BUILDER_ONLY","p18.e02":"BUILDER_ONLY","p19.e01":"BUILDER_ONLY","p2.e01":"BUILDER_ONLY","p2.e02":"BUILDER_ONLY","p2.e03":{"call":"portfolio_info","field":"$..name"},"p2.e04":{"call":"portfolio_level_series","field":"$.chart_data[0][0].raw_data"},"p2.e05":"BUILDER_ONLY","p2.e06":"BUILDER_ONLY","p2.e07":{"call":"portfolio_level_series","field":"$.chart_data[0][0].raw_data[-1][0]"},"p2.e16":{"call":"portfolio_level_series","field":"$.chart_data[0][0].raw_data[-1][0]"},"p2.e17":{"call":"portfolio_level_series","field":"$.chart_data[0][0].raw_data"},"p2.e18":{"call":"portfolio_level_series","field":"$.chart_data[0][0].raw_data"},"p2.e19":"BUILDER_ONLY","p2.e27":"BUILDER_ONLY","p20.e01":"BUILDER_ONLY","p21.e01":"BUILDER_ONLY","p22.e01":"BUILDER_ONLY","p23.e01":"BUILDER_ONLY","p3.e01":"BUILDER_ONLY","p3.e08":"BUILDER_ONLY","p3.e18":"BUILDER_ONLY","p3.e24":{"call":"portfolio_equity_exposure","field":"$.indicesData[0].data[?(@.calc_name in [\'stock_style_lg_cap_value\', \'stock_style_mid_cap_value\', \'stock_style_sm_cap_value\', \'stock_style_lg_cap_blend\', \'stock_style_mid_cap_blend\', \'stock_style_sm_cap_blend\', \'stock_style_lg_cap_growth\', \'stock_style_mid_cap_growth\', \'stock_style_sm_cap_growth\'])].calc_raw_value"},"p3.e25":{"call":"portfolio_region_exposure","field":"$.indicesData[0].data[?(@.calc_name in [\'region_exposure_developed_markets\', \'region_exposure_emerging_markets\'])].calc_raw_value"},"p3.e26":{"call":"portfolio_region_exposure","field":"$.indicesData[0].data[?(@.calc_name in [\'region_exposure_americas\', \'region_exposure_greater_europe\', \'region_exposure_greater_asia\'])].calc_raw_value"},"p5.e01":"BUILDER_ONLY","p5.e16":"BUILDER_ONLY","p5.e24":"BUILDER_ONLY","p5.e33":"BUILDER_ONLY","p5.e34":{"call":"portfolio_equity_exposure","field":"$.indicesData[0].data[?(@.calc_name in [\'stock_sector_cyclical\', \'stock_sector_basic_materials\', \'stock_sector_consumer_cyclical\', \'stock_sector_financial_services\', \'stock_sector_real_estate\', \'stock_sector_sensitive\', \'stock_sector_comm_services\', \'stock_sector_energy\', \'stock_sector_industrials\', \'stock_sector_technology\', \'stock_sector_defensive\', \'stock_sector_consumer_defensive\', \'stock_sector_healthcare\', \'stock_sector_utilities\'])].calc_raw_value"},"p6.e01":"BUILDER_ONLY","p6.e19":"BUILDER_ONLY","p6.e20":{"call":"portfolio_info","field":"$..name"},"p6.e21":{"call":"portfolio_level_series","field":"$.chart_data[0][0].raw_data"},"p6.e23":"BUILDER_ONLY","p7.e01":"BUILDER_ONLY","p7.e09":"BUILDER_ONLY","p7.e14":"BUILDER_ONLY","p8.e01":"BUILDER_ONLY","p8.e22":"BUILDER_ONLY","p9.e01":"BUILDER_ONLY","p9.e02":"BUILDER_ONLY","p9.e03":"BUILDER_ONLY","p9.e05":"BUILDER_ONLY","p9.e06":"BUILDER_ONLY","p9.e07":"BUILDER_ONLY","p9.e17":"BUILDER_ONLY"}')
doc = json.loads((MAPS / "overview_map.json").read_text(encoding="utf-8"))
now = {e["id"]: e.get("source") for e in doc["elements"]}
moved = [i for i, s in BASE.items() if now.get(i) != s]
builder = [i for i in ("p8.e08", "p8.e13") if isinstance(now.get(i), dict) and now[i].get("computed")]  # the 2 BUILDER_ONLY gain no computation
ok = len(now) >= 253 and not moved and not builder
verdict(ok, "elements=%d; elements outside the coverage table keep their sources: %d of %d (moved %s); BUILDER_ONLY kept: %s" % (
    len(now), len(BASE) - len(moved), len(BASE), moved[:6], not builder))
