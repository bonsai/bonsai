#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub @bonsai のメディアアート求人向けポートフォリオ生成（フィジカル寄り focus）"""
import json, collections, datetime, html

DATA = "bonsai_repos.jsonl"
KUSA = "kusa_3mo.json"
OUT = "index.html"
OUT_MD = "README.md"

repos = [json.loads(l) for l in open(DATA) if l.strip()]
orig = [r for r in repos if not r["fork"]]

# ============ フィジカル作品データ（メディアアート向け） ============
WORKS = {
    "Body / Biosensing": [
        ("uiap-ecg-monitor", "自作心電図計 — アナログフロントエンド + RISC-V で生体信号を可視化。計装アンプ(AD620)・Pan-Tompkins R波検出・TinyML 異常分類。バッテリー駆動・ガルバニック絶縁の安全設計。", "C / CH32V203 / TinyML"),
        ("uiap-voiceprint-auth", "声紋認証システム — エッジ端末(CH32V003)上で MFCC 特徴抽出による話者識別。サーボモーターで物理ロックを制御。", "C / DSP / MFCC"),
        ("uiap-sensor-hid", "USB HID センサー — RESET ボタンを HID デバイスとして MQTT ブリッジに接続する IoT インターフェース。", "C / USB HID / MQTT"),
    ],
    "Light": [
        ("led-board", "電光掲示板 (LED Board) — 光の文字盤。Web から駆動する LED ボード。", "TypeScript / HTML"),
        ("uiapduino-4led", "290円 RISC-V マイコン(CH32V003)で 4 LED を駆動 — 最小コストの光の制御実験。", "C / Arduino"),
        ("led-poc", "LED 表現の PoC 群（GDScript による光のシミュレーション）。", "GDScript"),
    ],
    "Sound": [
        ("4bit-music-riscv", "4-bit music on RISC-V — チップ上のレジスタで 4bit 音楽を鳴らす。", "RISC-V / HTML"),
        ("audio-patch-simulator-next", "モジュラーシンセ風パッチシミュレータ — Web Audio でケーブルを繋ぐ音の実験。", "JavaScript / Web Audio"),
        ("sound-gen", "AudioGen + MusicGen による lo-fi hiphop 生成パイプライン。", "Python / Jupyter"),
        ("8bit-Jazz", "8bit ジャズ — 制約の上に音楽を載せる試み。", "HTML"),
    ],
    "Interaction / Space": [
        ("microbit-smartlock", "micro:bit スマートロック — 古いスマホ + povo 2.0 で月額ほぼ0円の DIY スマートロック。", "Python / micro:bit"),
        ("wifi-visualizer", "WiFi 可視化 — 空間の電波をアートとして捉える。", "HTML"),
        ("wifi-ar-visualizer", "WiFi AR visualizer — 空間に重ねる電波の可視化。", "HTML"),
    ],
}

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
def lang_color(lang):
    palette = {
        "HTML": "#e34c26", "Python": "#3572A5", "TypeScript": "#3178c6",
        "JavaScript": "#f1e05a", "PowerShell": "#012456", "Go": "#00ADD8",
        "Shell": "#89e051", "Jupyter Notebook": "#DA5B0B", "Java": "#b07219",
        "Rust": "#dea584", "OCaml": "#ef7a08", "C#": "#178600", "C": "#555555",
        "GDScript": "#355570", "Elm": "#60B5CC", "Ruby": "#701516", "Svelte": "#ff3e00",
    }
    return palette.get(lang, "#8b949e")

def esc(s): return html.escape(s or "")

works_html = ""
for cat, items in WORKS.items():
    cards = "\n".join(
        f'''<div class="card">
  <a class="card-title" href="https://github.com/bonsai/{esc(name)}" target="_blank">{esc(name)}</a>
  <div class="card-desc">{esc(desc)}</div>
  <div class="card-meta"><span class="tech">{esc(tech)}</span></div>
</div>''' for name, desc, tech in items)
    works_html += f'<section><h2>{cat}</h2><div class="cards">{cards}</div></section>'

lang_bars = "\n".join(
    f'''<div class="bar-row"><div class="bar-label">{esc(lang)}</div>
    <div class="bar-track"><div class="bar-fill" style="width:{round(v / lang_max * 100, 1)}%;background:{lang_color(lang)}"></div></div>
    <div class="bar-val">{v}</div></div>'''
    for lang, v in lang_top)

h = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>bonsai — Media Artist Portfolio</title>
<style>
:root {{
  --bg: #0d1117; --panel: #161b22; --border: #30363d;
  --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff; --green: #3fb950;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: var(--bg); color: var(--text); font-family: "Hiragino Kaku Gothic ProN", "Noto Sans JP", sans-serif; line-height: 1.7; }}
.wrap {{ max-width: 980px; margin: 0 auto; padding: 32px 20px 80px; }}

header {{ padding: 40px 24px; background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%); border: 1px solid var(--border); border-radius: 20px; margin-bottom: 28px; text-align: center; }}
header img {{ width: 100px; height: 100px; border-radius: 50%; border: 3px solid var(--green); margin-bottom: 14px; }}
header h1 {{ font-size: 30px; }}
header .role {{ color: var(--green); font-weight: 700; letter-spacing: 1px; margin: 6px 0 10px; }}
header .statement {{ color: var(--muted); max-width: 640px; margin: 0 auto 14px; font-size: 14px; }}
header .links a {{ color: var(--accent); text-decoration: none; margin: 0 10px; font-size: 14px; }}
header .links a:hover {{ text-decoration: underline; }}

.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 14px; margin-bottom: 36px; }}
.tile {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 18px; text-align: center; }}
.tile .num {{ font-size: 28px; font-weight: 700; color: var(--green); }}
.tile .lbl {{ color: var(--muted); font-size: 12px; margin-top: 4px; }}

section {{ margin-bottom: 36px; }}
h2 {{ font-size: 19px; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 2px solid var(--border); }}

.cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 14px; }}
.card {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 16px; transition: border-color .15s, transform .15s; }}
.card:hover {{ border-color: var(--green); transform: translateY(-2px); }}
.card-title {{ color: var(--accent); font-weight: 700; font-size: 15px; text-decoration: none; }}
.card-title:hover {{ text-decoration: underline; }}
.card-desc {{ color: var(--muted); font-size: 13px; margin: 8px 0 10px; }}
.card-meta {{ font-size: 12px; }}
.tech {{ color: var(--green); font-family: ui-monospace, monospace; font-size: 11px; }}

.kusa-box {{ background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 20px; margin-bottom: 14px; }}
.kusa-box img {{ width: 100%; max-width: 480px; display: block; margin: 0 auto; }}

.bar-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 7px; font-size: 13px; }}
.bar-label {{ width: 130px; text-align: right; color: var(--muted); white-space: nowrap; }}
.bar-track {{ flex: 1; height: 18px; background: #21262d; border-radius: 9px; overflow: hidden; }}
.bar-fill {{ height: 100%; border-radius: 9px; min-width: 2px; }}
.bar-val {{ width: 44px; font-weight: 600; }}

.stack {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; }}
.stack .card h3 {{ font-size: 14px; color: var(--green); margin-bottom: 8px; }}
.stack .card ul {{ list-style: none; font-size: 13px; color: var(--muted); }}
.stack .card li {{ margin-bottom: 4px; }}

footer {{ text-align: center; color: var(--muted); font-size: 12px; margin-top: 40px; }}
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

<div class="stats">
  <div class="tile"><div class="num">{kusa_total}</div><div class="lbl">直近3ヶ月の貢献</div></div>
  <div class="tile"><div class="num">{kusa_active}/{kusa_days}</div><div class="lbl">アクティブ日</div></div>
  <div class="tile"><div class="num">{n_orig}</div><div class="lbl">オリジナル作品</div></div>
  <div class="tile"><div class="num">{total}</div><div class="lbl">公開リポジトリ</div></div>
</div>

{works_html}

<section>
  <h2>🌱 直近 3 ヶ月の活動</h2>
  <div class="kusa-box">
    <img src="kusa.svg" alt="Last 90 days contributions">
  </div>
</section>

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
</body>
</html>'''

open(OUT_MD, "w", encoding="utf-8").write(readme)
open(OUT, "w", encoding="utf-8").write(h)
print(f"OK: {OUT_MD} ({len(readme):,} bytes)")
print(f"OK: {OUT} ({len(h):,} bytes)")
