import pandas as pd
import pymongo
from itertools import combinations
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Auto-detect width


list_methods = ["avg_avg", "max_avg", "min_avg", "max_max", "min_min", "max_min", "min_max", "avg_min", "avg_max"]
cleint_name = "mongodb://localhost:27017/"
db_name = "Altruistic_result"
collection_name = '00009-00000001_0.1'


def get_similarity_inPercent(cleint_name, db_name, collection_name):


    df = pd.DataFrame(columns = ["avg_avg", "max_avg", "min_avg", "max_max", "min_min", "max_min", "min_max", "avg_min", "avg_max"])

    # Establish a connection to MongoDB
    client = pymongo.MongoClient(cleint_name)

    # Select the database
    db = client[db_name]

    # Select the collection
    collection = db[collection_name]

    # Find all documents in the collection
    cursor = collection.find({})

    # Create a list to store the documents
    documents_list = []

    # Iterate over the cursor to access each document
    for document in cursor:
        # Remove the '_id' field from the document
        document.pop('_id', None)
        documents_list.append(document)

    for committee_size in documents_list:
        for key_1, value_1 in committee_size.items():
            for key_2, value_2 in value_1.items():
                list_of_best_values =[]
                for key_3, value_3 in value_2.items():
                    # print(key_3)
                    # print(value_3)
                    items = list(value_3.items())
                    list_of_best_values.append(items[1][1])
                    # best_value = items[1][0]
    #                 list_best_value.append(best_value)
                df.loc[len(df)] = list_of_best_values
    #
    print(df)
    return df
df =get_similarity_inPercent(cleint_name, db_name, collection_name)
print(len(df))

def chunk_dataframe(df):
    # Calculate the integer chunk size
    chunk_size = 10
    num_chunks = len(df)//chunk_size

    chunked_dfs = []  # List to store chunked DataFrames

    for i in range(num_chunks):
        # Calculate start and end index for the chunk
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size

        # Handle the last chunk to include any remaining rows
        if i == num_chunks - 1:
            end_idx = len(df)  # Set end index to the last row index

        # Slice the DataFrame to get the chunk
        chunk = df.iloc[start_idx:end_idx]
        chunked_dfs.append(chunk)  # Append the chunk to the list of chunked DataFrames

    return chunked_dfs

list_of_chunked_fds=chunk_dataframe(df)
for i in list_of_chunked_fds:
    print(i)