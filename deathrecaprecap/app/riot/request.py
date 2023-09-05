import requests

class DeathData:

    def __init__(self):
        self.api_key = "RGAPI-2f805baf-cc5f-465d-a387-757517fe4b88"

    def create(self, gameid):
        all_death_data = self.condense_damage_sources(self.get_champion_kill_data(self.get_match_data(gameid)))
        return self.make_overview_data(all_death_data)


    def get_match_data(self, match):
        detailed_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}/timeline"
        detail_response = requests.get(detailed_request, headers = {"X-Riot-Token": self.api_key}).json()

        overview_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}"
        overview_response = requests.get(overview_request, headers = {"X-Riot-Token": self.api_key}).json()

        id_map = {}
        champ_map = {}
        for participant in overview_response["info"]["participants"]:
            id_map[participant["participantId"]] = participant["championName"]
            champ_map[participant["championName"]] = {
                "team": participant["teamId"],
                "summoner": participant["summonerName"]
            }

        return {
            "mapping": id_map,
            "champ_map": champ_map,
            "timeline": detail_response
        }

    def get_champion_kill_data(self, data):
        champ_kill_data = []

        for f in data["timeline"]["info"]["frames"]:
            for event in f["events"]:
                if event["type"] == "CHAMPION_KILL":
                    champ_kill_data.append({
                        "timestamp": event["timestamp"],
                        "victim": data["mapping"][event["victimId"]],
                        "damage_sources": event["victimDamageReceived"]
                    })
        
        return {
            "death_data": champ_kill_data,
            "champ_map": data["champ_map"]
        }


    def condense_damage_sources(self, data):
        death_data = data["death_data"]
        champ_map = data["champ_map"]

        condensed_death_data = []

        total_damage_team_100 = 0
        total_damage_team_200 = 0

        for death in death_data:
            condensed_death_data.append({})
            condensed_death_data[-1]["timestamp"] = death["timestamp"]
            condensed_death_data[-1]["victim"] = death["victim"]

            killers = {}

            for source in death['damage_sources']:
                if source['type'] != "OTHER":
                    continue

                k = source['name']

                # set up empty data if not present before
                if k not in killers:
                    killers[k] = {
                        'total': 0,
                        'physical': 0,
                        'magic': 0,
                        'true': 0,
                    }
                
                killers[k]['physical'] += source['physicalDamage']
                killers[k]['magic'] += source['magicDamage']
                killers[k]['true'] += source['trueDamage']
                total_damage = (source['physicalDamage'] + source['magicDamage'] + source['trueDamage'])
                killers[k]['total'] += total_damage

                if champ_map[death['victim']]['team'] == 200:
                    total_damage_team_100 += total_damage
                else:
                    total_damage_team_200 += total_damage
            
            condensed_death_data[-1]["killers"] = killers
        
        game_level_overview = {}


        return {
        "death_data": condensed_death_data,
        "game_participants": data["champ_map"]
        }



    def make_overview_data(self, data):
        all_deaths = data["death_data"]
        game_participants = data["game_participants"]
        overview_data = {}

        team_100_participants = []
        team_200_participants = []

        for name, details in game_participants.items():
            if details['team'] == 100:
                team_100_participants.append(name)
            else:
                team_200_participants.append(name)
        
        for champ in team_100_participants:
            overview_data[champ] = {
                'as_killer': {},
                'as_victim': {},
            }
            overview_data[champ]['as_killer']['aggregate'] = {
                'total': 0,
                'physical': 0,
                'magic': 0,
                'true': 0,
                'takedowns': 0,
            }

            for opponent in team_200_participants:
                overview_data[champ]['as_killer'][opponent] = {
                    'total': 0,
                    'physical': 0,
                    'magic': 0,
                    'true': 0,
                    'takedowns': 0,
                }
                overview_data[champ]['as_victim'][opponent] = {
                    'total': 0,
                    'physical': 0,
                    'magic': 0,
                    'true': 0,
                    'takedowns': 0,
                }
        
        for champ in team_200_participants:
            overview_data[champ] = {
                'as_killer': {},
                'as_victim': {},
            }
            overview_data[champ]['as_killer']['aggregate'] = {
                'total': 0,
                'physical': 0,
                'magic': 0,
                'true': 0,
                'takedowns': 0,
            }

            for opponent in team_100_participants:
                overview_data[champ]['as_killer'][opponent] = {
                    'total': 0,
                    'physical': 0,
                    'magic': 0,
                    'true': 0,
                    'takedowns': 0,
                }
                overview_data[champ]['as_victim'][opponent] = {
                    'total': 0,
                    'physical': 0,
                    'magic': 0,
                    'true': 0,
                    'takedowns': 0,
                }
            
            
        
        
        for death in all_deaths:
            victim = death['victim']

            for killer in death['killers']:
                tot_d = death['killers'][killer]['total']
                phys_d = death['killers'][killer]['physical']
                mag_d = death['killers'][killer]['magic']
                true_d = death['killers'][killer]['true']

                overview_data[victim]['as_victim'][killer]['total'] += tot_d
                overview_data[victim]['as_victim'][killer]['physical'] += phys_d
                overview_data[victim]['as_victim'][killer]['magic'] += mag_d
                overview_data[victim]['as_victim'][killer]['true'] += true_d
                overview_data[victim]['as_victim'][killer]['takedowns'] += 1

                overview_data[killer]['as_killer'][victim]['total'] += tot_d
                overview_data[killer]['as_killer'][victim]['physical'] += phys_d
                overview_data[killer]['as_killer'][victim]['magic'] += mag_d
                overview_data[killer]['as_killer'][victim]['true'] += true_d
                overview_data[killer]['as_killer'][victim]['takedowns'] += 1

                overview_data[killer]['as_killer']['aggregate']['total'] += tot_d
                overview_data[killer]['as_killer']['aggregate']['physical'] += phys_d
                overview_data[killer]['as_killer']['aggregate']['magic'] += mag_d
                overview_data[killer]['as_killer']['aggregate']['true'] += true_d
                overview_data[killer]['as_killer']['aggregate']['takedowns'] += 1
        
        listified = []
        for key, val in overview_data.items():
            val["name"] = key
            listified.append(val)
        
        return listified
