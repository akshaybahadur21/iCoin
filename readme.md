## iCoin
This code explains the working of Crypto-currency.


### Code Requirements
The example code is in Python ([version 2.7](https://www.python.org/download/releases/2.7/) or higher will work). 
1) import hashlib
2) import flask

### Description

A cryptocurrency (or crypto currency) is a digital asset designed to work as a medium of exchange using cryptography to secure the transactions and to control the creation of additional units of the currency. Cryptocurrencies are classified as a subset of digital currencies and are also classified as a subset of alternative currencies and virtual currencies.

####Concepts

1) [Proof-of-Work Algorithm](https://en.wikipedia.org/wiki/Proof-of-work_system)
2) [Concensus Algorithm](https://en.wikipedia.org/wiki/Consensus_(computer_science))

For more information, [see](https://en.wikipedia.org/wiki/Cryptocurrency)

###Steps

1) After you have set up the python code, you need to send a POST request of transferring iCoins to someone.

```
curl "localhost:5000/request_transaction" \
     -H "Content-Type: application/json" \
     -d '{"from": "Akshay", "to":"Raghav", "amount": 10}'
	 
```

2) Now mine the block for verification by send a GET request.

```
curl localhost:5000/mine
	 
```

3) You can check all the blocks by sending a GET request.

```
curl localhost:5000/blocks
	 
```


### Execution
To run the code, type `python block_chain.py`

```
python block_chain.py
```
