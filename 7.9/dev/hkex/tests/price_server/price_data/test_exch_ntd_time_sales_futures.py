from captain.lib.controlled_types import Worker

from commontests.price_server.templates.test_exch_ntd_time_sales_template import BaseTestNTDTimeAndSales
from commontests.utils import register_crews

from hkex.tests.utils import (mf_config, futures_filter, PFX_enabled, accumulate_ltq, EchoCount)

# Overrides
from hkex.tests.overrides import HKExOverrides


class TestNTDTimeAndSalesFutures(BaseTestNTDTimeAndSales):
    def __init__(self):
        super(TestNTDTimeAndSalesFutures, self).__init__()
        register_crews(Worker.DIRECT)

        self.market_config_and_filters = [(mf_config, [futures_filter])]

        self.accumulate_ltq_and_Aconfig_settings = [(False, {PFX_enabled: 'true', accumulate_ltq: '1', EchoCount: '0'}),
                                                    (True, {PFX_enabled: 'true', accumulate_ltq: '0', EchoCount: '0'})]

        self.overrides = HKExOverrides