from app.utils.github_client import get_repo_contents


def analyze_structure(owner, repo):

    try:
        contents = get_repo_contents(owner, repo)
    except:
        return 0

    structure_score = 0

    file_names = [item["name"].lower() for item in contents]

    if "tests" in file_names:
        structure_score += 2

    if "src" in file_names:
        structure_score += 2

    if "dockerfile" in file_names:
        structure_score += 1

    if "requirements.txt" in file_names or "package.json" in file_names:
        structure_score += 1

    return structure_score