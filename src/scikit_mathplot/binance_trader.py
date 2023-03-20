# -*- coding: utf-8 -*-

import numpy as np
from sklearn import linear_model
from datetime import datetime
import matplotlib.pyplot as plt


CRYPTO, VALUTA = range(2)
BOUGHT, SOLD = range(2)
HISTORY, FUTURE = range(2)
ZERO, FIRST, LAST = range(3)


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

    _traces = [2, 2]
    _history_trace = 2
    _future_trace = 2

    _future_zero = 0
    _future_first = 0
    _future_last = 0

    _diff_0 = 0
    _diff_first = 0
    _diff_last = 0

    _wallet = [0.0, 0.0]
    _equival = [0.0, 0.0]

    _bought_rate = 0
    _sold_rate = 0

    def __init__(self, fig=None, currency="BTC", wallet=(0.0, 0.0), traces=(2, 2)):

        # ********************************************************
        self._currency = currency

        self._wallet = list(wallet)
        self._traces = list(traces)

        self.fig = fig
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.on = False
        self.inst = True  # show instructions from the beginning

    def __str__(self):
        str_obj = ""

        str_obj += " Trader currency: " + self._currency
        str_obj += f' samples={self.get_sample_count}'
        str_obj += f' timedelta={self._time_delta}'
        str_obj += f' wallet={self._wallet}'
        str_obj += f' traces={self._traces}'

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
    def get_traces(self):
        return self._traces

    @property
    def get_rates(self):
        return self._bought_rate, self._sold_rate

    def predict_future(self):

        if self._times is None:
            return 1, 1

        self._history_trace = self._traces[HISTORY]
        self._future_trace = self._traces[FUTURE]

        sample_from = self.get_sample_count - self._history_trace
        sample_to = self.get_sample_count
        # print("get_sample_count=", self.get_sample_count, sample_from, sample_to, history_trace)

        regression = linear_model.LinearRegression()

        regression.fit(self._times[sample_from:sample_to, :], self._rates[sample_from:sample_to])

        self._future_times = np.array([self._times[sample_to - 1][0] + (itm * self._time_delta)
                                       for itm in range(self._future_trace)]).reshape(-1, 1)
        self._future_rates = regression.predict(self._future_times)

        return self._future_times, self._future_rates

    def get_futures(self):

        if self._rates is None or self._future_rates is None:
            return 0

        # print(len(self._future_rates), len(self._rates), self._future_rates[0], self._rates[self.get_sample_count-1])
        self._future_zero = self._future_rates[0]
        self._future_first = self._future_rates[1]
        self._future_last = self._future_rates[self._future_trace - 1]

        return self._future_zero, self._future_first, self._future_last

    def get_diffs(self):

        if self._rates is None or self._future_rates is None:
            return 0

        # print(len(self._future_rates), len(self._rates), self._future_rates[0], self._rates[self.get_sample_count-1])
        self._diff_0 = self._future_rates[0] - self._rates[self.get_sample_count-1]
        self._diff_first = self._future_rates[1] - self._future_rates[0]
        self._diff_last = self._future_rates[self._future_trace - 1] - self._future_rates[0]

        return self._diff_0, self._diff_first, self._diff_last


    def top_up_wallet(self, crypto=0, valuta=0):
        self._wallet[CRYPTO] += crypto
        self._wallet[VALUTA] += valuta

        return self._wallet

    def equival_wallet(self):
        cur_rate = self._rates[self.get_sample_count - 1]
        if self._wallet[CRYPTO] > 0:
            self._equival[VALUTA] = self._wallet[CRYPTO] * cur_rate
        if self._wallet[VALUTA] > 0:
            self._equival[CRYPTO] = self._wallet[VALUTA] / cur_rate

        return self._equival

    def sell_crypto(self):
        self._bought_rate = self._rates[self.get_sample_count - 1]
        crypto = self._wallet[CRYPTO]
        valuta = self._wallet[VALUTA]

        res_valuta = crypto * self._bought_rate
        self._wallet[CRYPTO] = 0
        self._wallet[1] += res_valuta

    def buy_crypto(self):
        self._sold_rate = self._rates[self.get_sample_count - 1]
        crypto = self._wallet[CRYPTO]
        valuta = self._wallet[VALUTA]

        res_crypto = valuta / self._sold_rate
        self._wallet[VALUTA] = 0
        self._wallet[CRYPTO] += res_crypto

    def block_sell(self):
        block = False
        curr_rate = self._rates[self.get_sample_count - 1]
        if self._sold_rate <= (1.001*curr_rate):
            block = True

        return block

    def _historical_inc(self):
        if self._traces[HISTORY] < self.get_sample_count:
            self._traces[HISTORY] += 1
            print("HISTORICAL=", self._traces[HISTORY])

    def _historical_dec(self):
        if self._traces[HISTORY] > 2:
            self._traces[HISTORY] -= 1
            print("HISTORICAL=", self._traces[HISTORY])

    def _future_inc(self):
        if self._traces[FUTURE] < 20:
            self._traces[FUTURE] += 1
            print("FUTURE=", self._traces[FUTURE])

    def _future_dec(self):
        if self._traces[FUTURE] > 2:
            self._traces[FUTURE] -= 1
            print("FUTURE=", self._traces[FUTURE])

    def on_key_press(self, event):

        print(event.key, "::", end="")

        if event.key == '1':
            if self.on:
                self._historical_inc()
        if event.key == '2':
            if self.on:
                self._historical_dec()
        if event.key == '3':
            if self.on:
                self._future_dec()
        if event.key == '4':
            if self.on:
                self._future_inc()

        if event.key == 'n':
            # self.distract = not self.distract
            pass

        if event.key == 'g':
            # self.on = not self.on
            pass
        if event.key == 't':
            self.on = not self.on
            print(self.on)


if __name__ == '__main__':

    fig = plt.figure(figsize=(10, 14))  # Figure(400x754)

    currency = 'USDT'
    trader_obj = Trader(fig=fig, currency=currency, wallet=(0.00123, 10.50), traces=(7, 10))
    text = ""
    text += str(trader_obj)
    print(text)
    # #######################################################################################
