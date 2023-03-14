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
