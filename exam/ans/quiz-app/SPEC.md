# AWS ANS-C01 適応型クイズ TUI アプリ — 設計書 (SPEC)

> 最終更新: 2026-05-24 ／ ステータス: 実装中（パイロット）

## 1. 目的

`exam/ans/services/` 配下の各サービス資料（README.md）に基づく試験問題を、
**学習者のレベルと苦手傾向に合わせて適応的に出題**する TUI アプリ。
問題は各サービスに併設した `questions.md` に静的バンクとして保持し、
アプリは「選んで出す」役割に徹する（実行時の LLM 生成は行わない）。

## 2. 全体構成

```
exam/ans/
├── services/
│   └── <category>/<service>/
│       ├── README.md          # 既存の学習資料
│       └── questions.md        # ★問題バンク（本アプリが読む）
└── quiz-app/
    ├── .mise.toml              # python = "3.14"
    ├── SPEC.md                 # 本書
    ├── README.md               # 起動方法
    ├── requirements.txt        # textual のみ（標準ライブラリ中心）
    ├── aws_quiz/
    │   ├── __main__.py         # エントリ（python -m aws_quiz）
    │   ├── models.py           # Question / Option データモデル
    │   ├── parser.py           # questions.md パーサ
    │   ├── sync.py             # README ハッシュによる陳腐化検知
    │   ├── store.py            # SQLite: 解答履歴・習熟度・Leitner
    │   ├── engine.py           # 適応出題アルゴリズム
    │   └── app.py              # Textual UI（画面遷移）
    └── data/
        └── progress.db         # SQLite（gitignore 対象）
```

## 3. 問題バンク形式（questions.md）

人間が読める Markdown かつ機械パース可能な形式。チェックボックスで正解を表現。

```markdown
---
service: vpc
domain_default: 4
source: README.md
source_sha256: <READMEのSHA256>
generated: 2026-05-24
---

## vpc-001
- type: single        # single（4択1正解） | multi（5択以上2正解以上）
- difficulty: medium  # easy | medium | hard
- domain: 4           # 試験分野 1-4（省略時は domain_default）
- tags: [security-group-vs-nacl, stateful-stateless]

特定の送信元IPアドレスをサブネット単位でブロックしたい。適切なのはどれか。

- [ ] A. セキュリティグループの拒否ルール
- [x] B. ネットワークACLのDenyルール
- [ ] C. ルートテーブルのブラックホール
- [ ] D. IAMポリシー

> **解説**: セキュリティグループは許可ルールのみでDeny不可。NACLはステートレスで
> Denyルールを持てるため、特定IPの遮断はNACLで行う。
> **出典**: [VPC README #3](README.md#3-セキュリティ制御-sg-vs-nacl最頻出)
```

### パース規則
- `---` で囲まれた先頭ブロック = ファイル frontmatter（`key: value`、リストは `[a, b]`）。
- `## <id>` = 問題の開始。直後の `- key: value` 群がメタデータ。
- 空行後の連続テキスト = 設問文。
- `- [ ] A. ...` / `- [x] B. ...` = 選択肢。`[x]` が正解。ラベル（A,B,…）で誤選択肢分析。
- `> **解説**:` / `> **出典**:` = 解説・出典（引用ブロック）。

## 4. 適応出題アルゴリズム

### 4.1 状態（SQLite に永続化）
- `mastery(scope, score)`: トピック（`service:<name>` と `tag:<name>`）ごとの習熟度 0–100。初期 50。
- `attempt(question_id, correct, chosen_labels, ts)`: 全解答履歴。
- `leitner(question_id, box, due_ts)`: 間隔反復の箱（1〜5）と次回出題日時。
- `question_stat(question_id, seen, correct, wrong_label_counts)`: 問題別統計。

### 4.2 習熟度更新（解答時）
```
正解: score += round((100 - score) * k)        # k=0.3
誤答: score -= round(score * k)                # k=0.3
```
問題が持つ複数タグ＋サービスの各 scope を更新。難易度で重み付け（hard 正解は +多め、easy 誤答は −多め）。

### 4.3 Leitner（間隔反復）
- 正解: box += 1（最大5）、due = now + interval[box]（1d,2d,4d,8d,16d）。
- 誤答: box = 1、due = now（即再出題候補）。

### 4.4 出題選択（適応モード）
スコアリングで候補問題を並べ、上位から重複を避けて出題：
```
priority =  w1 * (due期限切れ度)              # Leitnerで復習すべき
          + w2 * (1 - mastery/100)            # 苦手領域を優先
          + w3 * difficulty適合度              # mastery高→hard寄り、低→easy寄り
          + w4 * 鮮度(最近見てない)
          - penalty(陳腐化フラグ)
```
- `difficulty適合度`: ユーザーのサービス習熟度に対し、易しすぎ/難しすぎを減点（目標正答率 ~70% 帯を狙う）。

### 4.5 苦手克服モード
mastery 昇順に scope を並べ、下位 N トピックのタグ/サービスに該当する問題に限定して 4.4 を適用。

### 4.6 模擬試験モード
本番比率（設計30/実装26/運用20/セキュリティ24%）で分野配分、65問・時間計測。
採点はスケール換算の簡易版で 750 相当ラインを判定し、分野別正答率を提示。

## 5. 傾向分析
- **サービス別・タグ別の習熟度/正答率**を一覧。
- **誤選択肢分析**: `wrong_label_counts` から「この問題で最も選ばれた誤答」を集計し、
  混同パターン（例: NLB を ALB と誤認）を解説と紐づけて提示。

## 6. 同期（陳腐化検知）
- 起動時／同期コマンドで各 `questions.md` の `source_sha256` と
  実際の README の SHA256 を比較。
- 不一致なら該当サービスの問題に「要見直し ⚠」を付与し、一覧表示。
- アプリは出題を続行可能（ブロックしない）。再生成は別途バッチ。

## 6.5 ネットワーク基礎（fundamentals）
- `services/fundamentals/<topic>/` に基礎トピックを配置（README + questions.md）。各問 `domain: 0`。
- `DOMAINS` の分野 0 は配点 0 のため模擬試験には配分されない（本番に「基礎」枠は無い）が、
  適応・苦手・指定・誤答深掘りの各モードには含まれる。
- タグは `TAGS.md` の統制語彙（canonical）で統一。サービス問題と基礎が同じ概念タグを共有することで、
  「サービスで間違えた概念」を「基礎」へ降ろして復習できる（`TAG_TO_FUNDAMENTAL`）。

## 6.6 誤答深掘り（なぜ間違えたか）
- 誤答時に**原因の自己申告**（知識不足／勘違い・混同／ケアレス／二択で外した／未学習）を任意記録（`attempt.cause`）。
- 専用画面で、(1) 原因の内訳、(2) 弱点概念→復習すべき基礎トピック、(3) 混同パターン（よく選ぶ誤答選択肢）、
  (4) 誤答問題ごとの「設問／あなたの誤答／正解／原因／解説／基礎復習導線」を提示。
- 「弱点を基礎から復習する」で、誤答に紐づく基礎トピックに絞った復習セットを出題（`select_fundamentals_review`）。

## 7. 画面（Textual）
1. **メインメニュー**: モード選択／統計／同期状態。
2. **クイズ画面**: 設問・選択肢（single=ラジオ, multi=チェック）・即時採点・解説・出典。誤答時は原因の自己申告＋弱点概念→基礎の導線。
3. **結果画面**: 正答率・分野別・更新された習熟度。
4. **誤答深掘り画面**: 原因内訳・弱点概念→基礎・混同パターン・誤答問題リスト・基礎復習導線。
5. **統計画面**: 習熟度ヒートマップ、苦手 Top、混同パターン。
6. **同期画面**: 陳腐化サービス一覧。

キーバインド: `↑↓` 移動, `space` 選択, `enter` 決定, `q` 戻る/終了, `s` 統計。

## 8. 依存・運用
- ランタイム: mise（`.mise.toml` に `python = "3.14"`）。
- 依存: `textual`（TUI）。パース・DB は標準ライブラリ（`hashlib`, `sqlite3`, `re`）。
- 起動: `cd exam/ans/quiz-app && mise install && pip install -r requirements.txt && python -m aws_quiz`
- `data/progress.db` は `.gitignore`。

## 9. 段階
1. ✅ SPEC（本書）
2. アプリ骨組（models/parser/sync/store/engine/app）＋ VPC `questions.md` パイロット
3. （承認後）subagent で全コア◎○サービスの `questions.md` を並列量産
4. △サービスの簡潔バンク追加
```
