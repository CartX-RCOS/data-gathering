const { MongoClient } = require("mongodb");

// Replace the uri string with your connection string.
const uri = "";

const client = new MongoClient(uri);

async function run() {
    try {
      const database = client.db('inventory');
      const inventory = database.collection('hannaford');
  
      // Query for all items that have the item 'Chips'
      const query = { item: 'Chips' };
      const productsCursor = inventory.find(query);
  
      // Convert the cursor to an array of documents
      const products = await productsCursor.toArray();
  
      console.log(products);
    } finally {
      // Ensures that the client will close when you finish/error
      await client.close();
    }
}

run().catch(console.dir);