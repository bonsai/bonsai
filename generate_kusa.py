#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直近3ヶ月のコントリビューション草を「下から生える」アニメーション SVG に生成する"""
import json

KUSA = "kusa_3mo.json"
OUT = "kusa.svg"

data = json.load(open(KUSA))
weeks = data["weeks"]
total = data["totalContributions"]

# セルサイズ
CELL = 11          # マス
GAP = 3            # ギャップ
PITCH = CELL + GAP # 14
PAD_L = 16         # 左パディング（月ラベル用は上部）
PAD_T = 22         # 上（タイトル/合計）
PAD_B = 18         # 下（週ラベル）

W = PAD_L + len(weeks) * PITCH + 8
H = PAD_T + 7 * PITCH + PAD_B

# 草の色 (GitHub 風 4 段階)
COLORS = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
# ダークでも見えるよう 0 段階は薄いグレー

def level(count):
    if count <= 0: return 0
    if count < 3: return 1
    if count < 6: return 2
    if count < 10: return 3
    return 4

# 週ラベル（各週の先頭日付）
def week_label(week):
    first = week["contributionDays"][0]["date"]  # yyyy-mm-dd
    return f"{int(first[5:7])}/{int(first[8:10])}"

rects = []
for wi, week in enumerate(weeks):
    for di, day in enumerate(week["contributionDays"]):
        x = PAD_L + wi * PITCH
        y = PAD_T + di * PITCH
        c = level(day["contributionCount"])
        delay = wi * 0.32 + di * 0.05  # 週ごと・曜日ごとに順に生える
        rects.append(
            f'<rect class="k" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
            f'fill="{COLORS[c]}" style="animation-delay:{delay:.2f}s">'
            f'<title>{day["date"]}: {day["contributionCount"]} contributions</title></rect>'
        )

# 週ラベル
labels = "".join(
    f'<text x="{PAD_L + wi * PITCH + CELL / 2}" y="{H - 6}" class="lbl" text-anchor="middle">{week_label(weeks[wi])}</text>'
    for wi in range(len(weeks)) if wi % 2 == 0
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Last 90 days: {total} contributions">
<style>
  .k {{ transform-origin: center bottom; opacity: 0; animation: sprout .6s cubic-bezier(.34,1.56,.64,1) both; }}
  @keyframes sprout {{
    0%   {{ opacity: 0; transform: scaleY(0); }}
    60%  {{ opacity: 1; }}
    100% {{ opacity: 1; transform: scaleY(1); }}
  }}
  .lbl {{ font: 9px sans-serif; fill: #8b949e; }}
  .ttl {{ font: 11px sans-serif; font-weight: 700; fill: #c9d1d9; }}
  .sub {{ font: 9px sans-serif; fill: #8b949e; }}
</style>
<text x="{PAD_L}" y="14" class="ttl">🌱 Last 90 days — {total} contributions</text>
<text x="{PAD_L + len(weeks) * PITCH + 6}" y="14" class="sub" text-anchor="end">{(weeks[0]['contributionDays'][0]['date'])[:10]} → {(weeks[-1]['contributionDays'][-1]['date'])[:10]}</text>
{''.join(rects)}
{labels}
</svg>'''

open(OUT, "w", encoding="utf-8").write(svg)
print(f"OK: {OUT} ({len(svg):,} bytes) · {len(weeks)} weeks · {sum(len(w['contributionDays']) for w in weeks)} days")
