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
    for skill, repo_scores in skill_map.items():
        if not repo_scores:
            scores[skill] = 0
            continue
        avg = sum(repo_scores) / len(repo_scores)  # ✅ already floats
        scores[skill] = round(min(avg * 10, 10), 2)
    return scores
