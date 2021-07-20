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
    
    orders = session.query(Order).filter(Order.filled == None).all() 
    for e_order in orders:
      #2 Check if there are any existing orders that match
        if e_order.buy_currency == order_obj.sell_currency and e_order.sell_currency == order_obj.buy_currency:
          if e_order.sell_amount/ e_order.buy_amount >= order_obj.buy_amount/order_obj.sell_amount:
            #3.1 Set the filled field to be the current timestamp on both orders
            time = datetime.now()
            order_obj.filled = time
            e_order.filled = time
            session.commit()
            #3.2 Set counterparty_id to be the id of the other order
            e_order.counterparty_id = order_obj.id
            order_obj.counterparty_id = e_order.id
            session.commit()
            #3.3 if not completely filled

            if order_obj.buy_amount > e_order.sell_amount:
              c_by = order_obj.id
              n_buy = order_obj.buy_amount - e_order.sell_amount
              n_sell = n_buy * (order_obj.sell_amount/order_obj.buy_amount)
              new_order = Order(sender_pk=order_obj.sender_pk,receiver_pk=order_obj.receiver_pk, 
                      buy_currency=order_obj.buy_currency, sell_currency=order_obj.sell_currency, 
                      buy_amount=n_buy, sell_amount=n_sell, creator_id=c_by )
            elif e_order.buy_amount > order_obj.sell_amount:
              c_by = e_order.id
              n_buy = e_order.buy_amount - order_obj.sell_amount
              n_sell = n_buy * (e_order.sell_amount/e_order.buy_amount)
              new_order = Order(sender_pk=e_order.sender_pk,receiver_pk=e_order.receiver_pk, 
                      buy_currency=e_order.buy_currency, sell_currency=e_order.sell_currency, 
                      buy_amount=n_buy, sell_amount=n_sell, creator_id=c_by )
              break
    session.commit()
    