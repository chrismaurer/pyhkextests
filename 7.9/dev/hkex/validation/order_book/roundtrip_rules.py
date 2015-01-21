import operator

from ttapi import aenums, cppclient

from basis_validation.utils import get_core_vrmf
from basis_validation.order_book.utils import iter_orders, get_all_non_held_orders

# captain imports
from pyrate import Manager
from captain.plugins.validator import MultiError
from ttutil import in_, not_in_

from basis_validation.utils import compare
from basis_validation.order_book import rules
from basis_validation.order_book.utils import *
from hkex.tests.utils import *
from conditions import *

ttus = Manager.getTTUserSetup()

def hkex_exec_qty_is_same_as_fill_qty_book_all_orders(action, before, after):
    iter_orders(action, before, after, before.book,
                'after.book[sok].exec_qty', 'before.book[sok].fill_qty')

def exchange_credentials_is_populated_non_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_non_held_orders(before),
                'after.book[sok].exchange_credentials', "''", operator.ne)

def hkex_exec_qty_is_zero_all_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_held_orders(before),
                'after.book[sok].exec_qty', "0")

def hkex_fill_qty_is_zero_all_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_held_orders(before),
                'after.book[sok].fill_qty', "0")

def hkex_fill_qty_is_fill_qty_book_all_non_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_non_held_orders(before),
                'after.book[sok].fill_qty', "before.book[sok].fill_qty")

def hkex_order_qty_is_wrk_qty_book_all_persisted_orders(action, before, after):
    iter_orders(action, before, after, get_all_persisted_orders(before),
                'after.book[sok].order_qty', 'before.book[sok].wrk_qty')

def hkex_order_qty_is_order_qty_book_all_non_persisted_orders(action, before, after):
    iter_orders(action, before, after, get_all_non_persisted_orders(before),
                'after.book[sok].order_qty', "before.book[sok].order_qty")

def hkex_wrk_qty_is_zero_all_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_held_orders(before),
                'after.book[sok].wrk_qty', "0")

def hkex_wrk_qty_is_wrk_qty_book_all_non_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_non_held_orders(before),
                'after.book[sok].wrk_qty', "before.book[sok].wrk_qty")

def exchange_credentials_is_populated_held_orders(action, before, after):
    iter_orders(action, before, after, get_all_held_orders(before),
                'after.book[sok].exchange_credentials', "''", op=operator.ne)

def agile_id_tif_expired_orders_hkex(action, before, after):
    TIF_EXPIRED_ORDER = 1036
    sok_err_list = []

    for sok, order in before.book.items():
        agile_ids = [id_ for id_ in after.book[sok].RetrieveAttachmentIDs()]
        if before.book[sok].order_status != aenums.TT_ORDER_STATUS_HOLD:
            try:
                compare(TIF_EXPIRED_ORDER, agile_ids, in_)
            except Exception as e:
                sok_err_list.append((e, 'SOK {0}'.format(sok)))
        else:
            try:
                compare(TIF_EXPIRED_ORDER, agile_ids, not_in_)
            except Exception as e:
                sok_err_list.append((e, 'SOK {0}'.format(sok)))

    if len(sok_err_list) > 0:
        raise MultiError(sok_err_list)



