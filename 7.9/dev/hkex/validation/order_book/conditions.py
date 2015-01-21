import logging

from ttapi import aenums

from pyrate import Manager

log = logging.getLogger(__name__)

__all__ = ['get_all_held_orders', 'get_all_originally_held_orders',
           'get_all_persisted_orders', 'get_all_non_persisted_orders',
           'get_all_non_held_orders', 'is_book_order_onhold',
           'is_book_order_originally_onhold', 'is_book_order_persisted',
           'is_book_order_working']

ttus = Manager.getTTUserSetup()

def get_all_held_orders(before):
    held_orders = {}

    for sok, order in before.book.items():
        if before.book[sok].order_status == aenums.TT_ORDER_STATUS_HOLD:
            held_orders[sok] = order
    return held_orders

def get_all_originally_held_orders(before):
    held_orders = {}

    for sok, order in before.book.items():
        if before.book[sok].order_status == aenums.TT_ORDER_STATUS_HOLD:
            held_orders[sok] = order
    return held_orders

def get_all_persisted_orders(before):
    persisted_orders = {}

    for sok, order in before.book.items():
        if before.book[sok].order_status != aenums.TT_ORDER_STATUS_HOLD:
            persisted_orders[sok] = order
    return persisted_orders

def get_all_non_persisted_orders(before):
    non_persisted_orders = {}

    for sok, order in before.book.items():
        if before.book[sok].order_status == aenums.TT_ORDER_STATUS_HOLD:
            non_persisted_orders[sok] = order
    return non_persisted_orders

def get_all_non_held_orders(before):
    non_held_orders = {}

    for sok, order in before.book.items():
        if before.book[sok].order_status != aenums.TT_ORDER_STATUS_HOLD:
            non_held_orders[sok] = order
    return non_held_orders

def is_book_order_onhold(action, before, after):
    if get_all_held_orders(before):
        return True
    return False

def is_book_order_originally_onhold(action, before, after):
    if get_all_originally_held_orders(before):
        return True
    return False

def is_book_order_persisted(action, before, after):
    if get_all_persisted_orders(before):
        return True
    return False

def is_book_order_working(action, before, after):
    if get_all_non_held_orders(before):
        return True
    return False
