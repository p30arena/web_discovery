import dotenv from "dotenv";
dotenv.config(); // Load environment variables from .env file
import { PrismaClient } from "@prisma/client";
import { braveSearch } from "./brave";

const prisma = new PrismaClient();

async function searchProfiles(keyword: string, location: string) {
  try {
    const query = `site:instagram.com ${keyword} ${location}`;
    console.log("Search Query:", query);

    const data = await braveSearch(query);
    console.log("Brave Search API Response:", JSON.stringify(data, null, 2));

    // Extract profile information from the search results
    if (data && data.web.results.length > 0) {
      for (const result of data.web.results) {
        // Extract relevant information from the result
        const username = result.url.split("/")[3];
        const bio = result.description || "No bio available";
        const profileLocation = location;

        // Store the profile in the database
        await prisma.profile.create({
          data: {
            username: username,
            bio: bio,
            location: profileLocation,
          },
        });
      }
      console.log("Profiles successfully stored in the database.");
    } else {
      console.log("No profiles found.");
    }
  } catch (error) {
    console.error("Error searching profiles:", error);
  }
}

async function testSearch() {
  await searchProfiles("fashion", "New York");
}

testSearch();
