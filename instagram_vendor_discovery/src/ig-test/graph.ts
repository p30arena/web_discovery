const AccessToken =
  "IGAANcPcH8Bt5BZAE5uc2VPMzdnVTB0bmFIb3g1UFE3SkkybHFMeEFpTWlKVnBCUmRnMjRROURiZA215TzN5MEp5ZAHF0Tjg3Rzd1d180bTQxMlZAIQzd3RXN3ZAHpXR2hLd2ZA3ZAFpXMUtVd2s4b0xaa050dWUxWDZAUNERDVk1HZA1V6MAZDZD";
const Authorization = `Bearer ${AccessToken}`;

fetch(
  "https://graph.instagram.com/v22.0/me?fields=id,username,account_type,media_count,followers_count,follows_count,biography,website,profile_picture_url",
  {
    headers: {
      Authorization,
    },
  }
)
  .then((r) => r.json())
  .then((x) => console.log(x));

fetch(
  `https://graph.facebook.com/v22.0/ig_hashtag_search?user_id=17841441465513489&q=programming&access_token=${AccessToken}`,
  {
    headers: {
      Authorization,
    },
  }
)
  .then((r) => r.json())
  .then((x) => console.log(x));
