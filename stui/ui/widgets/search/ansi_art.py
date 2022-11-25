from textual.widgets import Static
from textual.app import ComposeResult

class AnsiArt(Static):
    
    def __init__(self, ansi_art):
        self.ansi_art = ansi_art
        super().__init__()
    
    def render(self) -> ComposeResult:
        return self.ansi_art