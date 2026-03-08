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

        if not repos:
            scores[skill] = 0
            continue

        total = 0

        for repo in repos:

            # ensure repo has score
            score = repo.get("score", 0)

            total += score

        avg = total / len(repos)

        # normalize score out of 10
        scores[skill] = round(min(avg * 10, 10), 2)

    return scores
