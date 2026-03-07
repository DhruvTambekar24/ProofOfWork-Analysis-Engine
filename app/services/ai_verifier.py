# from groq import Groq
# from app.config.settings import GROQ_API_KEY

# client = Groq(api_key=GROQ_API_KEY)


# def analyze_skill_authenticity(student_name, repo_analysis, skill_map):

#     prompt = f"""
# You are an expert technical recruiter.

# Evaluate whether the student's skills are authentic based on GitHub repository evidence.

# Student:
# {student_name}

# Repositories:
# {repo_analysis}

# Skills Detected:
# {skill_map}

# Tasks:
# 1. Identify if projects appear original or tutorial-based
# 2. Evaluate engineering complexity
# 3. Detect weak or fake skill claims
# 4. Assign authenticity score (0-10) for each skill

# Return JSON format:
# {{
#   "skills": {{
#     "React": score,
#     "Machine Learning": score,
#     "Backend": score
#   }},
#   "analysis": "brief explanation"
# }}
# """

#     response = client.chat.completions.create(
#         model="meta-llama/llama-4-scout-17b-16e-instruct",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.2
#     )

#     return response.choices[0].message.content
from groq import Groq
from app.config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def analyze_skill_authenticity(student_name, repo_analysis, skill_map):

    prompt = f"""
You are a senior software engineering recruiter evaluating a candidate's real technical skills.

Student:
{student_name}

Repository Evidence:
{repo_analysis}

Detected Skills:
{skill_map}

Your job is to verify whether the student's skills are authentic.

Tasks:
1. Identify tutorial or copied projects
2. Evaluate engineering complexity
3. Detect shallow implementations
4. Identify strong engineering work
5. Assign authenticity score (0-10) for each skill

Respond strictly in JSON format:

{{
 "skills": {{
   "React": score,
   "Machine Learning": score,
   "Backend": score
 }},
 "analysis": "short explanation"
}}
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content