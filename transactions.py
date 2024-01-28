from solathon import Client, Keypair, Transaction
from solathon.core.instructions import transfer


# Connect to the devnet cluster
client = Client("https://api.devnet.solana.com")


# House Wallet
# master_pub = "3RJZhPYZGc4tPKrb1E1mxLBKvGfkXEzzUuzJXdpMA8tV"
# master_priv = "3QfHhVR4MfURD9d7kLfnoDiJUDFeLAqVWEJX5UMG4cSMQwpFUHmDrSY5R1iRd89XVicB6UGM6w9mWma2hoTKLkSZ"


class transaction:
    def __init__(self):
        self.master_pub = "3RJZhPYZGc4tPKrb1E1mxLBKvGfkXEzzUuzJXdpMA8tV"
        self.master_priv = "3QfHhVR4MfURD9d7kLfnoDiJUDFeLAqVWEJX5UMG4cSMQwpFUHmDrSY5R1iRd89XVicB6UGM6w9mWma2hoTKLkSZ"

    def newUser(self):
        # Generate a Solana wallet public and private Keypair.
        new_account = Keypair()

        # Return this keypair.
        return new_account.public_key, new_account.private_key

    def songAccepted(self, escrowPub, escrowPriv, amount, djWallet):
        # Create a keypair from the users private key.
        sender = Keypair().from_private_key(escrowPriv)

        # MAKE THIS THE DJ'S WALLET ADDRES!!!!!
        receiver = djWallet

        # Amount of Solana tokens to be transferd in lamports.
        amount = (amount - 0.005) * 1000000000

        # Create an instruction to transfer the amount of Solana tokens defined by "amount" in lamports
        # from the users escrow public address to the house wallet address.
        instruction = transfer(
            from_public_key=escrowPub, to_public_key=receiver, lamports=int(amount))
        
   # In the variable "transaction" store the data of a transaction with the instruction created previousley
        # and then the signer of the transaction as the private key of the users escrow wallet(escrowPriv).
        transaction = Transaction(instructions=[instruction], signers=[sender])

        # Send the transaction to the Solana blockchain and return the repsonse.
        result = client.send_transaction(transaction)
        return result

    def songDeclined(self, djWallet, escrowPriv, escrowPub, amount):
        # Create a keypair from the house wallets private key.
        sender = Keypair().from_private_key(self.master_priv)

        # Amount of Solana tokens to be transferd in lamports.
        amount = (amount - 0.005) * 1000000000


        # Create a keypair from the users escrow private key.
        sender = Keypair().from_private_key(escrowPriv)

        # Create an instruction to transfer the amount of Solana tokens defined by "amount" * 5.9 in lamports
        # from the house wallet to the users wallet address.
        instruction = transfer(
            from_public_key=escrowPub,
            to_public_key=djWallet,
            lamports=int(amount - 0.005),
        )
        transaction = Transaction(instructions=[instruction], signers=[sender])
        result = client.send_transaction(transaction)
        print(result)
        return result

    # def getWalletBalance(self, walletAddress):
    #     return round(
    #         client.get_balance(walletAddress)["result"]["value"] / 1000000000, 2
    #     )

    # def getHouseWalletBalance(self):
    #     # SOL token balance is retrieved from the house wallet. The "value" from "result" is in lamports so is divided by one billion to convert to SOL
    #     return round(
    #         client.get_balance(self.master_pub)["result"]["value"] / 1000000000, 2
    #     )
