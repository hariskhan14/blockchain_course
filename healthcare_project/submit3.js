import { randomBytes } from 'crypto';
if (!global.crypto) global.crypto = {};
global.crypto.getRandomValues = (arr) => {
  const buf = randomBytes(arr.length);
  arr.set(buf);
  return arr;
};

// submit.js
import Web3 from 'web3';
import { encryptFile } from './encrypt.js';
import { sha256File } from './hash.js';
import fs from 'fs';

// — UPDATE these ↓ with your own values —
const GANACHE_URL      = 'http://127.0.0.1:8545';
const CONTRACT_ADDRESS = '0x85aa337a7F171fB08d52e042A2Cd7Ae76F215e9c';
const CONTRACT_ABI     = JSON.parse(fs.readFileSync('./PHR-abi.json'));

const web3 = new Web3(GANACHE_URL);
const phr  = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);

async function submit(patientId, plainPath) {
  // 1. encrypt
  const encPath = plainPath + '.enc';
  encryptFile(plainPath, encPath);
  await new Promise(r => setTimeout(r, 200)); // give FS a moment

  // 2. hash
  const hashHex = await sha256File(encPath);
  console.log('Encrypted hash:', hashHex);

  // 3. send tx
  const accounts = await web3.eth.getAccounts();
  const receipt  = await phr.methods
    .addRecord(patientId, '0x' + hashHex)
    .send({ from: accounts[0], gas: 200000 });
  console.log('Transaction mined in block', receipt.blockNumber);

  // 4. verify
  const count = await phr.methods.recordCount().call();
  console.log('Total records on‑chain:', count);

  const rec = await phr.methods.records(count - 1).call();
  console.log('Last record:', rec);
}

(async () => {
  process.env.AES_KEY = 'AES_KEY=038ab34c8116abfe741aad8127857de13d5a75ba41e0713ed2056e9af0d1c3e4';
  await submit('patient123', './phr-demo/scan1.pdf');
})();

