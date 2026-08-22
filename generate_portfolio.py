#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bonsai — 棲み分け構成
  README.md      = Stats（統計・データ）→ https://github.com/bonsai
  portfolio.html = Semantics（作品の意味・物語）→ https://bonsai.github.io/bonsai/
"""
import json, collections, html

DATA = "bonsai_repos.jsonl"
KUSA = "kusa_3mo.json"
OUT = "portfolio.html"
OUT_MD = "README.md"

repos = [json.loads(l) for l in open(DATA) if l.strip()]
orig = [r for r in repos if not r["fork"]]

# ============ 作品データ（セマンティクス用・3ジャンル） ============
# (name, コンセプト説明, 技術)
WORKS = {
    "Body": [
        ("uiap-ecg-monitor", "心臓の鼓動を回路が聴く。計装アンプで微弱な生体電位を増幅し、RISC-V で R 波を検出・TinyML で異常を分類する自作心電図計。", "C / CH32V203 / TinyML"),
        ("uiap-voiceprint-auth", "声は鍵になる。エッジ端末で MFCC により声紋を識別し、サーボモーターで物理ロックを開く。", "C / DSP / MFCC"),
        ("uiap-sensor-hid", "ボタンひとつを世界に繋ぐ。RESET ボタンを USB HID デバイスとして MQTT ブリッジ化する IoT インターフェース。", "C / USB HID / MQTT"),
        ("microbit-smartlock", "身体の接近で扉が開く。micro:bit と古いスマホで作る DIY スマートロック。", "Python / micro:bit"),
    ],
    "Light": [
        ("led-board", "言葉を光に変える電光掲示板。Web から駆動する LED ボード。", "TypeScript / HTML"),
        ("denkou-keijiban", "電光掲示板の Web 版。文字を光の粒として流す。", "HTML"),
        ("uiapduino-4led", "290円の回路に宿る光。CH32V003 RISC-V マイコンで 4 つの LED を駆動する最小の光の実験。", "C / Arduino"),
        ("led-poc", "光の表現の実験ノート。GDScript による LED シミュレーション。", "GDScript"),
        ("wifi-visualizer", "空間に漂う電波を光として見る WiFi 可視化。", "HTML"),
    ],
    "Sound": [
        ("4bit-music-riscv", "チップのレジスタが奏でる 4bit 音楽。RISC-V 上で音楽を鳴らす。", "RISC-V / HTML"),
        ("audio-patch-simulator-next", "ケーブルで繋ぐ音の宇宙。Web Audio でモジュラーシンセのパッチを再現する。", "JavaScript / Web Audio"),
        ("sound-gen", "AI が紡ぐ lo-fi hiphop。AudioGen + MusicGen による生成パイプライン。", "Python / Jupyter"),
        ("8bit-Jazz", "制約の上に乗るジャズ。8bit の世界で音楽を探る。", "HTML"),
        ("midi-to-score", "音を記号に、記号を音に。MIDI から楽譜へ変換する音楽情報処理。", "OCaml"),
    ],
}
WORK_DESC = {name: (desc, tech) for cat, items in WORKS.items() for name, desc, tech in items}

# jsonl と同期した動的ジャンル抽出（曼荼羅用）
GENRE_KEYWORDS = {
    "Body":  ["ecg", "voiceprint", "sensor", "microbit", "smartlock", "hid", "health", "biosign"],
    "Light": ["led", "board", "keijiban", "light", "visualiz", "visual"],
    "Sound": ["music", "audio", "sound", "midi", "8bit", "4bit", "jazz", "synth", "patch", "fm", "score"],
}

def build_genre_pool(orig_repos):
    """jsonl からジャンル別プールを作る。説明は WORKS のコンセプトを優先（jsonl 同期）。"""
    pool = {g: [] for g in GENRE_KEYWORDS}
    assigned = set()
    for r in sorted(orig_repos, key=lambda x: x.get("pushed_at") or "", reverse=True):
        if r["name"] in assigned:
            continue
        text = (r["name"] + " " + (r["description"] or "")).lower()
        for g, kws in GENRE_KEYWORDS.items():
            if any(k in text for k in kws):
                if r["name"] in WORK_DESC:
                    desc, tech = WORK_DESC[r["name"]]
                    lang = tech.split(" / ")[0]
                else:
                    desc, tech = (r["description"] or "")[:80], ""
                    lang = r["language"] or ""
                pool[g].append({
                    "name": html.escape(r["name"]),
                    "desc": html.escape(desc),
                    "lang": html.escape(lang),
                    "tech": html.escape(tech),
                    "url": f"https://github.com/bonsai/{r['name']}",
                    "pushed": (r.get("pushed_at") or "")[:10],
                })
                assigned.add(r["name"])
                break
    return pool

GENRE_POOL = build_genre_pool(orig)

# ============ 統計（README 用） ============
kusa = json.load(open(KUSA))
kusa_total = kusa["totalContributions"]
kusa_days = sum(len(w["contributionDays"]) for w in kusa["weeks"])
kusa_active = sum(1 for w in kusa["weeks"] for d in w["contributionDays"] if d["contributionCount"] > 0)

total = len(repos)
n_orig, n_fork = len(orig), len(repos) - len(orig)
langs = collections.Counter(r["language"] for r in orig if r["language"])
lang_top = langs.most_common(8)
lang_total = sum(langs.values())
lang_max = lang_top[0][1] if lang_top else 1

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

# ============================================================
# README.md — Stats（統計・データのプロフィール）
# ============================================================
readme = f'''# 🌱 bonsai — Stats Profile

> Media Artist · Saitama, Japan · good vibes only
>
> 📈 このページは **統計データ** のプロフィール。作品の意味・物語（セマンティクス）は
> **[🎨 Portfolio](https://bonsai.github.io/bonsai/)** へ。

![GitHub followers](https://img.shields.io/github/followers/bonsai?style=flat-square&label=Followers&color=3fb950)
![Repos](https://img.shields.io/badge/Repos-{total}-3fb950?style=flat-square)

## 📊 GitHub 統計

| 項目 | 数値 |
|---|---:|
| 公開リポジトリ | **{total}** |
| オリジナル | **{n_orig}** |
| フォーク | **{n_fork}** |
| GitHub 歴 | **18+ 年** (2008〜) |

## 🌱 直近 3 ヶ月の活動

<img src="kusa.svg" alt="Last 90 days contribution graph" width="100%">

| 指標 | 値 |
|---|---:|
| コントリビューション | **{kusa_total}** |
| アクティブ日 | **{kusa_active} / {kusa_days} 日** |
| プッシュ頻度 | ほぼ毎日 |

## 🛠️ 使用言語（オリジナル {n_orig} リポジトリ）

| 言語 | 数 | 割合 | 分布 |
|---|---:|---:|---|
{md_lang}

*Stats profile · 作品の物語は [Portfolio](https://bonsai.github.io/bonsai/) · [ko-fi](https://ko-fi.com/v0n5ai)*
'''

# ============================================================
# portfolio.html — Semantics（作品の意味・物語）
# ============================================================
def esc(s): return html.escape(s or "")

GENRE_JSON = json.dumps(GENRE_POOL, ensure_ascii=False)
pool_count = sum(len(v) for v in GENRE_POOL.values())

works_html = f'''<section id="mandala-sec">
  <h2>🕉️ Works Mandala <button class="shuffle" onclick="reshuffle()" title="入れ替える">🔄</button></h2>
  <p class="mandala-note">3 ジャンル × 3 作品 = 9 マス · 開くたびに入れ替わる · {pool_count} 作品から jsonl 同期で抽出</p>
  <div class="mandala" id="mandala"></div>
</section>'''

# 3テーマ（セマンティクス）
themes_html = f'''
<section id="statement">
  <h2>🧬 Artist Statement</h2>
  <p class="statement-body">
    私は <strong>身体・光・音</strong> という 3 つの領域で、センサーと回路とコードを跨いで作品を制作するメディアアーティストです。<br>
    RISC-V マイコン (CH32V シリーズ) を中心にした<strong>自作ハードウェア</strong>で、心電図という身体の内側の信号、声紋という個人の痕跡、
    290円の回路に宿る光、そしてチップ上の 4bit 音楽——<em>見えないものを可視化・可聴化</em>します。<br>
    センシングから表現までを<strong>一貫して自作</strong>することが私の制作スタイルです。
  </p>
  <div class="themes">
    <div class="theme-card">
      <div class="theme-icon">🫀</div>
      <h3>Body — 身体</h3>
      <p>微弱な生体信号を回路で増幅し、意味を与える。心電図・声紋・ボタンの触覚。</p>
    </div>
    <div class="theme-card">
      <div class="theme-icon">💡</div>
      <h3>Light — 光</h3>
      <p>290円の RISC-V マイコンから電光掲示板まで。光を最小のコストで制御する。</p>
    </div>
    <div class="theme-card">
      <div class="theme-icon">🔊</div>
      <h3>Sound — 音</h3>
      <p>チップ上のレジスタから Web Audio、AI 生成まで。制約の上に音楽を載せる。</p>
    </div>
  </div>
</section>'''

h = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>bonsai — Media Artist Portfolio</title>
<style>
/* デザイン原理（最小限・both で共通）:
   ① 緑 1 色のみアクセント（--accent）
   ② ダーク 2 階調（背景 / パネル）
   ③ 装飾なし・角丸 1 値（--r） */
:root {{
  --bg: #0d1117; --panel: #1e2530;      /* ② ダーク 2 階調 */
  --text: #e6edf3; --muted: #8b949e;    /* 文字（白 / 灰） */
  --accent: #3fb950; --panel-accent: #1a2b20;  /* ① テーマ body（緑） */
  --r: 14px;                            /* ③ 角丸 1 値 */
}}
/* テーマ切替: ② light（琥珀・光） / ③ sound（青・音） */
body[data-theme="light"] {{ --accent: #e8a33d; --panel-accent: #2b241a; }}
body[data-theme="sound"] {{ --accent: #58a6ff; --panel-accent: #1a2430; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: var(--bg); color: var(--text); font-family: "Hiragino Kaku Gothic ProN", "Noto Sans JP", sans-serif; line-height: 1.8; }}
.wrap {{ max-width: 980px; margin: 0 auto; padding: 32px 20px 80px; }}

header {{ padding: 44px 24px; background: var(--panel); border-radius: var(--r); margin-bottom: 28px; text-align: center; }}
header img {{ width: 100px; height: 100px; border-radius: 50%; margin-bottom: 14px; }}
header h1 {{ font-size: 30px; }}
header .role {{ color: var(--accent); font-weight: 700; letter-spacing: 2px; margin: 6px 0 10px; font-size: 13px; }}
header .statement {{ color: var(--muted); max-width: 620px; margin: 0 auto 16px; font-size: 14px; }}
header .links a {{ color: var(--accent); text-decoration: none; margin: 0 10px; font-size: 14px; }}
header .links a:hover {{ text-decoration: underline; }}

/* テーマ切替（3 ドット） */
.theme-switch {{ display: flex; gap: 8px; justify-content: center; margin-top: 14px; }}
.tdot {{ width: 18px; height: 18px; border-radius: 50%; border: 0; cursor: pointer; opacity: .4; transition: opacity .2s; }}
.tdot:hover, .tdot.active {{ opacity: 1; }}

section {{ margin-bottom: 40px; }}
h2 {{ font-size: 19px; margin-bottom: 16px; }}

/* Statement */
.statement-body {{ color: var(--text); font-size: 14.5px; max-width: 760px; margin: 0 auto 24px; }}
.statement-body em {{ color: var(--accent); font-style: normal; font-weight: 700; }}
.themes {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
.theme-card {{ background: var(--panel); border-radius: var(--r); padding: 20px 18px; text-align: center; }}
.theme-icon {{ font-size: 30px; margin-bottom: 8px; }}
.theme-card h3 {{ font-size: 14px; color: var(--accent); margin-bottom: 8px; letter-spacing: 1px; }}
.theme-card p {{ font-size: 12.5px; color: var(--muted); }}

/* 曼荼羅 */
.shuffle {{ background: var(--panel); color: var(--accent); font-size: 14px; border: 0; border-radius: var(--r); padding: 4px 14px; cursor: pointer; margin-left: 10px; }}
.shuffle:hover {{ color: var(--text); }}
.mandala-note {{ color: var(--muted); font-size: 12px; margin: -10px 0 16px; }}
.mandala {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 760px; margin: 0 auto; }}
.m-cell {{ display: flex; flex-direction: column; gap: 6px; background: var(--panel); border-radius: var(--r); padding: 14px; text-decoration: none; color: var(--text); }}
.m-cell:hover {{ color: var(--accent); }}
.m-cell:nth-child(5) {{ background: var(--panel-accent); }}
.m-genre {{ font-size: 10px; letter-spacing: 1px; color: var(--accent); font-weight: 700; }}
.m-name {{ font-size: 14px; font-weight: 700; word-break: break-all; }}
.m-desc {{ font-size: 11.5px; color: var(--muted); flex: 1; }}
.m-meta {{ font-size: 10.5px; color: var(--muted); display: flex; justify-content: space-between; }}
.m-lang {{ color: var(--accent); font-family: ui-monospace, monospace; }}

/* 制作の道具 */
.stack {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
.stack .card {{ background: var(--panel); border-radius: var(--r); padding: 18px; }}
.stack .card h3 {{ font-size: 14px; color: var(--accent); margin-bottom: 10px; }}
.stack .card ul {{ list-style: none; font-size: 13px; color: var(--muted); }}
.stack .card li {{ margin-bottom: 6px; }}

footer {{ text-align: center; color: var(--muted); font-size: 12px; margin-top: 44px; padding-top: 20px; }}
footer a {{ color: var(--accent); text-decoration: none; }}
footer a:hover {{ text-decoration: underline; }}

/* ===== スマホ最適化 ===== */
@media (max-width: 900px) {{
  .mandala {{ grid-template-columns: repeat(2, 1fr); max-width: 560px; }}
  .themes, .stack {{ grid-template-columns: 1fr; }}
}}
@media (max-width: 640px) {{
  .wrap {{ padding: 16px 12px 60px; }}
  header {{ padding: 28px 16px; margin-bottom: 20px; }}
  header img {{ width: 68px; height: 68px; margin-bottom: 10px; }}
  header h1 {{ font-size: 24px; }}
  header .statement {{ font-size: 13px; }}
  header .links a {{ font-size: 13px; margin: 0 7px; }}
  section {{ margin-bottom: 28px; }}
  h2 {{ font-size: 17px; }}
  .statement-body {{ font-size: 13.5px; }}
  .mandala {{ grid-template-columns: 1fr; max-width: 100%; gap: 8px; }}
  .m-cell {{ padding: 12px 14px; }}
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
  <p class="statement">身体・光・音を、センサーと回路とコードで繋ぐメディアアーティスト。<br>センシングから表現までを一貫して自作する。</p>
  <div class="links">
    <a href="https://github.com/bonsai">GitHub</a>
    <a href="https://ko-fi.com/v0n5ai">ko-fi</a>
  </div>
  <div class="theme-switch" title="テーマ切替（身体 / 光 / 音）">
    <button class="tdot" data-t="body"  onclick="setTheme('body')"  style="background:#3fb950" aria-label="Green"></button>
    <button class="tdot" data-t="light" onclick="setTheme('light')" style="background:#e8a33d" aria-label="Amber"></button>
    <button class="tdot" data-t="sound" onclick="setTheme('sound')" style="background:#58a6ff" aria-label="Blue"></button>
  </div>
</header>

{themes_html}

{works_html}

<section>
  <h2>🛠️ 制作の道具</h2>
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

<footer>
  📈 統計・活動データは <a href="https://github.com/bonsai">GitHub プロフィール</a> へ · <a href="https://ko-fi.com/v0n5ai">ko-fi</a>
</footer>
</div>
<script>
// ===== テーマ切替（3 テーマを動的に変更・localStorage 保存）=====
function setTheme(t) {{
  document.body.dataset.theme = t;
  localStorage.setItem('bonsai-theme', t);
  var dots = document.querySelectorAll('.tdot');
  for (var i = 0; i < dots.length; i++) {{
    dots[i].classList.toggle('active', dots[i].getAttribute('data-t') === t);
  }}
}}
(function() {{ setTheme(localStorage.getItem('bonsai-theme') || 'body'); }})();
</script>
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
  grid.innerHTML = cells.map(function(c) {{
    return '<a class="m-cell" href="' + c.r.url + '" target="_blank">' +
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
</body>
</html>'''

open(OUT_MD, "w", encoding="utf-8").write(readme)
open(OUT, "w", encoding="utf-8").write(h)
open("index.html", "w", encoding="utf-8").write(h)
print(f"OK: {OUT_MD} (stats) {len(readme):,} bytes")
print(f"OK: {OUT} (semantics) {len(h):,} bytes")
print("OK: index.html (Pages 用コピー)")
