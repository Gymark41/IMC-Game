# Trading class for the example game
from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Listing

import numpy as np
import pandas as pd
import math


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}


        for sym in state.listings.keys():
            # print(sym, type(state.listings[sym]), state.listings[sym])

            local_orderbook = CombinedOrderbook(state.order_depths[sym], state.listings[sym])
            if local_orderbook.best_sell_price:
                # orders = local_orderbook.vwap_buy(local_orderbook.best_sell_price + 10, 0.3)
                orders = local_orderbook.vwap_sell(local_orderbook.best_buy_price - 10, 0.5)

                result[sym] = orders
                print(state.timestamp, orders)
                print(state.timestamp, local_orderbook.df_buy_orders)

        # print(state.listings['BANANAS']['symbol'])
        #
        # print(state.toJSON())
        return result


class CombinedOrderbook:
    """A combination of the orderbook depth for each listing. Allows us to implement custom methods"""

    def __init__(self, order_depth: OrderDepth, listing: Listing):
        # print(order_depth)
        self.df_buy_orders = pd.DataFrame(order_depth.buy_orders.items(), columns=['price', 'amount'])
        self.df_sell_orders = pd.DataFrame(order_depth.sell_orders.items(), columns=['price', 'amount'])

        self.df_buy_orders["price"] = self.df_buy_orders['price'].astype(int)
        self.df_sell_orders["price"] = self.df_sell_orders['price'].astype(int)

        self.df_buy_orders = self.df_buy_orders.sort_values(by=['price'])
        self.df_sell_orders = self.df_sell_orders.sort_values(by=['price'])


        # print(listing)
        # print(self.df_sell_orders)

        self.symbol = listing['symbol']
        # print(listing)
        self.product = listing['product']

        self.best_sell_price = None
        self.best_buy_price = None
        self._calculate_buy_sell()

    def _calculate_buy_sell(self):
        # print(self.df_buy_orders)
        if not self.best_buy_price and len(self.df_buy_orders) > 0:
            self.best_buy_price = self.df_buy_orders['price'].max()
        if not self.best_sell_price and len(self.df_buy_orders) > 0:
            self.best_sell_price = self.df_sell_orders['price'].min()

    def vwap_buy(self, price_range: int, percentage: float, amount_cap=None) -> List[Order]:
        """Creates a Volume Weight Average Price Purchase, returns a dict of what we want to fulfill"""
        df_sell_order_within_price = self.df_sell_orders[self.df_sell_orders.price <= price_range]
        total_amount = abs(df_sell_order_within_price.amount.sum())
        df_sorted = df_sell_order_within_price.sort_values('price')

        return self._vwap_combined(df_sorted, total_amount, percentage, amount_cap)

    def vwap_sell(self, price_range: int, percentage: float, amount_cap=None) -> List[Order]:
        """Creates a Volume Weight Average Price Purchase, returns a dict of what we want to fulfill"""
        df_buy_order_within_price = self.df_buy_orders[self.df_buy_orders.price >= price_range]
        total_amount = abs(df_buy_order_within_price.amount.sum())
        df_sorted = df_buy_order_within_price.sort_values(by=['price'], ascending=False)

        return self._vwap_combined(df_sorted, total_amount, percentage, amount_cap)

    def _vwap_combined(self, df_sorted,  total_amount, percentage:float, amount_cap=None):

        purchase_quantity = math.ceil(total_amount * percentage) if not amount_cap else min(
            math.ceil(total_amount * percentage), amount_cap)

        orders = []

        for index, row in df_sorted.iterrows():
            purchase_on_row_amount = min(abs(row['amount']), abs(purchase_quantity))
            purchase_order = Order(self.symbol, row.price, purchase_on_row_amount)
            orders.append(purchase_order)
            purchase_quantity -= purchase_on_row_amount

            if purchase_quantity <= 0:
                break

        # print(orders)
        return orders
