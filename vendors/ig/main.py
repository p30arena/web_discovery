import os
import psycopg2
from dotenv import load_dotenv
from instagram import get_instagram_client, get_user_info

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def insert_profile(username, bio, followers, following, profile_picture_url, is_private):
    conn = connect_to_db()
    if conn is None:
        return

    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO profiles (username, bio, followers, following, profile_picture_url, is_private)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, bio, followers, following, profile_picture_url, is_private))

        conn.commit()
        print(f"Profile {username} inserted successfully.")

    except psycopg2.Error as e:
        print(f"Error inserting profile {username}: {e}")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    cl = get_instagram_client()
    user_info = get_user_info(cl, os.getenv("IG_ACCOUNT_USERNAME"))

    insert_profile(
        user_info.username,
        user_info.biography,
        user_info.follower_count,
        user_info.following_count,
        user_info.profile_pic_url,
        user_info.is_private
    )
