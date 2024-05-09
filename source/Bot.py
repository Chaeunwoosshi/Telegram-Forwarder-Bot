from InquirerPy import inquirer
from pygments.formatters import terminal

from source.Telegram import Telegram
from source.model.Credentials import Credentials
from source.model.ForwardConfig import ForwardConfig
from source.utils.Console import Terminal


class Bot:
    def __init__(self):
        self.telegram = Telegram(Credentials.get(True))

    options = [
        {"name": "Add/Update Credentials", "value": "1"},
        {"name": "List Chats", "value": "2"},
        {"name": "Forward Messages", "value": "3"},
        {"name": "Exit", "value": "0"}
    ]
    console = Terminal.console

    async def start(self):
        while True:
            choice = await inquirer.select(
                message="Menu:",
                choices=Bot.options).execute_async()
            if choice == "0":
                Terminal.console.print("[bold red]Exiting...[/bold red]")
                break
            elif choice == "1":
                await self.update_credentials()

            if choice == "2":
                await self.list_chats()

            elif choice == "3":
                await self.start_forward()

            else:
                self.console.print("[bold red]Invalid choice[/bold red]")

    async def update_credentials(self):
        self.console.clear()
        self.telegram.client.disconnect()
        self.telegram = Telegram(Credentials.get(False))

    async def list_chats(self):
        self.console.clear()
        await self.telegram.list_chats()

    async def start_forward(self):
        forwardConfig = ForwardConfig()
        forwardConfig = await forwardConfig.get(True)
        forward_options = [
            {
                "name": f"Use saved settings.\n    From: {forwardConfig.sourceName} \n    To: {forwardConfig.destinationName}",
                "value": "1"},
            {"name": "New settings", "value": "2"}
        ]
        forward_choice = await inquirer.select(
            message="Forward Settings:",
            choices=forward_options
        ).execute_async()

        if forward_choice == "2":
            forwardConfig = await ForwardConfig.get(False)

        await self.telegram.start_forward(forwardConfig)
