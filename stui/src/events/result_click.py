from textual.message import Message, MessageTarget
from textual import events

class ResultClick(Message):
    """
    Sends a message to the app to display the targeted
    result if it is clicked
    """
    def __init__(self, sender: MessageTarget, result: dict):
        self.result = result
        super().__init__(sender)