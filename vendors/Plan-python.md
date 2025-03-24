1. Database Setup: Set up a PostgreSQL database to store profile data, assessment scores, product information, and agent progress. Define database tables with appropriate schemas for each data type.
2. Implement Profile Search: Use the instagrapi lib to search for profiles based on keywords, location, and posts. Store the search results in the database.
3. Develop Profile Assessment Agent: For each profile in the database, check the bio, posts, and post quality. Calculate scores based on the criteria in Overview.md. Store the assessment scores in the database.
4. Extract Product Information: Extract product information from the bio and posts during profile assessment. Store the extracted product information in the database.
5. Need a FastAPI service, Expose both CLI and API access to the profile search and assessment tools.
6. Use Peewee for ORM
7. Use Types
8. Always Load Credentials, Configs, and Sensitive data from .env
9. Working directory is "ig_vendor_py"
10. Use LLM (Gemini Flash 2.0) for Profile Bio and Product Extraction
