# def compute_skill_authenticity(skill_map):

#     authenticity_scores = {}

#     for skill, scores in skill_map.items():

#         if not scores:
#             authenticity_scores[skill] = 0
#             continue

#         avg_score = sum(scores) / len(scores)

#         authenticity_scores[skill] = round(avg_score * 10, 2)

#     return authenticity_scores
def compute_skill_authenticity(skill_map):

    scores = {}

    for skill, repos in skill_map.items():

        total = 0

        for repo in repos:
            total += repo["score"]   # ✔ correct

        avg = total / len(repos)

        scores[skill] = round(avg * 10, 2)

    return scores
