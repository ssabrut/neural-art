const express = require("express");
const app = express();
const executeQuery = require("./db");
const cors = require("cors");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(cors());
app.get("/api/test", async (req, res) => {
  const results = await executeQuery("SELECT * FROM content_images");
  return res.status(200).send(results);
})

app.listen(3000, () => {
  console.log("Listened to port 3000");
});
