const express = require("express");
const mysql = require("mysql2");
const config = require('./config');
const app = express();
const port = 3000;

// test the port
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

// this function connects to the mySQL database
async function connectToSql() {
  try {
    const connection = mysql.createConnection(config);

    connection.connect((err) => {
      if (err) {
        console.error("Failed to connect to MySQL Server:", err);
        return;
      }
      console.log("Connected to MySQL Server successfully.");

      // Execute a SQL query to fetch data from the "target" table and prints out the value
      const query = "SELECT * FROM target";
      connection.query(query, (err, results) => {
        if (err) {
          console.error("Failed to fetch data from MySQL:", err);
          return;
        }

        // Print the fetched data
        results.forEach((row) => {
          console.log(`{Product ID: ${row.product_id}, Product Name: ${row.product_name}, Product Price: ${row.product_price}}`);
        });

        // Close the connection
        connection.end();
      });
    });
  } catch (err) {
    console.error("Failed to connect to MySQL Server:", err);
  }
}

// Call the function 
connectToSql();