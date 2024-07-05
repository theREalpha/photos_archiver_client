## Authentication
# Leaving this empty, script will ask for credentials everytime its run
AUTH_OBJ = {
    'uname':"",             # 'uname' : "dummyUsesrname"
    "passw":"",             # 'passw' : "VeryDummyPassword"
    "newUser":"True"
    }
# SessionID can be retrieved by logining in the website and copying the sessionID from response
# or from terminal after running the script once
# Not recommended as SessionID will expire
SESSIONID = None

## PATHS
PATH = 'downloads/'
DOMAIN_CRT = 'ca_bundle.crt'

## Media Type Filter, None = ask everytime, True/False = auto read from config
INCLUDE_PHOTOS= None
INCLUDE_VIDEOS= None

## Logger Module
# Set VERBOSE to True if you want to see all the logs, and MODONLY to True if you want to see only this module's verbose logs (MODONLY is set at level 11)
VERBOSE = False
MODONLY= True

## Threading settings
THREADING= True

### DONOT CHANGE FROM HERE (unless you spin your own server)

## API Settings
API_NAME = 'photoslibrary'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

## Authentication Server details
HOSTURL = 'pha.ovh'
PORT = 443