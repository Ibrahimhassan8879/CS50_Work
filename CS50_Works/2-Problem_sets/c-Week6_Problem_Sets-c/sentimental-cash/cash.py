# TODO
from cs50 import get_float
from math import trunc

Money = get_float("Change owed: ")
while (Money <= 0):
    Money = get_float("Change owed: ")
Money = 100 * Money


count_quarters = (Money - (Money % 25))/25
Money = Money - (count_quarters * 25)

count_dimes = (Money - (Money % 10))/10
Money = Money - (count_dimes * 10)


count_nickels = (Money - (Money % 5))/5
Money = Money - (count_nickels * 5)


count_pennies = (Money - (Money % 1))/1
Money = Money - (count_pennies * 1)

total_coins = count_quarters + count_dimes + count_nickels + count_pennies
print(total_coins)
