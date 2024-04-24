from pymongo import MongoClient

import integrate_funcs


db = MongoClient('localhost', 27017)['Altruistic_result']

file_path = r"D:\TU Clausthal\Masterarbeit\AltristicVotingCode\into_db\soc_urls_1.txt"


integrate_funcs.readURL_test_data(db, file_path)
