from textual.containers import Container, Vertical
from textual.app import ComposeResult

from ..comment import CommentText
from ..comment import CommentContainer
from .answer_container import AnswerContainer


class AnswerSection(Container):
    """Contains all answers to the current question"""
    def __init__(self, answer, comments=None):
        super().__init__()
        self.answer = answer
        self.answer_container = AnswerContainer(answer)
        self.comments = comments
        # Get comments associated with this answer
        self.comment_texts = [CommentText(comment) for comment in comments]
    
    def compose(self) -> ComposeResult:
        yield self.answer_container
        if len(self.comment_texts) > 0:
            yield CommentContainer(*tuple(self.comment_texts))
