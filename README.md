# TwitchPickUser
Simple Twitch Bot which semi-randomly picks a recent chatter from chat.

---
# Explanation
When the bot has started, it will start listening to chat messages in the channel listed in the settings.txt file. All chatters not listed in "BotAccountsToExclude" in the settings.txt file will be automatically entered into the raffle. Subscribers will have "SubscriberWeight" (again, the settings.txt file) as their weight, while non-subscribers will have "NonSubscriberWeight" as their weight. 

This allows you to impact exactly how you want the users to be picked, even allowing you to set these weights to 0 if you only want to pick between subscribers or non-subscribers.

When you want to actually pick a user, anyone with a rank listed in "RequiredRankToUseCommand" will be able to type "!pick" in Twitch Chat, and the Bot will automatically respond with the winner.

---

# Example

The console and chat output when "!pick" was typed by someone with the appropriate rank:
<pre>
<b>CubieDev was picked from 432 users</b>
</pre>

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "SubscriberWeight": 3,
    "NonSubscriberWeight": 1,
    "RequiredRankToUseCommand": [
        "broadcaster",
        "moderator",
        "subscriber"
    ],
    "BotAccountsToExclude": [
        "StreamElements",
        "MarbieBot",
        "Nightbot"
    ],
    "MaxTimeSinceLastChat": 300
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| SubscriberWeight     | The weight given to a subscriber | 3 |
| NonSubscriberWeight  | The weight given to a non-subscriber | 1 |
| RequiredRankToUseCommand | List of ranks a chatter must have to  be able to use "!pick" | ["broadcaster", "moderator", "subscriber"] |
| BotAccountsToExclude | List of (bot) accounts that the bot should not pick. | ["StreamElements", "MarbieBot", "Nightbot"] |
| MaxTimeSinceLastChat | The maximum amount of seconds since the last chat message from a user, for the user to be considered. | 300 | 

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Requirements
* [Python 3.6+](https://www.python.org/downloads/)
* [Module requirements](requirements.txt)<br>
Install these modules using `pip install -r requirements.txt`

Among these modules is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Other Twitch Bots

* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchAIDungeon](https://github.com/CubieDev/TwitchAIDungeon)
* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchCubieBotGUI](https://github.com/CubieDev/TwitchCubieBotGUI)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchRandomRecipe](https://github.com/CubieDev/TwitchRandomRecipe)
* [TwitchUrbanDictionary](https://github.com/CubieDev/TwitchUrbanDictionary)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchWeather](https://github.com/CubieDev/TwitchWeather)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchMMLevelPickerGUI](https://github.com/CubieDev/TwitchMMLevelPickerGUI) (Mario Maker 2 specific bot)
* [TwitchMMLevelQueueGUI](https://github.com/CubieDev/TwitchMMLevelQueueGUI) (Mario Maker 2 specific bot)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Meant for debugging purposes)
