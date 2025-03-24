import os
from dotenv import load_dotenv
import google.generativeai as genai
from client import cl
from models import Profile, Assessment, Product
from peewee import DoesNotExist

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def assess_profile(username):

    try:
        profile = Profile.get(Profile.username == username)
    except DoesNotExist:
        print(f"Profile {username} not found.")
        return

    user_id = cl.user_id_from_username(username)
    user_info = cl.user_info(user_id)

    # Use LLM to extract information from the profile bio
    prompt = f"Extract product information from the following bio: {user_info.biography}"
    response = model.generate_content(prompt)
    product_info = response.text

    # Calculate scores based on the criteria in Overview.md
    activity_recency_score = 0.0  # Implement logic to calculate this
    followers_authenticity_score = 0.0  # Implement logic to calculate this
    profile_picture_authenticity = 0.0  # Implement logic to calculate this
    bio_extraction_completeness = 0.0  # Implement logic to calculate this
    product_extraction_completeness = 0.0  # Implement logic to calculate this
    products_count = 0  # Implement logic to calculate this
    products_to_other_posts_ratio = 0.0  # Implement logic to calculate this

    assessment = Assessment.create(
        profile=profile,
        activity_recency_score=activity_recency_score,
        followers_authenticity_score=followers_authenticity_score,
        profile_picture_authenticity=profile_picture_authenticity,
        bio_extraction_completeness=bio_extraction_completeness,
        product_extraction_completeness=product_extraction_completeness,
        products_count=products_count,
        products_to_other_posts_ratio=products_to_other_posts_ratio,
    )

    # Extract product information from posts using LLM
    # Implement logic to extract product information from posts

    print(f"Profile {username} assessed successfully.")
    print(f"Product information: {product_info}")


if __name__ == "__main__":
    # Example usage: assess a profile
    assess_profile("store")
