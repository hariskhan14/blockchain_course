// server.js
// Polyfill Object.hasOwn for compatibility with older Node versions
if (typeof Object.hasOwn !== 'function') {
    Object.hasOwn = function(obj, prop) {
        return Object.prototype.hasOwnProperty.call(obj, prop);
    };
}

import express from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

// Resolve __dirname in ES module context
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Directory for storing uploaded PHR files
const uploadDir = path.join(__dirname, 'phr-demo');
if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });

// Multer storage configuration
const storage = multer.diskStorage({
    destination: (_req, _file, cb) => cb(null, uploadDir),
    filename: (_req, file, cb) => {
        const uniqueName = `${Date.now()}-${file.originalname}`;
        cb(null, uniqueName);
    }
});
const upload = multer({ storage });

const app = express();
// Serve static files from 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Endpoint to handle PDF uploads and submission
app.post('/upload', upload.single('pdf'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('No file uploaded.');
    }
    const filePath = path.join(uploadDir, req.file.filename);
    const patientId = path.parse(req.file.filename).name;

    // Spawn the submission script with the filename as argument
    const proc = spawn('node', ['submit.js', patientId, filePath], {
        cwd: __dirname,
        env: process.env,
        stdio: 'inherit'
    });

    proc.on('close', (code) => {
        if (code === 0) {
            res.send(`✅ Uploaded and submitted: ${req.file.filename}`);
        } else {
            res.status(500).send(`❌ Submit script failed (code ${code})`);
        }
    });
});

// Start the server
app.listen(3000, () => {
    console.log('📡 WebApp running at http://localhost:3000');
});
