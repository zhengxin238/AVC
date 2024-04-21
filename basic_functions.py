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

l = borda_score_altristic_func(friend_structure_list, df_step1, 0.5)

def get_top_x_candidates(committee_size, borda_score_altristic_df):
    column_sums = borda_score_altristic_df.sum()
    # Sort the DataFrame based on candidate values (ascending order)
    sorted_series = column_sums.sort_values(ascending=False)
    top_candidates = sorted_series.head(committee_size).index.tolist()
    return top_candidates


list_candidates = get_top_x_candidates(4,l)

# ===============================================================================================================
# above is to find a committee elected
# ===============================================================================================================


print(list_candidates)


# ===============================================================================================================
# with a committee elected, in the following part we calculate the nine values of measuring methods
# ===============================================================================================================
def committee_bordascore_df_func(voters, bordascore_df_original, list_candidates):
    committee_bordascore_df = pd.DataFrame(index=bordascore_df_original.index)  # Create empty DataFrame for committee Borda scores

    for voter in voters:
        score_temp = df_step1.loc[voter, list_candidates].sum()  # Calculate Borda score for the committee
        committee_bordascore_df.at[voter, 'Committee Borda Score'] = score_temp  # Assign Borda score to DataFrame

    return committee_bordascore_df

print(committee_bordascore_df_func(voters, df_step1, list_candidates))




# ===============================================================================================================
# below are not yet correct
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================

def avg_fsi_df_func(list_candidates, voters_f4, committee_bordascore_df, friend_structure):
    avg_fsi_df = pd.DataFrame(columns="avg", index=voters_f4)
    for friends in friend_structure:
        temp_score = 0
        for f in friends:
            temp_score += committee_bordascore_df.at[int(f), "Committee Borda Score"]
            avg_fsi_df.at[list_candidates, "Committee Borda Score"] = temp_score / len(friends)
    return avg_fsi_df


# ===============================================================================================================
# below are not yet correct
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================



def min_fsi_df_func(subsets_f5, voters_f5, committee_bordascore_df_f5, friend_structure):
    min_fsi_df = pd.DataFrame(columns=list(range(0, len(subsets_f5))), index=voters_f5)
    for i in range(0, len(subsets_f5)):
        m = 0
        for friends in friend_structure:
            temp = None
            for friend in friends:
                if (temp == None) or (temp >= committee_bordascore_df_f5.at[int(friend), i]):
                    temp = committee_bordascore_df_f5.at[int(friend), i]
            min_fsi_df.at[voters_f5[m], i] = temp
            m += 1
    return min_fsi_df







def max_fsi_df_func(subsets_f6, voters_f6, committee_bordascore_df_f6, friend_structure):
    max_fsi_df = pd.DataFrame(columns=list(range(0, len(subsets_f6))), index=voters_f6)
    for i in range(0, len(subsets_f6)):
        m = 0
        for friends in friend_structure:
            temp = None
            for friend in friends:
                if (temp == None) or (temp <= committee_bordascore_df_f6.at[int(friend), i]):
                    temp = committee_bordascore_df_f6.at[int(friend), i]
            max_fsi_df.at[voters_f6[m], i] = temp
            m += 1
    return max_fsi_df




