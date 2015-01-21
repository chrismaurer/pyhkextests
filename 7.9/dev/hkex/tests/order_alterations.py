###############################################################################
#
#                    Unpublished Work Copyright (c) 2010-2013
#                  Trading Technologies International, Inc.
#                       All Rights Reserved Worldwide
#
#          # # #   S T R I C T L Y   P R O P R I E T A R Y   # # #
#
# WARNING:  This program (or document) is unpublished, proprietary property
# of Trading Technologies International, Inc. and is to be maintained in
# strict confidence. Unauthorized reproduction, distribution or disclosure
# of this program (or document), or any program (or document) derived from
# it is prohibited by State and Federal law, and by local law outside of
# the U.S.
#
###############################################################################

# python imports
from collections import defaultdict

# pycppclient imports
from ttapi import cppclient, aenums

# captain imports
from pyrate.ttapi.order import TTAPIOrder
from captain import bind
from captain.lib import ChangeSide, SetOrderAttrs, TickRel
from captain.lib.controlled_types import (Tif, OrderType, OrderRes, ClearingMember,
                                          ExchangeClearingAccount as ECA)

__all__ = ['causes_del_rej', 'causes_hold_rej', 'causes_sub_rej', 'chg_into_del', 'chg_into_ifill',
           'chg_into_udel', 'held_chg', 'held_chg_rej', 'held_rep', 'held_rep_rej', 'rep_into_ifill',
           'resting_chg', 'resting_chg_rej', 'resting_rep', 'resting_rep_arej', 'resting_rep_drej',
           'resting_rep_rej', 'post_trig_chg', 'post_trig_rep', 'stop_chg', 'stop_rep',
           'lsm_chg', 'lsm_rep', 'ob_scope_chg', 'ob_scope_rep', 'chg_for_itrig',
           'rep_for_itrig']

ECA.VALID_PRIMARY.register('NewAccount')
ECA.VALID_NON_PRIMARY.register('xyx')
ECA.NUMERIC.register('1234134')
ClearingMember.VALID.register('cpngu')

resting_chg = [bind(SetOrderAttrs, {'chg_qty':2}),
               bind(TickRel, 2),
               bind(SetOrderAttrs, {'tif':Tif.GTD}),
               bind(SetOrderAttrs, {'acct_type': aenums.TT_ACCT_GIVEUP_1,
                                    'clearing_mbr':ClearingMember.VALID})]

resting_rep = [bind(SetOrderAttrs, {'chg_qty':-1}),
               bind(TickRel, 2),
               bind(SetOrderAttrs, {'tif':Tif.GTD}),
               [(bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_PRIMARY})),
                (bind(SetOrderAttrs, {'chg_qty':1}))]]
if hasattr(TTAPIOrder(), 'routing_key'):
    resting_rep.append(bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_NON_PRIMARY,
                                            'routing_key':ECA.VALID_NON_PRIMARY}))
else:
    resting_rep.append(bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_NON_PRIMARY}))


chg_into_del = [bind(SetOrderAttrs, {'chg_qty': cppclient.TT_INVALID_QTY})]

chg_into_udel = [None]

chg_into_ifill = [bind(SetOrderAttrs, {'chg_qty':2}),
                  bind(TickRel, 2)]

if hasattr(TTAPIOrder(), 'routing_key'):
    rep_into_ifill = [bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_NON_PRIMARY,
                                           'routing_key':ECA.VALID_NON_PRIMARY}),
                      [(bind(SetOrderAttrs, {'chg_qty':-1,
                                             'exchange_clearing_account':ECA.VALID_NON_PRIMARY,
                                             'routing_key':ECA.VALID_NON_PRIMARY})),
                       (bind(TickRel, 2))]]
else:
    rep_into_ifill = [bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_NON_PRIMARY}),
                      [(bind(SetOrderAttrs, {'chg_qty':-1,
                                             'exchange_clearing_account':ECA.VALID_NON_PRIMARY})),
                       (bind(TickRel, 2))]]

resting_chg_rej = [bind(SetOrderAttrs, {'limit_prc':cppclient.TT_INVALID_PRICE})]

resting_rep_rej = [bind(SetOrderAttrs, {'order_no':0})]

resting_rep_drej = [None]

resting_rep_arej = [bind(SetOrderAttrs, {'chg_qty': cppclient.TT_INVALID_QTY})]

causes_del_rej = [bind(SetOrderAttrs, {'order_no':0})]

causes_hold_rej = [bind(SetOrderAttrs, {'order_no':0})]

causes_sub_rej = [bind(SetOrderAttrs, {'acct_type':aenums.TT_ACCT_GIVEUP_1,
                                       'clearing_mbr':ClearingMember.BLANK})]

held_chg = resting_chg

held_chg_rej = causes_hold_rej

held_rep = resting_rep

held_rep_rej = resting_rep_rej

post_trig_chg = resting_chg

post_trig_rep = resting_rep

stop_chg = resting_chg
stop_rep = resting_rep
if hasattr(TTAPIOrder(), 'routing_key'):
    stop_rep.append(bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_NON_PRIMARY,
                                         'routing_key':ECA.VALID_NON_PRIMARY}))
else:
    stop_rep.append(bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_NON_PRIMARY}))

chg_for_itrig = []
rep_for_itrig = []
lsm_chg = []
lsm_rep = []

###########################
# OrderBook scenario sets #
###########################
ob_scope_chg = defaultdict(list)
for ob_scope in ['chg_to_book',
                 'pfill_chg_to_book',
                 'pfill_hold_chg_to_book']:
    ob_scope_chg[ob_scope] = [bind(SetOrderAttrs, {'chg_qty':-1}),
                              bind(SetOrderAttrs, {'exchange_clearing_account':ECA.VALID_PRIMARY}),
                              bind(SetOrderAttrs, {'chg_qty':1})]
for ob_scope in ['chg_to_mid_book',
                 'chg_as_held_to_mid_book']:
    ob_scope_chg[ob_scope] = [bind(SetOrderAttrs, {'chg_qty':7})]

ob_scope_chg['pfill_chg_to_share_book'] = [bind(SetOrderAttrs, {'chg_qty':5})]

ob_scope_rep = {'rep_to_book': ob_scope_chg['chg_to_book'],
                'rep_to_mid_book': ob_scope_chg['chg_to_mid_book'],
                'rep_as_held_to_mid_book': ob_scope_chg['chg_as_held_to_mid_book']}
