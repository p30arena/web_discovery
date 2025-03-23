import os
from dotenv import load_dotenv
from client import cl
from models import Profile
from peewee import IntegrityError

load_dotenv()

ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD")


def search_profiles(keywords, location=None):
    results = []
    for keyword in keywords:
        users = cl.search_users_v1(keyword, 10)  # Limit to 10 users per keyword
        for user in users:
            try:
                user_info = cl.user_info(user.pk)
                profile = Profile.create(
                    username=user_info.username,
                    full_name=user_info.full_name,
                    profile_pic_url=user_info.profile_pic_url,
                    bio=user_info.biography,
                    external_url=user_info.external_url,
                    followers=user_info.follower_count,
                    following=user_info.following_count,
                    posts=user_info.media_count,
                )
                results.append(profile)
            except IntegrityError:
                # Profile already exists
                pass
    return results


if __name__ == "__main__":
    keywords = ["shop", "store", "fashion"]
    profiles = search_profiles(keywords)
    print(f"Found {len(profiles)} profiles.")
    for profile in profiles:
        print(profile.username)
