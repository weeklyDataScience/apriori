def normalize_to_tuple(*args):
    if type(args) == 'string':
        return tuple([args])
    return tuple(sorted(args))

def filter_dict(d, threshold):
    d = { k: v for k, v in d.items() if v > threshold }
    return d