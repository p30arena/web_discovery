import axios from 'axios';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

const INSTAGRAM_API_URL = 'https://graph.instagram.com/v1/users/search'; // Update with the correct endpoint
const ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'; // Replace with your actual access token

async function searchProfiles(keyword: string, location: string) {
  try {
    const response = await axios.get(INSTAGRAM_API_URL, {
      params: {
        q: keyword,
        location: location,
        access_token: ACCESS_TOKEN,
      },
    });

    const profiles = response.data.data; // Adjust based on actual API response structure

    for (const profile of profiles) {
      await prisma.profile.create({
        data: {
          username: profile.username,
          bio: profile.bio,
          location: profile.location, // Ensure this is available in the API response
        },
      });
    }

    console.log('Profiles successfully stored in the database.');
  } catch (error) {
    console.error('Error searching profiles:', error);
  }
}

async function testSearch() {
  await searchProfiles('fashion', 'New York'); // Example parameters
}

testSearch();
