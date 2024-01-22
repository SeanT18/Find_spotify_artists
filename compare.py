from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id= os.getenv("CLIENT_ID")
cliend_secret = os.getenv("CLIENT_SECRET")

# print(client_id, cliend_secret)

def get_token():
    auth_string = client_id + ":" + cliend_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8 ")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url,headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Gets artists information from spotify search API
def get_artists(token, artist_names):
    url = "https://api.spotify.com/v1/search"
    query = f"?q={artist_names}&type=artist&limit=1"
    query_url = url + query
    headers= get_auth_header(token)
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("no artist exists with this name")
        return 0
    return json_result[0]


def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

# This will gets the artist details that will be needed and sorts based on popularity
def organize_artist_data(names):

    # Gets information from each artist name and organizes it into a new array
    artist_info = []
    for name in names:
        result = get_artists(token, name)
        if result == 0:
            print(f"{name} does not exist")
            continue
        artist_name = result["name"]
        followers = result["followers"]["total"]
        popularity = result["popularity"]
        info = {"name":artist_name, "followers":followers, "popularity":popularity}
        artist_info.append(info)

    # Sorts the artists by the popularity key
    for i in range(len(artist_info)):
        for j in range(0, len(artist_info) - i - 1):
            if(artist_info[j]["popularity"] < artist_info[j+1]["popularity"]):
                temp = artist_info[j]
                artist_info[j] = artist_info[j+1]
                artist_info[j+1] = temp
    return artist_info

def print_artists(artist_info):
    for i in range(len(artist_info)):
        print(f"{artist_info[i]['name']} has {artist_info[i]['followers']} followers which gives a popularity rating of {artist_info[i]['popularity']}")

token = get_token()
names = []
print("Enter 3 artists:")
for i in range(3):
    name = input()
    names.append(name)


artist_info = organize_artist_data(names)
print_artists(artist_info)


