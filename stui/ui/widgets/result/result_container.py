from __future__ import annotations
from textual.reactive import reactive
from textual.widget import Widget
from textual.message import Message, MessageTarget
from textual.app import ComposeResult
from textual import events
from textual.containers import Horizontal

from stui.src import events as src_events
from .result_box import ResultBox
from .result_info import ResultInfo 

class ResultContainer(Horizontal, can_focus=True):
    """
    Horizontal container containing result info (score, views, answers)
    along with ResultBox containing text
    """
    result_box: reactive[ResultBox | None] = reactive(ResultBox({}))
    result_info: reactive[ResultInfo | None] = reactive(ResultInfo({}))

    def __init__(self, result: dict) -> None:
        self.result = result
        self.is_answered = self.result["is_answered"]
        if self.is_answered == True:
            super().__init__(id="ResultContainer", classes="accepted")
        else:
            super().__init__(id="ResultContainer")
        self.result_box = ResultBox(result)
        self.result_info = ResultInfo(result)
        
    async def on_click(self, event: events.Click) -> Message:
        return self.emit_no_wait(src_events.ResultClick(self, self.result))

    def _on_focus(self, event: events.Focus) -> None:
        return super()._on_focus(event)

    def watch_mouse_over(self, value: bool) -> None:
        self.app.update_styles(self)

    def compose(self) -> ComposeResult:
        yield self.result_info
        yield self.result_box
