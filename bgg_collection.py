from lxml import etree
import requests, time, sys
from io import BytesIO
import csv
import os

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



game_info = []
for game_id in game_ids:
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
    print(game_url)
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
    playtime_min = game.xpath('/items/item/minplaytime')[0].attrib['value']
    playtime_max = game.xpath('/items/item/maxplaytime')[0].attrib['value']
    num_players_poll = game.xpath('/items/item/poll')[0]
    rec_players = []
    best_players = []

    for result in num_players_poll.xpath('results'):
        numplayers = result.attrib['numplayers'] #kept as str due to 'n+' results
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

for players in sorted(game_info_dict.keys()):
    best, rec = game_info_dict[players]
    print('Best at {} players'.format(players))
    for game in best:
        print('{} time: {}-{}min'.format(*game))

    print('')
    print('Recommended at {} players'.format(players))
    for game in rec:
        print('{} time: {}-{}min'.format(*game))

csvprint = input('Do you want to print this to a csv? (y/n)')
while csvprint.lower() not in ['y','yes','no','n']:
    print("Sorry I didn't catch that.")
    csvprint = input('Do you want to print this to a csv? (y/n)')

if csvprint.lower() in ['n','no']:
    sys.exit()

with open('collection_summary.csv','w') as csvfile:
    writer = csv.writer(csvfile,lineterminator="\n")

    for players in sorted(game_info_dict.keys()):
        best, rec = game_info_dict[players]
        writer.writerow([players,'min time','max time'])
        writer.writerow(['best'])
        if len(best) == 0:
            writer.writerow([''])
        for game in best:
            writer.writerow([game[0],game[1],game[2]])

        writer.writerow(['recommended'])
        for game in rec:
            writer.writerow([game[0],game[1],game[2]])
