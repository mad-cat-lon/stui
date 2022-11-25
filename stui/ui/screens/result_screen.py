from textual.screen import Screen
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import Container
from textual.widgets import Footer

from ..widgets.result import ResultContainer, ResultInfo, ResultBox, FilterMenu

class ResultScreen(Screen):
    """Display results of a query with a FilterMenu"""

    BINDINGS = [("escape", "app.pop_screen", "Remove result screen")]
    result_containers = reactive([])

    def __init__(self, results):
        super().__init__(name="result")
        self.raw_results = results
        self.generate_result_containers()
            
    def generate_result_containers(self, to_filter=None) -> None:
        """Generates ResultContainer instances from the raw json passed to ResultScreen"""
        if to_filter is None:
            if len(self.raw_results) < 50:
                self.result_containers = [ResultContainer(self.raw_results[i]) for i in range(len(self.raw_results))]
                return
            else:
                self.result_containers = [ResultContainer(self.raw_results[i]) for i in range(0, 50)]
                return
        else:
            if len(to_filter) < 50:
                self.result_containers = [ResultContainer(to_filter[i]) for i in range(len(to_filter))]
                return
            else:
                self.result_containers = [ResultContainer(to_filter[i]) for i in range(0, 50)]
                return 

    def filter_newest(self) -> None:
        """Filters raw results by most recently created"""
        filtered_newest = sorted(self.raw_results, key=lambda result: result["creation_date"], reverse=True)
        for index, result_container in enumerate(self.query(ResultContainer)):
            result_container.result_box.result = filtered_newest[index]
            result_container.result_info.result = filtered_newest[index]

    def filter_active(self) -> None:
        """Filters raw results by most recently active"""
        filtered_active = sorted(self.raw_results, key=lambda result: result["last_activity_date"], reverse=True)
        for index, result_container in enumerate(self.query(ResultContainer)):
            result_container.result_box.result = filtered_active[index]
            result_container.result_info.result = filtered_active[index]

    def filter_highest_score(self) -> None:
        """Filters raw results by highest score"""
        filtered_highest_score = sorted(self.raw_results, key=lambda result: result["score"], reverse=True)
        for index, result_container in enumerate(self.query(ResultContainer)):
            result_container.result_box.result = filtered_highest_score[index]
            result_container.result_info.result = filtered_highest_score[index]  

    def filter_unanswered(self) -> None:
        """Filters raw results by unanswered"""
        filtered_unanswered = sorted(self.raw_results, key=lambda result: result["answer_count"])
        for index, result_container in enumerate(self.query(ResultContainer)):
            result_container.result_box.result = filtered_unanswered[index]
            result_container.result_info.result = filtered_unanswered[index]
            
    def filter_most_answers(self) -> None:
        """Filters raw results by most answers"""
        filtered_most_answers = sorted(self.raw_results, key=lambda result: result["answer_count"], reverse=True)
        for index, result_container in enumerate(self.query(ResultContainer)):
            result_container.result_box.result = filtered_most_answers[index]
            result_container.result_info.result = filtered_most_answers[index]

    def on_filter_menu_filter_request(self, message: FilterMenu.FilterRequest) -> None:
        """Handles the FilterRequest event when a filter button is clicked"""
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

    def on_result_container_result_click(self, message: ResultContainer.ResultClick) -> None:
        self.app.show_question(message.result)

    def compose(self) -> ComposeResult:
        yield FilterMenu()
        yield Container(*tuple(self.result_containers))
        yield Footer()