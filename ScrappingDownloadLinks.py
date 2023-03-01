#import libraries
import requests
from bs4 import BeautifulSoup
import re
import sqlite3


main_url = input('Please enter the course link: ')
## to test the link will be hard injected
# main_url = 'https://alaatv.com/set/1286'

r = requests.get(main_url)
soup = BeautifulSoup(r.text, 'html.parser')

videos = soup.find_all('h2', {'class':'a--list1-title'})
links = ''
for i in videos:
    links += str(i)
    
links_lst = re.findall(r'href=\"(https:\/\/alaatv.com\/[\w\d\/]*)\"', links)

con = sqlite3.connect("AlaaDownloadLinks.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS links(tittle, link)")
con.commit()
for i in range(len(links_lst)):
    r = requests.get(links_lst[i])
    soup = BeautifulSoup(r.text, 'html.parser')
    video = soup.find_all('video')
    tittle = re.findall(r'>(.*)<', str(soup.find_all('h1'))).pop()
    invalid_names = ['/', '\\', ':', '*', '?', '<', '>', '|', chr(39)]

    for i in invalid_names:
        if i in tittle:
            tittle = tittle.replace(i, '-')
    
    downLink = re.findall(r'\"720p\" src=\"(https:\/\/[\w\d.\/]+)', str(video)).pop()
    data = []
    cur.execute("INSERT INTO links VALUES (\'%s\', \'%s\')"% (tittle, downLink))
    con.commit()