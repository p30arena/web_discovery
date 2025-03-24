import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from client import cl
from models import Profile, Assessment, Product
from peewee import DoesNotExist

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

class ProductInfo(BaseModel):
    product_name: str = Field(..., description="Name of the product")
    product_description: Optional[str] = Field(None, description="Description of the product")
    price: Optional[str] = Field(None, description="Price of the product")

class PostExtraction(BaseModel):
    products: List[ProductInfo] = Field(..., description="List of products extracted from the post")

class ActivityExtraction(BaseModel):
    activity: str = Field(..., description="Activity or category of the profile (e.g., beauty, fashion)")

def assess_profile(username):

    try:
        profile = Profile.get(Profile.username == username)
    except DoesNotExist:
        print(f"Profile {username} not found.")
        return

    user_id = cl.user_id_from_username(username)
    user_info = cl.user_info(user_id)

    # Use LLM to extract activity from the profile bio
    try:
        prompt = f"What is the main activity of this profile? Answer with one word: {user_info.biography}"
        response = model.generate_content(prompt, generation_config={
            'response_mime_type': 'application/json',
            'response_schema': ActivityExtraction,
        })
        activity = response.text.strip()
    except Exception as e:
        print(f"LLM Activity Extraction Error: {e}")
        # TODO: Implement more robust error handling (e.g., logging, retrying)
        activity = "Unknown"

    # Use LLM to extract product information from posts
    media = cl.user_medias(user_id, amount=5)  # Get the 5 latest posts
    product_info = []
    products = []
    for post in media:
        try:
            prompt = f"Extract product names and descriptions from the following text: {post.caption_text}"
            response = model.generate_content(prompt, generation_config={
                'response_mime_type': 'application/json',
                'response_schema': PostExtraction,
            })
            product_extraction: PostExtraction = PostExtraction.model_validate_json(response.text)
            products.extend(product_extraction.products)
            product_info.extend([p.model_dump() for p in product_extraction.products])
        except Exception as e:
            print(f"LLM Product Extraction Error: {e}")
            # TODO: Implement more robust error handling (e.g., logging, retrying)
            #products = []

    # Calculate scores based on the criteria in Overview.md
    # Activity Recency Score
    if media:
        latest_post_date = media[0].taken_at
        activity_recency_score = 1 / (1 + (datetime.now() - latest_post_date).days)
    else:
        activity_recency_score = 0.0

    # Followers Authenticity Score
    followers_authenticity_score = min(1, user_info.follower_count / 10000)  # Assuming 10k followers is a good start

    # Profile Picture Authenticity (Placeholder - needs LLM or image analysis)
    profile_picture_authenticity = 0.5  # Placeholder value

    # Bio Extraction Completeness
    bio_extraction_completeness = min(1, len(user_info.biography) / 100)  # Assuming 100 characters is a good bio

    # Product Extraction Completeness
    product_extraction_completeness = min(1, len(products) / 5)  # Assuming 5 products is good

    # Products Count
    products_count = len(products)

    # Products to Other Posts Ratio
    products_to_other_posts_ratio = products_count / len(media) if media else 0.0

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

    print(f"Profile {username} assessed successfully.")
    print(f"Activity: {activity}")
    print(f"Product information: {product_info}")


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assess an Instagram profile.")
    parser.add_argument("username", type=str, help="The username of the profile to assess.")
    args = parser.parse_args()

    assess_profile(args.username)
