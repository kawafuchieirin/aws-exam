# 要点文庫 (bunko)

AWS試験対策の学習ノートから「要点」だけを厳選し、スマホからセキュアに閲覧できる
個人用ドキュメントサイト。Astro + [Starlight](https://starlight.astro.build) 製の静的サイトで、
AWS Amplify Hosting（Basic認証）に GitHub Actions（OIDC）で自動デプロイする。

- インフラ構築（Terraform）と CI/CD の手順 → [`../infra/README.md`](../infra/README.md)

## 仕組み

```
exam/point/ans/*.md  ┐
                     ├─(content-manifest.json で厳選)─▶ src/content/docs/{ans,aip}/ ─▶ astro build ─▶ dist/
exam/point/aip/*.md  ┘            sync-content.mjs                                          │
                                                                              GitHub Actions が Amplify へ手動デプロイ
```

- **原本は `exam/` 配下のノート（唯一の情報源）**。このサイトは複製のみで原本は変更しない。
- 公開範囲は [`content-manifest.json`](./content-manifest.json) で明示管理。問題集 `questions.md` は意図的に除外。
- 生成物 `src/content/docs/{ans,aip}/` は `.gitignore` 済み（ビルド時に毎回再生成）。

## ローカル開発

前提: ルートの `.mise.toml`（node 22 / pnpm 9）。`mise install` 済みであること。

```bash
cd bunko
pnpm install
pnpm dev        # sync してから http://localhost:4321 で起動
pnpm build      # sync + 本番ビルド → dist/
pnpm preview    # ビルド結果をローカル確認
```

## コンテンツの追加・除外

`content-manifest.json` の `groups[].sources[]` を編集する。

| キー | 意味 |
| :-- | :-- |
| `dir` | 取込元ディレクトリ（`bunko/` からの相対） |
| `match` | `README.md` のような完全一致、または `*.md` |
| `recursive` | サブディレクトリも辿るか |

各ファイル先頭の `# 見出し` がページタイトルに昇格する。
