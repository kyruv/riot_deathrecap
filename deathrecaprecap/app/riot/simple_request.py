import requests
from django.conf import settings

class DeathData:
    
    special_aa_mapping = set([
        "tristanacritattack",
    ])

    spell_mapping = {
    "aatrox": {
      "aatroxq": "q",
      "aatroxw": "w",
      "aatroxe": "e",
      "aatroxr": "r"
    },
    "ahri": {
      "ahriq": "q",
      "ahriw": "w",
      "ahrie": "e",
      "ahrir": "r"
    },
    "akali": {
      "akaliq": "q",
      "akaliw": "w",
      "akalie": "e",
      "akalir": "r"
    },
    "akshan": {
      "akshanq": "q",
      "akshanw": "w",
      "akshane": "e",
      "akshanr": "r"
    },
    "alistar": {
      "pulverize": "q",
      "headbutt": "w",
      "alistare": "e",
      "ferocioushowl": "r"
    },
    "amumu": {
      "bandagetoss": "q",
      "auraofdespair": "w",
      "tantrum": "e",
      "curseofthesadmummy": "r"
    },
    "anivia": {
      "flashfrost": "q",
      "crystallize": "w",
      "frostbite": "e",
      "glacialstorm": "r"
    },
    "annie": {
      "annieq": "q",
      "anniew": "w",
      "anniee": "e",
      "annier": "r"
    },
    "aphelios": {
      "aphelioscalibrumq": "q",
      "apheliosseverumq": "q",
      "apheliosgravitumq": "q",
      "apheliosinfernumq": "q",
      "aphelioscrescendumq": "q",
      "apheliosq_clienttooltipwrapper": "q",

      # i think apheliosw is actually his AA
      "apheliosw": "aa",
      "apheliose_clienttooltipwrapper": "e",
      "apheliosr": "r"
    },
    "ashe": {
      "ashecritattack": "aa",
      "asheq": "q",
      "volley": "w",
      "ashespiritofthehawk": "e",
      "enchantedcrystalarrow": "r"
    },
    "aurelionsol": {
      "aurelionsolq": "q",
      "aurelionsolw": "w",
      "aurelionsole": "e",
      "aurelionsolr": "r"
    },
    "azir": {
      "azirqwrapper": "q",
      "azirw": "w",
      "azirewrapper": "e",
      "azirr": "r"
    },
    "bard": {
      "bardq": "q",
      "bardw": "w",
      "barde": "e",
      "bardr": "r"
    },
    "belveth": {
      "belvethq": "q",
      "belvethw": "w",
      "belvethe": "e",
      "belvethr": "r"
    },
    "blitzcrank": {
      "rocketgrab": "q",
      "overdrive": "w",
      "powerfist": "e",
      "staticfield": "r"
    },
    "brand": {
      "brandq": "q",
      "brandw": "w",
      "brande": "e",
      "brandr": "r"
    },
    "braum": {
      "braumq": "q",
      "braumw": "w",
      "braume": "e",
      "braumrwrapper": "r"
    },
    "briar": {
      "briarq": "q",
      "briarw": "w",
      "briarwattackspell": "w",
      "briare": "e",
      "briarr": "r"
    },
    "caitlyn": {
      "caitlynq": "q",
      "caitlynw": "w",
      "caitlyne": "e",
      "caitlynr": "r"
    },
    "camille": {
      "camilleq": "q",
      "camillew": "w",
      "camillee": "e",
      "camiller": "r"
    },
    "cassiopeia": {
      "cassiopeiaq": "q",
      "cassiopeiaw": "w",
      "cassiopeiae": "e",
      "cassiopeiar": "r"
    },
    "chogath": {
      "rupture": "q",
      "feralscream": "w",
      "vorpalspikes": "e",
      "feast": "r"
    },
    "corki": {
      "phosphorusbomb": "q",
      "carpetbomb": "w",
      "ggun": "e",
      "missilebarrage": "r"
    },
    "darius": {
      "dariuscleave": "q",
      "dariusnoxiantacticsonh": "w",
      "dariusaxegrabcone": "e",
      "dariusexecute": "r"
    },
    "diana": {
      "dianaq": "q",
      "dianaorbs": "w",
      "dianateleport": "e",
      "dianar": "r"
    },
    "draven": {
      "dravenspinning": "q",
      "dravenfury": "w",
      "dravendoubleshot": "e",
      "dravenrcast": "r"
    },
    "drmundo": {
      "drmundoq": "q",
      "drmundow": "w",
      "drmundoe": "e",
      "drmundor": "r"
    },
    "ekko": {
      "ekkoq": "q",
      "ekkow": "w",
      "ekkoe": "e",
      "ekkor": "r"
    },
    "elise": {
      "elisehumanq": "q",
      "elisehumanw": "w",
      "elisehumane": "e",
      "eliser": "r"
    },
    "evelynn": {
      "evelynnq": "q",
      "evelynnw": "w",
      "evelynne": "e",
      "evelynnr": "r"
    },
    "ezreal": {
      "ezrealq": "q",
      "ezrealw": "w",
      "ezreale": "e",
      "ezrealr": "r"
    },
    "fiddlesticks": {
      "fiddlesticksq": "q",
      "fiddlesticksw": "w",
      "fiddlestickse": "e",
      "fiddlesticksr": "r"
    },
    "fiora": {
      "fioraq": "q",
      "fioraw": "w",
      "fiorae": "e",
      "fiorar": "r"
    },
    "fizz": {
      "fizzq": "q",
      "fizzw": "w",
      "fizze": "e",
      "fizzr": "r"
    },
    "galio": {
      "galioq": "q",
      "galiow": "w",
      "galioe": "e",
      "galior": "r"
    },
    "gangplank": {
      "gangplankqwrapper": "q",
      "gangplankw": "w",
      "gangplanke": "e",
      "gangplankr": "r"
    },
    "garen": {
      "garenq": "q",
      "garenw": "w",
      "garene": "e",
      "garenr": "r"
    },
    "gnar": {
      "gnarq": "q",
      "gnarw": "w",
      "gnare": "e",
      "gnarr": "r"
    },
    "gragas": {
      "gragasq": "q",
      "gragasw": "w",
      "gragase": "e",
      "gragasr": "r"
    },
    "graves": {
      "gravesqlinespell": "q",
      "gravessmokegrenade": "w",
      "gravesmove": "e",
      "graveschargeshot": "r"
    },
    "gwen": {
      "gwenq": "q",
      "gwenw": "w",
      "gwene": "e",
      "gwenr": "r"
    },
    "hecarim": {
      "hecarimrapidslash": "q",
      "hecarimw": "w",
      "hecarimramp": "e",
      "hecarimult": "r"
    },
    "heimerdinger": {
      "heimerdingerq": "q",
      "heimerdingerw": "w",
      "heimerdingere": "e",
      "heimerdingerr": "r"
    },
    "illaoi": {
      "illaoiq": "q",
      "illaoiw": "w",
      "illaoie": "e",
      "illaoir": "r"
    },
    "irelia": {
      "ireliaq": "q",
      "ireliaw": "w",
      "ireliae": "e",
      "ireliar": "r"
    },
    "ivern": {
      "ivernq": "q",
      "ivernw": "w",
      "iverne": "e",
      "ivernr": "r"
    },
    "janna": {
      "howlinggale": "q",
      "sowthewind": "w",
      "eyeofthestorm": "e",
      "reapthewhirlwind": "r"
    },
    "jarvaniv": {
      "jarvanivdragonstrike": "q",
      "jarvanivgoldenaegis": "w",
      "jarvanivdemacianstandard": "e",
      "jarvanivcataclysm": "r"
    },
    "jax": {
      "jaxleapstrike": "q",
      "jaxempowertwo": "w",
      "jaxcounterstrike": "e",
      "jaxrapexform": "r"
    },
    "jayce": {
      "jaycetotheskies": "q",
      "jayceshockblast": "q",
      "jaycestaticfield": "w",
      "jaycethunderingblow": "e",
      "jaycestancehtg": "r",
      "jaycestancegth": "r"
    },
    "jhin": {
      "jhinq": "q",
      "jhinw": "w",
      "jhine": "e",
      "jhinr": "r"
    },
    "jinx": {
      "jinxq": "q",
      "jinxw": "w",
      "jinxe": "e",
      "jinxr": "r"
    },
    "kaisa": {
      "kaisaq": "q",
      "kaisaw": "w",
      "kaisae": "e",
      "kaisar": "r"
    },
    "kalista": {
      "kalistamysticshot": "q",
      "kalistaw": "w",
      "kalistaexpungewrapper": "e",
      "kalistarx": "r"
    },
    "karma": {
      "karmaq": "q",
      "karmaspiritbind": "w",
      "karmasolkimshield": "e",
      "karmamantra": "r"
    },
    "karthus": {
      "karthuslaywastea1": "q",
      "karthuswallofpain": "w",
      "karthusdefile": "e",
      "karthusfallenone": "r"
    },
    "kassadin": {
      "nulllance": "q",
      "netherblade": "w",
      "forcepulse": "e",
      "riftwalk": "r"
    },
    "katarina": {
      "katarinaq": "q",
      "katarinaw": "w",
      "katarinaewrapper": "e",
      "katarinar": "r"
    },
    "kayle": {
      "kayleq": "q",
      "kaylew": "w",
      "kaylee": "e",
      "kayler": "r"
    },
    "kayn": {
      "kaynq": "q",
      "kaynw": "w",
      "kayne": "e",
      "kaynr": "r"
    },
    "kennen": {
      "kennenshurikenhurlmissile1": "q",
      "kennenbringthelight": "w",
      "kennenlightningrush": "e",
      "kennenshurikenstorm": "r"
    },
    "khazix": {
      "khazixq": "q",
      "khazixw": "w",
      "khazixe": "e",
      "khazixr": "r"
    },
    "kindred": {
      "kindredq": "q",
      "kindredw": "w",
      "kindredewrapper": "e",
      "kindredr": "r"
    },
    "kled": {
      "kledq": "q",
      "kledw": "w",
      "klede": "e",
      "kledr": "r"
    },
    "kogmaw": {
      "kogmawq": "q",
      "kogmawbioarcanebarrage": "w",
      "kogmawvoidooze": "e",
      "kogmawlivingartillery": "r"
    },
    "ksante": {
      "ksanteq": "q",
      "ksantew": "w",
      "ksantee": "e",
      "ksanter": "r"
    },
    "leblanc": {
      "leblancq": "q",
      "leblancw": "w",
      "leblance": "e",
      "leblancr": "r"
    },
    "leesin": {
      "blindmonkqone": "q",
      "blindmonkwone": "w",
      "blindmonkeone": "e",
      "blindmonkrkick": "r"
    },
    "leona": {
      "leonashieldofdaybreak": "q",
      "leonasolarbarrier": "w",
      "leonazenithblade": "e",
      "leonasolarflare": "r"
    },
    "lillia": {
      "lilliaq": "q",
      "lilliaw": "w",
      "lilliae": "e",
      "lilliar": "r"
    },
    "lissandra": {
      "lissandraq": "q",
      "lissandraw": "w",
      "lissandrae": "e",
      "lissandrar": "r"
    },
    "lucian": {
      "lucianq": "q",
      "lucianw": "w",
      "luciane": "e",
      "lucianr": "r"
    },
    "lulu": {
      "luluq": "q",
      "luluw": "w",
      "lulue": "e",
      "lulur": "r"
    },
    "lux": {
      "luxlightbinding": "q",
      "luxprismaticwave": "w",
      "luxlightstrikekugel": "e",
      "luxr": "r"
    },
    "malphite": {
      "seismicshard": "q",
      "obduracy": "w",
      "landslide": "e",
      "ufslash": "r"
    },
    "malzahar": {
      "malzaharq": "q",
      "malzaharw": "w",
      "malzahare": "e",
      "malzaharr": "r"
    },
    "maokai": {
      "maokaiq": "q",
      "maokaiw": "w",
      "maokaie": "e",
      "maokair": "r"
    },
    "masteryi": {
      "alphastrike": "q",
      "meditate": "w",
      "wujustyle": "e",
      "highlander": "r"
    },
    "milio": {
      "milioq": "q",
      "miliow": "w",
      "milioe": "e",
      "milior": "r"
    },
    "missfortune": {
      "missfortunecritattack": "aa",
      "missfortunericochetshot": "q",
      "missfortuneviciousstrikes": "w",
      "missfortunescattershot": "e",
      "missfortunebullettime": "r"
    },
    "monkeyking": {
      "monkeykingdoubleattack": "q",
      "monkeykingdecoy": "w",
      "monkeykingnimbus": "e",
      "monkeykingspintowin": "r"
    },
    "mordekaiser": {
      "mordekaiserq": "q",
      "mordekaiserw": "w",
      "mordekaisere": "e",
      "mordekaiserr": "r"
    },
    "morgana": {
      "morganaq": "q",
      "morganaw": "w",
      "morganae": "e",
      "morganar": "r"
    },
    "naafiri": {
      "naafiriq": "q",
      "naafiriw": "w",
      "naafirie": "e",
      "naafirir": "r"
    },
    "nami": {
      "namiq": "q",
      "namiw": "w",
      "namie": "e",
      "namir": "r"
    },
    "nasus": {
      "nasusq": "q",
      "nasusw": "w",
      "nasuse": "e",
      "nasusr": "r"
    },
    "nautilus": {
      "nautilusanchordrag": "q",
      "nautiluspiercinggaze": "w",
      "nautilussplashzone": "e",
      "nautilusgrandline": "r"
    },
    "neeko": {
      "neekoq": "q",
      "neekow": "w",
      "neekoe": "e",
      "neekor": "r"
    },
    "nidalee": {
      "javelintoss": "q",
      "bushwhack": "w",
      "primalsurge": "e",
      "aspectofthecougar": "r"
    },
    "nilah": {
      "nilahq": "q",
      "nilahw": "w",
      "nilahe": "e",
      "nilahr": "r"
    },
    "nocturne": {
      "nocturneduskbringer": "q",
      "nocturneshroudofdarkness": "w",
      "nocturneunspeakablehorror": "e",
      "nocturneparanoia": "r"
    },
    "nunu": {
      "nunuq": "q",
      "nunuw": "w",
      "nunue": "e",
      "nunur": "r"
    },
    "olaf": {
      "olafaxethrowcast": "q",
      "olaffrenziedstrikes": "w",
      "olafrecklessstrike": "e",
      "olafragnarok": "r"
    },
    "orianna": {
      "orianaizunacommand": "q",
      "orianadissonancecommand": "w",
      "orianaredactcommand": "e",
      "orianadetonatecommand": "r"
    },
    "ornn": {
      "ornnq": "q",
      "ornnw": "w",
      "ornne": "e",
      "ornnr": "r"
    },
    "pantheon": {
      "pantheonq": "q",
      "pantheonw": "w",
      "pantheone": "e",
      "pantheonr": "r"
    },
    "poppy": {
      "poppyq": "q",
      "poppyw": "w",
      "poppye": "e",
      "poppyr": "r"
    },
    "pyke": {
      "pykeq": "q",
      "pykew": "w",
      "pykee": "e",
      "pyker": "r"
    },
    "qiyana": {
      "qiyanaq": "q",
      "qiyanaw": "w",
      "qiyanae": "e",
      "qiyanar": "r"
    },
    "quinn": {
      "quinnq": "q",
      "quinnw": "w",
      "quinne": "e",
      "quinnr": "r"
    },
    "rakan": {
      "rakanq": "q",
      "rakanw": "w",
      "rakane": "e",
      "rakanr": "r"
    },
    "rammus": {
      "powerball": "q",
      "defensiveballcurl": "w",
      "puncturingtaunt": "e",
      "tremors2": "r"
    },
    "reksai": {
      "reksaiq": "q",
      "reksaiw": "w",
      "reksaie": "e",
      "reksairwrapper": "r"
    },
    "rell": {
      "rellq": "q",
      "rellw_dismount": "w",
      "relle": "e",
      "rellr": "r"
    },
    "renata": {
      "renataq": "q",
      "renataw": "w",
      "renatae": "e",
      "renatar": "r"
    },
    "renekton": {
      "renektoncleave": "q",
      "renektonpreexecute": "w",
      "renektonsliceanddice": "e",
      "renektonreignofthetyrant": "r"
    },
    "rengar": {
      "rengarq": "q",
      "rengarw": "w",
      "rengare": "e",
      "rengarr": "r"
    },
    "riven": {
      "riventricleave": "q",
      "rivenmartyr": "w",
      "rivenfeint": "e",
      "rivenfengshuiengine": "r"
    },
    "rumble": {
      "rumbleflamethrower": "q",
      "rumbleshield": "w",
      "rumblegrenade": "e",
      "rumblecarpetbomb": "r"
    },
    "ryze": {
      "ryzeqwrapper": "q",
      "ryzew": "w",
      "ryzee": "e",
      "ryzer": "r"
    },
    "samira": {
      "samiraq": "q",
      "samiraw": "w",
      "samirae": "e",
      "samirar": "r"
    },
    "sejuani": {
      "sejuaniq": "q",
      "sejuaniw": "w",
      "sejuanie": "e",
      "sejuanir": "r"
    },
    "senna": {
      "sennaq": "q",
      "sennaw": "w",
      "sennae": "e",
      "sennar": "r"
    },
    "seraphine": {
      "seraphineq": "q",
      "seraphinew": "w",
      "seraphinee": "e",
      "seraphiner": "r"
    },
    "sett": {
      "settq": "q",
      "settw": "w",
      "sette": "e",
      "settr": "r"
    },
    "shaco": {
      "deceive": "q",
      "jackinthebox": "w",
      "twoshivpoison": "e",
      "hallucinatefull": "r"
    },
    "shen": {
      "shenq": "q",
      "shenw": "w",
      "shene": "e",
      "shenr": "r"
    },
    "shyvana": {
      "shyvanadoubleattack": "q",
      "shyvanaimmolationaura": "w",
      "shyvanafireball": "e",
      "shyvanatransformcast": "r"
    },
    "singed": {
      "poisontrail": "q",
      "megaadhesive": "w",
      "fling": "e",
      "insanitypotion": "r"
    },
    "sion": {
      "sionq": "q",
      "sionw": "w",
      "sione": "e",
      "sionr": "r"
    },
    "sivir": {
      "sivirq": "q",
      "sivirw": "w",
      "sivire": "e",
      "sivirr": "r"
    },
    "skarner": {
      "skarnervirulentslash": "q",
      "skarnerexoskeleton": "w",
      "skarnerfracture": "e",
      "skarnerimpale": "r"
    },
    "sona": {
      "sonaq": "q",
      "sonaw": "w",
      "sonae": "e",
      "sonar": "r"
    },
    "soraka": {
      "sorakaq": "q",
      "sorakaw": "w",
      "sorakae": "e",
      "sorakar": "r"
    },
    "swain": {
      "swainq": "q",
      "swainw": "w",
      "swaine": "e",
      "swainr": "r"
    },
    "sylas": {
      "sylasq": "q",
      "sylasw": "w",
      "sylase": "e",
      "sylasr": "r"
    },
    "syndra": {
      "syndraq": "q",
      "syndraw": "w",
      "syndrae": "e",
      "syndrar": "r"
    },
    "tahmkench": {
      "tahmkenchq": "q",
      "tahmkenchw": "w",
      "tahmkenche": "e",
      "tahmkenchrwrapper": "r"
    },
    "taliyah": {
      "taliyahq": "q",
      "taliyahwvc": "w",
      "taliyahe": "e",
      "taliyahr": "r"
    },
    "talon": {
      "talonq": "q",
      "talonw": "w",
      "talone": "e",
      "talonr": "r"
    },
    "taric": {
      "taricq": "q",
      "taricw": "w",
      "tarice": "e",
      "taricr": "r"
    },
    "teemo": {
      "blindingdart": "q",
      "movequick": "w",
      "toxicshot": "e",
      "teemorcast": "r"
    },
    "thresh": {
      "threshq": "q",
      "threshw": "w",
      "threshe": "e",
      "threshrpenta": "r"
    },
    "tristana": {
      "tristanaq": "q",
      "tristanaw": "w",
      "tristanae": "e",
      "tristanar": "r"
    },
    "trundle": {
      "trundletrollsmash": "q",
      "trundledesecrate": "w",
      "trundlecircle": "e",
      "trundlepain": "r"
    },
    "tryndamere": {
      "tryndamereq": "q",
      "tryndamerew": "w",
      "tryndameree": "e",
      "undyingrage": "r"
    },
    "twistedfate": {
      "wildcards": "q",
      "pickacard": "w",
      "cardmasterstack": "e",
      "destiny": "r"
    },
    "twitch": {
      "twitchhideinshadows": "q",
      "twitchvenomcask": "w",
      "twitchexpunge": "e",
      "twitchfullautomatic": "r"
    },
    "udyr": {
      "udyrq": "q",
      "udyrw": "w",
      "udyre": "e",
      "udyrr": "r"
    },
    "urgot": {
      "urgotq": "q",
      "urgotw": "w",
      "urgote": "e",
      "urgotr": "r"
    },
    "varus": {
      "varusq": "q",
      "varusw": "w",
      "varuse": "e",
      "varusr": "r"
    },
    "vayne": {
      "vaynetumble": "q",
      "vaynesilveredbolts": "w",
      "vaynecondemn": "e",
      "vayneinquisition": "r"
    },
    "veigar": {
      "veigarbalefulstrike": "q",
      "veigardarkmatter": "w",
      "veigareventhorizon": "e",
      "veigarr": "r"
    },
    "velkoz": {
      "velkozq": "q",
      "velkozw": "w",
      "velkoze": "e",
      "velkozr": "r"
    },
    "vex": {
      "vexq": "q",
      "vexw": "w",
      "vexe": "e",
      "vexr": "r"
    },
    "vi": {
      "viq": "q",
      "viw": "w",
      "vie": "e",
      "vir": "r"
    },
    "viego": {
      "viegoq": "q",
      "viegow": "w",
      "viegoe": "e",
      "viegor": "r"
    },
    "viktor": {
      "viktorpowertransfer": "q",
      "viktorgravitonfield": "w",
      "viktordeathray": "e",
      "viktorchaosstorm": "r"
    },
    "vladimir": {
      "vladimirq": "q",
      "vladimirsanguinepool": "w",
      "vladimire": "e",
      "vladimirhemoplague": "r"
    },
    "volibear": {
      "volibearq": "q",
      "volibearw": "w",
      "volibeare": "e",
      "volibearr": "r"
    },
    "warwick": {
      "warwickq": "q",
      "warwickw": "w",
      "warwicke": "e",
      "warwickr": "r"
    },
    "xayah": {
      "xayahpassive": "aa",
      "xayahq": "q",
      "xayahw": "w",
      "xayahe": "e",
      "xayahr": "r"
    },
    "xerath": {
      "xeratharcanopulsechargeup": "q",
      "xeratharcanebarrage2": "w",
      "xerathmagespear": "e",
      "xerathlocusofpower2": "r"
    },
    "xinzhao": {
      "xinzhaoq": "q",
      "xinzhaow": "w",
      "xinzhaoe": "e",
      "xinzhaor": "r"
    },
    "yasuo": {
      "yasuocritattack": "aa",
      "yasuocritattack2": "aa",
      "yasuocritattack3": "aa",
      "yasuocritattack4": "aa",
      "yasuoq1wrapper": "q",
      "yasuow": "w",
      "yasuoe": "e",
      "yasuor": "r"
    },
    "yone": {
      "yoneq": "q",
      "yonew": "w",
      "yonee": "e",
      "yoner": "r"
    },
    "yorick": {
      "yorickq": "q",
      "yorickw": "w",
      "yoricke": "e",
      "yorickr": "r"
    },
    "yuumi": {
      "yuumiq": "q",
      "yuumiw": "w",
      "yuumie": "e",
      "yuumir": "r"
    },
    "zac": {
      "zacq": "q",
      "zacw": "w",
      "zace": "e",
      "zacr": "r"
    },
    "zed": {
      "zedq": "q",
      "zedw": "w",
      "zede": "e",
      "zedr": "r"
    },
    "zeri": {
      "zeriq": "q",
      "zeriw": "w",
      "zerie": "e",
      "zerir": "r"
    },
    "ziggs": {
      "ziggsq": "q",
      "ziggsw": "w",
      "ziggse": "e",
      "ziggsr": "r"
    },
    "zilean": {
      "zileanq": "q",
      "zileanw": "w",
      "timewarp": "e",
      "chronoshift": "r"
    },
    "zoe": {
      "zoeq": "q",
      "zoew": "w",
      "zoee": "e",
      "zoer": "r"
    },
    "zyra": {
      "zyraq": "q",
      "zyraw": "w",
      "zyrae": "e",
      "zyrar": "r"
    }
  }

    def __init__(self):
        self.api_key = settings.RIOT_API_KEY
        

    def create(self, gameid):
        death_data, meta_data, champ_map = self.only_important_data(self.get_match_data(gameid))
        response = {
            "all_deaths": death_data,
            "meta_data": meta_data,
            "aggregate_placeholder": self.make_aggregate_data_holder(champ_map),
        }
        return response

    def only_important_data(self, responses):
        detail_response = responses[0]
        overview_response = responses[1]
        meta_data = {}

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
                if event["type"] == "GAME_END":
                    meta_data["end_time"] = event["timestamp"]

                if event["type"] == "CHAMPION_KILL":

                    killers = {}
                    for ds in event["victimDamageReceived"]:
                        if ds["type"] == "TOWER" or ds["type"] == "MINION" or ds["type"] == "MONSTER":
                            id = "NPC" + ("100" if champ_map[id_map[event["victimId"]]]["team"] == 200 else "200")
                            if id not in killers:
                                killers[id] = {
                                    "who": id,
                                    "physical": 0,
                                    "magic": 0,
                                    "true": 0,
                                    "aa": 0,
                                    "q": 0,
                                    "w": 0,
                                    "e": 0,
                                    "r": 0,
                                    "other": 0,
                                    "other_names": [],
                                }
                            
                            killers[id]["physical"] += ds["physicalDamage"]
                            killers[id]["magic"] += ds["magicDamage"]
                            killers[id]["true"] += ds["trueDamage"]

                            if ds["type"] == "TOWER":
                                killers[id]["aa"] += (ds["trueDamage"] + ds["magicDamage"] + ds["physicalDamage"])
                            
                            if ds["type"] == "MINION":
                                killers[id]["q"] += (ds["trueDamage"] + ds["magicDamage"] + ds["physicalDamage"])

                            if ds["type"] == "MONSTER":
                                killers[id]["w"] += (ds["trueDamage"] + ds["magicDamage"] + ds["physicalDamage"])
                            
                            continue
                            

                        elif ds["name"] not in champ_map:
                            continue

                        if ds["name"] not in killers:
                            killers[ds["name"]] = {
                                "who": ds["name"],
                                "physical": 0,
                                "magic": 0,
                                "true": 0,
                                "aa": 0,
                                "q": 0,
                                "w": 0,
                                "e": 0,
                                "r": 0,
                                "other": 0,
                                "other_names": [],
                            }
                        
                        killers[ds["name"]]["physical"] += ds["physicalDamage"]
                        killers[ds["name"]]["magic"] += ds["magicDamage"]
                        killers[ds["name"]]["true"] += ds["trueDamage"]

                        if "basicattack" in ds["spellName"].lower() or ds["spellName"].lower() in DeathData.special_aa_mapping:
                            killers[ds["name"]]["aa"] += (ds["trueDamage"] + ds["magicDamage"] + ds["physicalDamage"])
                        else:
                            spell_type = DeathData.spell_mapping[ds["name"].lower()].get(ds["spellName"].lower(), "other")
                            killers[ds["name"]][spell_type] += (ds["trueDamage"] + ds["magicDamage"] + ds["physicalDamage"])

                            if spell_type == "other":
                                spell_name = ds["spellName"].lower()
                                if spell_name == "":
                                    spell_name = "<empty_spell_name>"
                                killers[ds["name"]]["other_names"].append(spell_name)
                    
                    for key in killers:
                        killers[key]["other_names"] = list(set(killers[key]["other_names"]))


                    deaths.append({
                        "timestamp": event["timestamp"],
                        "who": id_map[event["victimId"]],
                        "killers": list(killers.values()),
                    })
        
        return deaths, meta_data, champ_map

    def get_match_data(self, match):
        detailed_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}/timeline"
        detail_response = requests.get(detailed_request, headers = {"X-Riot-Token": self.api_key}).json()

        overview_request = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}"
        overview_response = requests.get(overview_request, headers = {"X-Riot-Token": self.api_key}).json()

        return detail_response, overview_response

    
    def make_aggregate_data_holder(self, champ_map):
        overview_data = {}

        team_100_participants = []
        team_200_participants = []

        for name, details in champ_map.items():
            if details['team'] == 100:
                team_100_participants.append(name)
            else:
                team_200_participants.append(name)
        team_100_participants.append("NPC100")
        team_200_participants.append("NPC200")

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
                'aa': 0,
                'q': 0,
                'w': 0,
                'e': 0,
                'r': 0,
                'other': 0,
                'takedowns': 0,
                'other_names': [],
            }

            for opponent in team_200_participants:
                overview_data[champ]['as_killer'][opponent] = {
                    'total': 0,
                    'physical': 0,
                    'magic': 0,
                    'true': 0,
                    'aa': 0,
                    'q': 0,
                    'w': 0,
                    'e': 0,
                    'r': 0,
                    'other': 0,
                    'takedowns': 0,
                    'other_names': [],
                }
                overview_data[champ]['as_victim'][opponent] = {
                    'total': 0,
                    'physical': 0,
                    'magic': 0,
                    'true': 0,
                    'aa': 0,
                    'q': 0,
                    'w': 0,
                    'e': 0,
                    'r': 0,
                    'other': 0,
                    'takedowns': 0,
                    'other_names': [],
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
                'aa': 0,
                'q': 0,
                'w': 0,
                'e': 0,
                'r': 0,
                'other': 0,
                'takedowns': 0,
                'other_names': [],
            }

            for opponent in team_100_participants:
                overview_data[champ]['as_killer'][opponent] = {
                    'total': 0,
                    'physical': 0,
                    'magic': 0,
                    'true': 0,
                    'aa': 0,
                    'q': 0,
                    'w': 0,
                    'e': 0,
                    'r': 0,
                    'other': 0,
                    'takedowns': 0,
                    'other_names': [],
                }
                overview_data[champ]['as_victim'][opponent] = {
                    'total': 0,
                    'physical': 0,
                    'magic': 0,
                    'true': 0,
                    'aa': 0,
                    'q': 0,
                    'w': 0,
                    'e': 0,
                    'r': 0,
                    'other': 0,
                    'takedowns': 0,
                    'other_names': [],
                }
        
        return overview_data