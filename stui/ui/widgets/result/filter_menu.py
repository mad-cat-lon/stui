from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button
from textual.message import Message, MessageTarget

class FilterMenu(Horizontal):

    class FilterRequest(Message):
        """Message object to be passed back to ResultScreen when a filter is selected"""
        def __init__(self, sender: MessageTarget, filter: str):
            self.filter = filter
            super().__init__(sender)

    def compose(self) -> ComposeResult:
        yield Button(label="Newest", name="filter_newest")
        yield Button(label="Active", name="filter_active")
        yield Button(label="Most answers", name="filter_most_answers")
        yield Button(label="Unanswered", name="filter_unanswered")
        yield Button(label="Highest score", name="filter_highest_score")
   
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        await self.emit(self.FilterRequest(self, event.button.name))