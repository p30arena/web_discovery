// src/productInformation.ts
import { GoogleGenerativeAI, Schema, SchemaType } from "@google/generative-ai";

export interface ProductInformation {
  name: string;
  description: string;
  price?: number;
  imageUrl?: string;
  size?: string;
  color?: string;
}

const geminiApiKey = process.env.GEMINI_API_KEY;

const productSchema: Schema = {
  description: "List of products",
  type: SchemaType.ARRAY,
  items: {
    type: SchemaType.OBJECT,
    properties: {
      name: {
        type: SchemaType.STRING,
        description: "Name of the product",
        nullable: false,
      },
      description: {
        type: SchemaType.STRING,
        description: "Description of the product",
        nullable: true,
      },
      price: {
        type: SchemaType.NUMBER,
        description: "Price of the product",
        nullable: true,
      },
      size: {
        type: SchemaType.STRING,
        description: "Size of the product",
        nullable: true,
      },
      color: {
        type: SchemaType.STRING,
        description: "Color of the product",
        nullable: true,
      },
    },
    required: ["name"],
  },
};

export async function extractProductInformation(
  text: string
): Promise<ProductInformation[]> {
  // Implement product information extraction logic here
  const productInfo: ProductInformation[] = [];

  if (!geminiApiKey) {
    console.error("Gemini API key not found in .env file");
    return productInfo;
  }

  const genAI = new GoogleGenerativeAI(geminiApiKey);
  const model = genAI.getGenerativeModel({
    model: "gemini-2.0-flash",
    generationConfig: {
      responseMimeType: "application/json",
      responseSchema: productSchema,
    },
  });

  const prompt = `Extract product information from the following text:\n${text}\n\n`;

  try {
    const result = await model.generateContent(prompt);
    const textResponse = result.response.text();

    console.log("LLM Response:", textResponse);

    try {
      const jsonResponse = JSON.parse(textResponse) as ProductInformation[];
      return jsonResponse;
    } catch (error) {
      console.error("Error parsing JSON response:", error);
      return productInfo;
    }
  } catch (error) {
    console.error("Error generating content:", error);
    return productInfo;
  }
}
