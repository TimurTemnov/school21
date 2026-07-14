def make_dict(list_of_tuples):
    dict = {
        list_of_tuples[0][1] : [list_of_tuples[0][0]]
    }
    for tuple in list_of_tuples[1:]:
        if (tuple[1] in dict.keys()):
            dict[tuple[1]].append(tuple[0])
        else:
            dict[tuple[1]] = [ tuple[0] ]

    return dict
        

def to_dictionary():
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
    
    for key in dict:
        for i in range(len(dict[key])):
            print(f"'{key}' : '{dict[key][i]}'")


if __name__ == '__main__':
    to_dictionary()