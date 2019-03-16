# associated medium post: https://medium.com/@ethervolution/ethereum-create-raw-json-rpc-requests-with-python-for-deploying-and-transacting-with-a-smart-7ceafd6790d9
import requests
import json
import web3 # Release 4.0.0-beta.8
import pprint
import time

# create persistent HTTP connection
session = requests.Session()
w3 = web3.Web3()
pp = pprint.PrettyPrinter(indent=2)

requestId = 0 # is automatically incremented at each request

URL = 'http://localhost:8502' # url of my geth node
PATH_GENESIS = '/home/abdullah/Ethereum_Project/devnet/genesis.json'
PATH_SC_TRUFFLE = '/home/abdullah/Ethereum_Project/devnet/storage_smart_contract_example/' # smart contract path

# extracting data from the genesis file
genesisFile = json.load(open(PATH_GENESIS))
CHAINID = genesisFile['config']['chainId']
PERIOD  = genesisFile['config']['clique']['period']
GASLIMIT = int(genesisFile['gasLimit'],0)

# compile your smart contract with truffle first
truffleFile = json.load(open(PATH_SC_TRUFFLE + '/build/contracts/AdditionContract.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# Don't share your private key !
myAddress = '0xc84602b9CAc192AEa6731A4f806DFDC7338B23aE' # address funded in genesis file
myPrivateKey = '0x430cf87eaad520ea2fbf975f17fa2cd820c3ddf1e269e6857fecec4b6732eed0'


''' =========================== SOME FUNCTIONS ============================ '''
# see http://www.jsonrpc.org/specification
# and https://github.com/ethereum/wiki/wiki/JSON-RPC

def createJSONRPCRequestObject(_method, _params, _requestId):
    return {"jsonrpc":"2.0",
            "method":_method,
            "params":_params, # must be an array [value1, value2, ..., valueN]
            "id":_requestId}, _requestId+1
    
def postJSONRPCRequestObject(_HTTPEnpoint, _jsonRPCRequestObject):
    response = session.post(_HTTPEnpoint,
                            json=_jsonRPCRequestObject,
                            headers={'Content-type': 'application/json'})

    return response.json()

print ('Nonce No')
''' ======================= DEPLOY A SMART CONTRACT ======================= '''
### get your nonce
requestObject, requestId = createJSONRPCRequestObject('eth_getTransactionCount', [myAddress, 'latest'], requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
myNonce = w3.toInt(hexstr=responseObject['result'])
print('nonce of address {} is {}'.format(myAddress, myNonce))

print('Uploading the contract and creating a transaction')
### create your transaction
transaction_dict = {'from':myAddress,
                    'to':'', # empty address for deploying a new contract
                    'chainId':CHAINID,
                    'gasPrice':1, # careful with gas price, gas price below the --gasprice option of Geth CLI will cause problems. I am running my node with --gasprice '1'
                    'gas':2000000, # rule of thumb / guess work
                    'nonce':myNonce,
                    'data':bytecode} # no constrctor in my smart contract so bytecode is enough
print('Signing the transaction')
### sign the transaction
signed_transaction_dict = w3.eth.account.signTransaction(transaction_dict, myPrivateKey)
params = [signed_transaction_dict.rawTransaction.hex()]
print('Sending this transaction to Your Node')
### send the transacton to your node
requestObject, requestId = createJSONRPCRequestObject('eth_sendRawTransaction', params, requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
transactionHash = responseObject['result']
print('contract submission hash {}'.format(transactionHash))
print(' Kindly wait as your Transaction is mining')
### wait for the transaction to be mined and get the address of the new contract
while(True):
    requestObject, requestId = createJSONRPCRequestObject('eth_getTransactionReceipt', [transactionHash], requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    receipt = responseObject['result']
    if(receipt is not None):
        if(receipt['status'] == '0x1'):
            contractAddress = receipt['contractAddress']
            print('newly deployed contract at address {}'.format(contractAddress))
        else:
            pp.pprint(responseObject)
            raise ValueError('transacation status is "0x0", failed to deploy contract. Check gas, gasPrice first')
        break
    time.sleep(PERIOD/10)


''' ================= SEND A TRANSACTION TO SMART CONTRACT  ================'''
### get your nonce
requestObject, requestId = createJSONRPCRequestObject('eth_getTransactionCount', [myAddress, 'latest'], requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
myNonce = w3.toInt(hexstr=responseObject['result'])
print('nonce of address {} is {}'.format(myAddress, myNonce))

### prepare the data field of the transaction
# function selector and argument encoding
# https://solidity.readthedocs.io/en/develop/abi-spec.html#function-selector-and-argument-encoding
value1, value2 = 10, 32 # random numbers here
function = 'add(uint256,uint256)' # from smart contract
methodId = w3.sha3(text=function)[0:4].hex()
param1 = (value1).to_bytes(32, byteorder='big').hex()
param2 = (value2).to_bytes(32, byteorder='big').hex()
data = '0x' + methodId + param1 + param2

print(methodId)
print (data)


transaction_dict = {'from':myAddress,
                    'to':contractAddress,
                    'chainId':CHAINID,
                    'gasPrice':1, # careful with gas price, gas price below the threshold defined in the node config will cause all sorts of issues (tx not bieng broadcasted for example)
                    'gas':2000000, # rule of thumb / guess work
                    'nonce':myNonce,
                    'data':data}


signed_transaction_dict = w3.eth.account.signTransaction(transaction_dict, myPrivateKey)
params = [signed_transaction_dict.rawTransaction.hex()]

### send the transacton to your node
print('executing {} with value {},{}'.format(function, value1, value2))
