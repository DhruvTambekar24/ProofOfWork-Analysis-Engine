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

    for skill, evidence in skill_map.items():

        avg_score = sum(evidence) / len(evidence)

        evidence_bonus = min(len(evidence) * 0.5, 2)

        final_score = (avg_score * 10) + evidence_bonus

        scores[skill] = round(final_score, 2)

    return scores