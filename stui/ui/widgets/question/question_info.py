from textual.widgets import Static
from textual.app import ComposeResult
from datetime import datetime

class QuestionScoreInfo(Static):

    def __init__(self, question):
        super().__init__()
        self.question = question

    def render(self) -> ComposeResult:
        score_sym = "votes"
        score_val = f"[bold yellow]{self.question['score']}[/bold yellow]"
        render_str = f"{score_val} {score_sym}"
        return render_str

class QuestionDateInfo(Static):
    
    def __init__(self, question):
        super().__init__()
        self.question = question
    
    def render(self) -> ComposeResult:
        last_activity_date = self.question["last_activity_date"]
        last_activity_date_formatted = datetime.fromtimestamp(last_activity_date).strftime("%Y-%m-%d")
        creation_date = self.question["creation_date"]
        creation_date_formatted = datetime.fromtimestamp(creation_date).strftime("%Y-%m-%d")
        render_str = f"Asked on [bold green]{creation_date_formatted}[/bold green]\nLast activity on [bold green]{last_activity_date_formatted}[/bold green]"
        return render_str
