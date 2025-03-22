import os
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_USERNAME = os.getenv("IG_ACCOUNT_USERNAME")
ACCOUNT_PASSWORD = os.getenv("IG_ACCOUNT_PASSWORD")

cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)



user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
medias = cl.user_medias(user_id, 20)
