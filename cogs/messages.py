from ..models import Message

class MessagesCog:
    def __init__(self, client):
        self.client = client

    async def on_message(self, message: Message):
        if message.text.startswith("/"):
            await self.handle_command(message)

    async def handle_command(self, message: Message):
        command, *args = message.text[1:].split()
        if command == "ping":
            await self.client.send_message(message.sender.pk, "Pong!")