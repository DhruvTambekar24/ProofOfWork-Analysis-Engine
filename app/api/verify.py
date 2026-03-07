# from fastapi import APIRouter
# from app.services.github_service import fetch_repositories
# from app.services.repo_analyzer import analyze_repository
# from app.services.skill_extractor import extract_skills
# from app.services.authenticity_engine import compute_skill_authenticity

# router = APIRouter()

# @router.post("/verify")

# def verify_student(student: dict):

#     username = student["github_username"]

#     repos = fetch_repositories(username)

#     repo_analysis = []

#     for repo in repos:

#         analysis = analyze_repository(username, repo)

#         repo_analysis.append(analysis)

#     skill_map = extract_skills(repo_analysis)

#     authenticity = compute_skill_authenticity(skill_map)

#     return {
#         "student": student["name"],
#         "skills": authenticity,
#         "repos_analyzed": len(repo_analysis)
#     }
# from fastapi import APIRouter
# from app.services.github_service import fetch_repositories
# from app.services.repo_analyzer import analyze_repository
# from app.services.skill_extractor import extract_skills
# from app.services.authenticity_engine import compute_skill_authenticity
# from app.services.ai_verifier import analyze_skill_authenticity

# router = APIRouter()

# @router.post("/verify")

# def verify_student(student: dict):

#     username = student["github_username"]
#     name = student["name"]

#     repos = fetch_repositories(username)

#     repo_analysis = []

#     for repo in repos:
#         result = analyze_repository(username, repo)
#         repo_analysis.append(result)

#     skill_map = extract_skills(repo_analysis)

#     base_scores = compute_skill_authenticity(skill_map)

#     ai_analysis = analyze_skill_authenticity(
#         name,
#         repo_analysis,
#         skill_map
#     )

#     return {
#         "student": name,
#         "repos_analyzed": len(repo_analysis),
#         "base_scores": base_scores,
#         "ai_verification": ai_analysis
#     }
from fastapi import APIRouter

from app.services.github_service import fetch_repositories
from app.services.repo_analyzer import analyze_repository
from app.services.skill_extractor import extract_skills
from app.services.authenticity_engine import compute_skill_authenticity
from app.services.ai_verifier import analyze_skill_authenticity
from app.services.evidence_graph import build_skill_graph

router = APIRouter()


@router.post("/verify")
def verify_student(student: dict):

    username = student["github_username"]
    name = student["name"]

    repos = fetch_repositories(username)

    repo_analysis = []

    for repo in repos:

        analysis = analyze_repository(username, repo)

        repo_analysis.append(analysis)

    skill_map = extract_skills(repo_analysis)

    base_scores = compute_skill_authenticity(skill_map)

    skill_graph = build_skill_graph(skill_map)

    ai_analysis = analyze_skill_authenticity(
        name,
        repo_analysis,
        skill_map
    )

    return {
        "student": name,
        "repos_analyzed": len(repo_analysis),
        "repositories": repo_analysis,
        "base_scores": base_scores,
        "ai_verification": ai_analysis,
        "skills_detected": list(skill_map.keys())
    }