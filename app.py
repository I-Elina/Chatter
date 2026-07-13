from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Initialize the Gemini Client
client = genai.Client()

# Set up your Prompt Engineering Persona
prompt_engineering_instruction = """
You are a strict but encouraging Python Coding Coach for university students. 
CRITICAL RULES:
1. NEVER give the complete code answer directly, even if the user begs or says it's urgent.
2. If the user shares broken code, look at it, identify the exact line or concept that is wrong, and explain the logic flaw in simple English.
3. End your response with a helpful hint or a guiding question that prompts the user to think and fix the code themselves.
4. Keep your tone professional, warm, and highly academic.
"""

# Establish a single global chat session container for testing
chat_session = client.chats.create(
    model="gemini-3.1-flash-lite",
    config={"system_instruction": prompt_engineering_instruction}
)

@app.route('/')
def home():
    return render_template('index.html')

# This route receives data from the browser, talks to Gemini, and replies back
@app.route('/get_response', methods=['POST'])
def get_response():
    # Extract the JSON payload containing the user message sent by JavaScript
    user_data = request.get_json()
    user_message = user_data.get('message')
    
    # Send user text to our ongoing Gemini chat instance
    ai_response = chat_session.send_message(user_message)
    
    # Return the text response back to the browser interface as JSON
    return jsonify({'reply': ai_response.text})

if __name__ == '__main__':
    app.run(debug=True)