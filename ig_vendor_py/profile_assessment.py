import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List
from typing_extensions import Annotated
from datetime import datetime
from client import cl
from models import Profile, Assessment, Product
from peewee import DoesNotExist
import time
import argparse

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

class ProductInfo(BaseModel):
    product_name: str
    product_description: str
    price: str

class PostExtraction(BaseModel):
    products: List[ProductInfo]

class ActivityExtraction(BaseModel):
    activity: str

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
        prompt = f"What is the main activity or category of this Instagram profile? Answer with one word: {user_info.biography}"
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
    retries = 3
    media = []
    for i in range(retries):
        try:
            media = cl.user_medias(user_id, amount=5)  # Get the 5 latest posts
            break  # If successful, break the loop
        except Exception as e:
            print(f"Error fetching media (attempt {i+1}/{retries}): {e}")
            time.sleep(2)  # Wait for 2 seconds before retrying
    else:
        print("Failed to fetch media after multiple retries.")
        media = []

    product_info = []
    products = []
    for post in media:
        try:
            prompt = f"""
Extract the products attributes (name, description, and price) from the following Instagram post: {post.caption_text}. 
- If no products are mentioned, return an empty list (`[]`) for `products`.
- For each product, include all attributes (`product_name`, `product_description`, `price`).
- If an attribute is not available in the post, use `N/A` as the value.
- Do not omit any fields; all must be present in the output.
"""
            response = model.generate_content(prompt, generation_config={
                'response_mime_type': 'application/json',
                'response_schema': PostExtraction,
            })
            product_extraction: PostExtraction = PostExtraction.model_validate_json(response.text)
            products.extend(product_extraction.products)
            product_info.extend([p.model_dump() for p in product_extraction.products])
            for product in product_extraction.products:
                Product.create(
                    profile=profile,
                    product_name=product.product_name,
                    product_description=product.product_description,
                    price=product.price,
                )
        except Exception as e:
            print(f"LLM Product Extraction Error: {e}")
            print(post.caption_text)
            # TODO: Implement more robust error handling (e.g., logging, retrying)
            #products = []

    # Calculate scores based on the criteria in Overview.md
    # Activity Recency Score
    if media:
        latest_post_date = media[0].taken_at.replace(tzinfo=None)
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
    print(f"Profile Assessment: {assessment}")

    return assessment


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assess an Instagram profile.")
    parser.add_argument("username", type=str, help="The username of the profile to assess.")
    args = parser.parse_args()

    assess_profile(args.username)
