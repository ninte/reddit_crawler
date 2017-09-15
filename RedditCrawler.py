import praw
import urllib
import hashlib
import mmap
import sys
import os
import ConfigParser
from os import listdir
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

MAX_POSTS = 10
SUBREDDIT = 'earthporn'


def imgcheck(s, imagen, tipo):
    global j
    global i
    md = hashlib.md5(imagen).hexdigest()
    if s.find(md) != -1:
        print('Pic already downloaded')
    else:
        hashes.write(md + '\n')
        i += 1
        with open('images/' + str(i) + tipo, 'wb') as imgFile:
            imgFile.write(imagen)
        j += 1
        print(str(j) + ' downloaded pics')

if len(sys.argv) > 2:
    MAX_POSTS = int(sys.argv[1])
    SUBREDDIT = int(sys.argv[1])
elif len(sys.argv) > 1:
    MAX_POSTS = int(sys.argv[1])

Config = ConfigParser.ConfigParser()
Config.read('config.ini')

client_id = Config.get('IMGUR','clientid')  #imgur API id
client_secret = Config.get('IMGUR','clientsecret') #imgur API secret
client_imgur = ImgurClient(client_id, client_secret)  # imgur client

r = praw.Reddit(client_id=Config.get('REDDIT','clientid'), client_secret=Config.get('REDDIT','clientsecret'),
                user_agent='Image crawler by ninte')
subreddit = SUBREDDIT
submissions = r.subreddit(subreddit).hot(limit=MAX_POSTS)

hashes = open('hashes.txt', 'a+')
if os.stat('hashes.txt').st_size == 0:
    hashes.write('\n')
    hashes.close
    hashes = open('hashes.txt', 'a+')
s = mmap.mmap(hashes.fileno(), 0, access=mmap.ACCESS_READ)
if not os.path.isdir('images'):
    os.makedirs('images')
i = len(listdir('images'))
j = 0

for k, sub in enumerate(submissions):
    print('Searching in post ' + str(k + 1) + ' of ' + str(MAX_POSTS))
    if not sub.is_self and 'imgur.com/' in sub.url and not (
            'imgur.com/a/' in sub.url or 'imgur.com/gallery/' in sub.url):
        try:
            item = client_imgur.get_image(sub.url.split('com/')[1].split('.')[0])
            f = urllib.urlopen(item.link)
            img = f.read()
            extension = item.type.split('/')[1]
            if not extension == 'gif':
                imgcheck(s, img, '.' + extension)
            f.close()
        except ImgurClientError as e:
            print(e.error_message)
    elif not sub.is_self and 'i.redd.it' in sub.url:
        f = urllib.urlopen(sub.url)
        img = f.read()
        extension = sub.url.split('.')[-1]
        if not extension == 'gif':
            imgcheck(s, img, '.' + extension)
        f.close()

hashes.close()
print('\nDownloaded ' + str(j) + ' images \nTotal images: ' + str(i))
