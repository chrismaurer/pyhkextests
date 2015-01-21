import logging

from ttapi import aenums, cppclient

from basis_validation import *
from basis_validation.order.conditions import *

log = logging.getLogger(__name__)

__all__ = ['does_exchange_send_timestamp',
           'is_order_sent_to_exchange',
           'is_gateway_reject',
           'is_exchange_reject']

def is_gateway_reject(action, before, after):
    """
    This is your gateway reject function to fill in
    """
    if after.pending.order_status != aenums.TT_ORDER_STATUS_REJECTED:
        return False

    if before.order_session.feed_down:
        return True

    if before.pending.order_action == aenums.TT_ORDER_ACTION_INQUIRE:
        return True

    if before.pending.order_action == aenums.TT_ORDER_ACTION_HOLD and \
       before.book.order_status == aenums.TT_ORDER_STATUS_HOLD:
        return True

    if before.pending.order_type == aenums.TT_LIMIT_ORDER and \
       before.pending.limit_prc == cppclient.TT_INVALID_PRICE and \
       after.order_callbacks[-1].message == 'Invalid price.':
        return True

    if before.pending.acct_type in [aenums.TT_ACCT_GIVEUP_1,
                                    aenums.TT_ACCT_GIVEUP_2,
                                    aenums.TT_ACCT_UNALLOCATED_1,
                                    aenums.TT_ACCT_UNALLOCATED_2] and \
       before.pending.clearing_mbr == '':
        return True

    if before.pending.order_action in [aenums.TT_ORDER_ACTION_ADD,
                                       aenums.TT_ORDER_ACTION_RESUBMIT]:
        # orders that return True in this block can be added on hold
        # but if sent to the exchange will be rejected by the gateway
        # Please see 155021 which references OS rule 4.7.8
        if before.pending.order_type not in [aenums.TT_LIMIT_ORDER,
                                             aenums.TT_MARKET_TO_LIMIT_ORDER] or \
           before.pending.order_restrict not in [aenums.TT_NO_ORDER_RES,
                                                 aenums.TT_FOK_ORDER_RES,
                                                 aenums.TT_IOC_ORDER_RES] or \
           before.pending.order_flags != aenums.TT_NO_ORDER_MOD or \
           before.pending.tif == 'GIS' or \
           after.pending.order_no == '':
            return True

    if before.pending.order_action not in [aenums.TT_ORDER_ACTION_ADD,
                                           aenums.TT_ORDER_ACTION_RESUBMIT]:
        if before.pending.order_no == 0 or after.pending.order_no < 999999:
            return True

    if before.pending.order_action == aenums.TT_ORDER_ACTION_DELETE and \
       before.book.order_action == aenums.TT_ORDER_ACTION_DELETE and \
       before.book.order_status == aenums.TT_ORDER_STATUS_OK:
        return True

    if before.pending.order_status == aenums.TT_ORDER_STATUS_HOLD and \
       before.pending.order_action != aenums.TT_ORDER_ACTION_RESUBMIT:
        return True

    if before.pending.order_status == aenums.TT_ORDER_STATUS_OK and \
       before.pending.order_action == aenums.TT_ORDER_ACTION_RESUBMIT:
        return True

    if hasattr(action, 'order_status'):
        if action.order_status == 'Risk Reject':
            return True

    return False

def is_exchange_reject(action, before, after):
    return (after.pending.order_status == aenums.TT_ORDER_STATUS_REJECTED and
            not is_gateway_reject(action, before, after))

def is_order_sent_to_exchange(action, before, after):
    if is_risk_reject(action, before, after):
        return False
    if ((after.pending.order_action == aenums.TT_ORDER_ACTION_ADD or
         after.pending.order_action == aenums.TT_ORDER_ACTION_INQUIRE or
         (after.pending.order_action == aenums.TT_ORDER_ACTION_CHANGE and not
          (after.pending.order_status == aenums.TT_ORDER_STATUS_REJECTED and
           is_gateway_reject(action, before, after))) or
         after.pending.order_action == aenums.TT_ORDER_ACTION_RESUBMIT ) and
          ( after.pending.order_status == aenums.TT_ORDER_STATUS_OK or
            (after.pending.order_status == aenums.TT_ORDER_STATUS_REJECTED and
             is_exchange_reject(action, before, after)) ) or
           ( after.pending.order_action == aenums.TT_ORDER_ACTION_HOLD and
             after.pending.order_status == aenums.TT_ORDER_STATUS_HOLD ) or
             ( after.pending.order_action == aenums.TT_ORDER_ACTION_DELETE and
               after.pending.order_status == aenums.TT_ORDER_STATUS_OK and not
               is_book_order_status_hold(action, before, after) ) or
                (after.pending.order_action == aenums.TT_ORDER_ACTION_HOLD and
                 after.pending.order_status == aenums.TT_ORDER_STATUS_DELETED and
                 is_exchange_reject(action, before, after))
                ):

        return True
    return False

def does_exchange_send_timestamp(action, before, after):
      return is_order_sent_to_exchange(action, before, after)

#def is_order_sent_to_exchange(action, before, after):
#    return does_exchange_send_timestamp(action, before, after)
#    if after.pending.order_status == aenums.TT_ORDER_STATUS_REJECTED:
#       return is_exchange_reject(action, before, after)
#
#    if before.pending.order_action in (aenums.TT_ORDER_ACTION_DELETE,
#                                       aenums.TT_ORDER_ACTION_REPLACE) and \
#       before.pending.order_status == aenums.TT_ORDER_STATUS_HOLD and \
#       after.pending.order_status == aenums.TT_ORDER_STATUS_OK:
#        return False
#
#    if before.pending.order_action == aenums.TT_ORDER_ACTION_HOLD and \
#       before.pending.order_status == aenums.TT_ORDER_STATUS_OK and \
#       after.pending.order_status == aenums.TT_ORDER_STATUS_HOLD:
#        return True

#    return after.pending.order_status == aenums.TT_ORDER_STATUS_OK

#def does_exchange_send_timestamp(action, before, after):
#    return not(is_gateway_reject(action, before, after) \
#               or (before.pending.order_status == aenums.TT_ORDER_STATUS_HOLD \
#                   and before.pending.order_action != aenums.TT_ORDER_ACTION_RESUBMIT)
#               or (after.pending.order_status == aenums.TT_ORDER_STATUS_HOLD \
#                   and after.pending.order_action == aenums.TT_ORDER_ACTION_HOLD
#                   and not before.pending.order_status == aenums.TT_ORDER_STATUS_OK)
#               or (before.pending.order_status == aenums.TT_ORDER_STATUS_HOLD \
#                   and after.pending.order_action == aenums.TT_ORDER_ACTION_HOLD))
