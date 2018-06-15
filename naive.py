from collections import defaultdict
import utils
import functools
import itertools

THRESHOLD_PROPORTION = 0.05 # proportion of baskets in which an itemset must appear to be considered "frequent"
TARGET_ITEMSET_SIZE = 3

# read in data
TOY_DATA = 'blog-baskets.txt'
REAL_DATA = 'baskets.txt'

with open(TOY_DATA) as f:
    lines = f.readlines()
f.close()

NUM_LINES = len(lines)
THRESHOLD_COUNT = THRESHOLD_PROPORTION * NUM_LINES

naive_counts = defaultdict(functools.partial(defaultdict, int))

def naive_get_frequent_itemsets(baskets, naive_counts, itemset_size):
    for basket in baskets:
        items = basket.split()
        if len(items) < itemset_size:
            continue
        itemsets = [utils.normalize_to_tuple(*combo) for combo in itertools.combinations(items, itemset_size)]
        for itemset in itemsets:
            naive_counts[itemset_size][itemset] += 1
    
    naive_counts[itemset_size] = { k: v for k, v in naive_counts[itemset_size].items() if v > THRESHOLD_COUNT }
    return naive_counts

# TODO: Implement this yourself - check your work against the naive solution
def apriori_algorithm():
    pass

# run the naive approach
for size in range(1, TARGET_ITEMSET_SIZE + 1):
    naive_get_frequent_itemsets(lines, naive_counts, size)

# print the results from the naive approach
for size in range(1, TARGET_ITEMSET_SIZE + 1):
    print('\n---\n\nFrequent itemsets of size {0}:\n'.format(size))
    for itemset, count in naive_counts[size].items():
        print('{0}: {1}'.format(itemset, count))
