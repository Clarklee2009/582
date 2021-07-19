from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    #1 insert the order
    order_obj = Order(sender_pk=order['sender_pk'],receiver_pk=order['receiver_pk'], 
                      buy_currency=order['buy_currency'], sell_currency=order['sell_currency'], 
                      buy_amount=order['buy_amount'], sell_amount=order['sell_amount'] )
    session.add(order_obj)
    session.commit()
    orders = session.query(Order).filter(Order.filled != "").all() 
    for e_order in orders:
      #2 Check if there are any existing orders that match
        if e_order.buy_currency == order['sell_currency'] and e_order.sell_currency == order['buy_currency']:
          if e_order.sell_amount/ e_order.buy_amount >= order.buy_amount/order.sell_amount:
            #3.1 Set the filled field to be the current timestamp on both orders
            time = datetime.now()
            order["filled"] = time
            e_order.filled = time
            
            #3.2 Set counterparty_id to be the id of the other order
    
    session.add(order_obj)
    session.commit()