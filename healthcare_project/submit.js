
// submit-web3.js
import Web3 from 'web3';
import fs from 'fs';
import { encryptFile } from "./encrypt.js";
import { sha256File } from "./hash.js";

// pull in the CLI args
const [,, patientId, plainPath] = process.argv;
if (!patientId || !plainPath) {
  console.error("Usage: node submit-web3.js <patientId> <path/to/file.pdf>");
  process.exit(1);
}

console.log("Patient id", patientId)
console.log("Path", plainPath)

const GANACHE_URL = "http://127.0.0.1:8545";
const CONTRACT_ADDRESS = '0x8A73F2E91968D0eD571E135d0e0031f18f8EAce7'; // Your contract address
const CONTRACT_ABI = JSON.parse(fs.readFileSync("./PHR-abi.json"));

// The private key of the admin account (the account that deployed the contract)
const ADMIN_PRIVATE_KEY = "8c4fdc5e9b1d77d1b22136c65106a7d626c0c5823148701fe48c7542acd8c2e8"; // Remove the 0x prefix if it exists

async function checkAdmin() {
  const web3 = new Web3(GANACHE_URL);

  // Add account to web3 wallet
  const account = web3.eth.accounts.privateKeyToAccount(
    ADMIN_PRIVATE_KEY.startsWith('0x') ? ADMIN_PRIVATE_KEY : '0x' + ADMIN_PRIVATE_KEY
  );
  web3.eth.accounts.wallet.add(account);

  // Create contract instance
  const phr = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);

  console.log("Contract address:", CONTRACT_ADDRESS);
  console.log("Your address:", account.address);

  try {
    // Get the admin address from the contract
    const adminAddress = await phr.methods.admin().call();
    console.log("Contract admin address:", adminAddress);

    if (adminAddress.toLowerCase() === account.address.toLowerCase()) {
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

    // 3. Set up web3 with the right account
    const web3 = new Web3(GANACHE_URL);

    // Add account to web3 wallet
    const account = web3.eth.accounts.privateKeyToAccount(
      ADMIN_PRIVATE_KEY.startsWith('0x') ? ADMIN_PRIVATE_KEY : '0x' + ADMIN_PRIVATE_KEY
    );
    web3.eth.accounts.wallet.add(account);

    // 4. Create contract instance
    const phr = new web3.eth.Contract(CONTRACT_ABI, CONTRACT_ADDRESS);

    // 5. send the tx
    console.log(`Adding record for patient: ${patientId} with hash: 0x${hashHex}`);

    const gasEstimate = await phr.methods.addRecord(patientId, "0x" + hashHex).estimateGas({
      from: account.address
    }).catch(e => {
      console.log("Gas estimation failed, using default");
      return 300000; // Default gas limit
    });

    console.log(`Estimated gas: ${gasEstimate}`);

    const receipt = await phr.methods.addRecord(patientId, "0x" + hashHex)
      .send({
        from: account.address,
        gas: Math.floor(gasEstimate * 1.5), // Add 50% buffer to gas estimate
      });

    console.log("⛓ Transaction successful!");
    console.log("Transaction hash:", receipt.transactionHash);
    console.log("Block number:", receipt.blockNumber);

    // 6. verify
    const count = await phr.methods.recordCount().call();
    console.log("📑 Total records:", count.toString());

    return receipt;
  } catch (error) {
    console.error("Error in submit function:");
    console.error(error.message || error);
    throw error;
  }
}

// Helper function to list all accounts
async function listAccounts() {
  const web3 = new Web3(GANACHE_URL);
  const accounts = await web3.eth.getAccounts();

  console.log("Available accounts in Ganache:");
  for (let i = 0; i < accounts.length; i++) {
    const balance = await web3.eth.getBalance(accounts[i]);
    console.log(`[${i}] ${accounts[i]} - Balance: ${web3.utils.fromWei(balance, 'ether')} ETH`);
  }

  return accounts;
}

// Function to restart Ganache with safer parameters
function restartGanacheInstructions() {
  console.log("\n=====================================================");
  console.log("RECOMMENDED: Restart Ganache with safer parameters:");
  console.log("=====================================================");
  console.log("ganache-cli --gasLimit 8000000 --defaultBalanceEther 1000");
  console.log("\nThis will help prevent crashes by giving more gas and resources to your local chain.");
}

(async () => {
  try {
    process.env.AES_KEY = "038ab34c8116abfe741aad8127857de13d5a75ba41e0713ed2056e9af0d1c3e4";

    // Show restart instructions
    restartGanacheInstructions();

    console.log("\n=== Listing Ganache Accounts ===");
    await listAccounts();

    console.log("\n=== Starting Submission ===");
    await submit(patientId, plainPath);

    console.log("\n✅ SUCCESS: Record added successfully!");
  } catch (e) {
    console.error("\n❌ ERROR: Failed to add record:");
    console.error(e.message || e);
    process.exit(1);
  }
})();