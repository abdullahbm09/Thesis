import requests
# create persistent HTTP connection
session = requests.Session()
# as defined in https://github.com/ethereum/wiki/wiki/JSON-RPC#net_version
method = 'eth_accounts'
params = []
payload= {"jsonrpc":"2.0",
           "method":method,
           "params":params,
           "id":1907}
headers = {'Content-type': 'application/json'}
response = session.post('http://localhost:8545', json=payload, headers=headers)
print('raw json response: {}'.format(response.json()))
print('network id: {}'.format(response.json()['result']))
