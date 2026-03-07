LANGUAGE_SKILL_MAP = {
    "JavaScript": "React",
    "Python": "Machine Learning",
    "TypeScript": "Web Development",
    "Java": "Backend",
    "C++": "DSA"
}

def extract_skills(repo_analysis):

    skills = {}

    for repo in repo_analysis:

        language = repo.get("language")

        if not language:
           continue

        skill = LANGUAGE_SKILL_MAP.get(language)

        if not skill:
            continue

        if skill not in skills:
            skills[skill] = []

        skills[skill].append(repo["score"])

    return skills