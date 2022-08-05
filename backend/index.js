const express = require("express");
const app = express();
const executeQuery = require("./db");
const cors = require("cors");
const multer = require("multer");

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads");
  },
  filename: async (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const upload = multer({
  storage,
});

app.get("/api/test", async (req, res) => {
  const results = await executeQuery("SELECT * FROM content_images");
  return res.status(200).send(results);
})

try {
  app.post("/api/upload", upload.single('file'), async (req, res) => {
    const results = await executeQuery("INSERT INTO content_images (image) VALUES (?)", [req.file.originalname]);
    return res.status(200).download(`uploads/${req.file.originalname}`);
  })
} catch (error) {
  return res.status(500).send(error.message);
}

app.listen(3000, () => {
  console.log("Listened to port 3000");
});
