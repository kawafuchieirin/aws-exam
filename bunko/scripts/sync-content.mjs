#!/usr/bin/env node
// 既存の学習ノート(markdown)を content-manifest.json に従って厳選し、
// Starlight が読む src/content/docs/<group> 配下へ取り込む。
//
// 設計方針:
// - ソース(../exam 配下)は「信頼できる唯一の情報源」。ここでは複製のみ行い、原本は変更しない。
// - 生成物 src/content/docs/<group> は毎回作り直す（冪等）。手書きの index.mdx だけは残す。
// - 各ファイルの先頭 H1 を Starlight の frontmatter title に昇格し、本文の重複 H1 は除去する。
//
// なぜコピー方式か: ノートが複数ディレクトリに散在しており、Astro の content collection は
// プロジェクト内のパスしか辿れないため。マニフェストで公開範囲を明示的に管理する狙いもある。

import { readFileSync, writeFileSync, mkdirSync, rmSync, readdirSync, statSync } from 'node:fs';
import { dirname, join, basename, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const DOCS_DIR = join(ROOT, 'src', 'content', 'docs');
const manifest = JSON.parse(readFileSync(join(ROOT, 'content-manifest.json'), 'utf8'));

/** 単純な再帰ウォーク。match は完全一致(README.md)か "*.md" を許容。 */
function findFiles(dir, match, recursive) {
  const abs = resolve(ROOT, dir);
  const out = [];
  let entries;
  try {
    entries = readdirSync(abs, { withFileTypes: true });
  } catch {
    console.warn(`[sync] スキップ: ディレクトリが見つかりません ${dir}`);
    return out;
  }
  for (const e of entries) {
    const full = join(abs, e.name);
    if (e.isDirectory()) {
      if (recursive) out.push(...findFiles(full, match, recursive));
      continue;
    }
    const ok = match === '*.md' ? e.name.endsWith('.md') : e.name === match;
    if (ok) out.push(full);
  }
  return out;
}

/** YAML 文字列の安全なクォート（ダブルクォートとバックスラッシュをエスケープ）。 */
function yamlString(s) {
  return `"${s.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

/** 本文先頭の H1 を title として取り出し、本文からは取り除く。 */
function extractTitle(body, fallback) {
  const lines = body.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^#\s+(.+?)\s*$/);
    if (m) {
      lines.splice(0, i + 1);
      return { title: m[1].trim(), body: lines.join('\n').replace(/^\s+/, '') };
    }
    if (lines[i].trim() !== '') break; // H1 以外の本文が先に来たら諦める
  }
  return { title: fallback, body };
}

/** services/<category>/<service>/README.md → <category>/<service> のような出力スラッグを作る。 */
function deriveSlug(srcAbs, srcDirAbs) {
  const rel = relative(srcDirAbs, srcAbs).replace(/\\/g, '/');
  const parts = rel.split('/');
  const file = parts.pop();
  if (file === 'README.md') {
    // 直下の README はグループのインデックス(/ans/ 等)に、配下の README は親ディレクトリ名に
    return parts.length > 0 ? parts.join('/') : 'index';
  }
  return rel.replace(/\.md$/, '');
}

// docs 配下の生成物(各グループ)を一旦クリア。手書き index.mdx 等は温存。
for (const g of manifest.groups) {
  rmSync(join(DOCS_DIR, g.id), { recursive: true, force: true });
}

let total = 0;
for (const g of manifest.groups) {
  let order = 0;
  for (const src of g.sources) {
    const srcDirAbs = resolve(ROOT, src.dir);
    const files = findFiles(src.dir, src.match, src.recursive).sort();
    for (const f of files) {
      const raw = readFileSync(f, 'utf8');
      const fallback = basename(f, '.md');
      const { title, body } = extractTitle(raw, fallback);
      const slug = deriveSlug(f, srcDirAbs);
      const outPath = join(DOCS_DIR, g.id, `${slug}.md`);
      const sourceRel = relative(resolve(ROOT, '..'), f).replace(/\\/g, '/');
      order += 1;
      const fm = [
        '---',
        `title: ${yamlString(title)}`,
        'tableOfContents:',
        '  maxHeadingLevel: 3',
        `sidebar:`,
        `  order: ${order}`,
        '---',
        '',
        `> 出典ノート: \`${sourceRel}\`（自動同期。原本を編集して再ビルドすると反映されます）`,
        '',
      ].join('\n');
      mkdirSync(dirname(outPath), { recursive: true });
      writeFileSync(outPath, fm + body + '\n');
      total += 1;
    }
  }
  console.log(`[sync] ${g.id}: ${g.label}`);
}

console.log(`[sync] 完了: ${total} ファイルを ${relative(process.cwd(), DOCS_DIR)} へ取り込みました`);
