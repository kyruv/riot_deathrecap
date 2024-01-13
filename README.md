# riot_deathrecap

https://relyk3.pythonanywhere.com/

This is a for-fun project using the riot games api to visualize damage done that contributed to deaths.

1. Get the match id from https://www.leagueofgraphs.com/match/na/4764831104 searching up your recent games. Copy paste it from the end of the URL, formatting like NA1_4764831104. Hit submit. Alternatively hit copy match id button from the post game lobby.
2. Click on the bars to switch between physical/magic/true breakdown and aa/q/w/e/r/other breakdown (NPC breaks down tower/minion/monster)
3. Hover over bars to get actual number or what riot classified the damage as if it was other
4. Click on specific deaths in the timeline on the bottom to just highlight that one (click it again to go back to a sum of all deaths)
5. Or drag the left white bar and right white bar on the timeline to highlight a section of deaths which is nice for looking at single teamfights or early/mid/late game
6. Click the icon of each champ to go into a view to see only them (who they were killing and who they were being killed by)


New champ TODO:

currently the static data is not loaded by the static data api. Steps required to add new champ support

1. download the latest static data and grab the image from https://developer.riotgames.com/docs/lol (search Data Dragon)
2. move new champ image from 13.24.1 > img > champion to app > static > champ_images
3. update app > riot > champs.py to have new champ name
4. update app > riot > simple_request.py to have the mapping for champ name to ability breakdown
5. push to github
6. on pythonanywhere, pull from github
7. run python manage.py collectstatic
8. hit the reload website button
