import os
from dotenv import load_dotenv
from models import create_tables, Profile, Assessment, Product
from peewee import IntegrityError

load_dotenv()

db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")

# Initialize database tables
from models import Profile, Assessment, Product
from models import db
db.drop_tables([Profile, Assessment, Product])
create_tables()

# Test data
try:
    profile = Profile.create(
        username="test_profile",
        full_name="Test Profile",
        bio="Test bio",
        followers=100,
        following=50,
        posts=20,
    )

    assessment = Assessment.create(
        profile=profile,
        activity_recency_score=0.8,
        followers_authenticity_score=0.9,
    )

    product = Product.create(profile=profile, name="Test Product", description="Test description")

    print("Database initialized and test data created successfully!")

except IntegrityError as e:
    print(f"Error creating test data: {e}")
