import fs from 'fs';
import { pipeline } from '@xenova/transformers';

// Helper function for averaging embeddings
const averageEmbedding = (tensor) => {
    const [numItems, numTokens, embeddingSize] = tensor.dims;
    const array = Array.from(tensor.data);
    const averagedEmbeddings = [];
    for (let i = 0; i < numItems; i++) {
        const itemEmbedding = new Array(embeddingSize).fill(0);
        for (let j = 0; j < numTokens; j++) {
            const startIndex = (i * numTokens + j) * embeddingSize;
            for (let k = 0; k < embeddingSize; k++) {
                itemEmbedding[k] += array[startIndex + k];
            }
        }
        const averagedItemEmbedding = itemEmbedding.map(value => value / numTokens);
        averagedEmbeddings.push(averagedItemEmbedding);
    }
    return averagedEmbeddings;
};

// Process a single product file for embedding
async function processSingleProduct(filePath) {
    try {
        const rawData = fs.readFileSync(filePath);
        const productData = JSON.parse(rawData);

        // Initialize model for embedding
        const model = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
        
        const item = productData.name + (productData.categories || "");
        const embeddings = await model([item]);

        if (embeddings.data instanceof Float32Array) {
            const averagedEmbedding = averageEmbedding(embeddings)[0];
            productData.embedding = averagedEmbedding;
            console.log(JSON.stringify(productData));
        } else {
            console.error("Error with embeddings data.");
        }

    } catch (error) {
        console.error("Error processing product:", error);
    }
}

// Run processSingleProduct function with the file path argument
const filePath = process.argv[2];
processSingleProduct(filePath);