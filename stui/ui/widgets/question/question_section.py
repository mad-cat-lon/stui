from textual.containers import Container
from textual.app import ComposeResult

from .question_container import QuestionContainer
from .question_title import QuestionTitle
from ..comment import CommentText
from ..comment import CommentContainer

class QuestionSection(Container):

    def __init__(self, question, comments=None):
        super().__init__()
        self.question = question
        self.comments = comments
        self.question_title = QuestionTitle(self.question["title"])
        self.question_container = QuestionContainer(self.question)
        self.comment_texts = [CommentText(comment) for comment in self.comments]

    def compose(self) -> ComposeResult:
        yield QuestionTitle(self.question["title"])
        yield self.question_container
        yield CommentContainer(*tuple(self.comment_texts))
        