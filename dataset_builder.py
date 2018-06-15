import numpy as np
from random import shuffle
from faker import Faker

fake = Faker()

'''
If you'd like to use something other than ISBN numbers in your datasets,
faker provides good support for that. I encourage you to read the docs
to learn about the different providers that they have available:
https://faker.readthedocs.io/en/latest/providers.html
'''

NUM_BASKETS = 1000
NUM_UNIQUE_ITEMS = 30

while NUM_BASKETS <= 1000:
    item_dict = {}

    for i in range(1, NUM_UNIQUE_ITEMS + 1):
        item_dict[i] = fake.isbn13(separator="-")

    filename = 'dataset_{0}_baskets_{1}_objects.txt'.format(str(NUM_BASKETS), str(NUM_UNIQUE_ITEMS))

    with open(filename, 'w') as f:
        for i in range(NUM_BASKETS):
            curr_basket = []
            for i in range(1, NUM_UNIQUE_ITEMS):
                if np.random.uniform() < 1/i:
                    curr_basket.append(item_dict[i])
            shuffle(curr_basket)
            f.write(' '.join(curr_basket) + '\n')
    f.close()
    NUM_BASKETS *= 10
