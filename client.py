#!/usr/bin/env python3
import requests
import json
from urllib.parse import parse_qs, urlparse
from src.objects import MediaItem, AlbumItem
from src.utility import downloader
from config import DOMAIN_CRT, SESSIONID, INCLUDE_PHOTOS, INCLUDE_VIDEOS, HOSTURL, PORT, AUTH_OBJ

url = f'https://{HOSTURL}:{PORT}'
try:
    resp = requests.get(url+'/ping', verify=DOMAIN_CRT, allow_redirects=False)
except requests.exceptions.SSLError:
    exit("Wrong certificate added please check")
except requests.exceptions.ConnectionError:
    exit("Server Down or Unreachable")

if not SESSIONID:
    if not AUTH_OBJ['uname']:
        AUTH_OBJ['uname'] = input("enter username(0 for new user registration): ")
        if AUTH_OBJ['uname'] == '0':
            AUTH_OBJ['uname'] = input("enter New username: ")
            if not AUTH_OBJ['uname']:
                exit("Username cannot be empty")
            AUTH_OBJ['newUser'] = "True"
    AUTH_OBJ['passw'] = AUTH_OBJ['passw'] if AUTH_OBJ['passw'] else input("enter password: ").strip()
    resp = requests.post(url+'/auth', data=AUTH_OBJ,
                         verify=DOMAIN_CRT, allow_redirects=False)
    while True:
        if resp.is_redirect:
            print(resp.headers['location'])
            qs = parse_qs(urlparse(resp.headers['location']).query)
            sessionID = qs['state'][0]
            input(
                "waiting for user login in browser, press enter to continue after getting a session ID")
            break
        elif resp.status_code == 410:
            print(resp.content.decode())
            AUTH_OBJ['newUser'] = "True"
            resp = requests.post(url+'/auth', data=AUTH_OBJ,
                                 verify=DOMAIN_CRT, allow_redirects=False)
            continue
        elif resp.status_code == 401:
            exit(resp.content.decode())
        else:
            sessionID = resp.text.split(":")[1]
            break
else: sessionID = SESSIONID
data = {
    'sessionID': sessionID,
}
type = int(input("\n1. Media\n2. Album\nChoose media type to retrieve: "))
if type == 1:
    data['type'] = 'media'

elif type == 2:
    resp = requests.post(url+'/listalbums', data=data,
                         verify=DOMAIN_CRT, allow_redirects=False)
    res = json.loads(resp.content)
    albums = [AlbumItem(x) for x in res['albums']]
    for i in range(len(albums)):
        print(f"({i+1}). {albums[i]}")
    albnum = int(input(f"({i+2}). All albums\nChoose album number:"))
    if albnum > len(albums)+1:
        exit("Invalid album number, please try again")
    data['type'] = 'album'
    data['albnum'] = albnum
else:
    exit("Invalid media type selected")
limit = input("Retrieve limit(Default=200): ")
limit = int(limit) if limit else ''
if INCLUDE_PHOTOS==None or INCLUDE_VIDEOS==None:
    includePhotos = False if input(
        "Include Photos(y/n Default=y): ").lower() in {"n", "no"} else True
    includeVideos = False if input(
        "Include Videos(y/n Default=y): ").lower() in {"n", "no"} else True
else:
    includePhotos = INCLUDE_PHOTOS
    includeVideos = INCLUDE_VIDEOS
pageToken = input("Page Token(Default=none): ").strip()
data['limit'] = limit
data['includePhotos'] = includePhotos
data['includeVideos'] = includeVideos
data['pageToken'] = pageToken
print("retrieving", data)
resp = requests.post(url+'/result', data=data,
                     verify=DOMAIN_CRT, allow_redirects=False)
resp = json.loads(resp.content)
mediaItems = [MediaItem(x) for x in resp['mediaItems']]
processingItems = [MediaItem(x) for x in resp['processingItems']]
result=''
result = downloader(mediaItems)
if len(result['failed'])!=0 or len(processingItems)!=0:
    with open('log.txt', 'w') as log:
        log.write(json.dumps(processingItems))
        log.write(json.dumps(result))
    print("Failed downloads logged in log.txt")
if resp.get('nextPageToken',False):
    print(f"Possible next page token: {resp['nextPageToken']}")