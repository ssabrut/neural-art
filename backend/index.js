const express = require("express");
const app = express();
const executeQuery = require("./db");
const cors = require("cors");
const multer = require("multer");
const zip = require('express-zip');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    if (req.query.event2 == 'styles' && req.files[1]) {
      cb(null, "uploads/styles");
    } else {
      cb(null, "uploads/contents");
    }
  },
  filename: async (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage });

app.get("/api/test", async (req, res) => {
  const results = await executeQuery("SELECT * FROM content_images");
  return res.status(200).send(results);
})

app.post("/api/upload", upload.array('files', 2), async (req, res, next) => {
  try {
    const contentImage = await executeQuery("INSERT INTO content_images (image) VALUES (?)", [req.files[0].filename]);
    const styleImage = await executeQuery("INSERT INTO style_images (image) VALUES (?)", [req.files[1].filename]);

    return res.status(200).send([
      `uploads/${req.query.event1}/${req.files[0].filename}`,
      `uploads/${req.query.event2}/${req.files[1].filename}`,
    ]);
  } catch (e) {
    return res.status(500).send(e.message);
  }
});

app.get('/api/download/', async (req, res) => {
  try {
    return res.status(200).download(req.body.path);
  } catch (e) {
    return res.status(500).send(e.message);
  }
});

app.listen(3000, () => {
  console.log("Listened to port 3000");
});
