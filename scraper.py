from lxml import html
import requests

title_list = []

for i in range(1,100,10):
    page = requests.get('http://www.dicetower.com/game-video/eric-summerers-top-100-games-all-time-{}-{}'.format(i+9,i))
    tree = html.fromstring(page.content)

    titles = tree.find_class('gt_bgg')
    print(titles)
    for title in titles[::-1]:
        title_list.append(title.attrib['href'])

print(title_list)

