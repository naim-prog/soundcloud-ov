import sys
import os
import json
import datetime
import argparse
import requests


def meet_requirements():

    try:
        import requests
    except ImportError:
        print("Couldn't import 'requests'. Before running this script run 'pip install -r requirements.txt'")
        exit(1)


def try_oauth_and_cli_id(o_auth, cli_id):
    headers_req = {
        'Authorization': f'OAuth {o_auth}',
        "Accept": "application/json",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }

    req = requests.get(f'https://api-v2.soundcloud.com/me?client_id={cli_id}', headers=headers_req)

    # Something went wrong
    if not req.status_code == 200:
        print(f"Trying to reach soundcloud you got a {req.status_code} status code")
        exit(1)


def template_output_json():
    return {
        "artists": {
            "0": {
                "artist_name": "artist_name",
                "times_reproduced": 0
            }
        },
        "tracks": {
            "0": {
                "number_of_repros": 0,
                "track_name": "track_name",
                "artist_name": "artist_name"
            }
        },
        "total_reproduction_time": 0,
        "number_of_genres": 0,
        "most_played_genre": "genre"
    }


def make_html(ov_output):
    # Make the HTML
    with open("result.json", "w") as f:
        json.dump(ov_output, f, indent=4)

    # Exit the program
    exit(0)


def make_scov(o_auth, cliend_id, lang_file):
    # Header for requests
    headers_req = {
        'Authorization': f'OAuth {o_auth}',
        "Accept": "application/json",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }

    # Timestamp time in seconds
    actual_time_seconds = int(datetime.datetime.now().timestamp())
    # When a tracks was reproduced more than 1 year (- 1 day) stop recording data
    stop_time_seconds   = actual_time_seconds - 31536000

    ov_output_file = template_output_json()

    # First request is with this, from here till the end is necesary to use
    # the next_href that api provide so you dont lost any track
    # Requests to play history 30 tracks
    request_play_history = dict(requests.get(f'https://api-v2.soundcloud.com/me/play-history/tracks?client_id={cliend_id}&limit=30', headers=headers_req).json())
    
    while(True):

        # Iterate over the 30 tracks
        for track in request_play_history.get('collection'):
            # If was reproduced before stop_time_seconds make the HTML result
            if track.get('played_at') < stop_time_seconds:
                make_html(ov_output_file)

            # Add the duration to the total time (seconds)
            track_duration = int(track.get('track').get('duration')/1000)
            ov_output_file.update({'total_reproduction_time': ov_output_file.get('total_reproduction_time') + track_duration})

            # Variables to make code cleaner
            actual_track_id  = str(track.get('track_id'))
            actual_artist_id = str(track.get('track').get('user').get('id'))

            # -------------------------------- TRACK INFO --------------------------------

            # If track is on the dict update it; if not add it
            if ov_output_file.get('tracks').get(actual_track_id):
                # Number of repros track_id
                number_repros = ov_output_file.get('tracks').get(actual_track_id).get('number_of_repros') + 1
                # Update number of repros
                ov_output_file.get('tracks').update({actual_track_id: {'number_of_repros': number_repros}})

            # First time the track appear
            else:
                dict_update = {
                    'number_of_repros': 1,
                    'track_name': track.get('track').get('title'),
                    'artist_name': track.get('track').get('user').get('full_name')
                }

                ov_output_file.get('tracks').update({actual_track_id: dict_update})

            # -------------------------------- ARTIST INFO --------------------------------

            # Artist is already in the json
            if ov_output_file.get('artists').get(actual_artist_id):
                # Increment the number of times reproduced
                times_reproduced = ov_output_file.get('artists').get(actual_artist_id).get("times_reproduced")
                ov_output_file.get('artists').get(actual_artist_id).update({"times_reproduced": times_reproduced + 1})

            # First time of this artist
            else:
                ov_output_file.get('artists').update({actual_artist_id: {"times_reproduced": 1, "artist_name": track.get('track').get('user').get('full_name')}})

        # If URL is None make the HTML json
        if request_play_history.get('next_href') == None:
            make_html(ov_output_file)

        # We request the next tracks behind the last of this 30 tracks
        request_play_history = dict(requests.get(request_play_history.get('next_href'), headers=headers_req).json())
        

if __name__ == "__main__":

    # First we need to check that we have all the requirements installed
    meet_requirements()

    # Prepare to parse the arguments
    parser = argparse.ArgumentParser(description='Make a year OverView of your songs and artists')
    parser.add_argument('-o', '--o-auth', help='O-Auth Token for Soundcloud requests', type=str)
    parser.add_argument('-i', '--client-id', help='Client ID for Soundcloud requests', type=str)
    parser.add_argument('-l', '--lang', help='Language of the output OverView', type=str, default='en')

    # Parse args
    args = parser.parse_args(sys.argv[1:])

    # Try if o-auth and client id works
    try_oauth_and_cli_id(args.o_auth, args.client_id)

    # Open lang file
    if os.path.isfile(f'langs/{args.lang}.json'):
        lang_file = open(f'langs/{args.lang}.json', 'r')
        lang_file = json.load(lang_file)
    else:
        print("This language is not supported yet sorry.\nIf you want to translate to this language help me here: https://github.com/naim-prog/soundcloud-ov")
        exit(1)

    # Make the OV
    make_scov(args.o_auth, args.client_id, lang_file)
