from preflibtools.instances import PrefLibInstance, OrdinalInstance

'''
# instance = PrefLibInstance()
instance = OrdinalInstance()
# instance.parse_file("00001-00000001.soi")
file_path = r"https://www.preflib.org/static/data/agh/00009-00000002.soc"
instance.parse_url(file_path)
# instance.parse_file(file_path)


# Additional members of the class are the orders,  their multiplicity and the number of unique orders
preferenceList = []
tuple_first_level = instance.flatten_strict()
for tuple_second_level in tuple_first_level:
    for i in range (1,(tuple_second_level[1]+1)):
        preferenceList.append(list(tuple_second_level[0]))
print(preferenceList)'''


def getPreferenceList(file_path):
    instance = OrdinalInstance()
    instance.parse_url(file_path)
    preferenceList = []
    tuple_first_level = instance.flatten_strict()
    for tuple_second_level in tuple_first_level:
        for i in range(1, (tuple_second_level[1] + 1)):
            preferenceList.append(list(tuple_second_level[0]))
    # print(111111111111111111111111111)
    return preferenceList





def getNumberOfVoters(file_path):
    instance = OrdinalInstance()
    instance.parse_url(file_path)
    num = instance.num_voters
    return num


def getNumberOfAlternatives(file_path):
    instance = OrdinalInstance()
    instance.parse_url(file_path)
    num = instance.num_alternatives
    return num

