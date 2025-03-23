import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config(); // Load environment variables from .env file
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

const INSTAGRAM_API_URL = 'https://graph.instagram.com/v1/users/search'; // Update with the correct endpoint
const ACCESS_TOKEN = process.env.ACCESS_TOKEN as string; // Read access token from environment variables


if (!ACCESS_TOKEN) {
    console.error('ACCESS_TOKEN is not defined. Please check your .env file.');
    process.exit(1); // Exit the process if the access token is not defined
}

async function searchProfiles(keyword: string, location: string) {
  try {
    console.log('Request parameters:', {
        q: keyword,
        location: location,
        access_token: ACCESS_TOKEN, // Remove extra quotes if present
    }); // Log request parameters

    const requestUrl = `${INSTAGRAM_API_URL}?q=${keyword}&location=${location}&access_token=${ACCESS_TOKEN}`;
    console.log('Request URL:', requestUrl); // Log the full request URL

    const response = await axios.get(requestUrl); // Corrected axios.get call

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
    const axiosError = error as any; // Type assertion to any
    console.error('Error searching profiles:', axiosError.message);
    if (axiosError.response) {
        console.error('Response status:', axiosError.response.status);
        console.error('Response data:', axiosError.response.data);
    }
  }
}

async function testSearch() {
  await searchProfiles('fashion', 'New York'); // Example parameters
}

testSearch();
