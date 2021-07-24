from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
#     print("this is test*************************************")
    sig = content["sig"]
    pk = content["payload"]["pk"]
    payload = json.dumps(content["payload"])

    platform = content["payload"]["platform"]
    result = False
#     print("this is result^^^^^^^^^^^^^", result)
    if platform == "Ethereum":
      eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
      if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == pk:
          print( "Eth sig verifies!" )
          result = True
    elif platform == "Algorand":
      if algosdk.util.verify_bytes(payload.encode('utf-8'),sig,pk):
          print( "Algo sig verifies!" )
          result = True
    #Check if signature is valid
#     print("this is result", result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002', debug=True)
    