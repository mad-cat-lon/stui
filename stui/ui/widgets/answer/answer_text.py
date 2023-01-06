from textual.widgets import Static 
from textual.app import ComposeResult
from rich.markdown import Markdown 

class AnswerText(Static):

    def __init__(self, answer):
        super().__init__()
        self.answer = answer
    
    def render(self) -> ComposeResult:
        return Markdown(self.answer["body_markdown"])
    