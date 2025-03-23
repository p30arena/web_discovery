import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function assessProfiles(): Promise<void> {
  const profiles = await prisma.profile.findMany();

  for (const profile of profiles) {
    const score = calculateProfileScore(profile);

    await prisma.assessmentScore.create({
      data: {
        profileId: profile.id,
        activityRecency: score.activityRecencyScore,
        followersAuthenticity: score.followersAuthenticityScore,
        profilePictureAuthenticity: score.profilePictureAuthenticity,
        bioExtractionCompleteness: score.bioExtractionCompleteness,
        productExtractionCompleteness: score.productExtractionCompleteness,
        productsCount: score.productsCount,
        productsToOtherPostsRatio: score.productsToOtherPostsRatio,
      },
    });
  }

  console.log(
    "Profiles successfully assessed and scores stored in the database."
  );
}

function calculateProfileScore(profile: any): any {
  // Placeholder logic for calculating scores based on profile data
  return {
    activityRecencyScore: 5, // Example score
    followersAuthenticityScore: 4,
    profilePictureAuthenticity: 3,
    bioExtractionCompleteness: 5,
    productExtractionCompleteness: 4,
    productsCount: 2,
    productsToOtherPostsRatio: 1,
  };
}

// Example usage
assessProfiles();
