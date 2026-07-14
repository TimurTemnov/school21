def make_dict(list_of_tuples):
    dict= {
        list_of_tuples[0][0] : list_of_tuples[0][1]
    }
    for tuple in list_of_tuples[1:]:
        dict[tuple[0]] = tuple[1]
    return dict
    
def print_sort_dict(dict):
    sorted_keys = []

    for _ in range(len(dict.keys())):
        max_value = -1
        max_country = ""
        for key in dict.keys():
            if (int(dict[key]) > max_value) and not(key in sorted_keys):
                max_country = key
                max_value = int(dict[key])
        sorted_keys.append(max_country)
    
    for i in range(len(sorted_keys)):
        for j in range(i+1, len(sorted_keys)):
            if (dict[sorted_keys[i]] == dict[sorted_keys[j]]) and (sorted_keys[i] > sorted_keys[j]):
                sorted_keys[i], sorted_keys[j] = sorted_keys[j], sorted_keys[i]
            
    return sorted_keys
            
            



def dict_sorter():
    list_of_tuples = [
    ('Russia', '25'),
    ('France', '132'),
    ('Germany', '132'),
    ('Spain', '178'),
    ('Italy', '162'),
    ('Portugal', '17'),
    ('Finland', '3'),
    ('Hungary', '2'),
    ('The Netherlands', '28'),
    ('The USA', '610'),
    ('The United Kingdom', '95'),
    ('China', '83'),
    ('Iran', '76'),
    ('Turkey', '65'),
    ('Belgium', '34'),
    ('Canada', '28'),
    ('Switzerland', '26'),
    ('Brazil', '25'),
    ('Austria', '14'),
    ('Israel', '12')
    ]
    dict = make_dict(list_of_tuples)
    
    sorted_keys = print_sort_dict(dict)
    for i in range(len(sorted_keys)):
        print(sorted_keys[i])

if __name__ == '__main__':
    dict_sorter()