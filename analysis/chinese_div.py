#!/usr/bin/env python3
"""The three Chinese divination charts (三式 and 梅花) at the 19:00 Malaysia draw time, as parameter families.

Da Liu Ren (大六壬, family "dlr"), from the kinliuren package (九宗门 rules, night Noble at the 戌 hour):
    dlr_month_general   月将 (by the solar term pair: 雨水/驚蟄 -> 亥 ... 大寒/立春 -> 子)
    dlr_gan_upper       干上神, upper branch of the first lesson
    dlr_zhi_upper       支上神, upper branch of the third lesson
    dlr_initial / dlr_middle / dlr_final   三传
    dlr_method          the rule that produced the transmissions (賊尅, 比用, 涉害, 遙尅, 昴星, 別責, 八專, 伏吟, 返吟)
    dlr_subpattern      its named case (元首, 重審, 知一, ...)
    dlr_initial_general heavenly general on the initial transmission
    dlr_initial_kin     the initial transmission's relation to the day stem (父母, 兄弟, 子孫, 妻財, 官鬼)
    dlr_noble_earth     the earth branch under the Noble (貴人)
    dlr_initial_void    the initial transmission falls in the day's void (旬空)
Mei Hua Yi Shu (梅花易数, family "mh"), time method on the same sum as plum_trigrams (year branch + lunar month +
lunar day; + hour 戌 = 11 for the lower trigram and the moving line); plum_trigrams itself is the main hexagram:
    mh_moving_line      动爻 1-6
    mh_changed          变卦 (upper-lower, Xiantian numbers 1 乾 ... 8 坤)
    mh_mutual           互卦 (lines 3-5 over lines 2-4)
    mh_ti / mh_yong     体卦 (the trigram without the moving line) and 用卦
    mh_tiyong           用 to 体: 生体, 体生用 (泄), 克体, 体克用, 比和
    mh_ti_season        体's element in the month: 旺, 相, 休, 囚, 死
    mh_changed_vs_ti    the changed 用 trigram to 体, as mh_tiyong
Tai Yi Shen Shu (太乙神数, family "ty"), daily chart (日計) of the 太乙統宗 school from the kintaiyi package:
    ty_ju               局 number (阳遁 / 阴遁 1-72)
    ty_palace           太乙落宮
    ty_tianyi / ty_diyi 天乙, 地乙
    ty_wenchang         文昌 (主目) position
    ty_shiji            始擊 (客目) position
    ty_jishen           計神
    ty_host_calc / ty_guest_calc / ty_set_calc   主算, 客算, 定算
    ty_host_general / ty_guest_general           主大將, 客大將 palaces
    ty_door             八門值事
    ty_five_generals    推五將發不發 (whether the five generals go out, or which are blocked)
    ty_host_guest       推主客相關法 (host-guest relation)
All values for every date of data/astro_params.csv go to data/astro_params_chinese_div.csv. enable() appends them
after the divisional-chart parameters (vargas.enable() first), so earlier indices stay.

python3 analysis/chinese_div.py   (builds the CSV, checks a few hand-worked charts)
"""

import csv
import datetime as dt
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import almanac  # noqa: E402
import common  # noqa: E402
import ephemeris as eph  # noqa: E402
import extra_astro as xa  # noqa: E402
import vargas  # noqa: E402

CSV = os.path.join(common.DATA, "astro_params_chinese_div.csv")
FAMILIES = {
    "dlr": ["dlr_month_general", "dlr_gan_upper", "dlr_zhi_upper", "dlr_initial", "dlr_middle", "dlr_final",
            "dlr_method", "dlr_subpattern", "dlr_initial_general", "dlr_initial_kin", "dlr_noble_earth",
            "dlr_initial_void"],
    "mh": ["mh_moving_line", "mh_changed", "mh_mutual", "mh_ti", "mh_yong", "mh_tiyong", "mh_ti_season",
           "mh_changed_vs_ti"],
    "ty": ["ty_ju", "ty_palace", "ty_tianyi", "ty_diyi", "ty_wenchang", "ty_shiji", "ty_jishen", "ty_host_calc",
           "ty_guest_calc", "ty_set_calc", "ty_host_general", "ty_guest_general", "ty_door", "ty_five_generals",
           "ty_host_guest"],
}
NEW = [p for f in FAMILIES.values() for p in f]
GAN, ZHI = "甲乙丙丁戊己庚辛壬癸", "子丑寅卯辰巳午未申酉戌亥"
TERMS = dict(zip(almanac.SOLAR_TERMS, ["春分", "清明", "穀雨", "立夏", "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", "處暑",
                                       "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒", "立春",
                                       "雨水", "驚蟄"]))
CMONTH = list("正二三四五六七八九十") + ["十一", "十二"]

# Mei Hua: Xiantian trigram numbers, lines bottom to top (1 = yang), elements
TRIGRAM = {1: "乾", 2: "兌", 3: "離", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}
LINES = {1: (1, 1, 1), 2: (1, 1, 0), 3: (1, 0, 1), 4: (1, 0, 0), 5: (0, 1, 1), 6: (0, 1, 0), 7: (0, 0, 1), 8: (0, 0, 0)}
FROM_LINES = {v: k for k, v in LINES.items()}
ELEMENT = {1: "金", 2: "金", 3: "火", 4: "木", 5: "木", 6: "水", 7: "土", 8: "土"}
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
SEASON_OF_BRANCH = dict(zip(ZHI, "冬季春春季夏夏季秋秋季冬"))            # 子 winter, 丑 季 (earth month), 寅 spring ...
SEASON_STATE = {"春": dict(木="旺", 火="相", 水="休", 金="囚", 土="死"), "夏": dict(火="旺", 土="相", 木="休", 水="囚", 金="死"),
                "秋": dict(金="旺", 水="相", 土="休", 火="囚", 木="死"), "冬": dict(水="旺", 木="相", 金="休", 土="囚", 火="死"),
                "季": dict(土="旺", 金="相", 火="休", 木="囚", 水="死")}


def relation(yong, ti):
    """Element relation of 用 to 体."""
    if yong == ti:
        return "比和"
    if GENERATES[yong] == ti:
        return "生体"
    if GENERATES[ti] == yong:
        return "体生用"
    if CONTROLS[yong] == ti:
        return "克体"
    return "体克用"


def meihua(s, month_branch):
    """s = year branch number + lunar month + lunar day (the plum_trigrams sum)."""
    up, lo, mv = s % 8 or 8, (s + 11) % 8 or 8, (s + 11) % 6 or 6
    lines = list(LINES[lo] + LINES[up])                                # lines 1-6, bottom to top
    changed = lines.copy()
    changed[mv - 1] ^= 1
    c_lo, c_up = FROM_LINES[tuple(changed[:3])], FROM_LINES[tuple(changed[3:])]
    m_lo, m_up = FROM_LINES[tuple(lines[1:4])], FROM_LINES[tuple(lines[2:5])]
    ti, yong = (up, lo) if mv <= 3 else (lo, up)
    c_yong = c_lo if mv <= 3 else c_up
    return {"mh_moving_line": mv, "mh_changed": f"{c_up}-{c_lo}", "mh_mutual": f"{m_up}-{m_lo}",
            "mh_ti": TRIGRAM[ti], "mh_yong": TRIGRAM[yong], "mh_tiyong": relation(ELEMENT[yong], ELEMENT[ti]),
            "mh_ti_season": SEASON_STATE[SEASON_OF_BRANCH[month_branch]][ELEMENT[ti]],
            "mh_changed_vs_ti": relation(ELEMENT[c_yong], ELEMENT[ti])}


def liuren(term, lunar_month, day_gz, hour_gz):
    from kinliuren import kinliuren as K
    r = K.Liuren(term, CMONTH[lunar_month - 1], day_gz, hour_gz).result(0)
    tp = r["三傳"]
    sky = r["地轉天盤"]                                               # earth branch -> heavenly branch above it
    noble = [e for e, g in r["地轉天將"].items() if g in ("貴", "貴人")]
    lessons = r["四課"]
    return {"dlr_month_general": sky[hour_gz[1]], "dlr_gan_upper": lessons["一課"][0][0],
            "dlr_zhi_upper": lessons["三課"][0][0], "dlr_initial": tp["初傳"][0], "dlr_middle": tp["中傳"][0],
            "dlr_final": tp["末傳"][0], "dlr_method": r["格局"][0].rstrip("1"), "dlr_subpattern": r["格局"][1],
            "dlr_initial_general": tp["初傳"][1], "dlr_initial_kin": tp["初傳"][2],
            "dlr_noble_earth": noble[0] if noble else "?", "dlr_initial_void": tp["初傳"][3] == "空"}


def taiyi(day):
    import kintaiyi
    sys.path.insert(0, os.path.dirname(kintaiyi.__file__))           # the package imports its modules flat
    from kintaiyi import kintaiyi as K
    K.config.starhouse = lambda *a: ""                                  # 28-mansion lookup, unused, fails on some dates
    p = K.Taiyi(day.year, day.month, day.day, 19, 0).pan(2, 0)         # 日計, 太乙統宗
    v = lambda x: x[0] if isinstance(x, list) else x                    # noqa: E731
    return {"ty_ju": p["局式"]["文"], "ty_palace": int(p["太乙落宮"]), "ty_tianyi": p["天乙"], "ty_diyi": p["地乙"],
            "ty_wenchang": v(p["文昌"]), "ty_shiji": p["始擊"], "ty_jishen": p["計神"], "ty_host_calc": int(v(p["主算"])),
            "ty_guest_calc": int(v(p["客算"])), "ty_set_calc": int(v(p["定算"])), "ty_host_general": int(p["主將"]),
            "ty_guest_general": int(p["客將"]), "ty_door": p["八門值事"], "ty_five_generals": p["推五將發不發"],
            "ty_host_guest": p["推主客相闗法"]}


def chart_inputs(day):
    jd = eph.julian_day(dt.datetime.combine(day, dt.time(11)))       # 19:00 MYT
    ch = almanac.chinese(day, eph.sun_longitude(jd))
    lm, ld, _ = eph.lunar_date(day)
    day_gz = GAN[almanac.STEMS.index(ch["day_stem"])] + ZHI[almanac.BRANCHES.index(ch["day_branch"])]
    hour_gz = GAN[almanac.STEMS.index(ch["hour_stem_19h"])] + "戌"
    yb = almanac.BRANCHES.index(ch["year_pillar"].split()[1]) + 1
    return TERMS[ch["solar_term"]], lm, ld, day_gz, hour_gz, yb, ZHI[almanac.BRANCHES.index(ch["month_branch"])]


def factors(date):
    day = dt.date.fromisoformat(date)
    term, lm, ld, day_gz, hour_gz, yb, mb = chart_inputs(day)
    out = {**liuren(term, lm, day_gz, hour_gz), **meihua(yb + lm + ld, mb), **taiyi(day)}
    return {k: str(x) for k, x in out.items()}


def build():
    dates = sorted(common.load_params())
    with open(CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date"] + NEW)
        for i, d in enumerate(dates):
            f = factors(d)
            w.writerow([d] + [f[p] for p in NEW])
            if i % 500 == 0:
                print(d, flush=True)
    print(f"wrote {CSV}: {len(dates)} dates x {len(NEW)} parameters")


_T = {}


def table():
    if not _T:
        if not os.path.exists(CSV):
            build()
        with open(CSV) as fh:
            _T.update({r.pop("date"): r for r in csv.DictReader(fh)})
    return _T


def family(name):
    return FAMILIES[name]


_orig = {}


def enable():
    """Append every Chinese divination parameter after the divisional charts (idempotent)."""
    if _orig:
        return
    vargas.enable()
    _orig.update(params=xa.extra_params, codes=xa.codes_all)

    def extra_params():
        return _orig["params"]() + NEW

    def codes_all(dates):
        xa.extra_params = _orig["params"]
        try:
            base = _orig["codes"](dates)
        finally:
            xa.extra_params = extra_params
        T = table()
        cols = []
        for p in NEW:
            vals = sorted({r[p] for r in T.values()})
            ix = {v: i for i, v in enumerate(vals)}
            cols.append([ix[T[d][p]] for d in dates])
        return np.hstack([base, np.array(cols).T])
    xa.extra_params, xa.codes_all = extra_params, codes_all


def self_check():
    """Hand-worked examples: Mei Hua from the rules; Da Liu Ren against the kinliuren README example."""
    bad = []
    # s = 1: upper 1 乾, lower (1+11)%8 = 4 震, moving (12)%6 -> 6: top line flips, 乾 -> 兌; 体 = lower 震 (木),
    # 用 = upper 乾 (金): 金 controls 木 -> 克体; changed 用 兌 (金) -> 克体; mutual lines 2-4 of 震乾 (100 111) = 0,0,1 -> 艮,
    # lines 3-5 = 0,1,1 -> 巽 -> 5-7
    m = meihua(1, "寅")
    want = {"mh_moving_line": 6, "mh_changed": "2-4", "mh_mutual": "5-7", "mh_ti": "震", "mh_yong": "乾",
            "mh_tiyong": "克体", "mh_ti_season": "旺", "mh_changed_vs_ti": "克体"}
    bad += [(k, m[k], v) for k, v in want.items() if m[k] != v]
    r = liuren("冬至", 11, "丁未", "乙巳")
    want = {"dlr_initial": "卯", "dlr_middle": "亥", "dlr_final": "未", "dlr_method": "賊尅", "dlr_subpattern": "元首"}
    bad += [(k, r[k], v) for k, v in want.items() if r[k] != v]
    print("self-check failures:", bad or "none")


if __name__ == "__main__":
    self_check()
    build()
    T = table()
    for p in NEW:
        print(p, len({r[p] for r in T.values()}), "values")
