"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time



class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()

        :type order: List
        order represents the list of products that the costumer bought

        :type cart_id: List
        cart_id is the list of cart_id for each cart in carts
        """
        Thread.__init__(self)
        self.carts = carts
        self.name = kwargs["name"]
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.order = []
        self.cart_id = []
        i = 0
        while i < len(carts):
            self.cart_id.append(self.marketplace.new_cart())
            i += 1

    def run(self):
        """
        Iterate through the list of carts.
        For each cart, execute the commands according to
        their type and the given quantity:
        -for add, the consumer adds the product to their cart
        if he fails he waits for self.retry_wait_time
        -for remove, the consumer removes the product from the cart

        For each cart_id, an order is placed an the lists obtained
        are concatenated to the self.order list.
        """
        for cart in range(len(self.carts)):
            for command in self.carts[cart]:
                if command["type"] == "add":
                    i = 0
                    while i < command["quantity"]:
                        tmp = self.marketplace.add_to_cart(self.cart_id[cart], command["product"])
                        if not tmp:
                            time.sleep(self.retry_wait_time)
                        else:
                            i += 1
                else:
                    for i in range(command["quantity"]):
                        self.marketplace.remove_from_cart(self.cart_id[cart], command["product"])
        for i in range(len(self.cart_id)):
            self.order.extend(self.marketplace.place_order(self.cart_id[i]))
        for tmp in self.order:
            print("{} bought {}".format(self.name, tmp))
