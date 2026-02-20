from flask import Flask, request, render_template, jsonify
from google import genai
import os

app = Flask(__name__)

# SECURITY FIX: We fetch the key safely from the server environment
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route('/')
def home():
    return render_template('index.html')

# UPDATED: Analyze route now handles JSON and returns structured data
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_skills = data.get('candidate_profile')
    
    # We explicitly tell the AI to return a structured JSON format
    prompt = f"""
    You are an expert technical recruiter. Analyze the following candidate profile:
    {user_skills}

    Return a JSON object with exactly these keys:
    - "roles": an array of 3 strings (the best entry-level job titles)
    - "resume_bullets": an array of 2 strings (strong resume bullet points based on their skills)
    - "missing_link_skill": a string (the 1 single most important technical skill to learn next)
    - "missing_link_reason": a short string (why this skill bridges the gap)
    """
    
    # Force the AI to output valid JSON
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    # The response.text is now perfectly formatted JSON, so we return it directly
    return response.text

# Chatbot Route (Remains unchanged)
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    prompt = f"""
    You are a helpful, encouraging FAQ chatbot embedded on a career advice website.
    Provide a very concise, friendly, and practical answer (2-3 sentences max).
    User Question: {user_message}
    """
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return jsonify({'reply': response.text})

if __name__ == '__main__':
    app.run(debug=True)