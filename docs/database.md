# Memory
Some of the things stored in the bot are ephemeral data stored in memory and are lost between reboots. These are things that are volatile, short lived, or expected to be overwritten such as caches

## Message Cache
The UserMessageCache in db/memory.py is used to hold a short history of message data to check short term message patterns, primarily focused on Spam detection and prevention

The UserMessageCache stores message data in the MessageContent class format for simpler equality checks with a smaller memory footprint

Below is a basic use of the cache for checking if a message is being spammed
```py
    async def on_message(self, message: Message):
        if not isinstance(message.author, Member):
            return
        is_spam = self.message_cache.check_spam(message)
        if is_spam:
            await message.author.timeout_for(datetime.timedelta(hours=1), reason="Spam")

```

