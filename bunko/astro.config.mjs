// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// 公開URL。Amplify のドメインが決まったら環境変数 SITE_URL で上書きする
// （CI で SITE_URL=https://main.xxxx.amplifyapp.com を渡す）。
const site = process.env.SITE_URL || 'https://example.amplifyapp.com';

// https://astro.build/config
export default defineConfig({
	site,
	integrations: [
		starlight({
			title: '要点文庫',
			description: 'AWS試験対策の自分用 要点まとめ。スマホからセキュアに閲覧。',
			defaultLocale: 'ja',
			locales: {
				root: { label: '日本語', lang: 'ja' },
			},
			pagefind: true, // 全文検索（静的・クライアントサイドで完結）
			sidebar: [
				{
					label: 'ANS-C01 ネットワーク要点',
					items: [
						{ label: '📝 問題集トラッカー', link: '/ans/quiz' },
						{ autogenerate: { directory: 'ans' } },
					],
				},
				{ label: 'AIP-C01 生成AI 参考書', items: [{ autogenerate: { directory: 'aip' } }] },
			],
		}),
	],
});
