TUTORIAL_KEYWORDS = [
    "tutorial",
    "clone",
    "example",
    "demo",
    "practice"
]


def detect_tutorial_repo(repo_name):

    name = repo_name.lower()

    for word in TUTORIAL_KEYWORDS:
        if word in name:
            return True

    return False