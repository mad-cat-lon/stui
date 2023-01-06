
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container, Vertical

from ..widgets.question import QuestionSection
from ..widgets.answer import AnswerSection
from ..widgets.answer import AnswerContainer

class QuestionScreen(Screen):

    """Displays a selected question with comments and answers"""
    BINDINGS = [("escape", "app.pop_screen", "Back to results page")]
    def __init__(self, question_id) -> None:
        self.question_id = question_id
        super().__init__(name="question")
        self.get_question()
        self.get_question_comments()
        self.get_question_answers()
        self.get_answers_comments()

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

    def get_question_answers(self) -> None:
        self.question_answers = self.app.stackAPI.fetch(
            "questions/{ids}/answers",
            ids=[self.question_id],
            filter="*_u5VrDMFZBa"
        )["items"]

    def get_answers_comments(self) -> None:
        self.answers_comments = {}
        for answer in self.question_answers:
            answer_id = answer["answer_id"]
            answer_comments = self.app.stackAPI.fetch(
                "answers/{ids}/comments",
                ids=[answer_id],
                filter="7W_5HvYg2"
            )["items"]
            self.answers_comments[answer_id] = answer_comments         

    def compose(self) -> ComposeResult:
        yield Header()
        yield QuestionSection(
            self.question,
            self.question_comments
        )
        #yield Container(*tuple(AnswerContainer(answer) for answer in self.question_answers))
        yield Footer()
    
    def on_mount(self) -> None:
        if self.question_answers != 0:
            for answer in self.question_answers:
                self.mount(AnswerContainer(
                    answer,
                    self.answers_comments[answer["answer_id"]]
                ))