import json

import pandas as pd
import pymongo

from from_db import read_from_db_sone


# list_methods = ["avg_avg", "max_avg", "min_avg", "max_max", "min_min", "max_min", "min_max", "avg_min", "avg_max"]
# cleint_name = "mongodb://localhost:27017/"
# db_name = "Altruistic_result"
# collection_name = '00009-00000001_0.1'

def integrataed_single_entry_dfList(cleint_name, db_name, collection_name):
    df = read_from_db_one.get_stepone_df(cleint_name, db_name, collection_name)

    list_of_chunked_fds = read_from_db_one.chunk_dataframe(df)
    dfs = read_from_db_one.get_resultdf_original(list_of_chunked_fds)

    normorlised_dfs = read_from_db_one.get_normalised_result(dfs)
    return normorlised_dfs


# l = integrataed_single_entry_dfList(cleint_name, db_name, collection_name)
# for i in l:
#     print(i)




def store_dfs_in_mongodb(cleint_name_t,database_name_t, collection_name_t, integrataed_single_entry_dfList):
    """
    Store a list of pandas DataFrames into MongoDB.

    Parameters:
    - uri (str): MongoDB connection URI (e.g., 'mongodb://localhost:27017/')
    - database_name (str): Name of the MongoDB database
    - collection_name (str): Name of the MongoDB collection to store DataFrames
    - list_of_dfs (list): List of pandas DataFrames to store in MongoDB
    """
    # Connect to MongoDB
    mongo_client = pymongo.MongoClient(cleint_name_t)

    # Access the specified database and collection
    db = mongo_client[database_name_t]
    collection = db[collection_name_t]

    try:
        # Store each DataFrame in MongoDB
        for idx, df in enumerate(integrataed_single_entry_dfList):
            # Convert DataFrame to JSON string
            df_json = df.to_json(orient='split')
            # Insert JSON data into MongoDB
            collection.insert_one({'df_id': idx, 'df_data': json.loads(df_json)})

        print("DataFrames stored successfully in MongoDB.")

    except Exception as e:
        print(f"Error occurred while storing DataFrames in MongoDB: {e}")

    finally:
        # Close MongoDB connection
        mongo_client.close()


# store_dfs_in_mongodb("mongodb://localhost:27017/","Dataset_9compares", "test001", l)






def iterate_all_cllections(cleint_name, db_name_from, db_name_to):
# MongoDB connection settings
    mongo_client = pymongo.MongoClient(cleint_name)  # Update MongoDB URI as needed

    # Access the database
    db = mongo_client[db_name_from]

    # List all collections in the database
    collection_names = db.list_collection_names()
    used_names = mongo_client[db_name_to].list_collection_names()
# Convert lists to sets to find unique elements
# Find strings that appear only in one of the sets
    set1 = set(collection_names)
    set2 = set(used_names)

    # Find strings that appear only in one of the sets
    unique_collection_names = list(set1 - set2)

    # Iterate through each collection
    for collection_name in unique_collection_names:

        temp_list = integrataed_single_entry_dfList(cleint_name, db_name_from, collection_name)
        store_dfs_in_mongodb(cleint_name, db_name_to, collection_name, temp_list)

    # Close MongoDB connection
    mongo_client.close()

cleint_name = "mongodb://localhost:27017/"
db_name_from = "Altruistic_result"
db_name_to ="Dataset_9compares"


iterate_all_cllections(cleint_name, db_name_from, db_name_to)