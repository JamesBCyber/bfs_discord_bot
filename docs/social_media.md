# Social Media
Social Media channels can be registered for tracking so that new video uploads can be announced automatically

All media classes should inherit from the SocialMedia class from media_impl.py in order to allow generic calls to standardized functions, specifically the get_newest() method which returns the str url of the video or None 

## Youtube
src/bfs_discord_bot/modules/youtube.py has the YoutubeMedia class which tracks the channel handle and the most recent video id in order to prevent double posting

It is built off the googleapi code and the google-api-python-client library

## Instagram
TODO

## X / Twitter
TODO

## TikTok
TODO
