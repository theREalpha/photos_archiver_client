# Photos Archiver Client

CLI Client to download media from google photos. More details at [pha.ovh](https://pha.ovh)\
A personal project to download media from google photos as their takeout takes ages to process and doesn't allow selectively downloading either only photos or videos.\
*(Is currently in testing mode as is a personal project, hence is rate limited and only allowed for `test users`. Contact me through email or by creating an Issue if you want to be added as a tester to use this script).*\
*Check out [photo_archiver](https://github.com/theREalpha/photo_archiver/) if you want to use a serverless service with your own API credentials, or wait for server release for this client to host your own server*

## Features

* <b>Media Download</b>:\
Allows download of media directly uploaded to google photos or media in specific album or from all albums present in the account.
    >Note: Currently doesn't support shared albums. Work around is showing shared albums within your albums by `Shared Album> Meatballs menu> Show in albums`
* <b>Selective Media download</b>:\
Supports Filtering based of Media Type (Photos/Videos). Can be set in `config.py` to skip being asked everytime program is run.
* <b>Multi-Threading</b>:\
Supports Multi-Threading to download media faster. Can be disabled through `config.py`
* <b>Limit and Offset</b>:\
The number of items to be downloaded can be limited by entering limit when prompted in terminal.
If there are more items than limit, program will output a `pageToken` for next `limit` number of items.\
The page token  can be entered when script is run again and prompted for page token.\
Note:
    >Limit has to stay constant b/w requests using page tokens.\
    >Download URLs expire within 1 hr from creation. It is recommended to set limit to lower amounts if you have slower internet speeds. (default is 200 to accomodate slower internet speeds and CPUs)

## Installation

Note: This module requires `requests` to be installed and is part of `requirements.txt`

```bash
# Clone the repository
git clone https://github.com/theREalpha/photos_archiver_client.git

# Navigate to the project directory
cd photos_archiver_client

# Install dependencies
pip install -r requirements.txt
```

## Usage
* App in testing mode and will stay in it unless notified. If you require access to the app, contact me through email or create an issue if you want to be added as a tester with your mail id for which you need access.
* For First time user's without a user account, register within the terminal or on webpage and create an account. (this account has no relation to your google account other than the fact that it is used to secure your refresh_token for continued access to the app).
* Once account is created, you can add details to the `config.py` file for automatic login. Leaving the details empty, users will be asked for credentials everytime program is run.
* You can populate the returned session id from response of login on [webpage]('https://pha.ovh/login') or from terminal after running the script in the `config.py` file to skip login process in terminal.
    > Note: SessionID will expire hence setting username and password in AUTH_OBJ in `config.py` is recommended.
* <details>
  <summary>example config.py</summary>
  
  ```python
    AUTH_OBJ = {
        "uname":"dummyUsesrname",
        "passw":"VeryDummyPassword",
        "newUser":"False"
        }
    SESSIONID = None

    PATH = 'downloads/'
    DOMAIN_CRT = 'ca_bundle.crt'

    INCLUDE_PHOTOS= True
    INCLUDE_VIDEOS= False

    VERBOSE = True
    MODONLY= True

    THREADING= True

    API_NAME = 'photoslibrary'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

    HOSTURL = 'pha.ovh'
    PORT = 443
    ```
</details>

* To use the program, run the command

```bash
# Run the project
python client.py
```

## Planned Features
* Maintaining db for media items retrieved through this script for future runs.
* Auto refreshing download URLs if they expire.

## 
Any suggestions or feedback, please create an issue on [github](https://github.com/theREalpha/photos_archiver_client/issues)
