def calculate_commit_ownership(commits, username):

    total = len(commits)
    if total == 0:
        return 0

    student_commits = 0

    for c in commits:
        if c["commit"]["author"]["name"].lower() == username.lower():
            student_commits += 1

    return student_commits / total