from textual.containers import Container, Vertical
from textual.app import ComposeResult

from .answer_text import AnswerText
from ..comment import CommentText
from ..comment import CommentContainer

class AnswerContainer(Container):

    def __init__(self, answer, comments) -> None:
        self.answer = answer
        self.answer_text = AnswerText(self.answer)
        self.comments = comments
        self.comment_texts = [CommentText(comment) for comment in self.comments]
        self.accepted = self.answer["is_accepted"]
        if self.accepted == False:
            super().__init__(id="AnswerContainer")
        else:
            super().__init__(id="AnswerContainer", classes="accepted")

    def compose(self) -> ComposeResult:
        yield self.answer_text
        if len(self.comments) > 0:
            yield Vertical(
                *tuple([CommentContainer(comment_text) for comment_text in self.comment_texts])
            )