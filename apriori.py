from collections import defaultdict
import operator

THRESHOLD = 1000

item_counts = defaultdict(int)
pair_counts = defaultdict(int)
triple_counts = defaultdict(int)

# read in the data
with open('./dataset_100000_baskets_5000_objects.txt') as f:
    lines = f.readlines()
f.close()

def normalize_group(*args):
    return str(sorted(args))

def generate_pairs(*args):
    pairs = []
    for idx_1 in range(len(args) - 1):
        for idx_2 in range(idx_1 + 1, len(args)):
            pairs.append(normalize_group(args[idx_1], args[idx_2]))
    return pairs

# FIRST PASS -----------------------------------------

# first pass - find candidate items
for line in lines:
    for item in line.split():
        item_counts[item] += 1

# first pass - find frequent items
frequent_items = set()
for key in item_counts:
    if item_counts[key] > THRESHOLD:
        frequent_items.add(key)

print('There are {0} unique items, {1} of which are frequent'.format(len(item_counts), len(frequent_items)))

# SECOND PASS -----------------------------------------

# second pass - find candidate pairs
# when building candidate pairs, only consider frequent items
for line in lines:
    items = line.split()
    for idx_1 in range(len(items) - 1):
        if items[idx_1] not in frequent_items:
            continue
        for idx_2 in range(idx_1 + 1, len(items)):
            if items[idx_2] not in frequent_items:
                continue
            pair = normalize_group(items[idx_1], items[idx_2]) # this way [a, b] is the same as [b, a]
            pair_counts[pair] += 1

# second pass - find frequent pairs
frequent_pairs = set()
for key in pair_counts:
    if pair_counts[key] > THRESHOLD:
        frequent_pairs.add(key)

print('There are {0} candidate pairs, {1} of which are frequent'.format(len(pair_counts), len(frequent_pairs)))

# THIRD PASS -----------------------------------------

# third pass - find candidate triples
# when building candidate triples, only consider frequent items and pairs
for line in lines:
    items = line.split()
    for idx_1 in range(len(items) - 2):
        if items[idx_1] not in frequent_items: # first item must be frequent
            continue
        for idx_2 in range(idx_1 + 1, len(items) - 1):
            first_pair = normalize_group(items[idx_1], items[idx_2])
            if items[idx_2] not in frequent_items or first_pair not in frequent_pairs: # second item AND first pair must be frequent
                continue
            for idx_3 in range(idx_2 + 1, len(items)):
                if items[idx_3] not in frequent_items:
                    continue
                # now check that all pairs are frequent, since this is a precondition to being a frequent triple
                pairs = generate_pairs(items[idx_1], items[idx_2], items[idx_3])
                if any(pair not in frequent_pairs for pair in pairs):
                    continue
                triple = normalize_group(items[idx_1], items[idx_2], items[idx_3])
                triple_counts[triple] += 1

# third pass - find frequent triples
# frequent_triples = set()
# for key in triple_counts:
#     if triple_counts[key] > THRESHOLD:
#         frequent_triples.add(key)

num_candidate_triples = len(triple_counts) # before filtering
triple_counts = { k: v for k, v in triple_counts.items() if v > THRESHOLD } # filter for frequent triples
print('There are {0} candidate triples, {1} of which are frequent'.format(num_candidate_triples, len(triple_counts)))

# VIEW OUR RESULTS -------------------------------------
print('--------------')
sorted_triples = sorted(triple_counts.items(), key=operator.itemgetter(1))

for entry in sorted_triples:
    print('{0}: {1}'.format(entry[0], entry[1]))
