# HKEx Imports
import roundtrip_rules as hkex_order_roundtrip
from conditions import *

## OrderBook Imports
from basis_validation import order_book
from basis_validation.validator import FullValidator

from .conditions import *
from .roundtrip_rules import * 

def setup_order_book(order_book_table):

#    order_book_table = table.get_rule('order_book')

    order_book_table.replace_condition('is_book_order_onhold', is_book_order_onhold)
    order_book_table.replace_condition('is_book_order_working', is_book_order_working)
    order_book_table.add_condition(is_book_order_persisted)

#### Following overrides and optout rules only for the partiall fill order: #####
    order_book_table.add_rule(hkex_order_roundtrip.hkex_exec_qty_is_same_as_fill_qty_book_all_orders, cond='is_action_DownloadOrderBook and is_book_order_working ')
    order_book_table.optout_rule('exec_qty_is_exec_qty_book_all_orders', 'is_action_DownloadOrderBook and is_book_order_working', new_rule='hkex_exec_qty_is_same_as_fill_qty_book_all_orders', note='Eurex os does not update the exec_qty on real time for non immediate fill and get the exec qty on download from Exchange')
    order_book_table.override_rule('time_exch_is_time_exch_book_all_orders', 'True', 2, note='Due to not receiving the order updates for the not immediate pfill orders this will not be the same as before')
    order_book_table.override_rule('exch_trans_no_is_exch_trans_no_book_all_orders', 'True', 3, note='Due to not receiving the order updates for the not immediate pfill orders this will not be the same as before')
    order_book_table.override_rule('date_processed_is_date_processed_book_all_orders', 'True', 5, note='the lean hold order will have date GTC ')
    order_book_table.override_rule('time_processed_is_time_processed_book_all_orders', 'True', 6, note='the lean hold order will have time zero')

    # exchange_credentials
    order_book_table.replace_rule('exchange_credentials_is_populated_non_held_orders', hkex_order_roundtrip.exchange_credentials_is_populated_non_held_orders)

    # exec_qty
    order_book_table.add_rule(hkex_order_roundtrip.hkex_exec_qty_is_zero_all_held_orders, cond='False')
    order_book_table.optout_rule('exec_qty_is_exec_qty_book_all_orders',
                                       'is_book_order_onhold',
                                       'hkex_exec_qty_is_zero_all_held_orders',
                                       'exec_qty is 0 for working GTDs after an OS restart')
    # fill_qty
    order_book_table.add_rule(hkex_order_roundtrip.hkex_fill_qty_is_zero_all_held_orders, cond='False')
    order_book_table.optout_rule('fill_qty_is_fill_qty_book_all_orders',
                                       'is_book_order_onhold',
                                       'hkex_fill_qty_is_zero_all_held_orders',
                                       'fill_qty is 0 for working GTDs after an OS restart')
    order_book_table.add_rule(hkex_order_roundtrip.hkex_fill_qty_is_fill_qty_book_all_non_held_orders, cond='False')
    order_book_table.optout_rule('fill_qty_is_fill_qty_book_all_orders',
                                       'is_book_order_onhold',
                                       'hkex_fill_qty_is_fill_qty_book_all_non_held_orders',
                                       'Different algorithm for getting non-held orders on Eurex')
    # order_qty
    order_book_table.add_rule(hkex_order_roundtrip.hkex_order_qty_is_wrk_qty_book_all_persisted_orders, cond='False')
    order_book_table.optout_rule('order_qty_is_order_qty_book_all_orders',
                                       'is_book_order_persisted',
                                       'hkex_order_qty_is_wrk_qty_book_all_persisted_orders',
                                       'order_qty is book wrk_qty for working GTDs after an OS restart')
    order_book_table.add_rule(hkex_order_roundtrip.hkex_order_qty_is_order_qty_book_all_non_persisted_orders, cond='False')
    order_book_table.optout_rule('order_qty_is_order_qty_book_all_orders',
                                       'is_book_order_persisted',
                                       'hkex_order_qty_is_order_qty_book_all_non_persisted_orders',
                                       'Different algorithm for getting non-held orders on Eurex')
    # wrk_qty
    order_book_table.add_rule(hkex_order_roundtrip.hkex_wrk_qty_is_zero_all_held_orders, cond='False')
    order_book_table.optout_rule('wrk_qty_is_wrk_qty_book_all_orders',
                                       'is_book_order_onhold',
                                       'hkex_wrk_qty_is_zero_all_held_orders',
                                       'wrk_qty is 0 for working GTDs after an OS restart')

    order_book_table.add_rule(hkex_order_roundtrip.hkex_wrk_qty_is_wrk_qty_book_all_non_held_orders, cond='False')
    order_book_table.optout_rule('wrk_qty_is_wrk_qty_book_all_orders',
                                       'is_book_order_onhold',
                                       'hkex_wrk_qty_is_wrk_qty_book_all_non_held_orders',
                                       'Different algorithm for getting non-held orders on Eurex')

    # agile attachments
    order_book_table.add_rule(hkex_order_roundtrip.agile_id_tif_expired_orders_hkex, cond='False')
    order_book_table.optout_rule('agile_id_tif_expired_orders_not_received_all_orders',
                                       'is_book_order_onhold',
                                       'agile_id_tif_expired_orders_hkex',
                                       'Eurex adds agile attachment TIF_EXPIRED_ORDER for working GTDs after an OS restart')

