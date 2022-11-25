from __future__ import annotations
from rich.align import Align
from rich.box import DOUBLE
from rich.console import RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from stackapi import StackAPI
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Header, Footer, Input, Static, Button
from textual.screen import Screen
from textual.containers import Container, Horizontal, Vertical
from textual.widget import Widget
from textual import events
from textual.reactive import reactive
from textual.message import Message, MessageTarget
from datetime import datetime 
import sys 
import html
    
class ResultBox(Widget):
    """Widget to display individual results of a query"""
    
    result: reactive[dict | None] = reactive({})
    class ResultRequest(Message):
        """Send a message back if result box is clicked"""
        def __init__(self, sender: MessageTarget, result: dict):
            self.result = result
            super().__init__(sender)
        
    def __init__(self, result: dict) -> None:
        super().__init__()
        self.result = result

    def render(self) -> ComposeResult:
        tags = self.result["tags"]
        owner_display_name = self.result["owner"]["display_name"]
        owner_link = self.result["owner"]["link"] if "link" in self.result["owner"].keys() else None
        view_count = self.result["view_count"]
        answer_count = self.result["answer_count"]
        score = self.result["score"]
        last_activity_date = self.result["last_activity_date"]
        last_activity_date_formatted = datetime.fromtimestamp(last_activity_date).strftime("%Y-%m-%d")
        creation_date = self.result["creation_date"]
        creation_date_formatted = datetime.fromtimestamp(creation_date).strftime("%Y-%m-%d")
        title = html.unescape(self.result["title"])
        render_str = f"""    [bold]{title}[/bold]
    Asked by [bold green]{owner_display_name}[/bold green] on [yellow]{creation_date_formatted}[/yellow], last active on [yellow]{last_activity_date_formatted}[/yellow]
    [yellow]{score}[/yellow] pts    [yellow]{view_count}[/yellow] views     [yellow]{answer_count}[/yellow] answers
    {tags}
        """
        return render_str
    
    async def on_click(self, event: events.Click):
        return self.emit_no_wait(self.ResultRequest(self, self.result))

    def _on_focus(self, event: events.Focus) -> None:
        return super()._on_focus(event)


class QuestionInfo(Static):

    def __init__(self, question):
        super().__init__()
        self.question = question

    def render(self) -> ComposeResult:
        render_str = ""

class CommentContainer(Static):

    def __init__(self, comment):
        super().__init__()
        self.comment = comment 
    
    def render(self) -> ComposeResult:
        render_str = self.comment["body_markdown"] 
        render_str += f" - {self.comment['owner']['display_name']}"
        return Markdown(render_str)

class QuestionContainer(Container):

    def __init__(self, question) -> None:
        super().__init__()
        self.question = question
        self.generate_question_box()
        self.generate_question_info()

    def generate_question_box(self) -> None:
        self.question_box = QuestionBox(self.question)

    def generate_question_info(self) -> None:
        self.question_info = QuestionInfo(self.question)

    def compose(self) -> ComposeResult:
        yield self.question_box
#        yield self.question_info

class QuestionSection(Container):

    def __init__(self, question, comments=None):
        super().__init__()
        self.question = question
        self.comments = comments
        self.generate_question_container()
        self.generate_comment_containers()
    
    def generate_question_container(self):
        self.question_container = QuestionContainer(self.question)
    
    def generate_comment_containers(self):
        self.comment_boxes = [CommentContainer(comment) for comment in self.comments]

    def compose(self) -> ComposeResult:
        yield self.question_container
        yield Container(*tuple(self.comment_boxes))
        

class AnswerContainer(Container):

    def __init__(self, answer, comments=None):
        super().__init__()
        self.answer = answer
        self.comments = comments
    
    def compose(self) -> ComposeResult:
        # TODO: Answer container should have rendered answer along with comments
        pass 

class SearchBox(Static):

    def on_input_submitted(self, event: Input.Submitted):
        results = self.app.stackAPI.fetch("search/advanced", q=event.value)
        self.app.show_results(results, event.value)

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter your search term here: ")


class AnsiArt(Static):
    
    def __init__(self, ansi_art):
        self.ansi_art = ansi_art
        super().__init__()
    
    def render(self) -> ComposeResult:
        return self.ansi_art

class FilterMenu(Horizontal):

    class FilterRequest(Message):
        """Message object to be passed back to ResultScreen when a filter is selected"""
        def __init__(self, sender: MessageTarget, filter: str):
            self.filter = filter
            super().__init__(sender)

    def compose(self) -> ComposeResult:
        yield Button(label="Newest", name="filter_newest")
        yield Button(label="Active", name="filter_active")
        yield Button(label="Most answers", name="filter_most_answers")
        yield Button(label="Unanswered", name="filter_unanswered")
        yield Button(label="Highest score", name="filter_highest_score")
   
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        await self.emit(self.FilterRequest(self, event.button.name))

class SearchScreen(Screen):

    BINDINGS = [("escape", "app.pop_screen", "Remove current screen")]
    
    def compose(self) -> ComposeResult:
        ansi_art = """
 ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗      ██████╗ ██╗    ██╗
██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║     ██╔═══██╗██║    ██║
██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║     ██║   ██║██║ █╗ ██║
██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══╝  ██║     ██║   ██║██║███╗██║
╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██║     ███████╗╚██████╔╝╚███╔███╔╝
╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ 
        """
        yield Header()
        yield AnsiArt(ansi_art)
        yield SearchBox()
        yield Footer()  

class ResultScreen(Screen):
    """Display results of a query with a FilterMenu"""

    BINDINGS = [("escape", "app.pop_screen", "Remove result screen")]
    result_boxes = reactive([])

    def __init__(self, results):
        super().__init__(name="result")
        self.raw_results = results
        self.generate_result_boxes()
            
    def generate_result_boxes(self, to_filter=None) -> None:
        """Generates ResultBox instances from the raw json passed to ResultScreen"""
        if to_filter is None:
            if len(self.raw_results) < 50:
                self.result_boxes = [ResultBox(self.raw_results[i]) for i in range(len(self.raw_results))]
                return
            else:
                self.result_boxes = [ResultBox(self.raw_results[i]) for i in range(0, 50)]
                return
        else:
            if len(to_filter) < 50:
                self.result_boxes = [ResultBox(to_filter[i]) for i in range(len(to_filter))]
                return
            else:
                self.result_boxes = [ResultBox(to_filter[i]) for i in range(0, 50)]
                return 

    def filter_newest(self) -> None:
        """Filters raw results by most recently created"""
        filtered_newest = sorted(self.raw_results, key=lambda result: result["creation_date"], reverse=True)
        for index, result_box in enumerate(self.query(ResultBox)):
            result_box.result = filtered_newest[index]

    def filter_active(self) -> None:
        """Filters raw results by most recently active"""
        filtered_active = sorted(self.raw_results, key=lambda result: result["last_activity_date"], reverse=True)
        for index, result_box in enumerate(self.query(ResultBox)):
            result_box.result = filtered_active[index]

    def filter_highest_score(self) -> None:
        """Filters raw results by highest score"""
        filtered_highest_score = sorted(self.raw_results, key=lambda result: result["score"], reverse=True)
        for index, result_box in enumerate(self.query(ResultBox)):
            result_box.result = filtered_highest_score[index]
    
    def filter_unanswered(self) -> None:
        """Filters raw results by unanswered"""
        filtered_unanswered = sorted(self.raw_results, key=lambda result: result["answer_count"])
        for index, result_box in enumerate(self.query(ResultBox)):
            result_box.result = filtered_unanswered[index]

    def filter_most_answers(self) -> None:
        """Filters raw results by most answers"""
        filtered_most_answers = sorted(self.raw_results, key=lambda result: result["answer_count"], reverse=True)
        for index, result_box in enumerate(self.query(ResultBox)):
            result_box.result = filtered_most_answers[index]

    def on_filter_menu_filter_request(self, message: FilterMenu.FilterRequest) -> None:
        """Handles the FilterRequest event when a filtering button is clicked"""
        if message.filter == "filter_active":
            self.filter_active()
        elif message.filter == "filter_newest":
            self.filter_newest()
        elif message.filter == "filter_highest_score":
            self.filter_highest_score()
        elif message.filter == "filter_unanswered":
            self.filter_unanswered()
        elif message.filter == "filter_most_answers":
            self.filter_most_answers()

    def on_result_box_result_request(self, message: ResultBox.ResultRequest) -> None:
        self.app.show_question(message.result)

    def compose(self) -> ComposeResult:
        yield FilterMenu()
        yield Container(*tuple(self.result_boxes))
        yield Footer()

class QuestionScreen(Screen):

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

class Client(App):
    """Main browsing client interface"""

    CSS_PATH = "main.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("e", "exit", "Exit browser"),
        ("s", "push_screen('search')", "Search page")
        ]
    SCREENS = {
        "search": SearchScreen(name="search")
    }
    query = ""
    
    def set_stackAPI(self, stackAPI) -> None:
        """ Sets stackAPI object"""
        self.stackAPI = stackAPI

    def compose(self) -> ComposeResult:
        """Creating child widgets"""
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen("search")

    def show_results(self, results, query) -> None:
        if self.query == "":
            self.query = query
            self.results = results["items"]
            result_screen = ResultScreen(self.results)
            self.install_screen(result_screen, name=f"result-{query}")
            self.SCREENS[f"result-{query}"] = result_screen
            self.push_screen(self.SCREENS[f"result-{query}"])
            return 
        elif self.query != "" and self.query != query:
            self.results = results["items"]
            result_screen = ResultScreen(self.results)
            if f"result-{query}" in self.SCREENS.keys():
                self.push_screen(self.SCREENS[f"result-{query}"])
            else:
                self.install_screen(result_screen, name=f"result-{query}")
                self.SCREENS[f"result-{query}"] = result_screen
                self.push_screen(self.SCREENS[f"result-{query}"])
            return
        elif self.query == query:
            self.push_screen(self.SCREENS[f"result-{query}"])
            return 

    def show_question(self, result) -> None:
        question_id = result["question_id"]
        if question_id not in self.SCREENS.keys():
            question_screen = QuestionScreen(question_id) 
            self.install_screen(question_screen, name=str(question_id))
            self.SCREENS[question_id] = question_screen
            self.push_screen(self.SCREENS[question_id])
        else:
            self.push_screen(self.SCREENS[question_id])

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark 

    def action_exit(self) -> None:
        exit() 

if __name__ == "__main__":
    stackAPI = StackAPI('stackoverflow', key="9XXRaYFBeJ*32qbNBYZRTA((")
    stackAPI.max_pages = 1 
    stackAPI.page_size = 100
    app = Client()
    app.set_stackAPI(stackAPI)
    app.run()