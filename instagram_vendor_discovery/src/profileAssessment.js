"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const client_1 = require("@prisma/client");
const prisma = new client_1.PrismaClient();
function assessProfiles() {
    return __awaiter(this, void 0, void 0, function* () {
        const profiles = yield prisma.profile.findMany();
        for (const profile of profiles) {
            const score = calculateProfileScore(profile);
            yield prisma.assessment.create({
                data: {
                    profileId: profile.id,
                    activityRecencyScore: score.activityRecencyScore,
                    followersAuthenticityScore: score.followersAuthenticityScore,
                    profilePictureAuthenticity: score.profilePictureAuthenticity,
                    bioExtractionCompleteness: score.bioExtractionCompleteness,
                    productExtractionCompleteness: score.productExtractionCompleteness,
                    productsCount: score.productsCount,
                    productsToOtherPostsRatio: score.productsToOtherPostsRatio,
                },
            });
        }
        console.log('Profiles successfully assessed and scores stored in the database.');
    });
}
function calculateProfileScore(profile) {
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
