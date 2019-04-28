
from TwitchWebsocket import TwitchWebsocket
import random, time, json

class Settings:
    def __init__(self, bot):
        try:
            # Try to load the file using json.
            # And pass the data to the GoogleTranslate class instance if this succeeds.
            with open("settings.txt", "r") as f:
                settings = f.read()
                data = json.loads(settings)
                bot.setSettings(data['Host'],
                                data['Port'],
                                data['Channel'],
                                data['Nickname'],
                                data['Authentication'],
                                data['SubscriberWeight'],
                                data['NonSubscriberWeight'],
                                data['RequiredRankToUseCommand'],
                                data["BotAccountsToExclude"],
                                data["MaxTimeSinceLastChat"]
                                )
        except ValueError:
            raise ValueError("Error in settings file.")
        except FileNotFoundError:
            # If the file is missing, create a standardised settings.txt file
            # With all parameters required.
            with open('settings.txt', 'w') as f:
                standard_dict = {
                                    "Host": "irc.chat.twitch.tv",
                                    "Port": 6667,
                                    "Channel": "#<channel>",
                                    "Nickname": "<name>",
                                    "Authentication": "oauth:<auth>",
                                    "SubscriberWeight": 3,
                                    "NonSubscriberWeight": 1,
                                    "RequiredRankToUseCommand": ["broadcaster", "moderator", "subscriber"],
                                    "BotAccountsToExclude": ["StreamElements", "MarbieBot", "Nightbot"],
                                    "MaxTimeSinceLastChat": 300
                                }
                f.write(json.dumps(standard_dict, indent=4, separators=(',', ': ')))
                raise ValueError("Please fix your settings.txt file that was just generated.")

class Chatter:
    # Simple data structure to store weight and time of a user who chatted.
    def __init__(self, weight, t):
        self.weight = weight
        self.t = t

class VoteBot:
    def __init__(self):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.sub_weight = None
        self.reg_weight = None
        self.req_ranks = None
        self.accounts_to_exclude = None
        self.timeout = None
        
        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        self.chatters = {}
        self.t_reset = round(time.time())

        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=["membership", "tags", "commands"],
                                  live=True)
        self.ws.start_bot()

    def setSettings(self, host, port, chan, nick, auth, sub_weight, reg_weight, req_ranks, accounts_to_exclude, timeout):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth
        self.sub_weight = sub_weight
        self.reg_weight = reg_weight
        self.req_ranks = req_ranks
        self.accounts_to_exclude = [a.lower() for a in accounts_to_exclude]
        self.timeout = timeout

    def weighted_choice(self):
        # Randomly choose r as an int between 0 and the total amount of weight total
        total = sum(self.chatters[key].weight for key in self.chatters)
        r = random.randint(0, total)
        
        # Continuously reduce r by the weight while looping through all chatters, 
        # until it would have resulted in a negative (or zero) r.
        # When this happens, return the name of the user that won.
        for key in self.chatters:
            if self.chatters[key].weight >= r:
                return key
            r -= self.chatters[key].weight

    def message_handler(self, m):
        if m.type == "PRIVMSG":
            # Update chatters either by updating the time, or adding the new chatter.
            if m.user not in self.accounts_to_exclude:
                if m.tags["display-name"] not in self.chatters:
                    if "subscriber" in m.tags['badges']:
                        if self.sub_weight != 0:
                            self.chatters[m.tags["display-name"]] = Chatter(self.sub_weight, round(time.time()))
                    else:
                        if self.reg_weight != 0:
                            self.chatters[m.tags["display-name"]] = Chatter(self.reg_weight, round(time.time()))
                else:
                    # Note that I don't update the weight of an existing member, 
                    # meaning that if this bot was to be run for long periods of times
                    # it would likely get incorrectly label users. 
                    # This can be fixed by uncommenting the line below:
                    #self.chatters[m.tags["display-name"]].weight = self.sub_weight if "subscriber" in m.tags['badges'] else self.reg_weight
                    self.chatters[m.tags["display-name"]].t = round(time.time())
            
            if time.time() - self.t_reset > self.timeout:
                # Whenever its been over self.timeout seconds since the last reset, 
                # reset all chatters (aka purge chatters from the list that haven't chatted in the previous self.timeout seconds)
                b = len(self.chatters)
                self.reset_chatters()
                print(f"Purged {b - len(self.chatters)} users from the potential vote, leaving {len(self.chatters)} eligible users.")
                self.t_reset = round(time.time())

            # Check for commands
            if m.message.startswith("!pick") and self.allowed_chatter(m.tags["badges"]):
                # Make sure all chatters in self.chatters have chatted in the last self.timeout seconds
                self.reset_chatters()
                # Pick a winner and broadcast them.
                winner = self.weighted_choice()
                print(f"{winner} was picked from {len(self.chatters)} users.")
                self.ws.send_message(f"{winner} was picked from {len(self.chatters)} users.")
    
    def allowed_chatter(self, badges):
        # Check if user is allowed to use the !pick command.
        for ranks in self.req_ranks:
            if ranks in badges:
                return True
        return False

    def reset_chatters(self):
        # Remove all elements from the dict where the previous message was more than self.timeout seconds ago.
        self.chatters = {key: self.chatters[key] for key in self.chatters if time.time() - self.chatters[key].t < self.timeout}

if __name__ == "__main__":
    VoteBot()
