"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time



class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()

        @type producer_id: Int
        producer_id is the id of the producer
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.producer_id = self.marketplace.register_producer()

    def run(self):
        """
        Iterate through the list of products.
        For each product, the producer tries to publish the given quantity
        if he succeeds, he waits the given time,
        if he fails, he waits for self.republish_wait_time and he tries again.
        """
        while True:
            for i in range(len(self.products)):
                qty = 0
                while qty < self.products[i][1]:
                    tmp = self.marketplace.publish(self.producer_id, self.products[i][0])
                    if not tmp:
                        time.sleep(self.republish_wait_time)
                    else:
                        time.sleep(self.products[i][2])
                        qty += 1
