import requests
import json
import web3 # Release 4.0.0-beta.8
import pprint
import time


w3 = web3.Web3()





contractAddress1 = '0x2f5b0073bcfa2dd04ab00066a902fbfcf51af033'
contractAddress = w3.toChecksumAddress(contractAddress1)
