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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const axios_1 = __importDefault(require("axios"));
const client_1 = require("@prisma/client");
const prisma = new client_1.PrismaClient();
const INSTAGRAM_API_URL = 'https://graph.instagram.com/v1/users/search'; // Update with the correct endpoint
const ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'; // Replace with your actual access token
function searchProfiles(keyword, location) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield axios_1.default.get(INSTAGRAM_API_URL, {
                params: {
                    q: keyword,
                    location: location,
                    access_token: ACCESS_TOKEN,
                },
            });
            const profiles = response.data.data; // Adjust based on actual API response structure
            for (const profile of profiles) {
                yield prisma.profile.create({
                    data: {
                        username: profile.username,
                        bio: profile.bio,
                        location: profile.location, // Ensure this is available in the API response
                    },
                });
            }
            console.log('Profiles successfully stored in the database.');
        }
        catch (error) {
            console.error('Error searching profiles:', error);
        }
    });
}
function testSearch() {
    return __awaiter(this, void 0, void 0, function* () {
        yield searchProfiles('fashion', 'New York'); // Example parameters
    });
}
testSearch();
