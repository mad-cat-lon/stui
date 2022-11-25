from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer 

from ..widgets.search import AnsiArt, SearchBox
class SearchScreen(Screen):
    """Search screen to enter a search term"""
    BINDINGS = [("escape", "app.pop_screen", "Remove current screen")]
    
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
        yield AnsiArt(ansi_art)
        yield SearchBox()
        yield Footer()  