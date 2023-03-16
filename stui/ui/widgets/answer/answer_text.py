from textual.widgets import Static 
from textual.app import ComposeResult
from rich.markdown import Markdown 

class AnswerText(Static):

    def __init__(self, answer):
        super().__init__()
        self.answer = answer
    
    def render(self) -> ComposeResult:
        render_str = self.answer["body_markdown"]
        render_str += f"\n - {self.answer['owner']['display_name']}"
        return Markdown(render_str)
    