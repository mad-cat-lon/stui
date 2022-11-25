
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer

from ..widgets.question import QuestionSection

class QuestionScreen(Screen):
    """Displays a selected question with comments and answers"""
    BINDINGS = [("escape", "app.pop_screen", "Back to results page")]
    def __init__(self, question_id) -> None:
        self.question_id = question_id
        super().__init__(name="question")
        self.get_question()
        self.get_question_comments()

    def get_question(self) -> None:
        self.question = self.app.stackAPI.fetch(
            "questions",
            ids=[self.question_id],
            filter="XSD-19EdRLI7S-XpO)HNviPdtonNZlt"
        )["items"][0]

    def get_question_comments(self) -> None:
        self.question_comments = self.app.stackAPI.fetch(
            "questions/{ids}/comments",
            ids=[self.question_id],
            filter="7W_5HvYg2"
        )["items"]

    def compose(self) -> ComposeResult:
        yield Header()
        yield QuestionSection(self.question, self.question_comments)
        yield Footer()