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