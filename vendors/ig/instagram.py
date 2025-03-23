import os
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_USERNAME = os.getenv("IG_ACCOUNT_USERNAME")
ACCOUNT_PASSWORD = os.getenv("IG_ACCOUNT_PASSWORD")


def get_instagram_client():
    cl = Client()
    try:
        cl.login(ACCOUNT_USERNAME, password=ACCOUNT_PASSWORD)
    except Exception as e:
        print(f"Error logging in: {e}")
        return None
    return cl


def get_user_info(client, username):
    user_id = client.user_id_from_username(username)
    user_info = client.user_info(user_id)
    return user_info


def search_profiles_by_keyword(client, keyword, count=20):
    try:
        users = client.search_users(keyword)
        return users[:count]  # Limit the number of results
    except Exception as e:
        print(f"Error searching users: {e}")
        return []
