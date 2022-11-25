from textual.containers import Container
from textual.app import ComposeResult

from .question_info import QuestionInfo
from .question_text import QuestionText
from .question_title import QuestionTitle

class QuestionContainer(Container):

    def __init__(self, question) -> None:
        super().__init__()
        self.question = question
        self.question_text = QuestionText(self.question)
        self.question_info = QuestionInfo(self.question)

    def compose(self) -> ComposeResult:
        #yield self.question_info
        yield self.question_text