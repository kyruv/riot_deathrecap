import requests
from django.conf import settings
import datetime

class PlayerGames:
    
    def __init__(self):
        self.api_key = settings.RIOT_API_KEY
        self.puuid_mapping = {}

        self.queue_map = {
            450: "ARAM",
            720: "ARAM Clash",
            440: "Ranked Flex",
            430: "Blind",
            420: "Ranked Solo",
            400: "Normal",
            700: "Clash",
            830: "Co-op vs AI",
        }
    
    def create(self, playerid, start=0):

        return self._do_request(playerid, start)
    
    def _do_request(self, playerid, start=0):
        if playerid not in self.puuid_mapping:
            split = playerid.split("-")
            if len(split) != 2:
                return None
            
            puuid_request = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{split[0]}/{split[1]}"
            detail_response = requests.get(puuid_request, headers = {"X-Riot-Token": self.api_key}).json()

            if 'puuid' not in detail_response:
                return None
            self.puuid_mapping[playerid] = detail_response['puuid']
            

        detailed_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid_mapping[playerid]}/ids?start={start}&count=10"
        matches = requests.get(detailed_request, headers = {"X-Riot-Token": self.api_key}).json()

        print(matches)
        return self._add_match_details(self.puuid_mapping[playerid], matches)

    def _add_match_details(self, puuid, matches):

        recent_match_with_details = []

        for m in matches:

            overview_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{m}"
            overview_response = requests.get(overview_request, headers = {"X-Riot-Token": self.api_key}).json()

            for participant in overview_response["info"]["participants"]:
                if participant['puuid'] == puuid:
                    recent_match_with_details.append({
                        'gameid': m,
                        'time': datetime.datetime.fromtimestamp(int(overview_response["info"]["gameStartTimestamp"]/1000)),
                        'queue': overview_response["info"]["queueId"] if overview_response["info"]["queueId"] not in self.queue_map else self.queue_map[overview_response["info"]["queueId"]],
                        'champ': participant["championName"],
                    })
        
        print(recent_match_with_details)
        return recent_match_with_details

