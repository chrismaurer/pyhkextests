from basis_validation import basis_conditions, basis_fill_roundtrip

import roundtrip_rules as hkex_fill_roundtrip
import conditions as hkex_fill_conditions

from basis_validation import *

from .conditions import *
from .roundtrip_rules import *

__all__ = ['setup_fill']

def setup_fill(fill_table):

    '''
    Steps to view all rules available.
    Start a python interpreter (python -i) with your PYTHONPATH set as if you're running automation.
    type:  from basis_validation import fill
    type:  from pprint import pprint
    To see fill rules type:  pprint( dir( fill.roundtrip ) )
    '''

    ids_table = fill_table.get_rule('roundtrip').get_rule('ids')
    misc_table = fill_table.get_rule('roundtrip').get_rule('misc')

    ###########
    # ## IDs ##
    ###########
    
    ids_table.add_rule(tmx_transaction_identifier_is_empty_or_not)
    ids_table.override_rule('transaction_identifier_is_not_empty', 'True', None,note='Running tmx_transaction_identifier_is_empty_or_not',)
#    ids_table.optout_rule('legs_transaction_identifier_is_empty', 'True', None, note='Running order_feed_and_fill_feed_transaction_no instead')
#    ids_table.optout_rule('non_legs_transaction_identifier_is_not_empty', 'True', None, note='Running order_feed_and_fill_feed_transaction_no instead')
#    ids_table.add_rule(order_feed_and_fill_feed_transaction_no, cond='True')

    #fillkey
    ids_table.add_rule(basis_fill_roundtrip.fill_key_is_not_empty)

#    #transaction_identifier
#    ids_table.add_rule(basis_fill_roundtrip.transaction_identifier_is_not_empty_on_fill_feed, cond='True')
#    ids_table.add_rule(basis_fill_roundtrip.transaction_identifier_is_empty_on_order_feed, cond='False')
#    ids_table.optout_rule('transaction_identifier_is_not_empty', 'True',
#                          'transaction_identifier_is_empty_on_order_feed',
#                          'transaction_identifier is not filled in for order feed fills')

    ##################
    # ##    Misc    ##
    ##################

    # exchange_credentials
    misc_table.replace_rule('exchange_credentials_is_populated',
                            hkex_fill_roundtrip.exchange_credentials_is_populated)
