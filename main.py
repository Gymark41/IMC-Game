# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from datamodel import *
import json

from ExampleTrader import Trader

from types import SimpleNamespace


def generate_states():
    # Use a breakpoint in the code line below to debug your script.

    temp_states = []
    f = open("tradestate.txt", "r")
    lines = f.readlines()
    for line in lines:
        # print(line)
        leading_number = 0
        for c in line:
            if c == '{':
                break
            else:
                leading_number += 1

        x = json.loads(line[leading_number:])
        test_state = TradingState(**x)
        # print(test_state)

        # new_dict_listings = {}
        # for key in test_state.listings.keys():
        #     listings = test_state.listings[key]
        #     new_dict_listings[key] = Listing(**listings)
        #
        # test_state.listings = new_dict_listings
        # print("start:", test_state.order_depths)
        for key in test_state.order_depths.keys():
            order_depths = test_state.order_depths[key]
            # print(order_depths)
            new_order_depths = OrderDepth()
            new_order_depths.buy_orders = order_depths['buy_orders']
            new_order_depths.sell_orders = order_depths['sell_orders']
            # print(new_order_depths.buy_orders)
            test_state.order_depths[key] = new_order_depths

        # print("final: ", test_state.order_depths['BANANAS'].buy_orders)

        new_dict_own_trades = {}
        for key in test_state.own_trades.keys():
            own_trades = test_state.own_trades[key]
            new_list_for_own_trades = []
            for trade in own_trades:
                new_list_for_own_trades.append(Trade(**trade))
        test_state.own_trades = new_dict_own_trades

        new_dict_market_trades = {}
        for key in test_state.market_trades.keys():
            market_trades = test_state.market_trades[key]
            new_list_for_market_trades = []
            for trade in market_trades:
                new_list_for_market_trades.append(Trade(**trade))
        test_state.market_trades = new_dict_market_trades

        temp_states.append(test_state)
    return temp_states

def main():
    states = generate_states()
    myTrader = Trader()
    for state in states:
        myTrader.run(state)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
