
# from fastapi import APIRouter

# from app.services.github_service import fetch_repositories
# from app.services.repo_analyzer import analyze_repository
# from app.services.skill_extractor import extract_skills
# from app.services.authenticity_engine import compute_skill_authenticity
# from app.services.ai_verifier import analyze_skill_authenticity
# from app.services.evidence_graph import build_skill_graph
# from concurrent.futures import ThreadPoolExecutor

# router = APIRouter()


# @router.post("/verify")
# def verify_student(student: dict):

#     username = student["github_username"]
#     name = student["name"]

#     repos = fetch_repositories(username)

#     # repo_analysis = []

#     # for repo in repos:

#     #     analysis = analyze_repository(username, repo)

#     #     repo_analysis.append(analysis)  
#     repo_analysis = []

#     with ThreadPoolExecutor(max_workers=10) as executor:
#        results = executor.map(
#          lambda repo: analyze_repository(username, repo),
#          repos
#          )

#     repo_analysis = list(results)

#     skill_map = extract_skills(repo_analysis)

#     base_scores = compute_skill_authenticity(skill_map)

#     skill_graph = build_skill_graph(skill_map)

#     ai_analysis = analyze_skill_authenticity(
#         name,
#         repo_analysis,
#         skill_map
#     )

#     return {
#         "student": name,
#         "repos_analyzed": len(repo_analysis),
#         "repositories": repo_analysis,
#         "base_scores": base_scores,
#         "ai_verification": ai_analysis,
#         "skills_detected": list(skill_map.keys())
#     }
from fastapi import APIRouter
from concurrent.futures import ThreadPoolExecutor

from app.services.github_service import fetch_repositories
from app.services.repo_analyzer import analyze_repository
from app.services.skill_extractor import extract_skills
from app.services.authenticity_engine import compute_skill_authenticity
from app.services.ai_verifier import analyze_skill_authenticity
from app.services.evidence_graph import build_skill_graph

router = APIRouter()


def normalize_scores(base_scores: dict):

    normalized = {}

    for skill, score in base_scores.items():

        # ensure score is always between 0 and 10
        normalized[skill] = round(min(score, 10), 2)

    return normalized


def sanitize_repo_output(repos):

    """
    Remove heavy fields from repo output
    to keep API response clean.
    """

    cleaned = []

    for r in repos:

        cleaned.append({
            "repo": r.get("repo"),
            "language": r.get("language"),
            "ownership": round(r.get("ownership", 0), 2),
            "complexity": round(r.get("complexity", 0), 2),
            "structure": r.get("structure"),
            "tutorial_project": r.get("tutorial_project"),
            "plagiarism_risk": r.get("plagiarism_report", {}).get("risk_level", "UNKNOWN")
        })

    return cleaned

@router.post("/detailed-analysis")
def detailed_repo_analysis(student: dict):

    username = student["github_username"]

    repos = fetch_repositories(username)

    with ThreadPoolExecutor(max_workers=10) as executor:

        results = executor.map(
            lambda repo: analyze_repository(username, repo),
            repos
        )

    repo_analysis = list(results)

    return {
        "repositories": repo_analysis
    }
@router.post("/verify")
def verify_student(student: dict):

    username = student["github_username"]
    name = student["name"]

    repos = fetch_repositories(username)

    # ---- PARALLEL REPO ANALYSIS ----
    with ThreadPoolExecutor(max_workers=10) as executor:

        results = executor.map(
            lambda repo: analyze_repository(username, repo),
            repos
        )

    repo_analysis = list(results)

    # ---- SKILL EXTRACTION ----
    skill_map = extract_skills(repo_analysis)

    # ---- BASE AUTHENTICITY SCORES ----
    base_scores = compute_skill_authenticity(skill_map)

    # ---- NORMALIZE SCORES (0-10) ----
    base_scores = normalize_scores(base_scores)

    # ---- SKILL GRAPH (internal) ----
    skill_graph = build_skill_graph(skill_map)

    # ---- AI VERIFICATION ----
    ai_result = analyze_skill_authenticity(
        name,
        repo_analysis,
        skill_map
    )

    # ---- CLEAN AI OUTPUT ----
    ai_analysis = ai_result.get("analysis", "")
    ai_scores = ai_result.get("skills", {})

    # ---- CLEAN REPO OUTPUT ----
    cleaned_repos = sanitize_repo_output(repo_analysis)

    return {
        "student": name,
        "repos_analyzed": len(repo_analysis),

        "base_scores": base_scores,

        "ai_scores": ai_scores,

        "analysis": ai_analysis,

        "skills_detected": list(skill_map.keys()),

        # show minimal repo info only
        "repositories": cleaned_repos
    }
