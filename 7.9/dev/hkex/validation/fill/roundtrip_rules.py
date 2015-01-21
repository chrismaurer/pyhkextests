# Python Imports
import operator

# commontests imports
from basis_validation.fill.utils import iter_fills, get_all_leg_fill_callbacks

# Commontests Imports
from basis_validation.utils import compare
from basis_validation.fill.utils import *

import logging
log = logging.getLogger(__name__)

def exchange_credentials_is_populated(action, before, after):
    iter_fills(action, before, after, get_all_leg_fill_callbacks(after),
               'fill.exchange_credentials', "''", operator.ne)

############
# Id Rules
############
def tmx_transaction_identifier_is_empty_or_not(action, before, after):
    
    #Get all the fills on the order feed
    order_feed_fills = get_all_fill_callbacks_on_order_feed(after)
    #Get all the fills on the fill feed
    fill_feed_fills = get_all_fill_callbacks_on_fill_feed(after)
    
    #Look through all the order feed fills and verify transaction_no is zero
    for order_feed_fill in order_feed_fills['order feed']:
        compare(order_feed_fill.transaction_identifier, "", op=operator.eq)
        
    #Look through all the fill feed fills and verify transaction_no is NOT zero
    for fill_feed_fill in fill_feed_fills['fill feed']:
        compare(fill_feed_fill.transaction_identifier, "", op=operator.ne)
    
    
def order_feed_and_fill_feed_transaction_no(action, before, after):
    
    #Get order and fill feed fills
    order_feed_fills = get_all_fill_callbacks_on_order_feed(after)
    fill_feed_fills = get_all_fill_callbacks_on_fill_feed(after)
    
        
    
    for order_feed_fill in order_feed_fills['order feed']:
        #If the BD6 comes in first on the order feed then the order feed fill and the fill feed fill will be identical.
        #If the BD1 come in first on the order feed then the order feed fill and the fill feed fill will not be identical.
        #This is a race condition at the exchange.
        
        #Check to see if the fill came from a BD1
        if order_feed_fill.fill_key[-1:] == '1':
            #If the fill info came from a BD1 then it has no transaction_no
            #and we need to verify transaction_no is zero
            compare(order_feed_fill.transaction_identifier, "", op=operator.eq)
            compare(order_feed_fill.clearing_date, None, op=operator.ne)
            compare(order_feed_fill.trans_date, None, op=operator.ne)
            compare(order_feed_fill.trans_time, None, op=operator.ne)
            compare(order_feed_fill.giveup_mbr, None, op=operator.ne)
            compare(order_feed_fill.cntr_party, "", op=operator.eq)
            
        elif order_feed_fill.fill_key[-1:] == '6':
            # If the fill info came from a BD6 then it has transaction_no info
            #We need to verify transaction_no is != zero
            compare(order_feed_fill.transaction_identifier, "", op=operator.ne)
            compare(order_feed_fill.clearing_date, None, op=operator.ne)
            compare(order_feed_fill.trans_date, None, op=operator.ne)
            compare(order_feed_fill.trans_time, None, op=operator.ne)
            compare(order_feed_fill.giveup_mbr, None, op=operator.ne)
            
            
        else:
            compare(order_feed_fill.fill_key[-1:],'Last character on the order feed fill_key is not a 1')

    
    for fill_feed_fill in fill_feed_fills['fill feed']:
        
        #Check to see if the fill came from a BD1
        if fill_feed_fill.fill_key[-1:] == '1' or fill_feed_fill.fill_key[-1:] == '6':
            
            
            compare(fill_feed_fill.transaction_identifier, "", op=operator.ne)
            compare(fill_feed_fill.clearing_date, None, op=operator.ne)
            compare(fill_feed_fill.trans_date, None, op=operator.ne)
            compare(fill_feed_fill.trans_time, None, op=operator.ne)
            compare(fill_feed_fill.giveup_mbr, None, op=operator.ne)
       
        else:
            compare(fill_feed_fill.fill_key[-1:],'Last character on the fill feed fill_key is not a 1 or 6')
