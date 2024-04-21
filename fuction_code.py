from itertools import combinations
import pandas as pd
import xml.etree.ElementTree as ET
import graphCode
import prefLibParse
import networkx as nx

pd.set_option('display.max_columns', None)


def parse_graphml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    G = nx.Graph()

    # Define the XML namespace
    namespace = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

    # Iterate over nodes
    for node in root.findall('.//graphml:node', namespace):
        node_id = node.get('id')
        G.add_node(node_id)

    # Iterate over edges
    for edge in root.findall('.//graphml:edge', namespace):
        source = edge.get('source')
        target = edge.get('target')
        G.add_edge(source, target)

    return G

url = "https://www.preflib.org/static/data/agh/00009-00000002.soc"
g = parse_graphml("D:\TU Clausthal\Masterarbeit\pythonProject001\g_3_05_09_2")

candidates = list(range(1, (prefLibParse.getNumberOfAlternatives(url) + 1)))
voters = list(range(1, (prefLibParse.getNumberOfVoters(url) + 1)))
preference_in_table = prefLibParse.getPreferenceList(url)
friend_structure_list = graphCode.getFriendStructureList(g)
# =====================================================
# the input information

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


# candidates = list(range(1, (
#         prefLibParse.getNumberOfAlternatives(r"https://www.preflib.org/static/data/agh/00009-00000001.soc") + 1)))
# voters = list(
#     range(1, (prefLibParse.getNumberOfVoters(r"https://www.preflib.org/static/data/agh/00009-00000001.soc") + 1)))
# preference_in_table = prefLibParse.getPreferenceList(r"https://www.preflib.org/static/data/agh/00009-00000001.soc")
#
# # =====================================================f1
#
# g = graphCode.getGraph(1, len(voters))
# friend_structure_list = graphCode.getFriendStructureList(g)
#
# # =====================================================f1
#
# scale_free_graph = nx.barabasi_albert_graph(len(voters), 2)
# friend_structure_list_scale_free = graphCode.getFriendStructureList(scale_free_graph)
#
#
# # =====================================================f1

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


# print("bordascore each voter for each candidaate")
#
borda_score_df = borda_score_df_func(candidates, voters, preference_in_table)
print(borda_score_df)


# =====================================================f2

def subsets_candidates(candidates, committee_size):
    subsets = list(combinations(candidates, committee_size))

    return subsets


subsets = subsets_candidates(candidates, committee_size=3)
print(subsets)


# =====================================================f3

# index_names_bs = []
# for v in voters:
#     index_names_bs.append(v)
#
# column_names = list(range(0, len(subsets)))
# index_names = index_names_bs
# committee_bordascore_df = pd.DataFrame(columns=column_names, index=index_names)
# for voter in voters:
#     for i in range(0, len(subsets)):
#         score_temp = 0
#         for can in subsets[i]:
#             score_temp += borda_score_df.at[voter, can]
#         committee_bordascore_df.at[voter, i] = score_temp
#
# print(committee_bordascore_df)


def committee_borda_score_df_func(voters_f3, bordascore_df_f3, subsets_f3):
    index_names_bs = []
    for v in voters_f3:
        index_names_bs.append(v)

    column_names = list(range(0, len(subsets_f3)))
    index_names = index_names_bs

    committee_bordascore_df = pd.DataFrame(columns=column_names, index=index_names)
    for voter in voters_f3:
        for i in range(0, len(subsets_f3)):
            score_temp = 0
            for can in subsets_f3[i]:
                score_temp += bordascore_df_f3.at[voter, can]
            committee_bordascore_df.at[voter, i] = score_temp
    return committee_bordascore_df


c_bs_df = committee_borda_score_df_func(voters, borda_score_df, subsets)
print(c_bs_df)

# print(c_bs_df)


# =====================================================f4

# avg_fsi_df = pd.DataFrame(columns=list(range(0, len(subsets))), index=voters)
#
# for i in range(0, len(subsets)):
#     m = 0
#     for friends in friend_structure_list:
#         temp_score = 0
#         for f in friends:
#             temp_score += c_bs_df.at[f, i]
#             avg_fsi_df.at[voters[m], i] = temp_score / len(friends)
#         m += 1
#
# print(avg_fsi_df)
print(friend_structure_list)

def avg_fsi_df_func(subsets_f4, voters_f4, committee_bordascore_df_f4, friend_structure):
    avg_fsi_df = pd.DataFrame(columns=list(range(0, len(subsets_f4))), index=voters_f4)
    for i in range(0, len(subsets_f4)):
        m = 0
        for friends in friend_structure:

            temp_score = 0
            for f in friends:

                temp_score += committee_bordascore_df_f4.at[int(f), i]
                avg_fsi_df.at[voters_f4[m], i] = temp_score / len(friends)
            m += 1
    return avg_fsi_df


avgdf = avg_fsi_df_func(subsets, voters, c_bs_df, friend_structure_list)


# print(avgdf)


# =====================================================f5

# min_fsi_df = pd.DataFrame(columns=list(range(0, len(subsets))), index=voters)
# for i in range(0, len(subsets)):
#     m = 0
#     for friends in friend_structure_list:
#         temp = None
#         for friend in friends:
#             if (temp == None) or (temp >= c_bs_df.at[friend, i]):
#                 temp = c_bs_df.at[friend, i]
#         min_fsi_df.at[voters[m], i] = temp
#         m += 1
# print(min_fsi_df)


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


mindf = min_fsi_df_func(subsets, voters, c_bs_df, friend_structure_list)


# print(mindf)


# =====================================================f6

#
# max_fsi_df = pd.DataFrame(columns=list(range(0, len(subsets))), index=voters)
# for i in range(0, len(subsets)):
#     m = 0
#     for friends in friend_structure_list:
#         temp = None
#         for friend in friends:
#             if (temp == None) or (temp <= c_bs_df.at[friend, i]):
#                 temp = c_bs_df.at[friend, i]
#         max_fsi_df.at[voters[m], i] = temp
#         m += 1
# print(max_fsi_df)


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


maxdf = max_fsi_df_func(subsets, voters, c_bs_df, friend_structure_list)


# print(maxdf)

# avgavgdf = avgdf.mean()
# avgmindf = avgdf.min()
# avgmaxdf = avgdf.max()
#
# minavgdf = mindf.mean()
# minmindf = mindf.min()
# minmaxdf = mindf.max()
#
# maxavgdf = maxdf.mean()
# maxmindf = maxdf.min()
# maxmaxdf = maxdf.max()
#
# resultdf = pd.DataFrame()
#
# final = None
#
# final = resultdf._append(avgavgdf, ignore_index=True)._append(avgmindf, ignore_index=True)._append(avgmaxdf,
#                                                                                                    ignore_index=True)._append(
#     minavgdf, ignore_index=True)._append(minmindf, ignore_index=True)._append(minmaxdf,
#                                                                               ignore_index=True)._append(maxavgdf,
#                                                                                                          ignore_index=True)._append(
#     maxmindf, ignore_index=True)._append(maxmaxdf,
#                                          ignore_index=True)
#
# print(final)
#
# # final['Max'] = final.apply(max, axis=1)
# max_location = final.idxmax(axis=1)
#
# print(max_location)

def getfinaldf(avgdf, mindf, maxdf):
    avgavgdf = avgdf.mean()
    avgmindf = avgdf.min()
    avgmaxdf = avgdf.max()

    minavgdf = mindf.mean()
    minmindf = mindf.min()
    minmaxdf = mindf.max()

    maxavgdf = maxdf.mean()
    maxmindf = maxdf.min()
    maxmaxdf = maxdf.max()

    resultdf = pd.DataFrame()

    final = resultdf._append(avgavgdf, ignore_index=True)._append(avgmindf, ignore_index=True)._append(avgmaxdf,
                                                                                                       ignore_index=True)._append(
        minavgdf, ignore_index=True)._append(minmindf, ignore_index=True)._append(minmaxdf,
                                                                                  ignore_index=True)._append(maxavgdf,
                                                                                                             ignore_index=True)._append(
        maxmindf, ignore_index=True)._append(maxmaxdf,
                                             ignore_index=True)

    max_location = final.idxmax(axis=1)
    print(final)
    return max_location


print(getfinaldf(avgdf, mindf, maxdf))
print(subsets[6])
