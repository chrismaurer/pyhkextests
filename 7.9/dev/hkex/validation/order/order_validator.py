from basis_validation import *#basis_order_conditions, basis_order_roundtrip

import roundtrip_rules as hkex_order_roundtrip
import conditions as hkex_order_conditions

__all__ = ['setup_order']

def setup_order(order_table):
    
    '''
    Steps to view available validation options:
    Start a python intrepreter (python -i) with your PYTHONPATH set as if you're running automation.
    type:  from basis_validation import order
    type:  from pprint import pprint
    
    To see all available rules:
    pprint( dir( order.roundtrip ) )
    
    To see all available conditions:
    pprint( dir( order.conditions ) )
    '''

    core_enums_table = order_table.get_rule('roundtrip').get_rule('core_enums')
    date_and_time_table = order_table.get_rule('roundtrip').get_rule('date_and_time')
    ids_table = order_table.get_rule('roundtrip').get_rule('ids')
    misc_table = order_table.get_rule('roundtrip').get_rule('misc')
    prices_table = order_table.get_rule('roundtrip').get_rule('prices')
    quantities_table = order_table.get_rule('roundtrip').get_rule('quantities')

    ##################
    # ## Conditions ##
    ##################
    # replaces
    order_table.replace_condition('is_exchange_reject', hkex_order_conditions.is_exchange_reject)
    order_table.replace_condition('is_gateway_reject', hkex_order_conditions.is_gateway_reject)
    order_table.replace_condition('is_order_sent_to_exchange', hkex_order_conditions.is_order_sent_to_exchange)
    order_table.replace_condition('does_exchange_send_timestamp', hkex_order_conditions.does_exchange_send_timestamp)

    # from Basis
    order_table.add_condition(basis_order_conditions.is_book_order_at_exchange)
    order_table.add_condition(basis_order_conditions.is_order_sent_partially_filled)
    order_table.add_condition(basis_order_conditions.is_order_status_sent_hold)
    order_table.add_condition(basis_order_conditions.is_order_restrict_sent_none)
    order_table.add_condition(basis_order_conditions.is_going_to_be_immediately_partially_filled)
    order_table.add_condition(basis_order_conditions.is_going_to_be_immediately_triggered)

    #####################
    # ## Date and Time ##
    #####################

    date_and_time_table.optout_rule('time_exch_is_exchange_time', 'True',
                                    'time_exch_is_zero', 'time_exch is not filled in')
    date_and_time_table.optout_rule('date_exch_is_exchange_date', 'True',
                                    'date_exch_is_zero', 'date_exch is not filled in')

    ##################
    # ##    Ids     ##
    ##################

    # exchange_order_id
    ids_table.add_rule(basis_order_roundtrip.exchange_order_id_is_empty, cond='is_order_status_hold')
    ids_table.append_condition('exchange_order_id_is_empty', 'is_order_status_reject and (is_order_action_add or (is_order_action_resubmit and not is_book_order_at_exchange))')
    ids_table.append_condition('exchange_order_id_is_empty', 'is_order_action_delete and is_book_order_status_hold and not is_order_sent_to_exchange')
    ids_table.add_rule(basis_order_roundtrip.exchange_order_id_is_not_empty, cond='(is_order_action_add and not is_order_action_orig_replace) and is_order_status_ok')
    ids_table.append_condition('exchange_order_id_is_not_empty', 'is_order_action_resubmit and (is_order_status_ok or is_book_order_at_exchange)')
    ids_table.add_rule(basis_order_roundtrip.exchange_order_id_is_exchange_order_id_book, cond='is_order_action_delete and not (is_book_order_status_hold and not is_order_sent_to_exchange)')
    ids_table.append_condition('exchange_order_id_is_exchange_order_id_book', 'not (is_order_action_add or is_order_action_delete or is_order_action_resubmit) and (is_order_status_ok or is_order_status_reject)')
    ids_table.add_rule(basis_order_roundtrip.exchange_order_id_is_not_exchange_order_id_sent, cond='is_order_action_add and is_order_action_orig_replace and is_order_status_ok')

    # exchange_trans_no
    ids_table.add_rule(basis_order_roundtrip.exch_trans_no_is_empty, cond='True')

    # order_no
    ids_table.append_condition('order_no_old_is_order_no_sent', ' is_order_action_orig_void or is_order_status_reject')

    # order_no_old
    ids_table.append_condition('order_no_old_is_order_no_sent', ' is_exchange_reject')
    ids_table.append_condition('order_no_old_is_order_no_sent', 'is_order_action_orig_void and is_order_action_delete')

    # num_messages_sent_to_exchange
    ids_table.append_condition('num_messages_sent_to_exchange_is_one', 
                               'is_order_sent_to_exchange and not is_action_WaitForTrigger and \
                                not is_order_action_orig_void and not is_admin_request_rejected and \
                                not is_risk_reject')

    ##################
    # ##    Misc    ##
    ##################

    # exchange_credentials
    misc_table.replace_rule('exchange_credentials_is_populated',
                            hkex_order_roundtrip.exchange_credentials_is_populated)

    misc_table.override_rule('exchange_credentials_is_empty', 'is_risk_reject', None, note='Exchange creds are sent even when Risk Rejected')

    ##################
    # ##   Prices   ##
    ##################

    prices_table.append_condition('limit_prc_is_limit_prc_sent', 'not is_order_action_delete')
    prices_table.append_condition('limit_prc_is_limit_prc_book', 'is_order_action_delete')

    ##################
    # ## Quantities ##
    ##################

    # chg_qty
    quantities_table.append_condition('chg_qty_is_zero',
                                      cond='is_order_status_ok and is_order_action_delete and is_order_action_orig_change')

    # exec_qty
    quantities_table.append_condition('exec_qty_is_zero', cond='is_order_status_hold')
    quantities_table.append_condition('exec_qty_is_exec_qty_sent',
                                      cond='is_order_status_reject or is_order_action_update')
