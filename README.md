# My first ever blockchain
This has been a long time coming. I have been into this space(if reading about it all day erry day defines space) for a while now. 
The more I read about Blockchains and the technologies in the world of blockchains, the more I get attracted towards trying to build something with it. Believe it or not, this tech is game changing. 

Blockchains are gonna change the way things work, from the very basic tasks like uploading your data to complex ones like transfer of assets etc., it has the ability to revolutionise the system, 'our' system.  

So here it is, my first try at building a blockchain. Why have I started with this and not an actual blokchain like Ethereum or Bitcoin, well to get to know the fundamentals of how things work here and also getting to the core of the system was important for me.

# What do we have here?
Well this is a small version of a blockchain(written in Python) that can perform basic tasks of the underlying system like registering new nodes in a network,
add a new transaction(for now I have added just the amount), mine a new block, again the PoW(Proof of work) nonce is a very simple one and should'nt take much 'computational power'. And we have chain validation and chain view methods to validate and view the ledger respectively.

# Deployment
I've used Python Flask to write API's that provide the aforementioned functionalities. Again this is just a backend code and you can interact with it using Postman or cURL.
To deploy this on your localhost run 'python blockchain.py'

# Credits
Mr Daniel Van Flymen for posting an excellent article on Hackernoon. 
