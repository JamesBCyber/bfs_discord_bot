import discord
import datetime


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

    @staticmethod
    def cmp_raw_content(left: discord.Message, right: discord.Message) -> bool:
        """Compare discord.Messages based on text content, file attachments, and timestamps"""
        # Exclude check if the message has no files and is only 1 word
        # helps with things like "yes" and "no" answers
        if not left.attachments and len(left.content.split(" ")) <= 5:
            return False

        if not right.attachments and len(right.content.split(" ")) <= 5:
            return False

        # Avoid preserving messages that are too old as spam potential
        if abs(right.created_at - left.created_at) > datetime.timedelta(minutes=5):
            return False

        # both files and text match
        if left.attachments == right.attachments and left.content == right.content:
            return True

        # Check if files match with an empty message text in second message (re-uploding files)
        if (
            left.attachments == right.attachments
            and not left.content
            and not right.content
        ):
            return True

        return False

    def __eq__(self, value: object) -> bool:
        if isinstance(value, MessageContent):
            return MessageContent.cmp_raw_content(
                self.original_message, value.original_message
            )

        if isinstance(value, discord.Message):
            return MessageContent.cmp_raw_content(self.original_message, value)

        return NotImplemented
