# AWS ANS-C01 適応型クイズ TUI

`exam/ans/services/` の各サービス資料に基づく試験問題を、学習者のレベルと
苦手傾向に合わせて適応的に出題する TUI アプリ。設計は [SPEC.md](SPEC.md) を参照。

## 特徴
- **適応出題**: トピック別の習熟度スコア＋間隔反復(Leitner)＋難易度適合で最適な問題を選択。
- **苦手克服**: 習熟度の低い領域に集中して出題。
- **傾向分析**: サービス別・概念タグ別の習熟度、誤選択肢の混同パターンを可視化。
- **模擬試験**: 本番配点(分野別%)で65問、750相当ラインを判定。
- **Markdown 同期**: 各サービスの `questions.md` をパース。参照 README が変わると「要見直し ⚠」を表示。

## セットアップ
```bash
cd exam/ans/quiz-app
mise install                         # Python 3.14
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt      # textual
```

## 起動
```bash
python -m aws_quiz
```

## 問題バンクの場所
各サービスディレクトリに併設：
```
exam/ans/services/<category>/<service>/questions.md
```
形式は SPEC.md「3. 問題バンク形式」を参照。

## テスト
```bash
python -m aws_quiz.selftest      # パーサ・エンジン・ストアのスモークテスト（TUI不要）
```
