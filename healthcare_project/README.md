### 1. Problem Statement
Modern Personal Health Record (PHR) systems face three core challenges:

**Confidentiality**: Sensitive patient files (PDFs, images) must stay private.

**Integrity**: Patients and providers need cryptographic assurance that records haven’t been tampered with.

**Availability**: The system must remain responsive and fault‑tolerant, even if some nodes go down.

### 2. How We Solved the Problem
#### Encryption (Confidentiality)
Each uploaded PDF is AES‑256‑CBC encrypted off‑chain before any blockchain interaction.

#### Hashing & On‑chain Proof (Integrity)
We compute a SHA‑256 digest of the encrypted file and record that hash in a minimal Solidity contract (PHR.sol). Any later modification of the file breaks the hash.

#### PoA Blockchain / Ganache (Availability)
For the demo we used Ganache CLI—a local blockchain that auto‑mines every transaction—so data is always immediately available and network setup is trivial.

#### Simple Web App (End‑to‑End Flow)
An Express/Multer backend accepts user‑uploaded PDFs, triggers the encrypt→hash→on‑chain flow via our submit-web3.js script, and stores encrypted blobs in /phr-demo. A static front‑end lists all records in styled cards.

### 3. Project Setup & Toolchain
#### Blockchain & Smart Contract

Ganache CLI (local Ethereum testnet)

Solidity contract (PHR.sol) deployed via Remix or Hardhat

#### Backend API

Node.js & Express to serve the upload form and trigger submissions

Multer for handling multipart PDF uploads

Child_process.spawn to invoke our submission script

#### Off‑chain Helpers

encrypt.js: AES‑256‑CBC file encryption with Node’s crypto

hash.js: SHA‑256 digest computation

#### Submission Script

submit-web3.js using Web3.js: takes (patientId, filePath) CLI args, encrypts the file, hashes it, and calls addRecord(patientId, fileHash) on‑chain

#### Front‑end UI

public/index.html with Web3.js to read recordCount & records(i) and render each in a CSS‑styled “card” (Consolas font)

#### File Hosting

Encrypted blobs stored locally under /phr-demo/ (optionally later pin to IPFS for true decentralization)

### 4. What We Achieved
**End‑to‑End Demo**: A user can upload any PDF via a web form and immediately see it recorded on a blockchain in under a second.

#### Security Guarantees:

**Confidentiality** via AES encryption—only holders of the secret key can decrypt.

**Integrity** via on‑chain SHA‑256—any tampering is detectable.

**Availability** via Ganache’s instant mining and a simple Express server.

**Modular Architecture**: Easily swap out Ganache for a real PoA network or IPFS for storage, or extend the Solidity contract for access control.

This lightweight PHR project showcases the core “CIA” properties in a fully self‑contained demo you can run on any laptop.


```
ganache-cli -m testseed -e 1000

geth attach http://127.0.0.1:8545
> eth.accounts
> eth.blockNumber
> eth.sendTransaction({from: '0x5c0b07b93526cd047c193fac6d7c0f321aa8901f', to: '0x0536f6c3e7577bf74a21fe17957118d393452975', value: web3.toWei(50, 'ether')});
> web3.fromWei(eth.getBalance('0x5c0b07b93526cd047c193fac6d7c0f321aa8901f'), 'ether')
> eth.blockNumber


https://remix.ethereum.org/

create PHR.sol
Compile
Deploy with custom http address //connects to local ganeche server
// now, compile, deploy easily


// working
ganache-cli -m testseed --gasLimit 8000000 --defaultBalanceEther 1000 --networkId 5777

in code, update:
1. Deployed contract address
2. Deployed account's address
3. Deployed account's private key
4. Run submit.js
5. npx serve .
```


