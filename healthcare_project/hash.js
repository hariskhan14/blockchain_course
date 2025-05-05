// hash.js
import fs from 'fs';
import crypto from 'crypto';

export function sha256File(path) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    fs.createReadStream(path)
      .on('data', chunk => hash.update(chunk))
      .on('end', () => resolve(hash.digest('hex')))
      .on('error', reject);
  });
}
