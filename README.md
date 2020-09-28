Radescu Ioana

# Marketplace

	This project implements a Marketplace which is used by multiple producers in order to sell their products
	and by multiple consumers that are looking to buy the available products.


# CONSUMER

	Each cosumer has a list of add an remove operations, a name, a reference to the marketplace, a retry_wait_time, 
	a list of products that he buys and a list of cart ids.
	To build the list of cart ids the function new_cart is called and the id received is added to the list.

	The consumer will go through the list of carts and for every command he will test its type and do the specified 
	action as many times as it is required by the given quantity. 
	For an add command, the consumer will call the function add_to_cart in order to add the given product to the 
	current cart. If the add fails, he will wait for retry_wait_time and will try again.
	For a remove command, the consumer will call the remove_from_cart function to remove the product from the 
	current cart.

	After all the commands are executed, the consumer will call the function place_order on every cart in the cart 
	ids list in order to build the list of items he bought.


# PRODUCER

	Each producer has a list of products to be produced, a reference to the marketplace, a republish_wait_time and 
	a producer_id.
	To get the producer id, the function register_producer is called.

	The producer will continuously try to publish the products from the products list in the quantity specified. 
	If the publishing succeeds, he will wait for time given in the list of products, if it fails, he will wait for 
	republish_wait_time and will try again.


# MARKETPLACE

	Each marketplace has a queue_size_per_producer, a dictionary of producers, a disctionary of carts and two locks: 
	one for the producers dictionary and one for the carts.

	To register a producer, a producer_id will be obtained by geting the size of the producers dictionary(the first 
	producer will have the id 0, the second one will have the id 1 and so on). In order to do this, a lock will be used
	to prevent other threads from trying to modify the dictionary at that moment. After getting the producer_id, we 
	will create an entry in the producers dictionary for this id by building an empty list.

	To publish a poduct we will check if the given producer_id is registered. If true, we will check if there is any more
	space in the product list associated with this producer. If true, we will add the product to the product list of 
	this producer.

	In order to create a new cart a cart_id will be obtained by geting the size of the carts dictionary(same as for
	producers). In order to do this, a lock will be used to prevent other threads from trying to modify the dictionary
	at that moment. 
	After getting the cart_id, we will create an entry in the carts dictionary for this id by building an empty list.
	Each element of this list will be a dictionary with the keys "product" and "producer". This way, for each product 
	we will know the producer.

	When adding a product to a cart we first check if the given cart_id is a key in the carts dictionary. If yes, we
	check if the product is found in any of the product lists of the registered producers. If found, a new dictionary
	with the keys "product" and "producers" is created and added to the list of products from the given cart and, 
	also, the product is removed from the product list of the producer. To ensure the proper functioning of the 
	function, we place the adding and removing part in a try except block.

	To remove a product from ac cart we check if the given cart_id is a key in the carts dictionary. If yes, we check
	if any of the dictionaries in this list have the given product in their "product" field. If found, we remove the
	dictionary from the list and we add the product back to its producer's list of products.

	When placing an order, we create a list of all the values found in the "product" fields of the dictionaries from the 
	list associated to the given cart_id.
