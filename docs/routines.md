# Routines
Scheduled async tasks 


## Cache
To avoid holding too much memory, cache should be cleared in a routine

The UserMessageCache used for spam detection is dumped every hour, and uses the created_at timestamp to check for a 20 min delta, if larger, then the message is cleared from the cache, if all user messages got cleared, remove the user as a key in the Cache's hashmap

## Media Updates
Media updates use polling to fetch the most recent video every 20 minutes, sweeping through the platforms and channels, then using a set of guilds which are tracking the channel, and pushing an update to each guild's media channel
