from logging import warn

import discord
from discord import Member, Message
from .db.database import database
from .views.persistant_views import TestView
from .modules.spam.user_cache import UserMessageCache
from .db.media_tracker import SocialMediaTracker
from .db.greetings import GreetingsManager
import datetime


class Bot(discord.Bot):
    """Discord Bot used for Events"""

    message_cache: UserMessageCache
    media_tracker: SocialMediaTracker
    greetings_manager: GreetingsManager

    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)
        self.database = database
        self.message_cache = UserMessageCache()
        self.media_tracker = SocialMediaTracker()
        self.greetings_manager = GreetingsManager()

    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

        self.add_view(TestView())

    async def on_message(self, message: Message):
        """Message Event, checks if author is Member to track only server messages, not private chats"""
        if not isinstance(message.author, Member):
            return
        if self.message_cache.check_spam(message):
            await message.author.timeout_for(datetime.timedelta(weeks=2), reason="Spam")
            await self.message_cache.remove_duplicate_messages(message)

    async def on_member_join(self, member: Member):
        """Triggered when Member joins a server"""
        print("Triggered Join Event")
        print(member)
        print(dir(member))

    async def on_member_remove(self, member: Member):
        """Triggered when Member leaves or is removed from a server"""
        print("Triggered Remove Event")
        print(member)
        print(dir(member))
