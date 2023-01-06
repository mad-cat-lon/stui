from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Input
from tkinter import Tk

from ..widgets.search import AnsiArt, SearchBox

class SearchScreen(Screen):
    """Search screen to enter a search term"""
    BINDINGS = [
        ("escape", "app.pop_screen", "Remove current screen"),
        ]
    
    def on_input_submitted(self, event: Input.Submitted):
        results = self.app.stackAPI.fetch("search/advanced", q=event.value)
        self.app.show_results(results, event.value)

    def compose(self) -> ComposeResult:
        ansi_art = """
 ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗      ██████╗ ██╗    ██╗
██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║     ██╔═══██╗██║    ██║
██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║     ██║   ██║██║ █╗ ██║
██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  ██║     ██║   ██║██║███╗██║
╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██║     ███████╗╚██████╔╝╚███╔███╔╝
╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ 
        """
        yield Header()
        #yield AnsiArt(ansi_art)
        yield SearchBox()
        yield Footer()  