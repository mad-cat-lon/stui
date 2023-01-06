from textual.widgets import Static, Input
from textual.app import ComposeResult
from textual.binding import Binding

from tkinter import Tk

class SearchBox(Input):

    #TODO: find a way to add bindings without doing this
    BINDINGS = [
        Binding("left", "cursor_left", "cursor left", show=False),
        Binding("right", "cursor_right", "cursor right", show=False),
        Binding("backspace", "delete_left", "delete left", show=False),
        Binding("home", "home", "home", show=False),
        Binding("end", "end", "end", show=False),
        Binding("ctrl+d", "delete_right", "delete right", show=False),
        Binding("enter", "submit", "submit", show=True),
        Binding("ctrl+v", "paste", "paste", show=True)
    ]

    def __init__(self):
        super().__init__(placeholder="Enter your search term here: ")

    def action_paste(self) -> None:
        x = Tk()
        x.withdraw()
        value = x.clipboard_get()
        self.value = value
        self.cursor_position = len(self.value)