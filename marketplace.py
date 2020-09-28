"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer

        :type producers: Dictionary
        producers saves the producer_id as a key and a list of products as value

        :type carts: Dictionary
        carts saves the cart_id as a key and a list of dictionaries as value
        each of these dictionaries has a "producer" and a "product"

        :type producer_lock: Lock
        producer_lock is a lock used for the producers dictionary

        :type cart_lock: Lock
        cart_lock is a lock used for the carts dictionary
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = {}
        self.carts = {}
        self.producer_lock = Lock()
        self.cart_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.

        The producer_id is obtained by calculating
        the number of existent producers.
        Then, a list is created as the value for this dict key(producer_id).
        """
        self.producer_lock.acquire()
        producer_id = len(self.producers)
        self.producer_lock.release()
        self.producers[producer_id] = []

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.

        Check if the producer_id is a key in the producers dict.
        If true, check if there is any more space in the product list of this producer.
        If true, add the product in the product list of the producer and return True.
        In any other case, return False.
        """
        if producer_id in self.producers:
            if len(self.producers[producer_id]) < self.queue_size_per_producer:
                self.producers[producer_id].append(product)
                return True
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id

        The cart_id is obtained by calculating
        the number of existent carts.
        Then, a list is created as the value for this dict key(cart_id).
        """
        self.cart_lock.acquire()
        cart_id = len(self.carts)
        self.cart_lock.release()
        self.carts[cart_id] = []

        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again

        Check if the cart_id given is a key in the carts dict.
        If true, iterate through the producers dict keys and
        check if the product is found in the product lists associated.
        If true, create a dictionary with "producer" and "product" and
        add it to the carts[cart_id] list and remove the product from
        the product list of the producer.
        """
        if cart_id in self.carts:
            for tmp in self.producers:
                if product in self.producers[tmp]:
                    try:
                        aux = {}
                        aux["producer"] = tmp
                        aux["product"] = product
                        self.producers[tmp].remove(product)
                        self.carts[cart_id].append(aux)
                        return True
                    except ValueError:
                        pass
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart

        Check if the cart_id given is a key in the carts dict.
        If true, iterate through the carts[cart_id] list and check if
        any of the dictionaries in this list have the given product in
        their "product" field.
        If true, add the product to the producers dict in the product list
        of the associated producer and remove the found dictionary from
        the carts[cart_id] list.
        """
        if cart_id in self.carts:
            for tmp in self.carts[cart_id]:
                if tmp["product"] == product:
                    self.producers[tmp["producer"]].append(product)
                    self.carts[cart_id].remove(tmp)
                    break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart

        Create a list and add every product of the carts[cart_id] list.
        """
        order = []
        for tmp in self.carts[cart_id]:
            order.append(tmp["product"])
        return order
