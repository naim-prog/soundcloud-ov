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
    headers = {
        'Authorization': f'OAuth {o_auth}',
        "Accept": "application/json",
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }

    req = requests.get(f'https://api-v2.soundcloud.com/me?client_id={cli_id}', headers=headers)

    # Something went wrong
    if not req.status_code == 200:
        print(f"Trying to reach soundcloud you got a {req.status_code} status code")
        exit(1)

def make_scov(o_auth, cliend_id, lang_file):
    # Timestamp time in seconds
    actual_time_seconds = int(datetime.datetime.now().timestamp())
    # When a tracks was reproduced more than 1 year stop recording data
    stop_time_seconds   = actual_time_seconds - 31622400

    # Variables to dump on output
    total_reproduction_time = 0 # seconds

    if not os.path.isfile('template-output.json'):
        print("Couldn't found template output JSON")
        exit(1)

    with open('template-output.json', 'r') as f:
        ov_output_file = json.load(f)

    


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
