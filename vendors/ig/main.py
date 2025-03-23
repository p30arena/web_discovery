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


def calculate_activity_recency_score():
    # Implement logic to calculate activity recency score
    return 5  # Placeholder value


def calculate_followers_authenticity_score():
    # Implement logic to calculate followers authenticity score
    return 7  # Placeholder value


def calculate_profile_picture_authenticity():
    # Implement logic to calculate profile picture authenticity
    return 8  # Placeholder value


def calculate_bio_extraction_completeness():
    # Implement logic to calculate bio extraction completeness
    return 9  # Placeholder value


def calculate_product_extraction_completeness():
    # Implement logic to calculate product extraction completeness
    return 6  # Placeholder value


def calculate_products_count():
    # Implement logic to calculate products count
    return 3  # Placeholder value


def calculate_products_to_other_posts_ratio():
    # Implement logic to calculate products to other posts ratio
    return 4  # Placeholder value


if __name__ == "__main__":
    # Create a placeholder profile
    insert_profile(
        "placeholder_profile",
        "This is a placeholder profile.",
        100,
        50,
        "https://example.com/placeholder.jpg",
        False
    )

    # Get the profile ID of the placeholder profile
    conn = connect_to_db()
    if conn is None:
        exit()

    cur = conn.cursor()
    cur.execute("SELECT id FROM profiles WHERE username = 'placeholder_profile'")
    profile_id = cur.fetchone()[0]
    cur.close()
    conn.close()

    # Calculate the profile scores
    activity_recency_score = calculate_activity_recency_score()
    followers_authenticity_score = calculate_followers_authenticity_score()
    profile_picture_authenticity = calculate_profile_picture_authenticity()
    bio_extraction_completeness = calculate_bio_extraction_completeness()
    product_extraction_completeness = calculate_product_extraction_completeness()
    products_count = calculate_products_count()
    products_to_other_posts_ratio = calculate_products_to_other_posts_ratio()

    # Insert the profile scores into the database
    conn = connect_to_db()
    if conn is None:
        exit()

    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO profile_scores (profile_id, activity_recency_score, followers_authenticity_score, profile_picture_authenticity, bio_extraction_completeness, product_extraction_completeness, products_count, products_to_other_posts_ratio)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (profile_id, activity_recency_score, followers_authenticity_score, profile_picture_authenticity, bio_extraction_completeness, product_extraction_completeness, products_count, products_to_other_posts_ratio))

        conn.commit()
        print("Profile scores inserted successfully.")

    except psycopg2.Error as e:
        print(f"Error inserting profile scores: {e}")

    finally:
        cur.close()
        conn.close()
