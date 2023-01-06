from textual.containers import Container, Vertical
from textual.app import ComposeResult

from .question_container import QuestionContainer
from .question_title import QuestionTitle
from ..comment import CommentText
from ..comment import CommentContainer

class QuestionSection(Container):

    def __init__(self, question, comments=None):
        super().__init__(id="QuestionSection")
        self.question = question
        self.comments = comments
        self.question_title = QuestionTitle(self.question["title"])
        self.question_container = QuestionContainer(self.question)
        self.comment_texts = [CommentText(comment) for comment in self.comments]

    def compose(self) -> ComposeResult:
        yield QuestionTitle(self.question["title"])
        yield self.question_container
        if len(self.comments) > 0:
            yield Vertical(*tuple([CommentContainer(comment_text) for comment_text in self.comment_texts]))
    
    # def on_mount(self) -> ComposeResult:
    #     if len(self.comment_texts) > 0:
    #         for comment_text in self.comment_texts:
    #             self.mount(CommentContainer(comment_text))
        