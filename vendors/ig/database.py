import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Database credentials (replace with your actual credentials)
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


def create_tables():
    conn = connect_to_db()
    if conn is None:
        return

    cur = conn.cursor()

    # Define tables
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                bio TEXT,
                followers INTEGER,
                following INTEGER,
                profile_picture_url TEXT,
                is_private BOOLEAN
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS profile_scores (
                id SERIAL PRIMARY KEY,
                profile_id INTEGER REFERENCES profiles(id),
                activity_recency_score INTEGER,
                followers_authenticity_score INTEGER,
                profile_picture_authenticity INTEGER,
                bio_extraction_completeness INTEGER,
                product_extraction_completeness INTEGER,
                products_count INTEGER,
                products_to_other_posts_ratio INTEGER
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                profile_id INTEGER REFERENCES profiles(id),
                name VARCHAR(255),
                description TEXT,
                price DECIMAL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS agent_state (
                id SERIAL PRIMARY KEY,
                agent_name VARCHAR(255) UNIQUE NOT NULL,
                last_processed_profile INTEGER,
                current_search_query TEXT,
                is_paused BOOLEAN DEFAULT FALSE
            )
        """)

        conn.commit()
        print("Tables created successfully.")

    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")

    finally:
        cur.close()
        conn.close()


def calculate_activity_recency_score():
    # Implement logic to calculate activity recency score
    pass


def calculate_followers_authenticity_score():
    # Implement logic to calculate followers authenticity score
    pass


def calculate_profile_picture_authenticity():
    # Implement logic to calculate profile picture authenticity
    pass


def calculate_bio_extraction_completeness():
    # Implement logic to calculate bio extraction completeness
    pass


def calculate_product_extraction_completeness():
    # Implement logic to calculate product extraction completeness
    pass


def calculate_products_count():
    # Implement logic to calculate products count
    pass


def calculate_products_to_other_posts_ratio():
    # Implement logic to calculate products to other posts ratio
    pass


if __name__ == '__main__':
    create_tables()
