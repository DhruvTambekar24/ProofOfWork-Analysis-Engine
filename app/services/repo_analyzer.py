# from app.services.github_service import fetch_commits
# from app.utils.commit_analyzer import calculate_commit_ownership
# from app.services.structure_analyzer import analyze_structure


# def analyze_repository(username, repo):

#     commits = fetch_commits(repo["owner"], repo["name"])

#     ownership = calculate_commit_ownership(commits, username)

#     commit_count = len(commits)

#     complexity_score = min(commit_count / 50, 1)

#     structure_score = analyze_structure(repo["owner"], repo["name"])

#     repo_score = (
#         0.4 * ownership +
#         0.3 * complexity_score +
#         0.3 * structure_score
#     )

#     return {
#         "repo": repo["name"],
#         "language": repo["language"],
#         "ownership": ownership,
#         "complexity": complexity_score,
#         "structure": structure_score,
#         "score": repo_score
#     }
import requests

from app.services.github_service import fetch_commits
from app.utils.commit_analyzer import calculate_commit_ownership
from app.services.structure_analyzer import analyze_structure
from app.services.fraud_detector import detect_tutorial_repo
from app.services.plagiarism_detector import extract_code, ai_code_similarity


def get_readme(owner, repo):

    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"

    try:
        res = requests.get(url)

        if res.status_code == 200:
            return res.text[:2000]

        return ""

    except Exception:
        return ""


def analyze_repository(username, repo):

    owner = repo["owner"]
    repo_name = repo["name"]

    # --------------------------
    # Fetch commits
    # --------------------------

    commits = fetch_commits(owner, repo_name)

    # --------------------------
    # Commit ownership
    # --------------------------

    ownership = calculate_commit_ownership(commits, username)

    # --------------------------
    # Complexity estimation
    # --------------------------

    commit_count = len(commits)
    complexity_score = min(commit_count / 50, 1)

    # --------------------------
    # Project structure depth
    # --------------------------

    structure_score = analyze_structure(owner, repo_name)

    # --------------------------
    # Tutorial detection
    # --------------------------

    tutorial_flag = detect_tutorial_repo(repo_name)

    # --------------------------
    # README extraction
    # --------------------------

    readme = get_readme(owner, repo_name)

    # --------------------------
    # Code plagiarism detection
    # --------------------------

    code_samples = extract_code(owner, repo_name)

    plagiarism_report = {"risk_level": "UNKNOWN"}

    if code_samples:
        try:
            plagiarism_report = ai_code_similarity(
                repo_name,
                code_samples[:3]
            )
        except Exception:
            plagiarism_report = {"risk_level": "UNKNOWN"}

    # --------------------------
    # Repository authenticity score
    # --------------------------

    repo_score = (
        0.4 * ownership +
        0.3 * complexity_score +
        0.3 * structure_score
    )

    return {
        "repo": repo_name,
        "language": repo.get("language"),
        "ownership": ownership,
        "complexity": complexity_score,
        "structure": structure_score,
        "tutorial_project": tutorial_flag,
        "readme": readme,
        "plagiarism_report": plagiarism_report,
        "score": repo_score
    }
