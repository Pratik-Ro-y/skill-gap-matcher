from google import genai
import os

# Ensure your GEMINI_API_KEY is set in your environment variables
client = genai.Client()

# This text will eventually be captured dynamically from your HTML form
candidate_profile = """
Education: Pursuing BSc
Skills: Python, HTML, CSS, Hadoop, Hive, basic Android development
Projects: AI Study Notes & Quiz Generator, simple Android calculator
"""

prompt = f"""
You are an expert technical recruiter. Analyze the following candidate profile:
{candidate_profile}

Provide the output strictly in this format:
1. Top 3 Entry-Level Job Titles (Based on the exact skills provided).
2. Resume Upgrade: Two professional resume bullet points highlighting the projects to impress recruiters.
3. The Missing Link: The single most important technical skill they should learn next to bridge the gap to a full-stack or data engineering role.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)