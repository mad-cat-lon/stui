from textual.app import App, ComposeResult
from ..ui.screens import *
from textual.widgets import *
from stackapi import StackAPI

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