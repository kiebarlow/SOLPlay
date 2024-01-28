var wallet;
const lamports_per_sol = solanaWeb3.LAMPORTS_PER_SOL;
const network = "https://api.devnet.solana.com";
const connection = new solanaWeb3.Connection(network);

async function connectWallet() {
  try {
    wallet = await window.solana.connect();
    document.getElementById("connect_button").innerText = "Loading....";
    console.log(wallet.publicKey.toString());
    var request = new XMLHttpRequest();
    request.open("POST", 'https://f41500d7-b6cd-42f5-978e-105462cc503b-00-127igwaic3r9j.spock.replit.dev/api/login', true);
    request.setRequestHeader("Content-Type", "application/json");

    var payload = {
      wallet: wallet.publicKey.toString()
    };

    var jsonString = JSON.stringify(payload);
    request.send(jsonString);
    
    //Set a timeout before realoading page
    // setTimeout(function(){
    //     location.reload();
    //   }, 2000);

    return wallet.publicKey.toString();
  } catch (err) {
    console.log(err);
    throw err;
  }
}

async function payForSong(userId) {
    try {
      var price = document.getElementById('price').value;
      console.log("seb price here:" + price);
      const address = await connectWallet();
      await sendSolana(address, userId, price, "https://api.devnet.solana.com");
      console.log("done!!")
      document.getElementById("connect_button").innerText = "Succes!! TX confirmed!";
      grabFormContent(address);
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("connect_button").innerText = "Tx failed :(";
    }
  }
  
  async function sendSolana(senderAddress, receiverAddress, quantity, network) {
    try {
      // Re-initialize connection inside the function
      const connection = new solanaWeb3.Connection(network);
      const lamports = quantity * 1000000000;
      const destPubkey = new solanaWeb3.PublicKey(receiverAddress);
      const instruction = solanaWeb3.SystemProgram.transfer({
        fromPubkey: new solanaWeb3.PublicKey(senderAddress),
        toPubkey: destPubkey,
        lamports,
      });
      const transaction = await setWalletTransaction(instruction, connection);
      const signature = await signAndSendTransaction(wallet, transaction, connection);
    } catch (e) {
      console.warn("Failed", e);
     
    }
  }
  

async function setWalletTransaction(instruction, connection) {
  const transaction = new solanaWeb3.Transaction();
  transaction.add(instruction);
  transaction.feePayer = wallet.publicKey;
  const hash = await connection.getRecentBlockhash();
  console.log("blockhash", hash);
  transaction.recentBlockhash = hash.blockhash;
  return transaction;
}

async function signAndSendTransaction(wallet, transaction, connection) {
  const { signature } = await window.solana.signAndSendTransaction(transaction);
  await connection.confirmTransaction(signature);
  return signature;
}


function grabFormContent(wallet){
    var songName = document.getElementById('songName').value;
    var artist = document.getElementById('artist').value;
    var description = document.getElementById('description').value;
    var price = document.getElementById('price').value;
    var wallet = wallet;
    //djid is dj escrow??
    var djPersonalwallet = userId
    var djid = '2nYQtWp1kgVv4dbg2i8XggXyB4M4TZQ418xuCc9a3abJ';

    var payload = {
        songName: songName,
        artist: artist,
        description: description,
        price: price,
        wallet: wallet,
        djid: djPersonalwallet
    };

    var jsonString = JSON.stringify(payload);
    console.log(jsonString);
    // Create XMLHttpRequest
    var request = new XMLHttpRequest();
    request.open("POST", 'https://f41500d7-b6cd-42f5-978e-105462cc503b-00-127igwaic3r9j.spock.replit.dev/api/grabFormData', true);
    request.setRequestHeader("Content-Type", "application/json");

    request.send(jsonString);
}

