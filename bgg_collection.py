from lxml import etree
import requests, time, sys, csv, os
from io import BytesIO
from itertools import zip_longest

"""A scraper to pull the collection from a bgg user and return results by player count"""

#gets the location where we are executing so we can access files/folders next to it
dir_path = os.path.dirname(os.path.realpath(__file__))


username = input('Please enter the bgg username for the collection:')
col_url = 'https://www.boardgamegeek.com/xmlapi2/collection?username={}&excludesubtype=boardgameexpansion&own=1'.format(username)

print("Fetching collection for {}".format(username))
collection = requests.get(col_url)


counter = 0
while collection.status_code == 202:
    time.sleep(5)
    collection = requests.get(col_url)
    counter += 1
    if counter > 10:
        sys.exit()

if collection.status_code != 200:
    print('Sorry, something went wrong. See below and try again.')
    print(collection.status_code)
    sys.exit()


root = etree.parse(BytesIO(collection.content))

game_ids = []
for item in root.xpath('/items/item'):
    game_ids.append(item.attrib['objectid'])

# TODO: have it check mod times before asking and only updates ones that are xx days old
update = input("Do you want to update your game cache files? (y/n) ")
if update in ['y','Y','yes','Yes']:
    update = True
else:
    update = False

game_info = []
for game_id in game_ids:
    if game_id == 172242: # Hard skip on Exploding Kittens NSFW Deck to avoid duplicates
        continue
    if not update:
        try:
            with open(dir_path + '/game_cache/{}.xml'.format(game_id),'rb') as f:
                game_info.append(f.read())
                print('read file from cache id:', game_id)
                continue
        except FileNotFoundError:
            print('Creating a cache file for id {}.'.format(game_id))
        except:
            print(sys.exc_info()[0])
            pass

    game_url = 'https://www.boardgamegeek.com/xmlapi2/thing?id={}'.format(game_id)
    try:
        fetch = requests.get(game_url)
        game_info.append(fetch.content)
        if fetch.status_code != 200:
            sys.exit()
        with open(dir_path + '/game_cache/{}.xml'.format(game_id),'wb') as f:
            f.write(fetch.content)
            print('wrote new cache for id', game_id)
        time.sleep(2)
    except:
        print("Couldn't get",game_url)
        print(sys.exc_info()[0])
        time.sleep(10)
        continue    

game_info_dict = {}

for game_xml in game_info:
    game = etree.parse(BytesIO(game_xml))
    name = game.xpath('/items/item/name')[0].attrib['value']
    if len(name) > 25 and name.find(':') != -1: # Shorten long game names with :'s in them
        name = name[:name.find(':')]
    playtime_min = game.xpath('/items/item/minplaytime')[0].attrib['value']
    playtime_max = game.xpath('/items/item/maxplaytime')[0].attrib['value']
    num_players_poll = game.xpath('/items/item/poll')[0]
    rec_players = []
    best_players = []

    # Not enough votes, using the player count on the box as recommended
    if int(num_players_poll.attrib['totalvotes']) < 10:
        players_min = int(game.xpath('/items/item/minplayers')[0].attrib['value'])
        players_max = int(game.xpath('/items/item/maxplayers')[0].attrib['value'])
        for player_count in range(players_min, players_max + 1):
            game_info_dict.setdefault(player_count,([],[]))[1].append((name,playtime_min,playtime_max))
        continue

    # Use the player votes to determine playercounts at best and recommended
    for result in num_players_poll.xpath('results'):
        numplayers = result.attrib['numplayers'] # may have 'n+' as a result
        if numplayers[-1] == '+':
            numplayers = int(numplayers[:-1]) + 1 # set it to 1 above
        else:
            numplayers = int(numplayers)
        poll_results = result.xpath('result')
        if len(poll_results) == 0:
            continue
        best_votes = int(poll_results[0].attrib['numvotes'])
        recommended_votes = int(poll_results[1].attrib['numvotes'])
        bad_votes = int(poll_results[2].attrib['numvotes'] )
        
        if best_votes + recommended_votes > bad_votes:
            if best_votes > recommended_votes:
                #voted to be best at numplayers
                best_players.append(numplayers)
            else:
                #voted recommended at numplayers
                rec_players.append(numplayers)
    
    for player_count in best_players:
        game_info_dict.setdefault(player_count,([],[]))[0].append((name,playtime_min,playtime_max))
    for player_count in rec_players:
        game_info_dict.setdefault(player_count,([],[]))[1].append((name,playtime_min,playtime_max))

'''
for players in sorted(game_info_dict.keys()):
    if len(players) > 2:
        continue
    best, rec = game_info_dict[players]
    print('Best at {} players'.format(players))
    for game in best:
        print('{} time: {}-{}min'.format(*game))

    print('')
    print('Recommended at {} players'.format(players))
    for game in rec:
        print('{} time: {}-{}min'.format(*game))
<<<<<<< HEAD
'''
=======
    print('')
>>>>>>> a83022a6dd4605c2e7132527941373a023625957

csvprint = input('Do you want to print this to a csv? (y/n)')
while csvprint.lower() not in ['y','yes','no','n']:
    print("Sorry I didn't catch that.")
    csvprint = input('Do you want to print this to a csv? (y/n)')

if csvprint.lower() in ['n','no']:
    sys.exit()

with open(dir_path + '/{}.csv'.format(username),'w') as csvfile:
    writer = csv.writer(csvfile,lineterminator="\n")

    for players in sorted(game_info_dict.keys()):
        # Break out to combine party games below (9+ players)
        if players > 8: # TODO: Make it so all 9+ player games get combined into 1 listing with no duplicates
            break
        best, rec = game_info_dict[players]
        writer.writerow([str(players) + ' players'])
        writer.writerow(['Best Games', 'Avg Time'])
        for b in best:
            b_avg = (int(b[1]) + int(b[2])) // 2
            writer.writerow([b[0],str(b_avg) + ' mins'])
        writer.writerow([''])
        
        writer.writerow(['Recommended Games', 'Avg Time'])
        for r in rec:
            r_avg = (int(r[1]) + int(r[2])) // 2
            writer.writerow([r[0],str(r_avg) + ' mins'])
        writer.writerow([''])
        '''
        writer.writerow([players,'min time','max time'])
        writer.writerow(['best'])
        if len(best) == 0:
            writer.writerow([''])
        for game in best:
            writer.writerow([game[0],game[1],game[2]])

        writer.writerow(['recommended'])
        for game in rec:
            writer.writerow([game[0],game[1],game[2]])
        '''

    party_games = set()
    for players in reversed(sorted(game_info_dict.keys())):
        if players < 9:
            break
        best, rec = game_info_dict[players]
        for b in best:
            b_avg = (int(b[1]) + int(b[2])) // 2
            party_games.add((b[0],str(b_avg) + ' mins'))
        for r in rec:
            r_avg = (int(r[1]) + int(r[2])) // 2
            party_games.add((r[0],str(r_avg) + ' mins'))
    print(party_games)
    writer.writerow(['Large Party Games (9+)', 'Avg Time'])
    for game in party_games:
        writer.writerow(game)
        
