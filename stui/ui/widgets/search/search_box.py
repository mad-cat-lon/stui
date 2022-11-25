from textual.widgets import Static, Input
from textual.app import ComposeResult

class SearchBox(Static):

    def on_input_submitted(self, event: Input.Submitted):
        results = self.app.stackAPI.fetch("search/advanced", q=event.value)
        self.app.show_results(results, event.value)

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter your search term here: ")
