const variables = {
  data: {
    context: "blended",
    include_reel: "true",
    query: "مراقبت پوس",
    rank_token:
      "1742765024097|51488a32a5e721575033f81cb3ab885be79a0038f637ffc96f19b21a3406ea9c",
    search_surface: "web_top_search",
  },
  hasQuery: true,
};

fetch("https://www.instagram.com/graphql/query", {
  headers: {
    accept: "*/*",
    "accept-language": "en-US,en;q=0.9,ar;q=0.8,fa;q=0.7",
    "content-type": "application/x-www-form-urlencoded",
  },
  referrer:
    "https://www.instagram.com/reel/DHjNBFeswdY/?utm_source=ig_web_copy_link",
  referrerPolicy: "strict-origin-when-cross-origin",
  body: `av=17841441465513489&__d=www&__user=0&__a=1&__req=15&__hs=20170.HYP%3Ainstagram_web_pkg.2.1...1&dpr=2&__ccg=POOR&__rev=1021175318&__s=4kona0%3Ax4hwbz%3A34hk8g&__hsi=7485118350475369154&__dyn=7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8aUco2qwJyEiw9-1DwUx60p-0LVE4W0qa321Rw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2swtUd8-U2exi4UaEW2G0AEco4i5o2eUlwhEe88o5i7U1oEbUGdG1QwTU9UaQ0z8c86-3u2WE5B08-269wr86C1mwPwUQp1yUd8KUnAwCAK6E5y4UrwHwrE5SbBK4o&__comet_req=7&fb_dtsg=NAcNc2NDaCcbzC-wA1-so4O-2rTsV8Y_EIlJLJF--5SDevYIV7gEsgg%3A17865145036029998%3A1742737234&jazoest=25967&lsd=XzHRzQD19BLRhzwpQwEEmN&__spin_r=1021175318&__spin_b=trunk&__spin_t=1742764923&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisSearchBoxRefetchableQuery&variables=${encodeURIComponent(
    JSON.stringify(variables)
  )}&server_timestamps=true&doc_id=9346396502107496`,
  method: "POST",
  mode: "cors",
  credentials: "include",
})
  .then((r) => r.json())
  .then((x) => console.log(x));
