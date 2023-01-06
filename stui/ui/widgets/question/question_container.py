from textual.containers import Container, Horizontal, Vertical
from textual.app import ComposeResult

from .question_info import *
from .question_text import QuestionText
from .question_title import QuestionTitle

class QuestionContainer(Container):

    def __init__(self, question) -> None:
        super().__init__()
        self.question = question
        self.question_text = QuestionText(self.question)
        self.question_score_info = QuestionScoreInfo(self.question)
        self.question_date_info = QuestionDateInfo(self.question)
        
    def compose(self) -> ComposeResult:
        yield self.question_text