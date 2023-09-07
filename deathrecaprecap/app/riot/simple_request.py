import requests

class DeathData:

    


    def __init__(self):
        self.api_key = "RGAPI-e095cb6e-a409-4755-8b65-f001e9ba48c7"
        

    def create(self, gameid):
        return self.only_important_data(self.get_match_data(gameid))

    def only_important_data(self, responses):
        detail_response = responses[0]
        overview_response = responses[1]

        id_map = {}
        champ_map = {}
        for participant in overview_response["info"]["participants"]:
            id_map[participant["participantId"]] = participant["championName"]
            champ_map[participant["championName"]] = {
                "team": participant["teamId"],
                "summoner": participant["summonerName"]
            }

        deaths = []
        
        for f in detail_response["info"]["frames"]:
            for event in f["events"]:
                if event["type"] == "CHAMPION_KILL":

                    killers = {}
                    for damagesource in event["victimDamageDealt"]:
                        if damagesource["name"] not in killers:
                            killers[damagesource["name"]] = {
                                "who": damagesource["name"],
                                "physical": 0,
                                "magic": 0,
                                "true": 0,
                                "aa": 0,
                                "q": 0,
                                "w": 0,
                                "e": 0,
                                "r": 0,
                                "other": 0,
                            }




                        



                    deaths.append({
                        "timestamp": event["timestamp"],
                        "who": champ_map[event["victimId"]],
                        "killers": killers
                    })



    def get_match_data(self, match):
        detailed_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}/timeline"
        detail_response = requests.get(detailed_request, headers = {"X-Riot-Token": self.api_key}).json()

        overview_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}"
        overview_response = requests.get(overview_request, headers = {"X-Riot-Token": self.api_key}).json()

        return detail_response, overview_response

    
