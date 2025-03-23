import { PrismaClient } from "@prisma/client";
import { extractProductInformation } from "./productInformation";

const prisma = new PrismaClient();

let paused = false;
let lastProcessedProfileId: number | null = null;

async function assessProfiles(): Promise<void> {
  let profiles = await prisma.profile.findMany();

  if (lastProcessedProfileId !== null) {
    console.log("Resuming from profile ID:", lastProcessedProfileId);
    profiles = profiles.filter(profile => profile.id > lastProcessedProfileId!);
  }

  for (const profile of profiles) {
    if (paused) {
      console.log("Assessment paused. Resuming from profile ID:", lastProcessedProfileId);
      return;
    }

    // Check if the profile has already been assessed
    const existingAssessment = await prisma.assessmentScore.findFirst({
      where: {
        profileId: profile.id,
      },
    });

    if (existingAssessment) {
      console.log("Profile already assessed, skipping:", profile.id);
      lastProcessedProfileId = profile.id;
      continue;
    }

    const score = await calculateProfileScore(profile);

    await prisma.assessmentScore.create({
      data: {
        profileId: profile.id,
        activityRecency: (await score).activityRecencyScore,
        followersAuthenticity: (await score).followersAuthenticityScore,
        profilePictureAuthenticity: (await score).profilePictureAuthenticity,
        bioExtractionCompleteness: (await score).bioExtractionCompleteness,
        productExtractionCompleteness: (await score).productExtractionCompleteness,
        productsCount: (await score).productsCount,
        productsToOtherPostsRatio: (await score).productsToOtherPostsRatio,
      },
    });

    lastProcessedProfileId = profile.id;
    console.log("Profile assessed:", profile.id);
  }

  console.log(
    "Profiles successfully assessed and scores stored in the database."
  );
}

function pause() {
  paused = true;
  console.log("Assessment paused. Last processed profile ID:", lastProcessedProfileId);
}

function resume() {
  paused = false;
  console.log("Assessment resumed from profile ID:", lastProcessedProfileId);
  assessProfiles();
}

async function calculateProfileScore(profile: any): Promise<any> {
  // Placeholder logic for calculating scores based on profile data
  const productInfo = await extractProductInformation(profile.bio + " " + profile.posts);
  const productExtractionCompleteness = productInfo.length > 0 ? 5 : 1; // Example score based on whether any product info was extracted

  return {
    activityRecencyScore: 5, // Example score
    followersAuthenticityScore: 4,
    profilePictureAuthenticity: 3,
    bioExtractionCompleteness: 5,
    productExtractionCompleteness: productExtractionCompleteness,
    productsCount: productInfo.length,
    productsToOtherPostsRatio: 1,
  };
}

// Example usage
async function main() {
  await assessProfiles();
}

main();

// Example of pausing and resuming
// setTimeout(() => {
//   pause();
//   setTimeout(() => {
//     resume();
//   }, 5000); // Resume after 5 seconds
// }, 10000); // Pause after 10 seconds
