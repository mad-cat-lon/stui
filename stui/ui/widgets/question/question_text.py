from textual.widgets import Static
from textual.app import ComposeResult
from rich.markdown import Markdown

class QuestionText(Static):

    def __init__(self, question):
        super().__init__()
        self.question = question 
    
    def render(self) -> ComposeResult:
        # TODO: Implement this properly and as a container 
        return Markdown(self.question["body_markdown"])