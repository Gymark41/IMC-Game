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

        #
        # for sym in state.listings.keys():
        #     # print(sym, type(state.listings[sym]), state.listings[sym])
        #     local_orderbook = CombinedOrderbook(state.order_depths[sym], state.listings[sym])
        #     orders = local_orderbook.vwap_buy(local_orderbook.best_sell_price + 10, 0.5, amount_cap=10)
        #     result[sym] = orders

        print(state.listings['BANANAS']['symbol'])

        print(state.toJSON())
        return result


class CombinedOrderbook:
    """A combination of the orderbook depth for each listing. Allows us to implement custom methods"""

    def __init__(self, order_depth: OrderDepth, listing: Listing):
        self.df_buy_orders = pd.DataFrame(order_depth.buy_orders, columns=['price', 'amount'])
        self.df_sell_orders = pd.DataFrame(order_depth.sell_orders, columns=['price', 'amount'])

        self.df_buy_orders["price"] = self.df_buy_orders['price'].astype(int)
        self.df_sell_orders["price"] = self.df_sell_orders['price'].astype(int)

        self.df_buy_orders = self.df_buy_orders['price'].sort_values()
        self.df_buy_orders = self.df_sell_orders['price'].sort_values()


        # print(listing)
        # print(self.df_sell_orders)

        self.symbol = listing['symbol']
        self.product = listing['product']

        self.best_sell_price = None
        self.best_buy_price = None
        self._calculate_buy_sell()

    def _calculate_buy_sell(self):
        if not self.best_buy_price:
            self.best_buy_price = self.df_buy_orders['price'].max()
        if not self.best_sell_price:
            self.best_sell_price = self.df_sell_orders['price'].min()


    def vwap_buy(self, price_range: int, percentage: float, amount_cap=None) -> List[Order]:
        """Creates a Volume Weight Average Price Purchase, returns a dict of what we want to fulfill"""
        df_sell_order_within_price = self.df_sell_orders[self.df_sell_orders.price <= price_range]
        total_amount = df_sell_order_within_price.amount.sum()
        purchase_quantity = math.ceil(total_amount * percentage) if not amount_cap else min(
            math.ceil(total_amount * percentage), amount_cap)
        df_sorted = df_sell_order_within_price.sort_values('price')

        orders = []
        for row in df_sorted.iterrows():
            purchase_on_row_amount = min(row['amount'], purchase_quantity)
            purchase_order = Order(self.symbol, row.price, purchase_on_row_amount)
            orders.append(purchase_order)
            purchase_quantity -= purchase_on_row_amount

            if purchase_quantity <= 0:
                break

        # print(orders)
        return orders
