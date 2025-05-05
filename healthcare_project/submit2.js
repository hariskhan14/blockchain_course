// submit.js
// Polyfill for AbortController for older Node.js versions
import { AbortController } from "node-abort-controller";
global.AbortController = AbortController;

import { JsonRpcProvider, Wallet, Contract } from "ethers";
import fs from "fs";
import { encryptFile } from "./encrypt.js";
import { sha256File } from "./hash.js";

const GANACHE_URL = "http://127.0.0.1:8545";
const CONTRACT_ADDRESS = '0x8A73F2E91968D0eD571E135d0e0031f18f8EAce7';
const CONTRACT_ABI = JSON.parse(fs.readFileSync("./PHR-abi.json"));

// Important: This must be the private key of the account that deployed the contract
// If you deployed from Remix, this needs to be the private key of the account
// you were connected with in MetaMask when deploying
const ADMIN_PRIVATE_KEY = "8c4fdc5e9b1d77d1b22136c65106a7d626c0c5823148701fe48c7542acd8c2e8";

async function checkAdmin() {
  const provider = new JsonRpcProvider(GANACHE_URL);
  const wallet = new Wallet(ADMIN_PRIVATE_KEY, provider);
  const phr = new Contract(CONTRACT_ADDRESS, CONTRACT_ABI, wallet);

  console.log("Contract address:", CONTRACT_ADDRESS);
  console.log("Your address:", await wallet.getAddress());

  try {
    const adminAddress = await phr.admin();
    console.log("Contract admin address:", adminAddress);

    if (adminAddress.toLowerCase() === (await wallet.getAddress()).toLowerCase()) {
      console.log("✅ SUCCESS: Your wallet IS the admin!");
      return true;
    } else {
      console.log("❌ ERROR: Your wallet is NOT the admin!");
      console.log("You need to use the private key of the account that deployed the contract.");
      return false;
    }
  } catch (error) {
    console.error("Error checking admin:", error.message);
    return false;
  }
}

async function submit(patientId, plainPath) {
  try {
    // First check if we're using the admin account
    const isAdmin = await checkAdmin();
    if (!isAdmin) {
      console.log("Aborting submission because your account is not the admin");
      return;
    }

    // 1. encrypt & 2. hash
    const encPath = plainPath + ".enc";
    encryptFile(plainPath, encPath);
    await new Promise(r => setTimeout(r, 200));

    const hashHex = await sha256File(encPath);
    console.log("Encrypted hash:", hashHex);

    // 3. connect to Ganache with proper signer setup
    const provider = new JsonRpcProvider(GANACHE_URL);
    const wallet = new Wallet(ADMIN_PRIVATE_KEY, provider);

    // 4. contract with the wallet as signer
    const phr = new Contract(CONTRACT_ADDRESS, CONTRACT_ABI, wallet);

    // 5. send the tx
    console.log(`Adding record for patient: ${patientId} with hash: 0x${hashHex}`);
    const tx = await phr.addRecord(patientId, "0x" + hashHex, {
      gasLimit: 500000 // Set a manual gas limit to avoid estimation issues
    });
    console.log("Transaction sent:", tx.hash);

    // Wait for confirmation
    console.log("Waiting for confirmation...");
    const receipt = await tx.wait();
    console.log("⛓ Mined in block", receipt.blockNumber);

    // 6. verify
    const count = await phr.recordCount();
    console.log("📑 Total records:", count.toString());
  } catch (error) {
    console.error("Error in submit function:");
    if (error.info && error.info.error) {
      console.error("Contract error message:", error.info.error.message);
    } else {
      console.error(error.message || error);
    }
    throw error;
  }
}

// Helper function to show all available accounts in Ganache
async function listAccounts() {
  try {
    const provider = new JsonRpcProvider(GANACHE_URL);
    const accounts = await provider.listAccounts();

    console.log("Available accounts in Ganache:");
    for (let i = 0; i < accounts.length; i++) {
      const balance = await provider.getBalance(accounts[i]);
      console.log(`[${i}] ${accounts[i]} - Balance: ${balance.toString()} wei`);
    }

    return accounts;
  } catch (error) {
    console.error("Error listing accounts:", error.message);
    return [];
  }
}

(async () => {
  process.env.AES_KEY = "038ab34c8116abfe741aad8127857de13d5a75ba41e0713ed2056e9af0d1c3e4";
  try {
    console.log("=== Listing Ganache Accounts ===");
    await listAccounts();

    console.log("\n=== Checking Admin Status ===");
    await checkAdmin();

    console.log("\n=== Starting Submission ===");
    await submit("patient123", "./phr-demo/scan1.pdf");
  } catch (e) {
    console.error("Fatal error:");
    console.error(e);
    process.exit(1);
  }
})();