# -*- coding: utf-8 -*-

import numpy as np
from sklearn import linear_model
from datetime import datetime


class Trader:
    """
        This is an trader class
    """
    _currency = "UNDEF"

    _times = None
    _rates = None
    _time_delta = 0

    _future_times = None
    _future_rates = None

    _history_trace = 2
    _future_trace = 2

    _diff_0 = 0
    _diff_1 = 0
    _diff_last = 0

    _wallet = [0.0, 0.0]

    _buy_rate = 0
    _sell_rate = 0

    def __init__(self, currency="BTC", wallet=(0.0, 0.0)):

        # ********************************************************
        self._currency = currency
        self._wallet = list(wallet)

    def __str__(self):
        str_obj = ""

        str_obj += " Trader currency: " + self._currency
        str_obj += f' samples={self.get_sample_count}'
        str_obj += f' timedelta={self._time_delta}'
        str_obj += f' wallet={self._wallet}'

        return str_obj

    def __repr__(self):
        return f'Currensy name={self._currency}'

    def set_kilns(self, times, rates):
        self._times = times
        self._rates = rates
        self._time_delta = times[1] - times[0]

    @property
    def get_sample_count(self):
        if self._times is not None:
            return len(self._times)
        else:
            return 0

    @property
    def get_currency(self):
        return self._currency

    @property
    def get_wallet(self):
        return self._wallet

    @property
    def get_rates(self):
        return self._buy_rate, self._sell_rate

    def predict_future(self, history_trace=1, future_trace=2):

        if self._times is None:
            return 1, 1

        self._history_trace = history_trace
        self._future_trace = future_trace

        sample_from = self.get_sample_count - self._history_trace
        sample_to = self.get_sample_count
        # print("get_sample_count=", self.get_sample_count, sample_from, sample_to, history_trace)

        regression = linear_model.LinearRegression()

        regression.fit(self._times[sample_from:sample_to, :], self._rates[sample_from:sample_to])

        self._future_times = np.array([self._times[sample_to - 1][0] + (itm * self._time_delta)
                                       for itm in range(self._future_trace)]).reshape(-1, 1)
        self._future_rates = regression.predict(self._future_times)

        return self._future_times, self._future_rates

    def get_diffs(self):

        if self._rates is None or self._future_rates is None:
            return 0

        # print(len(self._future_rates), len(self._rates), self._future_rates[0], self._rates[self.get_sample_count-1])
        self._diff_0 = self._future_rates[0] - self._rates[self.get_sample_count-1]
        self._diff_1 = self._future_rates[1] - self._future_rates[0]
        self._diff_last = self._future_rates[self._future_trace - 1] - self._future_rates[0]

        return self._diff_0, self._diff_1, self._diff_last

    def top_up_wallet(self, crypto=0, valuta=0):
        self._wallet[0] += crypto
        self._wallet[1] += valuta

        return self._wallet

    def buy_crypto(self):
        self._buy_rate = self._rates[self.get_sample_count-1]
        crypto = self._wallet[0]
        valuta = self._wallet[1]

        res_valuta = crypto * self._buy_rate
        self._wallet[0] = 0
        self._wallet[1] += res_valuta

    def sell_crypto(self):
        self._sell_rate = self._rates[self.get_sample_count - 1]
        crypto = self._wallet[0]
        valuta = self._wallet[1]

        res_crypto = valuta / self._sell_rate
        self._wallet[1] = 0
        self._wallet[0] += res_crypto


if __name__ == '__main__':

    currency = 'USDT'

    trader_obj = Trader(currency=currency, )
    text = ""
    text += str(trader_obj)
    print(text)
    # #######################################################################################
