import requests
import json
import web3 # Release 4.0.0-beta.8
import pprint
import time

# create persistent HTTP connection
session = requests.Session()
w3 = web3.Web3()

myAddress1 = '0x0337518b10d11ff8c475ab2508ea120e3d7f41e7'
myPrivateKey1 = 'pwdnode1'
myAddress2 = '0x29a86118C1Ff89d474E9497D8B3FA890D9F7e30C'
myPrivateKey2 = '0xff8c4769d2e1d6f7bee613c422a1f9243f189bf5f9764c15b19c6439c0f56cd9'
contractAddress = '0x1f9eb9f5c0c94603f6fb1acf19f99ddd76600af7'

headers = {'Content-type': 'application/json'}

#Finding Nonce
payload= {"jsonrpc":"2.0",
           "method":"eth_getTransactionCount",
           "params": ['0x0337518b10d11ff8c475ab2508ea120e3d7f41e7','latest'], 
           "id":1515}



response = session.post('http://localhost:8501', json=payload, headers=headers)
#print('raw json response: {}'.format(response.json()))
myNonce1 = w3.toInt(hexstr=response.json()['result'])
print('nonce of address {} is {}'.format(myAddress1, myNonce1)) 
#print('nonce of address {} is {}'.format(myAddress, myNonce))


payload = {"jsonrpc":"2.0",
           "method":"eth_getTransactionCount",
           "params": ['0x29a86118C1Ff89d474E9497D8B3FA890D9F7e30C','latest'], 
           "id":1515}



response = session.post('http://localhost:8501', json=payload, headers=headers)
#print('raw json response: {}'.format(response.json()))
myNonce2 = w3.toInt(hexstr=response.json()['result'])
print('nonce of address {} is {}'.format(myAddress1, myNonce1)) 





data = '0x771602f7000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000020'




tx = {'to':contractAddress,
                    'chainId':1515,
                    'gasPrice':1, # careful with gas price, gas price below the threshold defined in the node config will cause all sorts of issues (tx not bieng broadcasted for example)
                    'gas':2000000, # rule of thumb / guess work
                    'nonce':myNonce1,
                    'data':data}

print('executing {} with value {},{}'.format(function, value1, value2))
### sign the transaction
#signed_transaction_dict = w3.eth.account.signTransaction(transaction_dict, myPrivateKey1)
#params = [signed_transaction_dict.rawTransaction.hex()]

### send the transacton to your node


payload= {"jsonrpc":"2.0",
           "method":"eth_getTransactionCount",
           "params": [{"from": myAddress1, "to": contractAddress, "chainId":1515, "gasPrice":1, "gas":2000000, "nonce" : myNonce1, "data" : data}],
           "id":1515}



response = session.post('http://localhost:8501', json=payload, headers=headers)
print('raw json response: {}'.format(response.json()))
#print('transaction hash {}'.format(response.json()['result']))
