import requests
import pandas as pd
import numpy as np
import os

CLIENT_ID = '***'
CLIENT_SECRET = '***'

AUTH_URL = "https://accounts.spotify.com/api/token"
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})
auth_response_data = auth_response.json()

access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
BASE_URL = 'https://api.spotify.com/v1/'
#r = requests.get(BASE_URL + 'search?q=tania%20bowra&type=artist', headers=headers)

playlist_id = input("What is the link of the public playlist?: ")
playlist_id = playlist_id.split("https://open.spotify.com/playlist/")
playlist_id = playlist_id[1].split("?si=")
playlist_id = playlist_id[0]
#print(playlist_id)

array_songs = []
array_artist = []

def getSongs(i): 
    playlist_request = 'playlists/{playlistID}/tracks?fields=items(added_by.id%2C%20track(name, artists))&limit=100&offset=' + str(i) #For some reason only gets 100 songs
    playlist_request = playlist_request.replace("{playlistID}", playlist_id)
    r = requests.get(BASE_URL + playlist_request, headers=headers)
    r = r.json()
    #print(r)

    df = pd.DataFrame.from_dict(r)
    #print(df.head)
    array = df.to_numpy()

    if len(array) != 0:
        #print(array)
        for e in array:
            d = np.array2string(e)
            #print(d)
            d = d.split('\'artist\'')
            artist = d[0]
            song = d[len(d)-1]
            #print(song)
            if song.rfind('\"') > song.rfind('\''):
                song = song.split('\'name\': \"')
                song = song[1].split('\"}}]')
                array_songs.append(song[0])
                #print(d[0])
            else:
                song = song.split('\'name\': \'')
                song = song[1].split('\'}}]')
                array_songs.append(song[0])
                #print(d[0])
            artist = artist.split('\'name\': ')
            artist = artist[1]
            if artist.find('\"') > -1:
                artist = artist.split('\", \'type\':')
                artist = artist[0].split('\"')
                array_artist.append(artist[1])
                #print(d[0])
            else:
                artist = artist.split('\', \'type\':')
                artist = artist[0].split('\'')
                array_artist.append(artist[1])
                #print(d[0])
        getSongs(int(i + 100))
    
getSongs(000)


#print(array_artist)

folder = input("What folder you want to save the data?: ")
#df2 = pd.DataFrame(np.array(array2), columns=["songs"])
df2 = pd.DataFrame({'song': array_songs, 'artist': array_artist}, columns=['song', 'artist'])
df2.to_csv(folder + '\\out.csv')  

