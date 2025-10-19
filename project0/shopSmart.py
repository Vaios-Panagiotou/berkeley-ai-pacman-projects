# shopSmart.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

#written by alphawastaken
"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""
from __future__ import print_function
import shop


def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """

    if orderList == [] or fruitShops == []:
        return None
    else:
        available_shops = []  #a list to store shops with all the desired fruits.

        #iterate through each fruit shop in the list.
        for shop in fruitShops:

            shop_products = 0  #a counter for matching products.

            #check if each fruit in the orderList is available in the shop.
            for i in orderList:
                if i[0] in shop.fruitPrices:
                    shop_products += 1

            # If the shop has all the desired fruits, add it to the available_shops list.
            if shop_products == len(orderList):
                available_shops.append(shop)
            shop_products = 0  #reset the counter for the next shop.

       

        if available_shops == []:
            return None
        else:
            best_shop = available_shops[0]

            #find the best shop based on the total price of the order.
            for shop in available_shops:
                if shop.getPriceOfOrder(orderList) < best_shop.getPriceOfOrder(orderList):
                    best_shop = shop

            return best_shop  #return the best shop found.





if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orders = [('apples', 1.0), ('oranges', 3.0)]
    dir1 = {'apples': 2.0, 'oranges': 1.0}
    shop1 = shop.FruitShop('shop1', dir1)
    dir2 = {'apples': 1.0, 'oranges': 5.0}
    shop2 = shop.FruitShop('shop2', dir2)
    shops = [shop1, shop2]
    print("For orders ", orders, ", the best shop is",
          shopSmart(orders, shops).getName())
    orders = [('apples', 3.0)]
    print("For orders: ", orders, ", the best shop is",
          shopSmart(orders, shops).getName())
