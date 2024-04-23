import pandas as pd

# pd.set_option('display.max_columns', None)

# # =====================================================
# # the input information
#
candidates = ['candidate_a', 'candidate_b', 'candidate_c', 'candidate_d', 'candidate_e', 'candidate_f']
voters = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']

preferences_v1 = [candidates[0], candidates[1], candidates[2], candidates[3], candidates[4], candidates[5]]
preferences_v2 = [candidates[1], candidates[3], candidates[4], candidates[2], candidates[5], candidates[0]]
preferences_v3 = [candidates[5], candidates[4], candidates[1], candidates[0], candidates[3], candidates[2]]
preferences_v4 = [candidates[3], candidates[2], candidates[0], candidates[5], candidates[1], candidates[4]]
preferences_v5 = [candidates[2], candidates[0], candidates[5], candidates[4], candidates[3], candidates[1]]
preferences_v6 = [candidates[4], candidates[5], candidates[3], candidates[1], candidates[0], candidates[2]]

preference_in_table = [preferences_v1, preferences_v2, preferences_v3, preferences_v4, preferences_v5, preferences_v6]

friends_v1 = [voters[1], voters[4], voters[5]]
friends_v2 = [voters[0], voters[4], voters[5]]
friends_v3 = [voters[3], voters[4]]
friends_v4 = [voters[2]]
friends_v5 = [voters[0], voters[1], voters[2]]
friends_v6 = [voters[0], voters[1]]

friend_structure_list = [friends_v1, friends_v2, friends_v3, friends_v4, friends_v5, friends_v6]


# =====================================================f1

def borda_score_df_func(candidates, voters, preference):
    column_names = []
    index_names = []
    for c in candidates:
        column_names.append(c)
    for v in voters:
        index_names.append(v)

    borda_score_df = pd.DataFrame(columns=column_names, index=index_names)
    for candidate in candidates:
        n = 0
        for voter in voters:
            borda_score_df.at[voter, candidate] = len(candidates) - 1 - preference[n].index(candidate)
            n += 1
    return borda_score_df


df_step1 = borda_score_df_func(candidates, voters, preference_in_table)


# print(df_step1)
# for index, voter in enumerate(voters):
#     new_row_values = df_step1.iloc[index] * 0.5
#     print(new_row_values)

def borda_score_altristic_func(friend_structure_list, borda_score_df, p):
    altruistic_df = pd.DataFrame()
    n = 0
    for index in range(len(borda_score_df)):
        new_row_values = df_step1.iloc[index] * 0.5

        for index2, fv in enumerate(friend_structure_list[n]):
            new_row_values += (borda_score_df.iloc[index2] * (1 - p)) / len(friend_structure_list[n])

        altruistic_df = altruistic_df._append(new_row_values, ignore_index=False)
        n += 1
    return altruistic_df

p=0.5
l = borda_score_altristic_func(friend_structure_list, df_step1, p)


def get_top_x_candidates(committee_size, borda_score_altristic_df):
    column_sums = borda_score_altristic_df.sum()
    # Sort the DataFrame based on candidate values (ascending order)
    sorted_series = column_sums.sort_values(ascending=False)
    top_candidates = sorted_series.head(committee_size).index.tolist()
    return top_candidates


list_candidates = get_top_x_candidates(4, l)

# ===============================================================================================================
# above is to find a committee elected
# ===============================================================================================================


print(list_candidates)


# ===============================================================================================================
# with a committee elected, in the following part we calculate the nine values of measuring methods, the first step is to calculate the barda score each voter give to this winning committee
# ===============================================================================================================
def committee_bordascore_df_func(voters, bordascore_df_original, list_candidates):
    committee_bordascore_df = pd.DataFrame(
        index=bordascore_df_original.index)  # Create empty DataFrame for committee Borda scores

    for voter in voters:
        score_temp = df_step1.loc[voter, list_candidates].sum()  # Calculate Borda score for the committee
        committee_bordascore_df.at[voter, 'Committee Borda Score'] = score_temp  # Assign Borda score to DataFrame

    return committee_bordascore_df


cbd = committee_bordascore_df_func(voters, df_step1, list_candidates)
print(cbd)


# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# above is the fwith the barda score df each voter give to this winning committee we calculte with the following 3 function the avg, min, max as the prepare for finding the nine values e.g. avg-avg, avg-min...
# ===============================================================================================================
def avg_fsi_df_func(voters_f4, committee_bordascore_df, friend_structure):
    avg_fsi_df = pd.DataFrame(columns=["avg"], index=voters_f4)
    for index, friends in enumerate(friend_structure):
        temp_score = 0
        for f in friends:
            temp_score += committee_bordascore_df.at[f, "Committee Borda Score"]
        avg_fsi_df.at[voters_f4[index], "avg"] = temp_score / len(friends)
    return avg_fsi_df


avgdf = avg_fsi_df_func(voters, cbd, friend_structure_list)

print(avgdf)

def min_fsi_df_func(voters_f5, committee_bordascore_df, friend_structure):
    min_fsi_df = pd.DataFrame(columns=["min"], index=voters_f5)
    for index, friends in enumerate(friend_structure):
        temp_score = 0
        for f in friends:
            if (temp_score == 0) or (committee_bordascore_df.at[f, "Committee Borda Score"] <= temp_score):
               temp_score = committee_bordascore_df.at[f, "Committee Borda Score"]
            min_fsi_df.at[voters_f5[index], "min"] = temp_score
    return min_fsi_df


mindf = min_fsi_df_func(voters, cbd, friend_structure_list)
print(mindf)


def max_fsi_df_func(voters_f6, committee_bordascore_df, friend_structure):
    max_fsi_df = pd.DataFrame(columns=["max"], index=voters_f6)
    for index, friends in enumerate(friend_structure):
        temp_score = 0
        for f in friends:
            if (temp_score == 0) or (committee_bordascore_df.at[f, "Committee Borda Score"] >= temp_score):
                temp_score = committee_bordascore_df.at[f, "Committee Borda Score"]
            max_fsi_df.at[voters_f6[index], "max"] = temp_score
    return max_fsi_df

maxdf = max_fsi_df_func(voters, cbd, friend_structure_list)
print(maxdf)









def getfinaldf(indexname,avgdf, mindf, maxdf):

    avgavgdf = avgdf.mean()
    minavgdf = avgdf.min()
    maxavgdf = avgdf.max()

    avgmindf = mindf.mean()
    minmindf = mindf.min()
    maxmindf = mindf.max()

    avgmaxdf = maxdf.mean()
    minmaxdf = maxdf.min()
    maxmaxdf = maxdf.max()

    resultdf = pd.DataFrame(columns=["result"])

    resultdf ["result"] = resultdf["result"]._append(avgavgdf, ignore_index=True)._append(maxavgdf, ignore_index=True)._append(minavgdf,
                                                                                                       ignore_index=True)._append(
        maxmaxdf, ignore_index=True)._append(minmindf, ignore_index=True)._append(maxmindf,
                                                                                  ignore_index=True)._append(minmaxdf,
                                                                                                             ignore_index=True)._append(
        avgmindf, ignore_index=True)._append(avgmaxdf,
                                             ignore_index=True)

    resultdf.index = indexname

    return resultdf


n_list = ["avg_avg", "max_avg", "min_avg", "max_max", "min_min","max_min","min_max","avg_min","avg_max"]

finaldf = getfinaldf(n_list,avgdf, mindf, maxdf)

print(finaldf)




def get_committee_dict(final_committee,candidates):
    indexed_strings = [f"x[{i}]" for i in range(len(candidates))]
    index_list = []
    for i in final_committee:
        index_of_element = candidates.index(i)
        index_list.append(index_of_element)
    index_list = sorted(index_list)
    result_dict = {key: 1 if key in [f"x[{idx}]" for idx in index_list] else 0 for key in indexed_strings}
    return result_dict


dictcandidates = get_committee_dict(list_candidates,candidates)
print(dictcandidates)




# ===============================================================================================================
# below are not yet correct
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================



# optimal_solution_dict = {}
# optimal_solution_dict["final_committee"] = dictcandidates
# optimal_solution_dict["optimized_value"] = finaldf.iloc["avg_avg","result"]
#
# result_list_dict_temp = {}
# result_list_dict_temp[str((p))] = {}
def get_result_dict(dictcandidates,n_list,finaldf):
    result_list_dict_temp = {}
    number_method = 0
    for name_method in n_list:
        optimal_solution_dict = {}
        optimal_solution_dict["final_committee"] = dictcandidates
        optimal_solution_dict["optimized_value"] = finaldf.iloc[number_method,0]
        result_list_dict_temp[str(p)]= {}
        result_list_dict_temp[str(p)][name_method] = {}
        result_list_dict_temp[str(p)][name_method] = optimal_solution_dict
        number_method+=1


print(get_result_dict(dictcandidates,n_list,finaldf))
# max_optimal_solution = optimal_solutions[max_optimal_index]
# max_optimal_solution_formatted = {f'x[{k}]': v for k, v in max_optimal_solution.items()}
# # max_optimal_objective = corresponding_objectives[max_optimal_index]
# optimal_solution_dict["final_committee"] = max_optimal_solution_formatted
# optimal_solution_dict["optimized_value"] = max(optimal_values)

# result_list_dict_temp[str((p))] = {}
#             result_list_dict_temp[str((p))]["avg_avg"] = result_dict_avg_avg
#             result_list_dict_temp[str((p))]["max_avg"] = result_dict_max_avg
#             result_list_dict_temp[str((p))]["min_avg"] = result_dict_min_avg
#             result_list_dict_temp[str((p))]["max_max"] = result_dict_max_max
#             result_list_dict_temp[str((p))]["min_min"] = result_dict_min_min
#             result_list_dict_temp[str((p))]["max_min"] = result_dict_max_min
#             result_list_dict_temp[str((p))]["min_max"] = result_dict_min_max
#             result_list_dict_temp[str((p))]["avg_min"] = result_dict_avg_min
#             result_list_dict_temp[str((p))]["avg_max"] = result_dict_avg_max