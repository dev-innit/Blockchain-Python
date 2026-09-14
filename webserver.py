from flask import Flask
from flask import request

node = Flask(__name__)

# store transcations in a list
this_transcations = []

@node.route('/transcations/new', methods=['POST'])

def new_transcation():
    if request.method == 'POST':
#on each new we extract the transcation data
        new_transcation = request.get_json()
        this_transcations.append(new_transcation)
        return "Transaction received!"
# since the transcations were succefully added we can return a success message
        print ("New transcation added: ")
        print ("FROM: {}".format(new_transcation['from']))
        print ("TO: {}".format(new_transcation['to']))
        print ("AMOUNT: {}".format(new_transcation['amount']))
        
        #then we let the clienn know it was successful
        return "Transaction submitted successfully!"
    
node.run()

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

def proof_of_work(last_proof):
    #create a variable that we will use to find the next proof of work
    incrementor = last_proof + 1
    #keep incrementing the incrementor until it's equal to a number divisible by 9 and the proof of work of the previous block
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
    
    proof = proof_of_work(last_proof)