import uuid
import random
import pandas as pd
import networkx as nx
import numpy as np
from pymongo import MongoClient
import basic_functions
import graphCode
import prefLibParse

# pd.set_option('display.max_columns', None)
#
# # =====================================================
# # the input information
#
# candidates = ['candidate_a', 'candidate_b', 'candidate_c', 'candidate_d', 'candidate_e', 'candidate_f']
# voters = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']
#
# preferences_v1 = [candidates[0], candidates[1], candidates[2], candidates[3], candidates[4], candidates[5]]
# preferences_v2 = [candidates[1], candidates[3], candidates[4], candidates[2], candidates[5], candidates[0]]
# preferences_v3 = [candidates[5], candidates[4], candidates[1], candidates[0], candidates[3], candidates[2]]
# preferences_v4 = [candidates[3], candidates[2], candidates[0], candidates[5], candidates[1], candidates[4]]
# preferences_v5 = [candidates[2], candidates[0], candidates[5], candidates[4], candidates[3], candidates[1]]
# preferences_v6 = [candidates[4], candidates[5], candidates[3], candidates[1], candidates[0], candidates[2]]
#
# preference_in_table = [preferences_v1, preferences_v2, preferences_v3, preferences_v4, preferences_v5, preferences_v6]
#
# friends_v1 = [voters[1], voters[4], voters[5]]
# friends_v2 = [voters[0], voters[4], voters[5]]
# friends_v3 = [voters[3], voters[4]]
# friends_v4 = [voters[2]]
# friends_v5 = [voters[0], voters[1], voters[2]]
# friends_v6 = [voters[0], voters[1]]
#
# friend_structure_list = [friends_v1, friends_v2, friends_v3, friends_v4, friends_v5, friends_v6]
#
# p = 0.5
# committee_size = 4
# n_list = ["avg_avg", "max_avg", "min_avg", "max_max", "min_min", "max_min", "min_max", "avg_min", "avg_max"]

# # =====================================================f1


# # =====================================================f1
# # =====================================================f1
# candidates = list(range(1, (
#         prefLibParse.getNumberOfAlternatives(r"https://www.preflib.org/static/data/agh/00009-00000001.soc") + 1)))
# voters = list(
#     range(1, (prefLibParse.getNumberOfVoters(r"https://www.preflib.org/static/data/agh/00009-00000001.soc") + 1)))
# preference_in_table = prefLibParse.getPreferenceList(r"https://www.preflib.org/static/data/agh/00009-00000001.soc")
#
# # =====================================================f1
# url = r"https://www.preflib.org/static/data/agh/00009-00000001.soc"
# p_graph = 0.5
# g = graphCode.getGraph(1, len(voters))
# friend_structure_list = graphCode.getFriendStructureList(g)
# collection = MongoClient('localhost', 27017)['Altruistic_result'][f'9999-00000001_{p_graph}']


# l = borda_score_altristic_func(friend_structure_list, df_step1, p)
# l = basic_functions.borda_score_altristic_func(friend_structure_list, basic_functions.borda_score_df_func(candidates, voters, preference_in_table), p)  ---candidates, voters, preference_in_table, p

# list_candidates = basic_functions.get_top_x_candidates(committee_size, l) ---committee_size
# coeff = basic_functions.getCoefficientMatrix(l)
# coeff = basic_functions.getCoefficientMatrix(basic_functions.borda_score_altristic_func(friend_structure_list, basic_functions.borda_score_df_func(candidates, voters, preference_in_table), p))
# optimal_solution_dict =  basic_functions.altristic_model_run_optimization(candidates,coeff,committee_size)




# list_candidates = basic_functions.from_dict_to_list (optimal_solution_dict)
# list_candidates = basic_functions.from_dict_to_list(basic_functions.altristic_model_run_optimization(candidates,
#                                                                                                      basic_functions.getCoefficientMatrix(
#                                                                                                          basic_functions.borda_score_altristic_func(
#                                                                                                              friend_structure_list,
#                                                                                                              basic_functions.borda_score_df_func(
#                                                                                                                  candidates,
#                                                                                                                  voters,
#                                                                                                                  preference_in_table),
#                                                                                                              p)),
#                                                                                                      committee_size)
#                                                     )


# cbd = basic_functions.committee_bordascore_df_func(voters, basic_functions.borda_score_df_func(candidates, voters, preference_in_table), list_candidates)

# cbd = basic_functions.committee_bordascore_df_func(voters, basic_functions.borda_score_df_func(candidates, voters, preference_in_table), basic_functions.from_dict_to_list(basic_functions.altristic_model_run_optimization(candidates,
#                                                                                                      basic_functions.getCoefficientMatrix(
#                                                                                                          basic_functions.borda_score_altristic_func(
#                                                                                                              friend_structure_list,
#                                                                                                              basic_functions.borda_score_df_func(
#                                                                                                                  candidates,
#                                                                                                                  voters,
#                                                                                                                  preference_in_table),
#                                                                                                              p)),
#                                                                                                      committee_size)))
#
# print(1111111111111111111111111111111)
# print(cbd)
# print(1111111111111111111111111111111)
# avgdf = basic_functions.avg_fsi_df_func(voters, cbd, friend_structure_list)
# mindf = basic_functions.min_fsi_df_func(voters, cbd, friend_structure_list)
# maxdf = basic_functions.max_fsi_df_func(voters, cbd, friend_structure_list)


# finaldf = getfinaldf(n_list,avgdf, mindf, maxdf)


#
# optimal_solution_dict = basic_functions.altristic_model_run_optimization(candidates,
#                                                                          basic_functions.getCoefficientMatrix(
#                                                                              basic_functions.borda_score_altristic_func(
#                                                                                  friend_structure_list,
#                                                                                  basic_functions.borda_score_df_func(
#                                                                                      candidates, voters,
#                                                                                      preference_in_table), p)),
#                                                                          committee_size)
def get_finaldf_integrated(candidates, voters, preference_in_table,
                           n_list, friend_structure_list, dict_committee):
    list_candidates = basic_functions.from_dict_to_list(candidates,dict_committee)

    cbd = basic_functions.committee_bordascore_df_func(voters, basic_functions.borda_score_df_func(candidates, voters,
                                                                                                   preference_in_table),
                                                       list_candidates)
    avgdf = basic_functions.avg_fsi_df_func(voters, cbd, friend_structure_list)
    mindf = basic_functions.min_fsi_df_func(voters, cbd, friend_structure_list)
    maxdf = basic_functions.max_fsi_df_func(voters, cbd, friend_structure_list)

    finaldf = basic_functions.getfinaldf(n_list, avgdf, mindf, maxdf)
    return finaldf


# print(2222222222222222222222222222222222)
# print(get_finaldf_integrated(candidates, voters, preference_in_table,
#                              n_list, friend_structure_list, optimal_solution_dict))
# print(2222222222222222222222222222222222)


# dictcandidates = basic_functions.get_committee_dict(list_candidates, candidates)
def get_one_entry_dict(candidates, voters, preference_in_table,n_list,friend_structure_list,p, committee_size):

    dictcandidates = basic_functions.altristic_model_run_optimization(candidates,
                                                                         basic_functions.getCoefficientMatrix(
                                                                             basic_functions.borda_score_altristic_func(
                                                                                 friend_structure_list,
                                                                                 basic_functions.borda_score_df_func(
                                                                                     candidates, voters,
                                                                                     preference_in_table), p)),
                                                                         committee_size)

    finaldf = get_finaldf_integrated(candidates, voters, preference_in_table,n_list, friend_structure_list, dictcandidates)

    dict = basic_functions.get_result_dict(dictcandidates, n_list, finaldf)

    return dict

# vv=get_one_entry_dict(candidates, voters, preference_in_table,n_list,friend_structure_list,p, committee_size)
# print(vv)
# #
# print(get_one_entry_dict(candidates, voters, preference_in_table, friend_structure_list, p, committee_size,
#                        n_list))


def getResultIntoDB_allMethods_graphnnormal_diff_committeesize_p(p_list, committee_size_list, candidates, voters,
                                                                 preference_in_table, collection_db, dsvalue, p_graph,
                                                                 n_list=["avg_avg", "max_avg", "min_avg", "max_max",
                                                                         "min_min", "max_min", "min_max", "avg_min",
                                                                         "avg_max"]):
    g = graphCode.getGraph(p_graph, len(voters))
    output_file = f"random_graph_{p_graph}_{dsvalue}_{uuid.uuid4()}"
    for committee_size in committee_size_list:
        committee_size_dict = {}
        result_list_dict_temp = {}

        for p in p_list:
            friend_structure_list = graphCode.getFriendStructureList(g)
            nx.write_graphml(g, output_file)
            result_dict = get_one_entry_dict(candidates, voters, preference_in_table,n_list,friend_structure_list,p, committee_size)
            # print(9999999999999999999999999999999999999999999999999999999999999999999999999)
            result_list_dict_temp[str((p))] = result_dict

        committee_size_dict[str(committee_size)] = result_list_dict_temp
        collection_db.insert_one(committee_size_dict)


# #
# getResultIntoDB_allMethods_graphnnormal_diff_committeesize_p(np.arange(0.8, 1.1, 0.1).tolist(),
#                                                              np.arange(6, len(list(range(1, (
#                                                                      prefLibParse.getNumberOfAlternatives(
#                                                                          url) + 1)))), 1).tolist(),
#                                                              list(range(1, (
#                                                                      prefLibParse.getNumberOfAlternatives(
#                                                                          url) + 1))), list(
#         range(1, (prefLibParse.getNumberOfVoters(url) + 1))),
#                                                              prefLibParse.getPreferenceList(url), collection, 876,
#                                                              p_graph)


# def runTestAll(url, collection_db, dsvalue, p_graph):
#     getResultIntoDB_allMethods_graphnnormal_diff_committeesize_p(np.arange(0.8, 1.1, 0.1).tolist(),
#                                                                  np.arange(6, len(list(range(1, (
#                                                                          prefLibParse.getNumberOfAlternatives(
#                                                                              url) + 1)))), 1).tolist(),
#                                                                  list(range(1, (
#                                                                          prefLibParse.getNumberOfAlternatives(
#                                                                              url) + 1))), list(
#             range(1, (prefLibParse.getNumberOfVoters(url) + 1))),
#                                                                  prefLibParse.getPreferenceList(url), collection_db,
#                                                                  dsvalue,
#                                                                  p_graph,
#                                                                  n_list=["avg_avg", "max_avg", "min_avg", "max_max",
#                                                                          "min_min", "max_min", "min_max", "avg_min",
#                                                                          "avg_max"])
#
#     return None


def readURL_test_data(database_location, file_path_with_URL):
    with (open(file_path_with_URL, 'r') as file):
        # Iterate through each line in the file
        for line in file:
            # Remove leading and trailing whitespace from the line
            line = line.strip()
            parts = line.split('/')
            # Get the last part of the URL (the filename)
            filename = parts[-1]
            # Remove the '.soc' extension
            filename_without_extension = filename.split('.')[0]
            # Extract the desired substring
            substring = filename_without_extension
            """filename_without_extension.split('-')[1]"""
            p_graph = random.random() * 0.8 + 0.1
            p_graph = round(p_graph, 2)
            getResultIntoDB_allMethods_graphnnormal_diff_committeesize_p(np.arange(0.1, 1.1, 0.1).tolist(),
                                                                         np.arange(1, len(list(range(1, (
                                                                                 prefLibParse.getNumberOfAlternatives(
                                                                                     line) + 1)))), 1).tolist(),
                                                                         list(range(1, (
                                                                                 prefLibParse.getNumberOfAlternatives(
                                                                                     line) + 1))), list(
                    range(1, (prefLibParse.getNumberOfVoters(line) + 1))),
                                                                         prefLibParse.getPreferenceList(line),
                                                                         database_location[
                                                                             substring + "_" + str(p_graph)], substring,
                                                                         p_graph)
