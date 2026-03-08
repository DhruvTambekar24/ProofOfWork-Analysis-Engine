
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


def normalize_scores(scores: dict):
    """
    Ensure skill scores are always between 0 and 10
    """
    normalized = {}

    for skill, score in scores.items():
        normalized[skill] = round(min(score, 10), 2)

    return normalized


def clean_repo_output(repos):
    """
    Remove heavy fields like README from API output
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


@router.post("/verify")
def verify_student(student: dict):

    try:

        username = student.get("github_username")
        name = student.get("name", username)

        if not username:
            return {"error": "github_username is required"}

        # -----------------------------
        # Fetch GitHub repositories
        # -----------------------------

        repos = fetch_repositories(username)

        if not repos:
            return {
                "student": name,
                "repos_analyzed": 0,
                "base_scores": {},
                "ai_verification": "No repositories found.",
                "skills_detected": []
            }

        # -----------------------------
        # Analyze repos in parallel
        # -----------------------------

        with ThreadPoolExecutor(max_workers=10) as executor:

            results = executor.map(
                lambda repo: analyze_repository(username, repo),
                repos
            )

        repo_analysis = list(results)

        # -----------------------------
        # Extract skills
        # -----------------------------

        skill_map = extract_skills(repo_analysis)

        # -----------------------------
        # Compute authenticity scores
        # -----------------------------

        base_scores = compute_skill_authenticity(skill_map)

        base_scores = normalize_scores(base_scores)

        # -----------------------------
        # Build skill evidence graph
        # -----------------------------

        skill_graph = build_skill_graph(skill_map)

        # -----------------------------
        # AI verification
        # -----------------------------

        ai_result = analyze_skill_authenticity(
            name,
            repo_analysis,
            skill_map
        )

        if isinstance(ai_result, dict):
            ai_text = ai_result.get("analysis", "")
        else:
            ai_text = str(ai_result)

        # -----------------------------
        # Clean repo output
        # -----------------------------

        cleaned_repos = clean_repo_output(repo_analysis)

        return {
            "student": name,
            "repos_analyzed": len(repo_analysis),

            "base_scores": base_scores,

            "ai_verification": ai_text,

            "skills_detected": list(skill_map.keys()),

            # optional repo summary
            "repositories": cleaned_repos
        }

    except Exception as e:

        # Prevent frontend crashes
        return {
            "error": "verification_failed",
            "message": str(e)
        }
