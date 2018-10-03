import intervals as I

def _merge_interval(result_set, op='union'):
    if len(result_set) == 0:
        return result_set

    attrs = [a for a in result_set[0].keys() if a not in ['valid_from', 'valid_to']]

    # Merge intervals
    res_interval_dict = dict()
    for v in result_set:
        k = []
        for a in attrs:
            k.append(v[a])
        k = tuple(k)

        try:
            if op == 'subtract':
                res_interval_dict[k] -= I.closed(v['valid_from'], v['valid_to'])
            elif op == 'intersection':
                res_interval_dict[k] &= I.closed(v['valid_from'], v['valid_to'])
            else: # op == 'union'
                res_interval_dict[k] |= I.closed(v['valid_from'], v['valid_to'])
        except KeyError:
            res_interval_dict[k] = I.closed(v['valid_from'], v['valid_to'])

    # Convert back to list of dict
    res = list()
    for k, v in res_interval_dict.items():
        for i in v:
            item = dict()
            for attr, val in zip(attrs, list(k)):
                item[attr] = val

            item['valid_from'] = i.lower
            item['valid_to'] = i.upper

            res.append(item)

    return res