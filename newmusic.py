import os
import sys
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
from difflib import SequenceMatcher
from pprint import pprint
from time import sleep
import re
import random

sys.path.insert(0, r"C:\Dropbox (RC)\Apps")

from dotenv import load_dotenv
load_dotenv()



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# instrumental, tribute
"""
FIRST SET UP ENVIRONMENT VARIABLES ON YOUR COMPUTER
https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10
SPOTIPY_CLIENT_ID = 
SPOTIPY_CLIENT_SECRET =
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'

Download git:
https://git-scm.com/download/win

AND RESTART THE COMPUTER

Then fix spotipy like this:
pip install git+https://github.com/plamere/spotipy.git --upgrade


"""

"""
sign ins
"""
print("signing into spotify...")
# spotify

user = os.environ["SPOTIFY_USER"]
playlist_id = os.environ["ULTIMATE_PLAYLIST_ID"]
scope = "playlist-modify-private, playlist-modify-public, user-library-read, playlist-read-private, user-library-modify"

try:
    token = util.prompt_for_user_token(
        user, redirect_uri="http://localhost:8080", scope=scope
    )  #'http://localhost/')
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{user}")
    token = util.prompt_for_user_token(
        user, redirect_uri="http://localhost:8080", scope=scope
    )

if token:
    spotify = spotipy.Spotify(auth=token)
    # results = spotify.search('weezer')
    # print(results)

# print(soup)



def classicSpotify():
    classicsList = []
    """
    classic spotify Playlists
    """
    cp = {"id": "37i9dQZF1DX3LDIBRoaCDQ", "max": "5"}  # classic punk 500k
    ea = {"id": "37i9dQZF1DXdTCdwCKzXwo", "max": "5"}  # early alt 250k
    ao60s = {
        "id": "37i9dQZF1DXaKIA8E7WcJj",
        "max": "5",
    }  # early alt 250k   spotify:user:spotify:playlist:
    alt80s = {
        "id": "37i9dQZF1DWTSKFpOdYF1r",
        "max": "5",
    }  # early alt 250k   spotify:user:spotify:playlist:
    alt00s = {"id": "37i9dQZF1DX0YKekzl0blG", "max": "2"}  # :
    # alt10s = {'id': '37i9dQZF1DX873GaRGUmPl'} #
    
    # favalbums = {"id": "6Kc6fUaWTyN8hhNe9a2iZm", "max": "3"}
    
    allOut50s = {"id": "37i9dQZF1DWSV3Tk4GO2fq", "max": "5"}

    playlist_list = [
        cp,
        ea,
        ao60s,
        alt80s,
        alt00s,
        allOut50s,
    ]
    # playlist_list = [favalbums]

    print(
        f"looking up spotify track_ids for the classic spotify playlists...{playlist_list}"
    )

    for playlist in playlist_list:
        tempclassicsList = []
        # print(playlist)

        max = playlist["max"]
        # print(max)
        # sys.exit()

        # get the results for every song in the playlist
        results = spotify.user_playlist_tracks(
            user, playlist["id"], "items(track(id))"
        )
        # pprint(results)

        # unless you're intentionally limiting the
        length = len(results["items"])

        my_randoms = random.sample(
            range(1, length), int(max)
        )  # a list of max numbers between 0 and the length of the playlist results

        # print(my_randoms)
        #
        # print(max)
        # counter = 0
        # sys.exit()
        # # extract the trackids for every song in the playlist from results
        for randomTrackNumber in my_randoms:
            track_id = results["items"][randomTrackNumber]["track"][
                "id"
            ]  # ['album']['id']
            # print(track_id)

            tempclassicsList.append(track_id)
            # counter = counter + 1
            # print(len(spotify_song_list))

        # makes sure there are no more than 50 songs from any classics playlist
        # the 50 limit will crash the program if any of these playlists have fewer than 50 tracks.
        # tempclassicsList = random.sample(tempclassicsList, 25)

        # adds the songs from the particular playlist to the full classic playlist
        classicsList = classicsList + tempclassicsList
        # print(len(classicsList))

    # pprint(classicsList)
    # print(len(classicsList))

    # pare the classic list down to 25
    # classicsList = random.sample(classicsList, 25)
    # print(classicsList)
    # sys.exit()

    return classicsList


def getSpotifySongsFromPlaylist(playlistId, quantity):

    spotifyList = []

    playlist = {"id": playlistId, "quantity": quantity}

    print(f"looking up spotify track_ids for the spotify playlists...{playlistId}")

    # get the results for every song in the playlist
    results = spotify.user_playlist_tracks(user, playlist["id"], "items(track(id))")
    # pprint(results)

    # unless you're intentionally limiting the
    length = len(results["items"])

    my_randoms = random.sample(
        range(1, length), int(quantity)
    )  # a list of max numbers between 0 and the length of the playlist results

    # # extract the trackids for every song in the playlist from results
    for randomTrackNumber in my_randoms:

        track_id = results["items"][randomTrackNumber]["track"]["id"]  # ['album']['id']

        spotifyList.append(track_id)

    return spotifyList





# no limit
def spotifyLookup(no_feat_list):
    print("looking up spotify track_ids for radio songs and itunes songs...")
    kworb_song_list = []
    for song in no_feat_list:
        try:
            result = spotify.search(song)
            # pprint(result)
            track_id = result["tracks"]["items"][0]["id"]
            kworb_song_list.append(track_id)
        except:
            print("spotify not responding....wait 1 secs")
            sleep(0.5)
    # pprint(kworb_song_list)
    # print(len(kworb_song_list))
    # sys.exit()

    return kworb_song_list




def removePlaylists(track_id_list):

    """
    remove rap and r&b..
    get all the track ids from rap caviar and are and be..
    check against track id list. bam..
    """

    bad_playlists = [
        "37i9dQZF1DX4SBhb3fqCJd",
        "37i9dQZF1DX0XUsuxWHRQd",
    ]  # are and be, rapcaviar

    rcav_track_ids = []

    for playlist in bad_playlists:

        results = spotify.user_playlist_tracks(
            user, playlist, "items(track(id))", limit=25
        )  # [:35]
        # pprint(results)
        max = len(results["items"])
        counter = 0
        while counter < max:
            track_id = results["items"][counter]["track"]["id"]  # ['album']['id']
            # pprint(track_id)
            rcav_track_ids.append(track_id)
            counter = counter + 1

    print("rcav_track_ids", len(rcav_track_ids))
    pprint(rcav_track_ids)

    track_id_listNORAP = [x for x in track_id_list if x not in rcav_track_ids]

    # pprint(track_id_listNORAP)

    # 4T3fNx3CgwDRRYgmFCbD4J

    # 6zeeWid2sgw4lap2jV61PZ

    return track_id_listNORAP


def newSpotify():

    """
    Newer music Spotify Playlists
    """

    spotify_song_list = []

    # max = how many songs will be picked at random from the top 30 of each playlist

    tth = {"id": "37i9dQZF1DXcBWIGoYBM5M", "max": "5"}  # 25 MILLION today's top hits
    nmf = {"id": "37i9dQZF1DX4JAvHpjipBk", "max": "1"}  # new music friday
    usv = {"id": "37i9dQZEVXbKuaTI1Z1Afx", "max": "1"}  # us viral

    hc = {"id": "37i9dQZF1DX1lVhptIYRda", "max": "1"}  # 5.2 MILLION hot country

    rt = {"id": "37i9dQZF1DXcF6B6QPhFDv", "max": "2"}  # 4.5 MILLION rock this

    ui = {"id": "37i9dQZF1DX2Nc3B70tvx0", "max": "2"}  # 2 MILLION ultimate indie
    ani = {"id": "37i9dQZF1DXdbXrPNafg9d", "max": "2"}  # 875k all new indie 1 mill
    loc = {"id": "37i9dQZF1DXdwmD5Q7Gxah", "max": "1"}  # 300K left of center

    # tna = the new alt 800K.  doesn't seem to be ordered.

    playlist_list = [tth, nmf, usv, loc, hc, ani, ui, rt]
    print(f"looking up spotify track_ids for the spotify playlists...{playlist_list}")

    for playlist in playlist_list:

        results = spotify.user_playlist_tracks(
            user, playlist["id"], "items(track(id))"
        )  # , playlist['max']) #[:35]
        # pprint(results)

        # this sets "max" according to the 'max' in the corresponding max in the dicts above.  2, 10 , etc
        max = playlist["max"]
        # print(max)

        my_randoms = random.sample(
            range(1, 31), int(max)
        )  # a list of random numbers which will correspond to the top 30 of the playlist. length of the list is max.

        # print(my_randoms)

        length = len(my_randoms)
        #
        # counter = 0

        for randomTrackNumber in my_randoms:
            # while counter < length:
            try:
                track_id = results["items"][randomTrackNumber]["track"][
                    "id"
                ]  # ['album']['id']
                # print(playlist, hc)
                if playlist == hc:
                    # print('matched')
                    countrySongId = track_id
                    # print('countrySongId', countrySongId)
                # pprint(track_id)
                spotify_song_list.append(track_id)
            except:
                pass
            # counter = counter + 1
            # print(len(spotify_song_list))
    # pprint(spotify_song_list)
    # print(len(spotify_song_list))
    return spotify_song_list, countrySongId


def getFact():
    # get the random fact
    with open(r'C:\Dropbox (RC)\Apps\kyoko\randomfacts.txt', 'r+', encoding='utf-8') as file:
        randomFactList = file.readlines()
    fact = random.choice(randomFactList).strip()
    fact = re.sub(r'^\d{1,3}\.', '', fact)

    return fact


def postDescription():
    # post a new playlist description
    fact = ''
    while fact == '':
        
        fact = getFact()
        # print(fact)

    # boilerplate = "These are the songs I'm checking out today. I update this playlist every day."
    description = fact# + '...............' + boilerplate
    # print(description)

    """ MUST UPDATE SPOTIPY LIKE THIS:
    https://stackoverflow.com/questions/47028093/attributeerror-spotify-object-has-no-attribute-current-user-saved-tracks
    """
    spotify.user_playlist_change_details(user, playlist_id, description=description)


def getPlaylistIdByName(name):
    print(f"looking up spotify playlist ids for playlist name {name}...")
    try:
        result = spotify.search(name, type="playlist")
        pprint(result)
        id = result["playlists"]["items"][0]["id"]
    except:
        print("spotify not responding....wait 1 secs")
        sleep(0.5)
    return id


def main(data):

    track_id_list = []
    pprint(data)
    for row in data:
        playlistId = getPlaylistIdByName(row["name"])
        quantity = row["quantity"]
        # get some songs from suzy's song playlist
        track_id_list = getSpotifySongsFromPlaylist(playlistId, quantity) + track_id_list


    print(len(track_id_list))
    
    # # remove songs that happen to be in banned playlists (such as rap playlists)
    # track_id_list = removePlaylists(track_id_list)
    # # get rid of tracks and artist you've marked as banned, either in your 'ban' playlist or your ban spreadsheet
    # track_id_list = removeBanned(track_id_list)
    # # get rid of most rap, based on spotify genre
    # track_id_list = removeGenres(track_id_list)

    # print(len(track_id_list))

    print("\nprinting to spotify playlist")    
        
    # # raondomize the order, making sure beethoven isn't in the first 20
    # # and country song isn't in the first 15
    # while (
    #         (
    #             (beethovenByAshkenazy[0] in track_id_list) and 
    #             (track_id_list.index(beethovenByAshkenazy[0]) <20)
    #         ) or 
    #         (
    #             (countrySongId in track_id_list) and 
    #             (track_id_list.index(countrySongId) <15)
    #         )
    #         ):
    random.shuffle(track_id_list)
    

    # pprint(finalList)

    # print to spotify
    spotify.user_playlist_replace_tracks(
        user, playlist_id, track_id_list
    )

    # print("kworb_song_list= ", len(kworb_song_list))
    # print("spotify_song_list= ", len(spotify_song_list))
    # print("classicsList= ", len(classicsList))
    # print("track_id_list= ", len(track_id_list))

    # change the playlist description to a random fact
    postDescription()

    return playlist_id

if __name__ == "__main__":



    main(rows)
