from textual.widgets import Static
from textual.app import ComposeResult
from rich.markdown import Markdown

# TODO: Standardize this to be more similar to the following:
# Section -> Container -> Text/Info
# Also, this is not actually a container
class CommentText(Static):
    def __init__(self, comment):
        super().__init__()
        self.comment = comment 
    
    def render(self) -> ComposeResult:
        render_str = self.comment["body_markdown"] 
        render_str += f" - {self.comment['owner']['display_name']}"
        return Markdown(render_str)
