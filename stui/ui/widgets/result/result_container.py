from __future__ import annotations
from textual.reactive import reactive
from textual.widget import Widget
from textual.message import Message, MessageTarget
from textual.app import ComposeResult
from textual import events
from textual.containers import Horizontal

from .result_box import ResultBox
from .result_info import ResultInfo 

class ResultContainer(Horizontal, can_focus=True):
    """
    Horizontal container containing result info (score, views, answers)
    along with ResultBox containing text
    """
    result_box: reactive[ResultBox | None] = reactive(ResultBox({}))
    result_info: reactive[ResultInfo | None] = reactive(ResultInfo({}))
    class ResultClick(Message):
        """Send a message back if result box is clicked"""
        def __init__(self, sender: MessageTarget, result: dict):
            self.result = result
            super().__init__(sender)

    def __init__(self, result: dict) -> None:
        super().__init__()
        self.result = result
        self.result_box = ResultBox(result)
        self.result_info = ResultInfo(result)

    async def on_click(self, event: events.Click) -> Message:
        return self.emit_no_wait(self.ResultClick(self, self.result))

    #TODO: Figure out how message bubbling works so we don't have to duplicate
    def on_result_box_result_click(self, event: ResultBox.ResultClick) -> None:
        self.emit_no_wait(self.ResultClick(self, self.result))

    def _on_focus(self, event: events.Focus) -> None:
        return super()._on_focus(event)

    def watch_mouse_over(self, value: bool) -> None:
        self.app.update_styles(self)

    def compose(self) -> ComposeResult:
        yield self.result_info
        yield self.result_box
