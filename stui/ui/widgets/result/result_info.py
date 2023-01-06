from __future__ import annotations
from textual.widget import Widget
from textual.widgets import Static
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.message import Message, MessageTarget
from textual import events

from stui.src import events as src_events

class ResultInfo(Widget):
    """Displays score, views and answer counts next to the ResultBox"""
    result: reactive[dict | None] = reactive({})

    def __init__(self, result) -> None:
        super().__init__()
        self.result = result

    def render(self) -> ComposeResult:
        score_sym = "votes"
        view_sym = "views"
        answer_sym = "answers"
        score_val = f"[bold yellow]{self.result['score']}[/bold yellow]"
        view_val = f"[bold yellow]{self.result['view_count']}[/bold yellow]"
        answer_val = f"[bold yellow]{self.result['answer_count']}[/bold yellow]"
        render_str = f"{score_val} {score_sym}\n{view_val} {view_sym}\n{answer_val} {answer_sym}"
        return render_str
    
    async def on_click(self, event: events.Click) -> Message:
        return self.emit_no_wait(src_events.ResultClick(self, self.result))

    def watch_mouse_over(self, value: bool) -> None:
        # TODO: Find a less hacky way to do this
        self.parent.toggle_class("hover")   