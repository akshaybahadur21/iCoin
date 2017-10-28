from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date
node = Flask(__name__)

class CreateBlock:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.create_hash()
  
  def create_hash(self):
    sha = hasher.sha256()
    sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
    return sha.hexdigest()


def create_first_block():
  return CreateBlock(0, date.datetime.now(), {
    "proof-of-work": 8831*547,
    "transactions": None
  }, "0")


miner_address = "frufhi55kefj-akshay-address-ndji45jjg6"
blockchain = []
blockchain.append(create_first_block())
this_nodes_transactions = []

peer_nodes = []
mining = True

@node.route('/request_transaction', methods=['POST'])
def transaction():
  new_request_data = request.get_json()
  this_nodes_transactions.append(new_request_data)
  print "Transaction"
  print this_nodes_transactions
  print new_request_data
  print "FROM: {}".format(new_request_data['from'].encode('ascii','replace'))
  print "TO: {}".format(new_request_data['to'].encode('ascii','replace'))
  print "AMOUNT: {}\n".format(new_request_data['amount'])
  return "Transaction successful\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_send = blockchain
  blocklist = ""
  for i in range(len(chain_send)):
    block = chain_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    assembled = json.dumps({
    "index": block_index,
    "timestamp": block_timestamp,
    "data": block_data,
    "hash": block_hash
    })
    if blocklist == "":
      blocklist = assembled
    else:
      blocklist += assembled
  return blocklist

def find_new_chains():
  chains = []
  for node_url in peer_nodes:
    block = requests.get(node_url + "/blocks").content
    block = json.loads(block)
    chains.append(block)
  return chains

def consensus():
  chains = find_new_chains()
  longest_chain = blockchain
  for chain in chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  blockchain = longest_chain

def proof_of_work(last_proof):
  flag = last_proof + 1
  proof_of_work_number=8831*547 #choose a combination 2 big prime number so that computational time is more
  while not (flag % proof_of_work_number == 0 and flag % last_proof == 0):
    flag += 1
  return flag

@node.route('/mine', methods = ['GET'])
def mine():
  last_block = blockchain[len(blockchain) - 1]
  last_proof = last_block.data['proof-of-work']
  proof = proof_of_work(last_proof)
  this_nodes_transactions.append(
    { "from": "System", "to": miner_address, "amount": 1 }
  )

  new_block_data = {
    "proof-of-work": proof,
    "transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = this_timestamp = date.datetime.now()
  last_block_hash = last_block.hash
  this_nodes_transactions[:] = []
  mined_block = CreateBlock(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  blockchain.append(mined_block)
  return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "\n"

node.run()

