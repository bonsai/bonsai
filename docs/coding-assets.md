# Coding Assets — Ontology × Metadata × BQML

## Purpose

`bonsai/repos` は Repository の一覧管理だけではなく、GitHub 上の Coding Asset を **聞けばすっと取り出せる記憶装置**として設計する。

Filesystem は保存場所。Metadata は意味。Search はアクセス手段。

> **Filesystem is storage. Metadata is memory. Search is access.**

## Asset

Repository、Gist、File、Script、Notebook、Config、Prompt、Workflow などを共通の `Asset` として扱う。

```text
Asset
├── Repository
├── Gist
├── File
├── Script
├── Notebook
├── Config
├── Prompt
└── Workflow
```

## Ephemeral

Asset の永続性を Ontology の属性として持つ。

```text
permanent    育てる
reusable     再利用する
experimental 実験
ephemeral    一時利用
archived     保存のみ
```

`ephemeral` でも捨てるとは限らない。**検索可能な状態で残す**。利用回数・関連Asset・品質などが増えれば `reusable`、さらに Repository 化候補へ遷移できる。

```text
Gist
 ↓
ephemeral
 ↓
search / usage
 ↓
reusable
 ↓
Repository化候補
```

## Metadata

ディレクトリ構造をAgentに辿らせるのではなく、ランダムアクセスできる metadata を充実させる。

```yaml
asset:
  id:
  source: repo | gist | file | external
  url:
  owner:
  repo:
  path:
  type:
  language:

meaning:
  description:
  purpose:
  concepts: []
  technologies: []
  domain: []

search:
  terms: []
  aliases: []
  keywords: []
  questions: []
  related_terms: []

relations:
  similar: []
  depends_on: []
  related_to: []
  alternative_to: []
  used_with: []

lifecycle:
  persistence: ephemeral | experimental | reusable | permanent | archived
  usage_count:
  quality:
  updated_at:
```

## Search Terms

特に `search.terms / aliases / questions` を重要なメタデータとする。

Agent が専門用語を知らなくても、自然言語の質問から Asset に到達できるようにする。

例:

```yaml
search:
  terms:
    - GitHub MCP
    - GitHub tools
    - repository automation
    - coding agent
    - GitHub API
  aliases:
    - GitHubをAgentから操作
    - repo操作MCP
  questions:
    - GitHubをCoding Agentから操作するものは？
    - repoをAgentから作成・管理するコードは？
```

検索履歴から新しい検索語を発見した場合は metadata に還流させる。

```text
query
 ↓
search
 ↓
result
 ↓
usage / adoption
 ↓
new search terms
 ↓
metadata enrichment
```

## Ontology × BQML

役割を分ける。

### Ontology

「これは何か」「何と何が関係するか」を定義する。

```text
Script --automates--> Workflow
Notebook --analyzes--> Dataset
Repository --implements--> Application
Asset --related_to--> Concept
```

### BQML

大量のGitHubデータから、人手で定義しきれない関係や価値を発見する。

```text
stars
forks
commits
issues
languages
topics
dependencies
README
search_terms
embeddings
activity
```

から、例えば：

```text
similarity
clustering
anomaly
health
usage / value
migration candidate
```

を推定し、metadata に還流する。

## External GitHub

自分の Repository は濃い一次資産として扱う。一方で、他人の Repository / Gist も検索対象にする。

```text
自分のrepo ─┐
            ├→ GitHub Asset Index → Search → Coding Agent
他人のrepo ─┤
Gist ───────┘
```

Coding Agent から GitHub MCP / `gh` CLI 等を介して実体へアクセスする。`bonsai/repos` は実体のコピーではなく、発見のための metadata / index を中心にする。

## Design Principle

最終目的は分類体系を人間に覚えさせることではない。

> **「あれ、なんだっけ？」と聞けば、関連する Asset がすっと出てくる。**

```text
Question
  ↓
Intent
  ↓
Metadata
  ↓
Exact / Semantic Search
  ↓
Candidate Assets
  ↓
GitHub MCP / gh
  ↓
Coding Agent
```

Ontology は意味を与える。Metadata は直接引ける索引になる。BQML はデータから新しい関係を発見する。
