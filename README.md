# 🎛️ bonsai — Media Artist / Creative Technologist

> **身体の信号と回路と音を、境界なく繋ぐメディアアーティスト**
>
> Saitama, Japan · good vibes only · [ko-fi](https://ko-fi.com/v0n5ai)

![GitHub followers](https://img.shields.io/github/followers/bonsai?style=flat-square&label=Followers&color=58a6ff)
![Repos](https://img.shields.io/badge/Repos-703-58a6ff?style=flat-square)

---

## 🧬 Artist Statement

RISC-V マイコン (WCH CH32V シリーズ) を中心にした**自作ハードウェア**で、心電図・声紋・LED・音を扱う作品を制作しています。
微弱な生体信号を回路で増幅し、エッジ上の TinyML で意味を与え、光と音として身体に返す——**センシングから表現までを一貫して自作**することが私の制作スタイルです。

## 🫀 Selected Works — Physical & Interactive

### Body / Biosensing

- **[uiap-ecg-monitor](https://github.com/bonsai/uiap-ecg-monitor)** — 自作心電図計 — アナログフロントエンド + RISC-V で生体信号を可視化。計装アンプ(AD620)・Pan-Tompkins R波検出・TinyML 異常分類。バッテリー駆動・ガルバニック絶縁の安全設計。 `C / CH32V203 / TinyML`
- **[uiap-voiceprint-auth](https://github.com/bonsai/uiap-voiceprint-auth)** — 声紋認証システム — エッジ端末(CH32V003)上で MFCC 特徴抽出による話者識別。サーボモーターで物理ロックを制御。 `C / DSP / MFCC`
- **[uiap-sensor-hid](https://github.com/bonsai/uiap-sensor-hid)** — USB HID センサー — RESET ボタンを HID デバイスとして MQTT ブリッジに接続する IoT インターフェース。 `C / USB HID / MQTT`

### Light

- **[led-board](https://github.com/bonsai/led-board)** — 電光掲示板 (LED Board) — 光の文字盤。Web から駆動する LED ボード。 `TypeScript / HTML`
- **[uiapduino-4led](https://github.com/bonsai/uiapduino-4led)** — 290円 RISC-V マイコン(CH32V003)で 4 LED を駆動 — 最小コストの光の制御実験。 `C / Arduino`
- **[led-poc](https://github.com/bonsai/led-poc)** — LED 表現の PoC 群（GDScript による光のシミュレーション）。 `GDScript`

### Sound

- **[4bit-music-riscv](https://github.com/bonsai/4bit-music-riscv)** — 4-bit music on RISC-V — チップ上のレジスタで 4bit 音楽を鳴らす。 `RISC-V / HTML`
- **[audio-patch-simulator-next](https://github.com/bonsai/audio-patch-simulator-next)** — モジュラーシンセ風パッチシミュレータ — Web Audio でケーブルを繋ぐ音の実験。 `JavaScript / Web Audio`
- **[sound-gen](https://github.com/bonsai/sound-gen)** — AudioGen + MusicGen による lo-fi hiphop 生成パイプライン。 `Python / Jupyter`
- **[8bit-Jazz](https://github.com/bonsai/8bit-Jazz)** — 8bit ジャズ — 制約の上に音楽を載せる試み。 `HTML`

### Interaction / Space

- **[microbit-smartlock](https://github.com/bonsai/microbit-smartlock)** — micro:bit スマートロック — 古いスマホ + povo 2.0 で月額ほぼ0円の DIY スマートロック。 `Python / micro:bit`
- **[wifi-visualizer](https://github.com/bonsai/wifi-visualizer)** — WiFi 可視化 — 空間の電波をアートとして捉える。 `HTML`
- **[wifi-ar-visualizer](https://github.com/bonsai/wifi-ar-visualizer)** — WiFi AR visualizer — 空間に重ねる電波の可視化。 `HTML`


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
| コントリビューション | **3673** |
| アクティブ日 | **91 / 93 日** |
| 公開リポジトリ | **703**（オリジナル 261） |

## 🛠️ 使用言語（オリジナル 261 リポジトリ）

| 言語 | 数 | 割合 | 分布 |
|---|---:|---:|---|
| HTML | 47 | 24% | `██████████████████` |
| Python | 42 | 21% | `████████████████▏░` |
| TypeScript | 29 | 14% | `███████████▏░░░░░░` |
| JavaScript | 27 | 14% | `██████████▍░░░░░░░` |
| PowerShell | 11 | 6% | `████▎░░░░░░░░░░░░░` |
| Go | 9 | 4% | `███▌░░░░░░░░░░░░░░` |
| Shell | 4 | 2% | `█▌░░░░░░░░░░░░░░░░` |
| Jupyter Notebook | 4 | 2% | `█▌░░░░░░░░░░░░░░░░` |

---

*このプロフィールは GitHub API の統計から自動生成されています。*
