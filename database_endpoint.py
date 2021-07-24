from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine, log, select, MetaData, Table
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only

from models import Base, Order, Log
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

#These decorators allow you to use g.session to access the database inside the request code
@app.before_request
def create_session():
    g.session = scoped_session(DBSession) #g is an "application global" https://flask.palletsprojects.com/en/1.1.x/api/#application-globals

@app.teardown_appcontext
def shutdown_session(response_or_exc):
    g.session.commit()
    g.session.remove()

"""
-------- Helper methods (feel free to add your own!) -------
"""

def log_message(d):
    # Takes input dictionary d and writes it to the Log table
    log_obj = Log(message = d)
    g.session.add(log_obj)
    g.session.commit()





    

"""
---------------- Endpoints ----------------
"""
    
@app.route('/trade', methods=['POST'])
def trade():
    if request.method == "POST":
        content = request.get_json(silent=True)
        # print( f"content = {json.dumps(content)}" )
        columns = [ "sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform" ]
        fields = [ "sig", "payload" ]
        platforms = ["Algorant", "Ethereum"]
        platform = content['payload']['platform']
        sig = content['sig']
        pk = content["payload"]["sender_pk"]
        payload = json.dumps(content["payload"])

        print(platform)
        error = False
        for field in fields:
            if not field in content.keys():
                print( f"{field} not received by Trade" )
                print( json.dumps(content) )
                log_message(content)
                return jsonify( False )
        
        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print( f"{column} not received by Trade" )
                error = True
            if platform not in platforms:
                error = True
        if error:
            # print( json.dumps(content) )
            log_message(content)
            return jsonify( False )

        #check if the signature is valid
        valid = False
        if platform == "Ethereum":
            eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
            print(eth_encoded_msg)
            if eth_account.Account.recover_message(eth_encoded_msg,signature=sig) == pk:
                print( "Eth sig verifies!" )
                valid = True
        elif platform == "Algorand":
            if algosdk.util.verify_bytes(payload.encode('utf-8'),sig,pk):
                print( "Algo sig verifies!" )
                valid = True
        #if valid, store in order table, if not store in log table
        if valid:
            order_obj = Order(sender_pk=content["payload"]['sender_pk'],receiver_pk=content["payload"]['receiver_pk'], 
                      buy_currency=content["payload"]['buy_currency'], sell_currency=content["payload"]['sell_currency'], 
                      buy_amount=content["payload"]['buy_amount'], sell_amount=content["payload"]['sell_amount'], sig=sig)
            g.session.add(order_obj)
            g.session.commit()
            print("add order to table")
        else:
            log_message(payload)
            print("add to log")




    return jsonify(True)  
        #Your code here
        #Note that you can access the database session using g.session


@app.route('/order_book')
def order_book():
    #Your code here
    #Note that you can access the database session using g.session
    
    list = []
    orders = g.session.query(Order).filter().all()
    for order in orders:
        print(order)
        list.append(order)
    result = {'data': list}
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002', debug=True)
