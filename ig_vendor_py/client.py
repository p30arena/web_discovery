import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")

cl = Client()
if os.access("session.json", mode=os.R_OK):
    session = cl.load_settings("session.json")
    if session:
        cl.set_settings(session)
try:
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    try:
        cl.get_timeline_feed() # check session
    except LoginRequired:
        print("Session is invalid, need to login via username and password")
        old_session = cl.get_settings()
        # use the same device uuids across logins
        cl.set_settings({})
        cl.set_uuids(old_session["uuids"])

        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    cl.dump_settings("session.json")
except Exception as e:
    print(f"Couldn't login user using session information: {e}")
    exit(-1)
