from lxml import etree
from io import BytesIO
import requests, time, sys, csv, os

"""A scraper to pull the ratings for a game by id"""

dir_path = os.path.dirname(os.path.realpath(__file__))

game_id = input('Please enter the bgg id for the game:')

col_url = 'https://www.boardgamegeek.com/xmlapi2/thing?id={}&ratingcomments=1&page=1&pagesize=100'.format(game_id)

print("Fetching information for {}".format(game_id))
game_info = requests.get(col_url)


counter = 0
while game_info.status_code == 202:
    time.sleep(5)
    game_info = requests.get(col_url)
    counter += 1
    if counter > 10:
        sys.exit()

if game_info.status_code != 200:
    print('Sorry, something went wrong. See below and try again.')
    print(game_info.status_code)
    sys.exit()


root = etree.parse(BytesIO(game_info.content))

rating_count = int(root.xpath('/items/item/comments')[0].attrib['totalitems'])

print('There are {} ratings for this game.'.format(rating_count))

pages = rating_count // 100

if rating_count % 100 != 0:
    pages += 1

ratings = []

for page_num in range(1,pages+1):
    fetched_page = requests.get('https://www.boardgamegeek.com/xmlapi2/thing?id={}&ratingcomments=1&page={}&pagesize=100'.format(game_id, page_num))
    time.sleep(2)
    while fetched_page.status_code == 202:
        print('Got 202, retrying')
        time.sleep(1)
        fetched_page = requests.get('https://www.boardgamegeek.com/xmlapi2/thing?id={}&ratingcomments=1&page={}&pagesize=100'.format(game_id, page_num))
    if fetched_page.status_code != 200:
        print('Sorry, something went wrong. See below and try again.')
        print(fetched_page.status_code)
        sys.exit()
    root = etree.parse(BytesIO(fetched_page.content))
    for vote in root.xpath('/items/item/comments/comment'):
        ratings.append(float(vote.attrib['rating']))
    if page_num % 10 == 0:
        print('Completed page {}'.format(page_num))

with open(dir_path + '/{}.csv'.format(game_id),'w') as csvfile:
    for num in ratings:
        csvfile.write(str(num)+'\n')

average = sum(ratings) / len(ratings)

print('Average rating: {}'.format(average))