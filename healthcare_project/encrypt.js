// encrypt.js
import crypto from 'crypto';
import fs from 'fs';

const KEY = Buffer.from('038ab34c8116abfe741aad8127857de13d5a75ba41e0713ed2056e9af0d1c3e4', 'hex'); // 32‑byte hex

export function encryptFile(inputPath, outputPath) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', KEY, iv);
  const out = fs.createWriteStream(outputPath);
  // write IV first so you can decrypt later
  out.write(iv);
  fs.createReadStream(inputPath).pipe(cipher).pipe(out);
}
