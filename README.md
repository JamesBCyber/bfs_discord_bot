# Discord Bot
Lorem ipsum

# TODO
Add timestamps to message tracking to ensure "spam" doesnt count 3 messages of "okay" in 15 minutes

Add FAQ detection
- Fuzzy match message content with an 85% confidence 
- Setup rules so multiple inputs can have a predefined response
- Send replies in embed, may have edits for color of embed
- Use a reaction to remove the FAQ response if message is undesired

Add Settings (diff from env) with write-through-cache
- Modifiable Server Settings
- Setting up channel rules
- Adding blacklisted words or phrases
- Adding FAQ responses on the fly


# Running
setup the .env file with basic configurations

At the moment the only thing required is a valid discord bot token

# Key Features
Most of the features for this bot are based on the goals of the Ben's Fintastic Sharks Team

## Bot Spam / Compromised Accounts
### UserMessageCache
Clears every hour
Stores a default of 10 messages per user
check_spam -> bool
remove_duplicate_messages -> deletes messages registered in cache that match the given message content

### Bot.on_message()
timeout spamming users for 2 weeks

## Automatic Responses to FAQ
fuzzy find messages

/faq
ephem embed with common / registered faq

## Link to Outside Platforms
- Youtube
  - uses the googleapi for youtube to validate the channel exists, and registers it to be tracked with it checking for new video updates every 20 minutes
- Instagram
- X / Twitter
- TikTok

## Display Welcome / Goodbye Message
allow registering/removing multiple messages to add variety 


## Help Menu
- Moderation
- QoL
- mod info
  - list of staff/dev
  - mod pages
  - socials
- how to contrib

