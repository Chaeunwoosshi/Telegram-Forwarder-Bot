from source.menu.AccountSelector import AccountSelector
from source.menu.MainMenu import MainMenu

class Bot:
    def __init__(self, api_id, api_hash, bot_token):
        # Pass the credentials to the AccountSelector
        self.account_selector = AccountSelector(api_id, api_hash, bot_token)
        self.main_menu = None

    async def start(self):
        try:
            # Select the account with the provided credentials
            telegram = await self.account_selector.select_account()
            self.main_menu = MainMenu(telegram)
            await self.main_menu.start()
        except Exception as err:
            raise err

