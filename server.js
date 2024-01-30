const express = require("express");
const app = express();
const port = 3000;
const mysql = require("mysql2");

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

const config = {
  host: "", // Update with your MySQL server address
  user: "", // Update with your MySQL username
  password: "", // Update with your MySQL password
  database: "cartx", // Update with your MySQL database name
};


async function connectToSql() {
  try {
    const connection = mysql.createConnection(config);
    await connection.connect();
    console.log("Connected to MySQL Server successfully.");

    // Run a query to fetch all data from the "products" table
    const query = "SELECT * FROM products";
    connection.query(query, (err, results) => {
      if (err) {
        console.error("Error executing the query:", err);
      } else {
        console.log("Data from 'products' table:");
        console.log(results);
      }

      // Close the connection
      connection.end();
    });
  } catch (err) {
    console.error("Failed to connect to MySQL Server:", err);
  }
}

connectToSql();