from __future__ import annotations
from textual.reactive import reactive
from textual.widget import Widget
from textual import events
from datetime import datetime 
from textual.message import Message, MessageTarget
from textual.app import ComposeResult
import html

class ResultBox(Widget):
    """Widget to display individual results of a query"""
    result: reactive[dict | None] = reactive({})
    class ResultClick(Message):
         """Send a message back if result box is clicked"""
         def __init__(self, sender: MessageTarget, result: dict):
             self.result = result
             super().__init__(sender)
    # class ResultHover(Message):
    #     """Send a message back if mouse hovers over result box"""
    #     def __init__(self, sender: MessageTarget, value: bool):
    #         self.value = value
    #         super().__init__(sender)

    def __init__(self, result: dict) -> None:
        super().__init__()
        self.result = result

    def render(self) -> ComposeResult:
        tags = self.result["tags"]
        owner_display_name = self.result["owner"]["display_name"]
        owner_link = self.result["owner"]["link"] if "link" in self.result["owner"].keys() else None
        view_count = self.result["view_count"]
        answer_count = self.result["answer_count"]
        score = self.result["score"]
        last_activity_date = self.result["last_activity_date"]
        last_activity_date_formatted = datetime.fromtimestamp(last_activity_date).strftime("%Y-%m-%d")
        creation_date = self.result["creation_date"]
        creation_date_formatted = datetime.fromtimestamp(creation_date).strftime("%Y-%m-%d")
        title = html.unescape(self.result["title"])
        render_str = f"""    [bold]{title}[/bold]
    Asked by [bold green]{owner_display_name}[/bold green] on [#f92672]{creation_date_formatted}[/#f92672], last active on [#f92672]{last_activity_date_formatted}[/#f92672]
    {tags}
        """
        return render_str
    
    async def on_click(self, event: events.Click):
        return self.emit_no_wait(self.ResultClick(self, self.result))

    def _on_focus(self, event: events.Focus) -> None:
        return super()._on_focus(event)

    # def watch_mouse_over(self, value: bool):
    #     return self.emit_no_wait(self.ResultHover(self, True))
        