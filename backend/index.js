const express = require("express");
const app = express();
const executeQuery = require("./db");
const cors = require("cors");
const multer = require("multer");
const { spawn } = require("child_process");

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
  var dataToSend = null;
  const python = spawn("python", ["script.py", 'node.js', 'python']);

  python.stdout.on('data', (data) => {
    console.log('Piping data from python script...')
    dataToSend = data.toString();
  });

  python.on('close', (code) => {
    console.log('Child process all stdio with code ' + code);
    return res.status(200).send(dataToSend);
  });
})

app.post("/api/upload", upload.array('files', 2), async (req, res, next) => {
  try {
    const contentImage = await executeQuery("INSERT INTO content_images (image) VALUES (?)", [req.files[0].filename]);
    const styleImage = await executeQuery("INSERT INTO style_images (image) VALUES (?)", [req.files[1].filename]);
    const content = contentImage.insertId;
    const style = styleImage.insertId;
    req.content = content;
    req.style = style;
    next();
  } catch (e) {
    return res.status(500).send(e.message);
  }
}, async (req, res, next) => {
  try {
    var dataToSend = null;
    const contentImage = await executeQuery("SELECT image FROM content_images WHERE id = (?)", [req.content]);
    const styleImage = await executeQuery("SELECT image FROM style_images WHERE id = (?)", [req.style]);
    const contentImagePath = `uploads/contents/${contentImage[0].image}`;
    const styleImagePath = `uploads/styles/${styleImage[0].image}`;
    const python = spawn("python", ["script.py", contentImagePath, styleImagePath]);

    python.stdout.on('data', (data) => {
      console.log('Piping data from python script...')
      dataToSend = data.toString();
    });

    python.on('close', (code) => {
      console.log('Child process all stdio with code ' + code);
      return res.status(200).send(dataToSend);
    });
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
