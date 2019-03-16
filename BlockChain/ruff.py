# associated medium post: https://medium.com/@ethervolution/ethereum-create-raw-json-rpc-requests-with-python-for-deploying-and-transacting-with-a-smart-7ceafd6790d9

''' =========================== Defining Libraries ============================ '''

import requests
import json
import web3 # Release 4.0.0-beta.8
import pprint
import time
import serial

''' =========================== INTIALIZING AND DEFINING VARIABLES ============================ '''
# create persistent HTTP connection
session = requests.Session()
w3 = web3.Web3()
pp = pprint.PrettyPrinter(indent=2)

requestId = 0 # is automatically incremented at each request

URL = 'http://localhost:8501' # url of my geth node
PATH_GENESIS = '/home/abdullah/Downloads/devnet/genesis.json'
PATH_SC_TRUFFLE = '/home/abdullah/Downloads/devnet/workspace/' # smart contract path

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
myAddress = '0x29a86118C1Ff89d474E9497D8B3FA890D9F7e30C' # address funded in genesis file
myPrivateKey = '0xff8c4769d2e1d6f7bee613c422a1f9243f189bf5f9764c15b19c6439c0f56cd9'

#Addition CONTRACT ADDRESS
contractAddress1 = '0x1f9eb9f5c0c94603f6fb1acf19f99ddd76600af7'


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





#addition contract
contractAddress = w3.toChecksumAddress(contractAddress1)
count = 0

''' ================= SEND A TRANSACTION TO SMART CONTRACT  ================'''
while (count < 11):

    t1 = time.time()
    requestObject, requestId = createJSONRPCRequestObject('eth_getTransactionCount', [myAddress, 'latest'], requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    myNonce = w3.toInt(hexstr=responseObject['result'])
    print('nonce of address {} is {}'.format(myAddress, myNonce))

    ### prepare the data field of the transaction
    # function selector and argument encoding
    # https://solidity.readthedocs.io/en/develop/abi-spec.html#function-selector-and-argument-encoding

    value1= 10 # data from sensor is in contract
    function = 'Sensor(uint256)' # from smart contract
    methodId = w3.sha3(text=function)[0:4].hex()
    param1 = (value1).to_bytes(32, byteorder='big').hex()
    data = '0x' + methodId + param1 

    transaction_dict = {'from':myAddress,
                        'to':contractAddress,
                        'chainId':CHAINID,
                        'gasPrice':1, # careful with gas price, gas price below the threshold defined in the node config will cause all sorts of issues (tx not bieng broadcasted for example)
                        'gas':2000000, # rule of thumb / guess work
                        'nonce':myNonce,
                        'data':data}

    ### sign the transaction
    signed_transaction_dict = w3.eth.account.signTransaction(transaction_dict, myPrivateKey)
    params = [signed_transaction_dict.rawTransaction.hex()]

    ### send the transacton to your node
    print('executing {} with value {}'.format(function, value1))
    requestObject, requestId = createJSONRPCRequestObject('eth_sendRawTransaction', params, requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    transactionHash = responseObject['result']
    print('transaction hash {}'.format(transactionHash))

    ### wait for the transaction to be mined
    while(True):
        requestObject, requestId = createJSONRPCRequestObject('eth_getTransactionReceipt', [transactionHash], requestId)
        responseObject = postJSONRPCRequestObject(URL, requestObject)
        receipt = responseObject['result']
        if(receipt is not None):
            if(receipt['status'] == '0x1'):
                print('transaction successfully mined')
            else:
                pp.pprint(responseObject)
                raise ValueError('transacation status is "0x0", failed to deploy contract. Check gas, gasPrice first')
            break
        time.sleep(PERIOD/10)



    ''' ============= READ YOUR SMART CONTRACT STATE USING GETTER  =============='''
    # we don't need a nonce since this does not create a transaction but only ask
    # our node to read it's local database

    ### prepare the data field of the transaction
    # function selector and argument encoding
    # https://solidity.readthedocs.io/en/develop/abi-spec.html#function-selector-and-argument-encoding
    # state is declared as public in the smart contract. This creates a getter function
    methodId = w3.sha3(text='state()')[0:4].hex()
    data = '0x' + methodId
    transaction_dict = {'from':myAddress,
                        'to':contractAddress,
                        'chainId':CHAINID,
                        'data':data}

    params = [transaction_dict, 'latest']
    requestObject, requestId = createJSONRPCRequestObject('eth_call', params, requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    state = w3.toInt(hexstr=responseObject['result'])
    print('using getter for public variables: result is {}'.format(state))
    t2 = time.time()
    T = t2 - t1
    print(T)
    count = count + 1






''' prints
nonce of address 0xF464A67CA59606f0fFE159092FF2F474d69FD675 is 4
contract submission hash 0x64fc8ce5cbb5cf822674b88b52563e89f9e98132691a4d838ebe091604215b25
newly deployed contract at address 0x7e99eaa36bedba49a7f0ea4096ab2717b40d3787
nonce of address 0xF464A67CA59606f0fFE159092FF2F474d69FD675 is 5
executing add(uint256,uint256) with value 10,32
transaction hash 0xcbe3883db957cf3b643567c078081343c0cbd1fdd669320d9de9d05125168926
transaction successfully mined
using getter for public variables: result is 42
using getState() function: result is 42
'''
