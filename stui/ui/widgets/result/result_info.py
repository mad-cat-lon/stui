from __future__ import annotations
from textual.widget import Widget
from textual.widgets import Static
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.message import Message, MessageTarget

class ResultInfo(Widget):
    """Displays score, views and answer counts next to the ResultBox"""
    result: reactive[dict | None] = reactive({})
    # class ResultHover(Message):
    #     """Send a message back if mouse hovers over result box"""
    #     def __init__(self, sender: MessageTarget, value: bool):
    #         self.value = value
    #         super().__init__(sender)

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
    
    # def watch_mouse_over(self, value: bool):
    #     return self.emit_no_wait(self.ResultHover(self, True))

