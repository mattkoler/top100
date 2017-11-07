import heapq
from difflib import SequenceMatcher

tom = ["Gloomhaven","Cosmic Encounter","Le Havre","Summoner Wars","Kemet","Heroscape","Arcadia Quest","Caverna: The Cave Farmers","Dice Masters","Viticulture","Thunderstone Quest","Project: Elite","Legendary: Marvel","Champions of Midgard","Race for the Galaxy","Rising Sun","Ticket to Ride","Terraforming Mars","Blood Rage","Pitchcar","Codex: Card-Time Strategy","Time's Up!","Glenn Drover's Empires: Age of Discovery – Deluxe Edition","Dominion","Ghost Stories","Eldritch Horror","Mansions of Madness: Second Edition","Duel of Ages II","Roll for the Galaxy","Descent: Journeys in the Dark (Second Edition)","Near and Far","Teenage Mutant Ninja Turtles: Shadows of the Past","Cyclades","Balderdash","BattleLore (Second Edition)","Sheriff of Nottingham","T.I.M.E Stories: The Marcy Case","Adventure Land","Catacombs","Orléans","Puerto Rico","Clank!","VIRAL","Cry Havoc","El Grande","Twilight Struggle","Automania","Lords of Waterdeep","Mage Wars Academy","Airlines Europe","Suburbia","Stockpile","Flick 'em Up!","Captain Sonar","The Voyages of Marco Polo","Concept","Carson City","Battleground: Fantasy Warfare","Mechs vs Minions","Century: Spice Road","Rum and Bones: Second Tide","Photosynthesis","Santorini","Spyfall","Dixit","Defenders of the Last Stand","Tiefe Taschen","Magic Maze","Francis Drake","Wallenstein (second edition)","Colosseum","The Godfather: The Board Game","Commands & Colors: Ancients","Tumblin-Dice","Seasons","Dream Factory","Libertalia","Domaine","Onitama","Werewolf","Battle Line","Memoir '44","Thunder & Lightning","Downforce","Through the Ages: A New Story of Civilization","Robinson Crusoe: Adventure on the Cursed Island","Star Wars: Armada","A Feast for Odin","Dungeon Twister","When I Dream","Targi","Yokohama","King of Tokyo","Star Wars: Rebellion","Pandemic Legacy","Smash Up","Zendo","Innovation","Werewords","The Chameleon"]
eric = ["Merchant of Venus","Pandemic","Alien Frontiers","Power Grid","Mice and Mystics","Dominion","Viticulture","Mechs vs Minions","Through the Ages: A New Story of Civilization","Pandemic Legacy","Potion Explosion","Tiny Epic Galaxies","Unlock!","Pandemic: The Cure","Istanbul","Legendary Encounters: An Alien Deck Building Game","T.I.M.E Stories: The Marcy Case","Splendor","RoboRally","Antike","Agricola","Food Chain Magnate","Scythe","Pathfinder Adventure Card Game: Rise of the Runelords – Base Set","Roll for the Galaxy","Indonesia","Legendary: A Marvel Deck Building Game","King of Tokyo","Logistico","Xia: Legends of a Drift System","Race for the Galaxy","Flip City","Paperback","Codenames","Orléans","Great Western Trail","Concordia","Eclipse","Terra Mystica","Firefly: The Game","TransAmerica","Specter Ops","Flash Point: Fire Rescue","Attika","Fantastiqa","Bus","Machi Koro","Innovation","Perry Rhodan: The Cosmic League","Mysterium","The Networks","Terraforming Mars","Merchant of Venus (second edition)","Valley of the Kings","Harry Potter Hogwarts Battle Cooperative Deck-Building Game","Ticket to Ride","Blood Rage","Spyfall","Airlines Europe","Imperial","Guildhall","Quicksilver","Trains","Myrmes","VOLT: Robot Battle Arena","Police Precinct","Adrenaline","EXIT: The Game – The Pharaoh's Tomb","Mage Knight Board Game","Sentinels of the Multiverse","KLASK","Snow Tails","Dice City","Clank!","Empires of the Void","Thunderstone","Impulse","Die Magier von Pangea","Reef Encounter","Copycat","Castles of Mad King Ludwig","Defenders of the Realm","Power Grid: The Card Game","Century: Spice Road","Tragedy Looper","Pueblo","Robinson Crusoe: Adventure on the Cursed Island","Panamax","Hero Realms","Glass Road","Eminent Domain","Auf Achse","Puzzle Strike","Entdecker","No Thanks!","Escape: The Curse of the Temple","Risk Legacy","Red7","Star Trek: Fleet Captains","Space Cadets: Dice Duel"]
sam = ["Blood Rage","TI4","Memoir '44","Star Wars Rebellion","Zombicide: Black Plague","Deception: Murder in Hong Kong","Rum and Bones: Second Tide","Conan","Sword & Sorcery","Tournament at Camelot","TZAAR","Imperial Settlers","Asante","YINSH","Five Tribes","Sentient","51st State Master Set","Balderdash","Race for the Galaxy","Targi","Onitama","Bang! The Dice Game","Stone Age","V-Commandos","Rising 5: Runes of Asteros","Wasteland Express Delivery Service","Kingsburg (Second Edition)","Dead of Winter: A Crossroads Game","Mission: Red Planet","Hero Realms","King of Tokyo","Tannhäuser","Star Wars: Imperial Assault","Summoner Wars","Sheriff of Nottingham","Inis","Codinca","Run, Fight, or Die!","Dice Town","Thunderstone Advance: Numenera","Bunny Kingdom","Spoils of War","Wettlauf nach El Dorado","Sola Fide: The Reformation","Photosynthesis","Age of War","VIRAL","Specter Ops","Cutthroat Kingdoms","Cry Havoc","Commissioned","Cosmic Encounter","Flick 'em Up!: Dead of Winter","Heroes of Normandie","Mansions of Madness: Second Edition","Carcassonne: Amazonas","Sagrada","Smash Up","Celestia","Discoveries","Ticket to Ride: Märklin","Blood Bowl (fourth edition)","Caverna: The Cave Farmers","BattleLore (Second Edition)","The Great War","Last Night on Earth: The Zombie Game","Cleopatra and the Society of Architects","Quantum","Neuroshima Hex!","Shogun","Power Grid","Queendomino","The Godfather: The Board Game","Champions of Midgard","First Class: All Aboard the Orient Express","Dice Forge","Scythe","Raptor","Ice Cool","Ca$h 'n Guns (second edition)","Twilight Struggle","Pandemic","Spyfall","Yamataï","Captain Sonar","Terraforming Mars","Santorini","Century: Spice Road","Vikingdoms","Dust 1947","Incan Gold","Star Realms","For Sale","Augustus","XenoShyft Onslaught","Tyrants of the Underdark","The Resistance","Nothing Personal","Catan Geographies: Germany","The Manhattan Project"]
zee = ["Pandemic","Onirim","Neuroshima Hex!","7 Wonders Duel","Blue Moon Legends","Ghost Stories","7 Wonders","King of Tokyo","Deus","Deception: Murder in Hong Kong","Rising Sun","Time Stories","Hanamikoji","Fire & Axe: A Viking Saga","Shadows over Camelot","Jamaica","Battlestar Galactica","Colosseum","7 Wonders","Fury of Dracula 3rd Edition","Cosmic Encounter","Jamaica","Yamataï","Arkham Horror: The Card Game","Karuba","Uluru","The Others","Factory Funner","Summoner Wars","Ticket to Ride: Europe","Archaeology: The New Expedition","Abyss","Liar's Dice","Saint Malo","Blue Moon City","Carcassonne: The City","It's Mine","Elysium","Sheep & Thief","San Juan (second edition)","T.I.M.E Stories: The Marcy Case","Blood Rage","Arena: Roma II","Ethnos","Mr. Jack","Tides of Madness","Among the Stars","Raptor","Forbidden Desert","Compatibility","Claustrophobia","Avenue","Bruges","Bärenpark","Libertalia","Mykerinos","Pow Wow","Witness","Gold West","K2","Mission: Red Planet","Las Vegas","Santiago de Cuba","Automania","Thunderbirds","Oceanos","R-Eco","Tintas","Notre Dame","Palazzo","Relic Runners","Onitama","Viceroy","LYNGK","Babel","Dixit","Hive","DVONN","Scythe","Queendomino","Cavemen: The Quest for Fire","Snow Tails","Vegas Showdown","Beasty Bar","Rising 5: Runes of Asteros","Alhambra","Shakespeare","The Pillars of the Earth","Citadels","Quadropolis","Magic: The Gathering","Robinson Crusoe: Adventure on the Cursed Island","Legends of Andor","Cleopatra and the Society of Architects","Dead Men Tell No Tales","Viticulture","Santorini","Friday","Shanghaien","Takenoko",]
people = ["Scythe","Pandemic","Pandemic Legacy Season 1","Blood Rage","7 Wonders","Terraforming Mars","Viticulture","7 Wonders Duel","Ticket To Ride","Codenames","Carcassonne","Five Tribes","Dominion","Castles of Burgundy","King of Tokyo","Dead Of Winter","Lords of Waterdeep","Splendor","Star Wars Rebellion","Power Grid","Concordia","Clank!","Orleans","Mechs vs. Minions","Robinson Crusoe","T.I.M.E Stories","Great Western Trail","Small World","Caverna","Terra Mystica","Roll for the Galaxy","Cosmic Encounter","Eldritch Horror","Sushi Go!","Agricola","Race for the Galaxy","Patchwork","Sheriff of Nottingham","Mansions of Madness 2nd Edition","Deception: Murder in Hong Kong","Legendary: A Marvel Deckuilding Game","Stone Age","Kemet","Twilight Struggle","Puerto Rico","Star Realms","Gloomhaven","Ticket to Ride: Europe","Dixit","Champions of Midgard","Through the Ages","The Resistance","Imperial Settlers","Star Wars: Imperial Assault","The Voyages of Marco Polo","Suburbia","Mysterium","Takenoko","Catan / Settlers of Catan","The Castles of Mad King Ludwig","Arkham Horror: The Card Game","Magic: The Gathering","Love Letter","Santorini","Tzolkin","Shadows Over Camelot","Ghost Stories","Battlestar Galactica","Captain Sonar","A Feast for Odin","Smash Up","Jaipur","BANG! The Dice Game","Keyflower","Mission: Red Planet","Fury of Dracula 3ed","Istanbul","Arcadia Quest","Memoir '44","Century: Spice Road","Jamaica","X-Wing Miniatures Game","Mage Knight","Le Havre","Seasons","Descent 2ed","Hanabi","Betrayal at House on the Hill","Twilight Imperium 3ed","Kingdomino","Onitama","Forbidden Desert","Alchemists","Inis","Zombicide: Black Plague","Food Chain Magnate","The Resistance: Avalon","Spyfall","Galaxy Trucker","Isle of Skye"]

combined_set = set()

for games in [tom,eric,sam,zee]:
    for game in games:
        if game in combined_set:
            continue
        combined_set.update((game,))

def matt_voting(list_of_lists,combined_set):
    three_votes = []
    two_votes = []
    for game in combined_set:
        occurance = 0
        score = []
        for ranking in list_of_lists:
            if game in ranking:
                occurance += 1
                score += [ranking.index(game),]
        if occurance > 3:
            score.remove(max(score))
            print(game, 'had 4 votes')
        if occurance > 2:
            heapq.heappush(three_votes,(sum(score),game))
        if occurance == 2:
            heapq.heappush(two_votes,(sum(score),game))
    while len(three_votes) > 0:
        print(heapq.heappop(three_votes)[1])
    while len(two_votes) > 0:
        print(heapq.heappop(two_votes)[1])

def detect_misspelling(combined_set):
    sorted_set = sorted(combined_set)
    for i,game in enumerate(sorted_set):
        for other in sorted_set[:i] + sorted_set[i+1:]:
            match = SequenceMatcher(None, game, other).find_longest_match(0, len(game), 0, len(other))
            if match.size > 5:
                print("Match found between {} // {}".format(game,other))

def star_ratings(tom,eric,sam,zee,people,combined_set):
    five_star = []
    four_star = []
    three_star = []
    for game in combined_set:
        rating = 0
        if game in tom:
            rating += 1
        if game in eric:
            rating += 1
        if game in sam:
            rating += 1
        if game in zee:
            rating += 1
        if game in people:
            rating += 1
        if rating == 5:
            five_star.append(game)
        elif rating == 4:
            four_star.append(game)
        elif rating == 3:
            three_star.append(game)
    print("\n-".join(["Five Star Games:"] + five_star))
    print('')
    print("\n-".join(["Four Star Games:"] + four_star))
    print('')
    print("\n-".join(["Three Star Games:"] + three_star))

star_ratings(tom,eric,sam,zee,people,combined_set)