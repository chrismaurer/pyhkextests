from captain.lib.controlled_types import Worker

from commontests.price_server.templates.test_exch_inside_market_template import BaseInsideMarketDepth
from commontests.utils import register_crews

from hkex.tests.utils import (mf_config, mf_option_config, mf_multi_leg_config,
                              option_filter, bounds_1_5, bounds_5_7, bounds_1_10,
                              PFX_enabled, NumDepthLevels, EchoCount)

from hkex.tests.overrides import HKExOverrides

__all__ = ['TestInsideMarketOptions']

class TestInsideMarketOptions(BaseInsideMarketDepth):

    def __init__(self):

        super(TestInsideMarketOptions, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters=[(mf_option_config, [option_filter])]

        self.visible_levels_and_Aconfig_settings = [(1, {PFX_enabled : 'true', NumDepthLevels : '5', EchoCount : '0'})]

        self.tradable_price_tick_bounds = bounds_1_5
        self.orders_per_price_level_bounds = bounds_5_7
        self.order_round_lot_multiplier_bounds = bounds_1_10
        self.overrides = HKExOverrides