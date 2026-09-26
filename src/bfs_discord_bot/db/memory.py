import discord


class UserMessageCache:
    """Short history cache for saved user messages
    reset within a scheduled task to clear cache and empty user list to save memory"""

    user_messages: dict[discord.Member | discord.User, list[MessageContent]]
    max_history: int

    def __init__(self, history: int = 10) -> None:
        self.user_messages = {}
        self.max_history = history

    def reset(self) -> None:
        """Clear cache to save memory"""
        self.user_messages = {}

    def check_spam(self, message: discord.Message):
        """Returns True if there are 3 duplicates within the last few messages in the cache"""
        msg = MessageContent(message)
        messages = self.user_messages.get(message.author, None)

        if messages is None:
            self.user_messages[message.author] = []
            messages = self.user_messages[message.author]

        dups = messages.count(msg)
        messages.append(msg)

        if len(messages) > self.max_history:
            messages.pop(0)

        return dups >= 3

    async def remove_duplicate_messages(self, spam: discord.Message):
        """Use the given bot to delete all messages that match the target message content"""
        messages = self.user_messages.get(spam.author, None)
        if messages is None:
            return

        spam_content = MessageContent(spam)
        for message in messages:
            if message == spam_content:
                await message.original_message.delete()


class MessageContent:
    """Simplified Message data for easy equality checks"""

    original_message: discord.Message

    def __init__(self, message: discord.Message) -> None:
        self.original_message = message

    def __eq__(self, value: object) -> bool:
        if isinstance(value, MessageContent):
            if self.original_message.attachments == value.original_message.attachments:
                return True
            return self.original_message.content == value.original_message.content

        if isinstance(value, discord.Message):
            if self.original_message.attachments == value.attachments:
                return True
            return self.original_message.content == value.content

        return NotImplemented
