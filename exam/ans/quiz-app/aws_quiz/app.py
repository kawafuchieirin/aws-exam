"""Textual TUI 本体：メニュー・クイズ・結果・統計・同期画面。"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.content import Content
from textual.css.query import NoMatches
from textual.geometry import Size
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Label,
    RadioButton,
    RadioSet,
    Rule,
    Static,
)

from . import engine
from .models import DOMAINS, MISTAKE_CAUSES, Question, domain_label
from .parser import load_all_questions
from .store import Store
from .sync import check_sync

SERVICES_ROOT = Path(__file__).resolve().parents[2] / "services"
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "progress.db"

DIFF_JP = {"easy": "易", "medium": "中", "hard": "難"}


class _WrapLabelMixin:
    """選択肢ラベルを折り返し表示する ToggleButton 派生の共通実装。

    Textual の ToggleButton は ``text-wrap: nowrap`` ＋ ラベルを ``first_line`` のみに切り詰め、
    高さを 1 行固定にするため、長い選択肢の末尾が "…" で省略され全文が読めない。
    ここでラベル全文を保持し、コンテンツ幅で折り返した行数を高さとして返すことで全文表示する。
    折り返し有効化の CSS（text-wrap: wrap など）は App 側の CSS で指定する。
    """

    def _make_label(self, label):  # type: ignore[override]
        # 親実装の `.first_line` 切り詰めを行わず、ラベル全文を保持する。
        return Content.from_text(label).rstrip()

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:  # type: ignore[override]
        # ボタン記号(3桁)と左右パディング(各1)を除いた幅で折り返した行数を高さにする。
        # やや控えめ（=高め）に見積もることで切り詰めを確実に防ぐ。
        height = self._label.get_height(self.styles, max(width - 5, 1))  # type: ignore[attr-defined]
        return max(height, 1)


class WrapRadioButton(_WrapLabelMixin, RadioButton):
    """ラベルを折り返す単一選択ボタン。"""


class WrapCheckbox(_WrapLabelMixin, Checkbox):
    """ラベルを折り返す複数選択ボックス。"""


class MenuScreen(Screen):
    BINDINGS = [Binding("q", "quit", "終了")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        app: QuizApp = self.app  # type: ignore
        stale = len(app.stale_services)  # 起動時に算出済みのものを再利用
        sync_msg = "✅ すべて最新" if stale == 0 else f"⚠ {stale} サービスが要見直し"
        yield Vertical(
            Static(f"[b]AWS ANS-C01 適応型クイズ[/b]", classes="title"),
            Static(f"問題数: {len(app.questions)}    解答履歴: {app.store.total_attempts()}    同期: {sync_msg}"),
            Rule(),
            Button("⓪ ネットワーク基礎モード", id="basics", variant="success"),
            Button("① 適応モード（おまかせ出題）", id="adaptive", variant="primary"),
            Button("② 苦手克服モード", id="weak", variant="warning"),
            Button("③ 模擬試験モード（65問）", id="mock", variant="error"),
            Button("④ サービス/分野指定", id="filter"),
            Button("⑤ 復習（間違えた問題）", id="review"),
            Button("🔍 誤答深掘り（なぜ間違えたか）", id="mistakes"),
            Button("📊 統計・傾向分析", id="stats"),
            Button("🔄 同期状態", id="sync"),
            classes="menu",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: QuizApp = self.app  # type: ignore
        bid = event.button.id
        if bid == "basics":
            qs = engine.select_by_filter(app.store, app.questions, 10, domain=0)
            if not qs:
                self.notify("基礎問題（fundamentals）が見つかりません。", severity="warning")
                return
            self.app.push_screen(QuizScreen(qs, "ネットワーク基礎モード"))
        elif bid == "adaptive":
            qs = engine.select_adaptive(app.store, app.questions, 10)
            self.app.push_screen(QuizScreen(qs, "適応モード"))
        elif bid == "weak":
            qs = engine.select_weak(app.store, app.questions, 10)
            self.app.push_screen(QuizScreen(qs, "苦手克服モード"))
        elif bid == "mock":
            qs = engine.build_mock_exam(app.questions, 65)
            self.app.push_screen(QuizScreen(qs, "模擬試験", mock=True))
        elif bid == "filter":
            self.app.push_screen(FilterScreen())
        elif bid == "review":
            qs = engine.select_review(app.store, app.questions, 10)
            if not qs:
                self.notify("復習対象の問題はまだありません。", severity="information")
                return
            self.app.push_screen(QuizScreen(qs, "復習モード"))
        elif bid == "mistakes":
            self.app.push_screen(MistakeScreen())
        elif bid == "stats":
            self.app.push_screen(StatsScreen())
        elif bid == "sync":
            self.app.push_screen(SyncScreen())


class FilterScreen(Screen):
    BINDINGS = [Binding("q", "app.pop_screen", "戻る")]

    def compose(self) -> ComposeResult:
        yield Header()
        app: QuizApp = self.app  # type: ignore
        services = sorted({q.service for q in app.questions})
        yield Vertical(
            Static("[b]サービスを選択[/b]"),
            *[Button(s, id=f"svc-{s}") for s in services],
            Rule(),
            Static("[b]または分野を選択[/b]"),
            *[Button(f"{domain_label(d)}: {DOMAINS[d][0]}", id=f"dom-{d}") for d in DOMAINS if d != 0],
            classes="menu",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: QuizApp = self.app  # type: ignore
        bid = event.button.id or ""
        if bid.startswith("svc-"):
            svc = bid[4:]
            qs = engine.select_by_filter(app.store, app.questions, 10, service=svc)
            self.app.push_screen(QuizScreen(qs, f"サービス: {svc}"))
        elif bid.startswith("dom-"):
            d = int(bid[4:])
            qs = engine.select_by_filter(app.store, app.questions, 10, domain=d)
            self.app.push_screen(QuizScreen(qs, domain_label(d)))


class QuizScreen(Screen):
    BINDINGS = [
        Binding("enter", "submit", "決定/次へ"),
        Binding("q", "app.pop_screen", "中断"),
    ]

    def __init__(self, questions: list[Question], mode: str, mock: bool = False):
        super().__init__()
        self.questions = questions
        self.mode = mode
        self.mock = mock
        self.idx = 0
        self.num_correct = 0
        self.answered = False
        self._last_attempt_id: int | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="body")
        yield Footer()

    def on_mount(self) -> None:
        if not self.questions:
            self.notify("出題できる問題がありません。", severity="warning")
            self.app.pop_screen()
            return
        self.run_worker(self._render_question(), exclusive=True)

    @property
    def current(self) -> Question:
        return self.questions[self.idx]

    async def _render_question(self) -> None:
        self.answered = False
        body = self.query_one("#body", VerticalScroll)
        await body.remove_children()  # 旧ウィジェットの除去完了を待つ（ID 重複防止）
        q = self.current
        tag = f"[{DIFF_JP.get(q.difficulty,'?')}] {q.service} {domain_label(q.domain)}"
        stale = " ⚠要見直し" if q.stale else ""
        widgets: list = [
            Static(f"[dim]{self.mode}  {self.idx+1}/{len(self.questions)}  {tag}{stale}[/dim]"),
            Static(f"\n[b]{q.stem}[/b]\n"),
        ]
        if q.qtype == "multi":
            widgets.append(Static(f"[yellow]複数選択（{len(q.correct_labels)}つ選ぶ）[/yellow]"))
            widgets += [WrapCheckbox(f"{o.label}. {o.text}", id=f"opt-{o.label}") for o in q.options]
        else:
            widgets.append(
                RadioSet(*[WrapRadioButton(f"{o.label}. {o.text}", id=f"opt-{o.label}") for o in q.options], id="radio")
            )
        widgets.append(Button("解答する", id="submit-btn", variant="primary"))
        await body.mount(*widgets)

    def _chosen(self) -> set[str]:
        q = self.current
        chosen: set[str] = set()
        if q.qtype == "multi":
            for o in q.options:
                cb = self.query_one(f"#opt-{o.label}", Checkbox)
                if cb.value:
                    chosen.add(o.label)
        else:
            rs = self.query_one("#radio", RadioSet)
            if rs.pressed_button and rs.pressed_button.id:
                chosen.add(rs.pressed_button.id.replace("opt-", ""))
        return chosen

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id in ("submit-btn", "next-btn"):
            self.action_submit()

    def action_submit(self) -> None:
        if self.answered:
            self._next()
            return
        q = self.current
        chosen = self._chosen()
        if not chosen:
            self.notify("選択してください。", severity="warning")
            return
        correct = q.is_correct(chosen)
        self.num_correct += int(correct)
        self._last_attempt_id = self.app.store.record_answer(q, chosen, correct)  # type: ignore
        self.answered = True
        self.run_worker(self._render_feedback(chosen, correct), exclusive=True)

    async def _render_feedback(self, chosen: set[str], correct: bool) -> None:
        q = self.current
        body = self.query_one("#body", VerticalScroll)
        verdict = "[green b]正解 ✅[/green b]" if correct else "[red b]不正解 ❌[/red b]"
        ans = "、".join(sorted(q.correct_labels))
        widgets: list = [Rule(), Static(f"{verdict}  正解: {ans}")]
        if not self.mock and q.explanation:
            widgets.append(Static(f"\n[i]{q.explanation}[/i]"))
            if q.source:
                widgets.append(Static(f"[dim]出典: {q.source}[/dim]"))
        # 誤答時：なぜ間違えたかの深掘り（自己申告＋弱点概念→基礎の導線）
        if not correct and not self.mock:
            chosen_txt = "、".join(
                f"{o.label}.{o.text}" for o in q.options if o.label in chosen and not o.correct
            )
            if chosen_txt:
                widgets.append(Static(f"\n[red]あなたの誤答[/red]: {chosen_txt}"))
            rec = engine.recommend_fundamental(q, self.app.store)  # type: ignore
            if rec:
                topic, tag, mastery = rec
                widgets.append(
                    Static(
                        f"[yellow]弱点概念[/yellow]: [b]{tag}[/b]（習熟度 {mastery:.0f}）"
                        f" → 基礎『{topic}』の復習が有効"
                    )
                )
            widgets.append(Static("\n[b]なぜ間違えた？[/b][dim]（任意・記録すると傾向分析に反映）[/dim]"))
            widgets.append(
                RadioSet(
                    *[RadioButton(v, id=f"cause-{k}") for k, v in MISTAKE_CAUSES.items()],
                    id="cause",
                )
            )
        label = "次へ →" if self.idx + 1 < len(self.questions) else "結果を見る"
        widgets.append(Button(label, id="next-btn", variant="success"))
        await body.mount(*widgets)

    def _save_cause(self) -> None:
        """誤答原因の自己申告が選択されていれば記録する。"""
        if self._last_attempt_id is None:
            return
        try:
            rs = self.query_one("#cause", RadioSet)
        except NoMatches:  # 正解遷移では #cause が存在しない（正常系）
            return
        btn = rs.pressed_button
        if btn and btn.id:
            self.app.store.set_cause(self._last_attempt_id, btn.id.replace("cause-", ""))  # type: ignore

    def _next(self) -> None:
        self._save_cause()
        if self.idx + 1 < len(self.questions):
            self.idx += 1
            self.run_worker(self._render_question(), exclusive=True)
        else:
            self.app.pop_screen()
            self.app.push_screen(ResultScreen(self.questions, self.num_correct, self.mock))


class ResultScreen(Screen):
    BINDINGS = [Binding("q", "app.pop_screen", "メニューへ")]

    def __init__(self, questions: list[Question], num_correct: int, mock: bool):
        super().__init__()
        self.questions = questions
        self.num_correct = num_correct
        self.mock = mock

    def compose(self) -> ComposeResult:
        yield Header()
        total = len(self.questions)
        rate = (self.num_correct / total * 100) if total else 0
        lines = [f"[b]結果[/b]  {self.num_correct}/{total} 正解（{rate:.0f}%）", ""]
        if self.mock:
            # 簡易スケール換算：正答率→100-1000
            scaled = round(100 + rate / 100 * 900)
            judge = "[green b]合格ライン到達 🎉[/green b]" if scaled >= 750 else "[red]あと一歩（750未満）[/red]"
            lines.append(f"スケールスコア(簡易): {scaled} / 1000  {judge}")
            lines.append("")
            lines.append("[b]分野別正答率[/b]（本セット内）")
            dom_total: dict[int, int] = defaultdict(int)
            for q in self.questions:
                dom_total[q.domain] += 1
            for d in sorted(dom_total):
                lines.append(f"  {domain_label(d)} {DOMAINS[d][0]}: {dom_total[d]}問出題")
        yield Vertical(Static("\n".join(lines)), Button("メニューへ戻る", id="back", variant="primary"), classes="menu")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()


class MistakeScreen(Screen):
    """誤答深掘り：なぜ間違えたか（自己申告原因・弱点概念・混同パターン・基礎復習導線）。"""

    BINDINGS = [Binding("q", "app.pop_screen", "戻る")]

    def compose(self) -> ComposeResult:
        yield Header()
        app: QuizApp = self.app  # type: ignore
        store = app.store
        qmap = {q.id: q for q in app.questions}
        wrong = store.wrong_questions()
        stats = store.question_stats()

        lines: list[str] = ["[b]🔍 誤答深掘り — なぜ間違えたか[/b]", ""]
        if not wrong:
            lines.append("まだ未克服の誤答はありません。問題を解くとここに分析が出ます。")
            yield VerticalScroll(Static("\n".join(lines)))
            yield Footer()
            return

        lines.append(f"未克服の誤答（最新解答が不正解）: [red b]{len(wrong)}[/red b] 問")

        # 1) 誤答原因の内訳（自己申告）
        causes = store.cause_counts()
        lines += ["", "[b]① 誤答原因の内訳（自己申告）[/b]"]
        if causes:
            total = sum(causes.values())
            for key, label in MISTAKE_CAUSES.items():
                c = causes.get(key, 0)
                if c:
                    bar = "█" * round(c / total * 20)
                    lines.append(f"  {label:<28} {bar} {c}")
        else:
            lines.append("  [dim]まだ原因が記録されていません（誤答時に選択すると集計されます）。[/dim]")

        # 各誤答問題の基礎推薦を1回だけ計算してキャッシュ（②と④で再利用）
        rec_cache: dict[str, tuple[str, str, float] | None] = {}
        for w in wrong:
            q = qmap.get(w["question_id"])
            if q:
                rec_cache[q.id] = engine.recommend_fundamental(q, store)

        # 2) 弱点概念 → 基礎トピック
        concept: dict[str, tuple[str, float, int]] = {}  # tag -> (topic, mastery, count)
        for qid, rec in rec_cache.items():
            if rec:
                topic, tag, mastery = rec
                cur = concept.get(tag)
                concept[tag] = (topic, mastery, (cur[2] if cur else 0) + 1)
        lines += ["", "[b]② 弱点概念と復習すべき基礎[/b]"]
        if concept:
            for tag, (topic, mastery, cnt) in sorted(concept.items(), key=lambda kv: kv[1][1])[:6]:
                lines.append(f"  [b]{tag}[/b]（習熟度 {mastery:.0f} / 誤答 {cnt}件） → 基礎『{topic}』")
        else:
            lines.append("  [dim]基礎に対応づく弱点概念は検出されていません。[/dim]")

        # 3) 混同パターン（最も選ばれた誤答選択肢）
        lines += ["", "[b]③ 混同パターン（よく選ぶ誤答）[/b]"]
        confusions = engine.confusion_patterns(
            qmap, stats, top_n=6, only_ids={w["question_id"] for w in wrong}
        )
        if confusions:
            for cnt, q, opt in confusions:
                lines.append(f"  [{q.service}] 「{opt.text[:42]}」を {cnt}回 誤選択")
        else:
            lines.append("  [dim]データがまだ十分ではありません。[/dim]")

        # 4) 誤答問題の深掘りリスト
        lines += ["", "[b]④ 誤答した問題（直近順）[/b]"]
        for w in wrong[:8]:
            q = qmap.get(w["question_id"])
            if not q:
                continue
            chosen = set(w["chosen"])
            your = "、".join(o.text[:34] for o in q.options if o.label in chosen and not o.correct)
            ans = "、".join(o.text[:34] for o in q.options if o.correct)
            cause_label = MISTAKE_CAUSES.get(w["cause"], "未記録") if w["cause"] else "未記録"
            lines.append(f"\n  [b]{q.id}[/b] [{q.service}]")
            lines.append(f"    Q: {q.stem[:60]}")
            lines.append(f"    [red]誤答[/red]: {your or '(無選択/部分選択)'}")
            lines.append(f"    [green]正解[/green]: {ans}")
            lines.append(f"    原因: {cause_label}")
            if q.explanation:
                lines.append(f"    [i]解説: {q.explanation[:80]}[/i]")
            rec = rec_cache.get(q.id)
            if rec:
                lines.append(f"    → 基礎復習: 『{rec[0]}』（弱点 {rec[1]}）")

        yield VerticalScroll(
            Static("\n".join(lines)),
            Button("弱点を基礎から復習する", id="review-fund", variant="success"),
            Button("メニューへ戻る", id="back", variant="primary"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        app: QuizApp = self.app  # type: ignore
        if event.button.id == "review-fund":
            wrong = app.store.wrong_questions()
            qs = engine.select_fundamentals_review(app.store, app.questions, wrong, 10)
            if not qs:
                self.notify("基礎に対応づく弱点が検出されませんでした。", severity="information")
                return
            self.app.push_screen(QuizScreen(qs, "弱点の基礎復習"))
        elif event.button.id == "back":
            self.app.pop_screen()


class StatsScreen(Screen):
    BINDINGS = [Binding("q", "app.pop_screen", "戻る")]

    def compose(self) -> ComposeResult:
        yield Header()
        app: QuizApp = self.app  # type: ignore
        store = app.store
        mastery = store.all_mastery()
        stats = store.question_stats()

        lines = ["[b]習熟度（低い順 = 苦手）[/b]", ""]
        if mastery:
            for scope, score in sorted(mastery.items(), key=lambda kv: kv[1])[:15]:
                bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
                lines.append(f"  {scope:<32} {bar} {score:5.1f}")
        else:
            lines.append("  まだデータがありません。問題を解いてください。")

        # 混同パターン（誤選択肢分析）
        lines += ["", "[b]混同パターン（よく選ばれた誤答）[/b]", ""]
        qmap = {q.id: q for q in app.questions}
        confusions = engine.confusion_patterns(qmap, stats, top_n=8)
        if confusions:
            for cnt, q, opt in confusions:
                lines.append(f"  [{q.service}] 「{opt.text[:40]}」を {cnt}回 誤選択")
        else:
            lines.append("  まだ十分なデータがありません。")

        yield VerticalScroll(Static("\n".join(lines)))
        yield Footer()


class SyncScreen(Screen):
    BINDINGS = [Binding("q", "app.pop_screen", "戻る")]

    def compose(self) -> ComposeResult:
        yield Header()
        lines = ["[b]同期状態（README 変更検知）[/b]", ""]
        for s in check_sync(SERVICES_ROOT):
            mark = "⚠ 要見直し" if s.stale else "✅ 最新"
            lines.append(f"  {mark}  {s.service}")
        if len(lines) == 2:
            lines.append("  questions.md がまだありません。")
        yield VerticalScroll(Static("\n".join(lines)))
        yield Footer()


class QuizApp(App):
    CSS = """
    .title { color: $accent; text-style: bold; padding: 1 0; }
    .menu { padding: 1 2; width: 80%; }
    Button { margin: 0 0 1 0; width: 100%; }
    #body { padding: 1 2; }
    Checkbox, RadioButton { margin: 0 0 0 0; }
    /* 選択肢ラベルを折り返して全文表示する（既定の nowrap/ellipsis を上書き）。
       App CSS は widget の DEFAULT_CSS より優先されるため確実に適用される。 */
    WrapRadioButton, WrapCheckbox {
        text-wrap: wrap;
        text-overflow: clip;
        height: auto;
    }
    WrapCheckbox { width: 1fr; }
    """
    TITLE = "AWS ANS-C01 Quiz"

    def __init__(self):
        super().__init__()
        self.stale_services: set[str] = set()
        self.questions = self._load()
        self.store = Store(DB_PATH)

    def _load(self) -> list[Question]:
        questions = load_all_questions(SERVICES_ROOT)
        # 起動時の同期チェックは1回だけ。結果を stale_services に保持し MenuScreen で再利用する。
        self.stale_services = {s.service for s in check_sync(SERVICES_ROOT) if s.stale}
        for q in questions:
            if q.service in self.stale_services:
                q.stale = True
        return questions

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())

    def on_unmount(self) -> None:
        try:
            self.store.close()
        except Exception:
            pass


def main() -> None:
    QuizApp().run()
