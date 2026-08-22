#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub @bonsai のメディアアート求人向けポートフォリオ生成（フィジカル寄り focus）"""
import json, collections, datetime, html

DATA = "bonsai_repos.jsonl"
KUSA = "kusa_3mo.json"
OUT = "portfolio.html"
OUT_MD = "README.md"

repos = [json.loads(l) for l in open(DATA) if l.strip()]
orig = [r for r in repos if not r["fork"]]

# ============ フィジカル作品データ（メディアアート向け・3ジャンル曼荼羅） ============
# README 用の静的リスト。HTML の曼荼羅は jsonl から動的抽出する。
WORKS = {
    "Body": [
        ("uiap-ecg-monitor", "自作心電図計 — アナログフロントエンド + RISC-V で生体信号を可視化。計装アンプ(AD620)・Pan-Tompkins R波検出・TinyML 異常分類。", "C / CH32V203 / TinyML"),
        ("uiap-voiceprint-auth", "声紋認証 — エッジ端末(CH32V003)上で MFCC による話者識別。サーボモーターで物理ロックを制御。", "C / DSP / MFCC"),
        ("uiap-sensor-hid", "USB HID センサー — RESET ボタンを HID デバイスとして MQTT ブリッジに接続する IoT インターフェース。", "C / USB HID / MQTT"),
        ("microbit-smartlock", "micro:bit スマートロック — 古いスマホ + povo 2.0 で月額ほぼ0円の DIY スマートロック。", "Python / micro:bit"),
    ],
    "Light": [
        ("led-board", "電光掲示板 (LED Board) — 光の文字盤。Web から駆動する LED ボード。", "TypeScript / HTML"),
        ("denkou-keijiban", "LED Board — 電光掲示板の Web 版。", "HTML"),
        ("uiapduino-4led", "290円 RISC-V マイコン(CH32V003)で 4 LED を駆動 — 最小コストの光の制御実験。", "C / Arduino"),
        ("led-poc", "LED 表現の PoC 群（GDScript による光のシミュレーション）。", "GDScript"),
        ("wifi-visualizer", "WiFi 可視化 — 空間の電波を光として捉える。", "HTML"),
    ],
    "Sound": [
        ("4bit-music-riscv", "4-bit music on RISC-V — チップ上のレジスタで 4bit 音楽を鳴らす。", "RISC-V / HTML"),
        ("audio-patch-simulator-next", "モジュラーシンセ風パッチシミュレータ — Web Audio でケーブルを繋ぐ音の実験。", "JavaScript / Web Audio"),
        ("sound-gen", "AudioGen + MusicGen による lo-fi hiphop 生成パイプライン。", "Python / Jupyter"),
        ("8bit-Jazz", "8bit ジャズ — 制約の上に音楽を載せる試み。", "HTML"),
        ("midi-to-score", "MIDI → 楽譜変換 — 音楽情報処理の実験。", "OCaml"),
    ],
}

# jsonl と同期した動的ジャンル抽出（曼荼羅用）
GENRE_KEYWORDS = {
    "Body":  ["ecg", "voiceprint", "sensor", "microbit", "smartlock", "hid", "health", "biosign"],
    "Light": ["led", "board", "keijiban", "light", "visualiz", "visual"],
    "Sound": ["music", "audio", "sound", "midi", "8bit", "4bit", "jazz", "synth", "patch", "fm", "score"],
}

def build_genre_pool(orig_repos):
    """jsonl のリポジトリからジャンル別プールを作る（1リポジトリ=1ジャンル、優先順 Body→Light→Sound）"""
    pool = {g: [] for g in GENRE_KEYWORDS}
    assigned = set()
    for r in sorted(orig_repos, key=lambda x: x.get("pushed_at") or "", reverse=True):
        if r["name"] in assigned:
            continue
        text = (r["name"] + " " + (r["description"] or "")).lower()
        for g, kws in GENRE_KEYWORDS.items():
            if any(k in text for k in kws):
                pool[g].append({
                    "name": html.escape(r["name"]),
                    "desc": html.escape((r["description"] or "")[:80]),
                    "lang": r["language"] or "",
                    "url": f"https://github.com/bonsai/{r['name']}",
                    "pushed": (r.get("pushed_at") or "")[:10],
                })
                assigned.add(r["name"])
                break
    return pool

GENRE_POOL = build_genre_pool(orig)

# 直近3ヶ月の草
kusa = json.load(open(KUSA))
kusa_total = kusa["totalContributions"]
kusa_days = sum(len(w["contributionDays"]) for w in kusa["weeks"])
kusa_active = sum(1 for w in kusa["weeks"] for d in w["contributionDays"] if d["contributionCount"] > 0)

# ============ 統計 ============
total = len(repos)
n_orig, n_fork = len(orig), len(repos) - len(orig)
langs = collections.Counter(r["language"] for r in orig if r["language"])
lang_top = langs.most_common(8)
lang_total = sum(langs.values())
lang_max = lang_top[0][1] if lang_top else 1

# 絵文字バー (10マス)
BLOCKS = ["░", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
def bar(v, mx, width=18):
    if mx <= 0: return "░" * width
    filled = v / mx * width
    full = int(filled)
    rest = filled - full
    s = "█" * full
    if rest > 0 and full < width:
        s += BLOCKS[min(int(round(rest * 8)), 8)]
    return s + "░" * max(width - len(s), 0)

md_lang = "\n".join(
    f"| {lang} | {v} | {v / lang_total * 100:.0f}% | `{bar(v, lang_max)}` |"
    for lang, v in lang_top)

# kusa SVG を読み込み、インライン用に class を付与
KUSA_SVG = open("kusa.svg", encoding="utf-8").read()
INLINE_KUSA = KUSA_SVG.replace('<svg class="kusa-svg"', '<svg class="kusa-svg inpage"', 1)

# ============ README (メディアアート求人向け) ============
def works_md():
    out = []
    for cat, items in WORKS.items():
        out.append(f"### {cat}")
        out.append("")
        for name, desc, tech in items:
            out.append(f"- **[{name}](https://github.com/bonsai/{name})** — {desc} `{tech}`")
        out.append("")
    return "\n".join(out)

readme = f'''# 🎛️ bonsai — Media Artist / Creative Technologist

> **身体の信号と回路と音を、境界なく繋ぐメディアアーティスト**
>
> Saitama, Japan · good vibes only · [ko-fi](https://ko-fi.com/v0n5ai)

![GitHub followers](https://img.shields.io/github/followers/bonsai?style=flat-square&label=Followers&color=58a6ff)
![Repos](https://img.shields.io/badge/Repos-{total}-58a6ff?style=flat-square)

---

## 🧬 Artist Statement

RISC-V マイコン (WCH CH32V シリーズ) を中心にした**自作ハードウェア**で、心電図・声紋・LED・音を扱う作品を制作しています。
微弱な生体信号を回路で増幅し、エッジ上の TinyML で意味を与え、光と音として身体に返す——**センシングから表現までを一貫して自作**することが私の制作スタイルです。

## 🫀 Selected Works — Physical & Interactive

{works_md()}

## 🛠️ Tech Stack

| 領域 | 技術 |
|---|---|
| ハードウェア | RISC-V マイコン (CH32V003/203/307) · Arduino · micro:bit · USB HID · MQTT · BLE |
| 信号処理 | MFCC / DSP / Pan-Tompkins · TinyML (BitNetMCU) · 固定小数点数演算 |
| メディア | Web Audio API · GLSL · リアルタイムレンダリング |
| 言語 | C · Python · TypeScript · JavaScript · GDScript · Elm · OCaml |

## 🌱 直近 3 ヶ月の活動

<img src="kusa.svg" alt="Last 90 days contribution graph" width="100%">

| 指標 | 値 |
|---|---:|
| コントリビューション | **{kusa_total}** |
| アクティブ日 | **{kusa_active} / {kusa_days} 日** |
| 公開リポジトリ | **{total}**（オリジナル {n_orig}） |

## 🛠️ 使用言語（オリジナル {n_orig} リポジトリ）

| 言語 | 数 | 割合 | 分布 |
|---|---:|---:|---|
{md_lang}

---

*このプロフィールは GitHub API の統計から自動生成されています。*
'''

# ============ HTML (ポートフォリオページ) ============
def esc(s): return html.escape(s or "")

# ===== 曼荼羅（3ジャンル×3作品、毎回ランダム配置）=====
GENRE_JSON = json.dumps(GENRE_POOL, ensure_ascii=False)
works_html = f'''<section id="mandala-sec">
  <h2>🕉️ Works Mandala <button class="shuffle" onclick="reshuffle()" title="入れ替える">🔄</button></h2>
  <p class="mandala-note">3 ジャンル × 3 作品 = 9 マス · 開くたびに入れ替わる · <span class="pool-count">{sum(len(v) for v in GENRE_POOL.values())} repos in pool (jsonl 同期)</span></p>
  <div class="mandala" id="mandala"></div>
</section>'''

lang_bars = "\n".join(
    f'''<div class="bar-row"><div class="bar-label">{esc(lang)}</div>
    <div class="bar-track"><div class="bar-fill" style="width:{round(v / lang_max * 100, 1)}%"></div></div>
    <div class="bar-val">{v}</div></div>'''
    for lang, v in lang_top)

h = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>bonsai — Media Artist Portfolio</title>
<style>
/* デザイン3要素: ① 緑の単色アクセント ② ダーク3階調(背景/パネル/線) ③ 円(曼荼羅・角丸) */
:root {{
  /* ② ダーク 3 階調 */
  --bg: #0d1117; --panel: #161b22; --border: #30363d;
  /* テキスト + ① 緑の単色アクセント */
  --text: #e6edf3; --muted: #8b949e; --accent: #3fb950;
  /* ③ 円: 角丸 3 段階 */
  --r-lg: 20px; --r-md: 14px; --r-sm: 8px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: var(--bg); color: var(--text); font-family: "Hiragino Kaku Gothic ProN", "Noto Sans JP", sans-serif; line-height: 1.7; }}
.wrap {{ max-width: 980px; margin: 0 auto; padding: 32px 20px 80px; }}

header {{ padding: 40px 24px; background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%); border: 1px solid var(--border); border-radius: var(--r-lg); margin-bottom: 28px; text-align: center; }}
header img {{ width: 100px; height: 100px; border-radius: 50%; border: 3px solid var(--accent); margin-bottom: 14px; }}
header h1 {{ font-size: 30px; }}
header .role {{ color: var(--accent); font-weight: 700; letter-spacing: 1px; margin: 6px 0 10px; }}
header .statement {{ color: var(--muted); max-width: 640px; margin: 0 auto 14px; font-size: 14px; }}
header .links a {{ color: var(--accent); text-decoration: none; margin: 0 10px; font-size: 14px; }}
header .links a:hover {{ text-decoration: underline; }}

.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 14px; margin-bottom: 36px; }}
.tile {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 18px; text-align: center; }}
.tile .num {{ font-size: 28px; font-weight: 700; color: var(--accent); }}
.tile .lbl {{ color: var(--muted); font-size: 12px; margin-top: 4px; }}

section {{ margin-bottom: 36px; }}
h2 {{ font-size: 19px; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 2px solid var(--border); }}

.cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 14px; }}
.card {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 16px; transition: border-color .15s, transform .15s; }}
.card:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
.card-title {{ color: var(--accent); font-weight: 700; font-size: 15px; text-decoration: none; }}
.card-title:hover {{ text-decoration: underline; }}
.card-desc {{ color: var(--muted); font-size: 13px; margin: 8px 0 10px; }}
.card-meta {{ font-size: 12px; }}
.tech {{ color: var(--accent); font-family: ui-monospace, monospace; font-size: 11px; }}

.kusa-box {{ background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 20px; margin-bottom: 14px; }}
.kusa-box img, .kusa-box svg {{ width: 100%; max-width: 480px; display: block; margin: 0 auto; }}

.bar-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 7px; font-size: 13px; }}
.bar-label {{ width: 130px; text-align: right; color: var(--muted); white-space: nowrap; }}
.bar-track {{ flex: 1; height: 18px; background: #21262d; border-radius: 9px; overflow: hidden; }}
.bar-fill {{ height: 100%; border-radius: 9px; min-width: 2px; background: var(--accent); }}
.bar-val {{ width: 44px; font-weight: 600; }}

.stack {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; }}
.stack .card h3 {{ font-size: 14px; color: var(--accent); margin-bottom: 8px; }}
.stack .card ul {{ list-style: none; font-size: 13px; color: var(--muted); }}
.stack .card li {{ margin-bottom: 4px; }}

footer {{ text-align: center; color: var(--muted); font-size: 12px; margin-top: 40px; }}

/* ===== 曼荼羅 ===== */
.shuffle {{ background: transparent; border: 1px solid var(--border); color: var(--accent); font-size: 15px; border-radius: var(--r-sm); padding: 2px 10px; cursor: pointer; margin-left: 10px; vertical-align: 2px; }}
.shuffle:hover {{ border-color: var(--accent); }}
.mandala-note {{ color: var(--muted); font-size: 12px; margin: -8px 0 14px; }}
.pool-count {{ color: var(--accent); }}
.mandala {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 760px; margin: 0 auto; position: relative; }}
.mandala::before {{ content: ""; position: absolute; inset: -14px; border: 1px dashed #30363d66; border-radius: 50%; pointer-events: none; }}
.m-cell {{ display: flex; flex-direction: column; gap: 6px; background: var(--panel); border: 1px solid var(--border); border-radius: var(--r-md); padding: 14px; text-decoration: none; color: var(--text); transition: border-color .15s, transform .15s; animation: mpop .5s cubic-bezier(.34,1.56,.64,1) both; }}
.m-cell:hover {{ border-color: var(--accent); transform: translateY(-3px); }}
.m-cell:nth-child(5) {{ border-color: var(--accent); background: linear-gradient(160deg, #1a2b20, #161b22); }}
@keyframes mpop {{ from {{ opacity: 0; transform: scale(.85); }} to {{ opacity: 1; transform: scale(1); }} }}
.m-genre {{ font-size: 10px; letter-spacing: 1px; color: var(--accent); font-weight: 700; }}
.m-name {{ font-size: 14px; font-weight: 700; color: var(--text); word-break: break-all; }}
.m-desc {{ font-size: 11.5px; color: var(--muted); flex: 1; }}
.m-meta {{ font-size: 10.5px; color: var(--muted); display: flex; justify-content: space-between; }}
.m-lang {{ color: var(--accent); font-family: ui-monospace, monospace; }}

/* ===== スマホ最適化 ===== */
@media (max-width: 900px) {{
  .mandala {{ grid-template-columns: repeat(2, 1fr); max-width: 560px; }}
  .stack {{ grid-template-columns: 1fr; }}
}}
@media (max-width: 640px) {{
  .wrap {{ padding: 16px 12px 60px; }}
  header {{ padding: 28px 16px; border-radius: 16px; margin-bottom: 20px; }}
  header img {{ width: 68px; height: 68px; border-width: 2px; margin-bottom: 10px; }}
  header h1 {{ font-size: 24px; }}
  header .statement {{ font-size: 13px; }}
  header .links a {{ font-size: 13px; margin: 0 7px; }}
  .stats {{ grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 24px; }}
  .tile {{ padding: 14px 8px; border-radius: 10px; }}
  .tile .num {{ font-size: 22px; }}
  section {{ margin-bottom: 28px; }}
  h2 {{ font-size: 17px; }}
  .mandala {{ grid-template-columns: 1fr; max-width: 100%; gap: 8px; }}
  .mandala::before {{ inset: -8px; }}
  .m-cell {{ padding: 12px 14px; border-radius: 12px; }}
  .kusa-box {{ padding: 14px 10px; border-radius: 12px; }}
  .bar-label {{ width: 96px; font-size: 12px; }}
  .bar-row {{ font-size: 12px; }}
  footer {{ font-size: 11px; }}
}}
</style>
</head>
<body>
<div class="wrap">

<header>
  <img src="https://avatars.githubusercontent.com/u/24775?v=4" alt="bonsai">
  <h1>bonsai <span style="font-size:15px;color:var(--muted);font-weight:400">/ v0n5ai</span></h1>
  <div class="role">MEDIA ARTIST / CREATIVE TECHNOLOGIST</div>
  <p class="statement">身体の信号と回路と音を、境界なく繋ぐメディアアーティスト。RISC-V マイコンを中心にした自作ハードウェアで、心電図・声紋・LED・音を扱う作品を制作。センシングから表現までを一貫して自作する。</p>
  <div class="links">
    <a href="https://github.com/bonsai">GitHub</a>
    <a href="https://ko-fi.com/v0n5ai">ko-fi</a>
    <a href="https://github.com/bonsai?tab=repositories">Repositories</a>
  </div>
</header>

<section id="kusa-anim">
  <h2>🌱 直近 3 ヶ月の活動</h2>
  <div class="kusa-box">
    {INLINE_KUSA}
  </div>
</section>

<div class="stats">
  <div class="tile"><div class="num">{kusa_total}</div><div class="lbl">直近3ヶ月の貢献</div></div>
  <div class="tile"><div class="num">{kusa_active}/{kusa_days}</div><div class="lbl">アクティブ日</div></div>
  <div class="tile"><div class="num">{n_orig}</div><div class="lbl">オリジナル作品</div></div>
  <div class="tile"><div class="num">{total}</div><div class="lbl">公開リポジトリ</div></div>
</div>

{works_html}

<section>
  <h2>🛠️ 技術スタック</h2>
  <div class="stack">
    <div class="card"><h3>ハードウェア</h3><ul>
      <li>RISC-V マイコン (CH32V003/203/307)</li>
      <li>Arduino / micro:bit / USB HID</li>
      <li>MQTT / BLE / センサー回路</li>
    </ul></div>
    <div class="card"><h3>信号処理</h3><ul>
      <li>MFCC / DSP / Pan-Tompkins</li>
      <li>TinyML (BitNetMCU 1-bit)</li>
      <li>固定小数点数演算 (Q15)</li>
    </ul></div>
    <div class="card"><h3>メディア</h3><ul>
      <li>Web Audio API</li>
      <li>GLSL シェーダー</li>
      <li>AI 音声生成 (AudioGen/MusicGen)</li>
    </ul></div>
  </div>
</section>

<section>
  <h2>言語分布（オリジナル {n_orig} リポジトリ）</h2>
  {lang_bars}
</section>

<footer>Generated from GitHub API · 2026-08-22</footer>
</div>
<script>
// ===== 曼荼羅（3ジャンル×3作品を毎回ランダム配置）=====
var GENRE_POOL = {GENRE_JSON};
function shuffleArr(arr) {{
  var a = arr.slice();
  for (var i = a.length - 1; i > 0; i--) {{
    var j = Math.floor(Math.random() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }}
  return a;
}}
function pick(arr, n) {{ return shuffleArr(arr).slice(0, n); }}
function renderMandala() {{
  var grid = document.getElementById('mandala');
  if (!grid) return;
  var genres = shuffleArr(Object.keys(GENRE_POOL));
  var cells = [];
  genres.forEach(function(g) {{
    pick(GENRE_POOL[g], 3).forEach(function(r) {{ cells.push({{g: g, r: r}}); }});
  }});
  cells = shuffleArr(cells);
  grid.innerHTML = cells.map(function(c, i) {{
    return '<a class="m-cell" style="animation-delay:' + (i * 0.06) + 's" href="' + c.r.url + '" target="_blank">' +
      '<span class="m-genre">' + c.g + '</span>' +
      '<span class="m-name">' + c.r.name + '</span>' +
      '<span class="m-desc">' + (c.r.desc || '—') + '</span>' +
      '<span class="m-meta"><span class="m-lang">' + (c.r.lang || '—') + '</span><span>' + c.r.pushed + '</span></span>' +
      '</a>';
  }}).join('');
}}
function reshuffle() {{ renderMandala(); }}
renderMandala();
</script>
<script>
(function() {{
  var box = document.getElementById('kusa-anim');
  if (!box) return;
  var svg = box.querySelector('svg');
  if (!svg) return;
  var obs = new IntersectionObserver(function(entries) {{
    entries.forEach(function(e) {{
      if (e.isIntersecting) {{
        // 可視領域に入るたびに再生し直す（スクロール連動）
        svg.classList.remove('play');
        void svg.getBoundingClientRect();
        svg.classList.add('play');
      }} else {{
        svg.classList.remove('play');
      }}
    }});
  }}, {{ threshold: 0.2 }});
  obs.observe(box);
}})();
</script>
</body>
</html>'''

open(OUT_MD, "w", encoding="utf-8").write(readme)
open(OUT, "w", encoding="utf-8").write(h)
# GitHub Pages 用: ルート URL で開けるよう index.html にも出力
open("index.html", "w", encoding="utf-8").write(h)
print(f"OK: {OUT_MD} ({len(readme):,} bytes)")
print(f"OK: {OUT} ({len(h):,} bytes)")
print("OK: index.html (Pages 用コピー)")
