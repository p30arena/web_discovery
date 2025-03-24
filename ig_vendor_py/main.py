import fastapi
import typer
from typing import Optional
from dotenv import load_dotenv
import profile_search
import profile_assessment

load_dotenv()

app = fastapi.FastAPI()
cli = typer.Typer()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search")
def search_profiles(keyword: str, location: Optional[str] = None):
    # Integrate profile_search logic here
    results = profile_search.search_profiles([keyword], location)
    return results

@app.get("/assess/{username}")
def assess_profile(username: str):
    # Integrate profile_assessment logic here
    results = profile_assessment.assess_profile(username)
    return results

@cli.command()
def search(keyword: str, location: Optional[str] = None):
    """
    Search for profiles based on keyword and location.
    """
    results = profile_search.search_profiles([keyword], location)
    print(results)

@cli.command()
def assess(profile_id: str):
    """
    Assess a profile by ID.
    """
    results = profile_assessment.assess_profile(profile_id)
    print(results)

if __name__ == "__main__":
    cli()
    # uvicorn.run(app, host="0.0.0.0", port=8000) # commented out to avoid blocking CLI
