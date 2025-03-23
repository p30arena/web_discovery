import axios from "axios";

interface Query {
  original: string;
  show_strict_warning: boolean;
  is_navigational: boolean;
  is_news_breaking: boolean;
  spellcheck_off: boolean;
  country: string;
  bad_results: boolean;
  should_fallback: boolean;
  postal_code: string;
  city: string;
  header_country: string;
  more_results_available: boolean;
  state: string;
}

interface Main {
  type: string;
  index: number;
  all: boolean;
}

interface Mixed {
  type: string;
  main: Main[];
  top: any[];
  side: any[];
}

interface Profile {
  name: string;
  url: string;
  long_name: string;
  img: string;
}

interface MetaUrl {
  scheme: string;
  netloc: string;
  hostname: string;
  favicon: string;
  path: string;
}

interface Thumbnail {
  src: string;
  original: string;
  logo: boolean;
}

interface Result {
  title: string;
  url: string;
  is_source_local: boolean;
  is_source_both: boolean;
  description: string;
  page_age?: string;
  profile: Profile;
  language: string;
  family_friendly: boolean;
  type: string;
  subtype: string;
  is_live: boolean;
  meta_url: MetaUrl;
  thumbnail?: Thumbnail;
  age?: string;
  deep_results?: {
    buttons: {
      type: string;
      title: string;
      url: string;
    }[];
  };
}

interface Web {
  type: string;
  results: Result[];
  family_friendly: boolean;
}

interface BraveSearchResult {
  query: Query;
  mixed: Mixed;
  type: string;
  web: Web;
}

export default BraveSearchResult;

// Brave Search API
const BRAVE_SEARCH_API_ENDPOINT =
  "https://api.search.brave.com/res/v1/web/search";
const BRAVE_SEARCH_API_KEY = process.env.BRAVE_SEARCH_API_KEY as string;

if (!BRAVE_SEARCH_API_KEY) {
  console.error(
    "BRAVE_SEARCH_API_KEY is not defined. Please check your .env file."
  );
  process.exit(1);
}

const headers = {
  Accept: "application/json",
  "X-Subscription-Token": BRAVE_SEARCH_API_KEY,
};

export const braveSearch = async (
  query: string
): Promise<BraveSearchResult | null> => {
  const encodedQuery = encodeURIComponent(query);
  const url = `${BRAVE_SEARCH_API_ENDPOINT}?q=${encodedQuery}`;

  try {
    const response = await axios.get(url, { headers });
    return response.data;
  } catch (error: any) {
    console.error("Error during Brave Search:", error.message);
    if (error.response) {
      console.error("Response status:", error.response.status);
      console.error("Response data:", error.response.data);
    }
    return null;
  }
};
