# associated medium post: https://medium.com/@ethervolution/ethereum-create-raw-json-rpc-requests-with-python-for-deploying-and-transacting-with-a-smart-7ceafd6790d9
import requests
import json
import web3 # Release 4.0.0-beta.8
import pprint
import time


# create persistent HTTP connection
session = requests.Session()


headers = {'Content-type': 'application/json'}
myAddress = '0x0337518b10d11ff8c475ab2508ea120e3d7f41e7'

#Finding Nonce

payload= {"jsonrpc":"2.0",
           "method":"eth_getTransactionCount",
           params: ['0x0337518b10d11ff8c475ab2508ea120e3d7f41e7','latest'], // state at the latest block],
           "id":1515}



response = session.post('http://localhost:8545', json=payload, headers=headers)
#print('raw json response: {}'.format(response.json()))
print('nonce of address {} is {}'.format(myAddress, response.json()['result'])) 
#print('nonce of address {} is {}'.format(myAddress, myNonce))

'''
#Check CoinBase
payload= {"jsonrpc":"2.0",
           "method":"eth_coinbase",
           "params":[],
           "id":1907}



response = session.post('http://localhost:8545', json=payload, headers=headers)
print('Client CoinBase: {}'.format(response.json()['result']))



#Get Balance
#account balance
myAddress1 = '0xa38b6dd8ab79dcc6cd22ac205b9e933fe91dec02'

payload= {"jsonrpc":"2.0",
           "method":"eth_getBalance",
           "params":[myAddress1, 'latest'],
           "id":1907}



response = session.post('http://localhost:8545', json=payload, headers=headers)
print('Account 1 Balance: {}'.format(response.json()['result']))

#Get Balance
#account balance
myAddress2 = '0xb945c4190d4711fad7081be33a947e9997fc52dc'

payload= {"jsonrpc":"2.0",
           "method":"eth_getBalance",
           "params":[myAddress2, 'latest'],
           "id":1907}



response = session.post('http://localhost:8545', json=payload, headers=headers)
print('Account 2 Balance: {}'.format(response.json()['result']))

#Block Number
payload= {"jsonrpc":"2.0",
           "method":"eth_blockNumber",
           "params":[],
           "id":1515
           }



response = session.post('http://localhost:8545', json=payload, headers=headers)
print('Block No: {}'.format(response.json()['result']))

#Transaction Count


payload= {"jsonrpc":"2.0",
           "method":"eth_getTransactionCount",
           "params":[myAddress1, 'latest'],
           "id":1515}



response = session.post('http://localhost:8545', json=payload, headers=headers)
print('Transaction Counnt: {}'.format(response.json()['result']))'''