# import requests
# from app.config.settings import GITHUB_API, GITHUB_TOKEN

# headers = {
#     "Authorization": f"token {GITHUB_TOKEN}"
# } if GITHUB_TOKEN else {}

# def get_user_repos(username):
#     url = f"{GITHUB_API}/users/{username}/repos"
#     res = requests.get(url, headers=headers)
#     return res.json()

# def get_repo_commits(owner, repo):
#     url = f"{GITHUB_API}/repos/{owner}/{repo}/commits"
#     res = requests.get(url, headers=headers)
#     return res.json()

# def get_repo_contents(owner, repo):
#     url = f"{GITHUB_API}/repos/{owner}/{repo}/contents"
#     res = requests.get(url, headers=headers)
#     return res.json()
import requests
from app.config.settings import GITHUB_API, GITHUB_TOKEN


headers = {}

if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"


def get_user_repos(username):

    url = f"{GITHUB_API}/users/{username}/repos"

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(res.text)
        raise Exception("GitHub API Error")

    return res.json()


def get_repo_commits(owner, repo):

    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits"

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return []

    return res.json()


def get_repo_contents(owner, repo):

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents"

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return []

    return res.json()