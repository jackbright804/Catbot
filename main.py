# Create a project and enable the photos api on google cloud platform
# Create an OAuth 2.0 Client ID from the APIs & Services > Credentials page on console.cloud.google.com and download it as json, name it credentials.json

# Import
from urllib import request
from googleScript import Create_Service
import os
import requests


# Globals
# Your google photos api credentials file goes here
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'photoslibrary'
VERSION_NUMBER = 'v1'
TARGET_ABLUM = 'Baby'
# Scope with max permissions, except album sharing
SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, VERSION_NUMBER, SCOPES)

# Get album ID of my cat's album
albums = service.albums().list().execute()
albumsList = albums.get('albums')
calvyAlbum = albumsList['title' == TARGET_ABLUM]
calvyAlbumId = calvyAlbum['id']

# Get list of photos in cat's album
photos = service.mediaItems().search(
    body={'albumId': calvyAlbumId, 'pageSize': 1}).execute()['mediaItems']
# Get URL of latest cat photo
latestPhotoUrl = photos[0]['baseUrl']

# Download the most recent photo
destinationFolder = './photos'
fileName = photos[0]['filename']
response = requests.get(latestPhotoUrl)
with open(os.path.join(destinationFolder, fileName), 'wb') as file:
    file.write(response.content)
    file.close()
