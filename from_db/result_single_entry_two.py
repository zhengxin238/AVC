from from_db import read_from_db_one


# list_methods = ["avg_avg", "max_avg", "min_avg", "max_max", "min_min", "max_min", "min_max", "avg_min", "avg_max"]
cleint_name = "mongodb://localhost:27017/"
db_name = "Altruistic_result"
collection_name = '00009-00000001_0.1'

def integrataed_single_entry_dfList(cleint_name, db_name, collection_name):
    df = read_from_db_one.get_stepone_df(cleint_name, db_name, collection_name)

    list_of_chunked_fds = read_from_db_one.chunk_dataframe(df)
    dfs = read_from_db_one.get_resultdf_original(list_of_chunked_fds)

    normorlised_dfs = read_from_db_one.get_normalised_result(dfs)
    return normorlised_dfs

l = integrataed_single_entry_dfList(cleint_name, db_name, collection_name)
for i in l:
    print(i)