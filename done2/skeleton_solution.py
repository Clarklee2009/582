from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime
rpcuser='quaker_quorum'
rpcpassword='franklin_fought_for_continental_cash'
rpcport=8332
rpcip='3.134.159.30'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpcuser, rpcpassword, rpcip, rpcport))


best_block_hash = rpc_connection.getbestblockhash()
# print(rpc_connection.getblock(best_block_hash))

commands = [ [ "getblockhash", height] for height in range(691) ]
block_hashes = rpc_connection.batch_(commands)
print(block_hashes)
blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
block_times = [ block["time"] for block in blocks ]
print(block_times)

count = -1
for time in block_times:
  count += 1
  unix_timestamp = float(time)
  utc_timestamp = datetime.utcfromtimestamp(unix_timestamp)
  print(utc_timestamp, count)
  
# commands = [ [ "getblockhash", height] for height in range(700) ]
# block_hashes = rpc_connection.batch_(commands)
# # print(block_hashes)
# blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
# block_times = [ block["time"] for block in blocks ]
# # print(block_times)


# unix_timestamp = float(block_times[689]) + 1232100000 
# utc_timestamp = datetime.utcfromtimestamp(unix_timestamp)

# print(unix_timestamp)
# print(utc_timestamp)
