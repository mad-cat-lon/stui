from textual.widgets import Static
from textual.app import ComposeResult

class QuestionInfo(Static):

    def __init__(self, question):
        super().__init__()
        self.question = question

    def render(self) -> ComposeResult:
        render_str = ""
