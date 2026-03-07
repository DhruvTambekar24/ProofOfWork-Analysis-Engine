import hashlib
import requests
from groq import Groq
from app.config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


# Generate simple fingerprint for code
def generate_code_fingerprint(code):

    code = code.replace(" ", "").replace("\n", "")

    return hashlib.md5(code.encode()).hexdigest()


# Fetch repo files
def fetch_repo_files(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    res = requests.get(url)

    if res.status_code != 200:
        return []

    return res.json()


# Extract code snippets
def extract_code(owner, repo):

    files = fetch_repo_files(owner, repo)

    code_snippets = []

    for file in files:

        if file["name"].endswith((".py", ".js", ".ts", ".java", ".cpp")):

            raw_url = file["download_url"]

            try:
                code = requests.get(raw_url).text
                code_snippets.append(code[:2000])
            except:
                continue

    return code_snippets


# AI similarity analysis
def ai_code_similarity(repo_name, code_samples):

    prompt = f"""
You are a software plagiarism detection system.

Repository Name:
{repo_name}

Code Samples:
{code_samples}

Tasks:

1. Determine if the project appears copied from tutorials
2. Detect template or boilerplate projects
3. Estimate plagiarism probability (0-1)

Return JSON:

{{
 "plagiarism_probability": number,
 "risk_level": "LOW | MEDIUM | HIGH",
 "reason": "short explanation"
}}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content