from app.utils.github_client import get_user_repos, get_repo_commits


def fetch_repositories(username):

    repos = get_user_repos(username)

    repo_list = []

    for repo in repos:

        repo_list.append({
            "name": repo["name"],
            "language": repo.get("language"),
            "owner": repo["owner"]["login"]
        })

    return repo_list


def fetch_commits(owner, repo_name):

    commits = get_repo_commits(owner, repo_name)

    return commits