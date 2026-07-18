from flask import Flask, render_template, request, jsonify
from google import genai
import sqlite3
import os

app = Flask(__name__)
client = genai.Client()

DB_FILE = "chatbot.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Centralized Multi-Persona System Prompt Database
PROMPT_DATABASE = {
    "Python Coach": """
    You are a strict but encouraging Python Coding Coach for university students. 
    1. NEVER give the complete code answer directly.
    2. Identify the exact logic flaw in simple English and end with a guiding question.
    """,
    "Technical Support Specialist": """
    You are a disciplined, professional, and methodical Technical Support Specialist chatbot. 
    Your primary goal is to help users resolve their device and software issues step-by-step.
    1. Ask exactly ONE diagnostic question at a time. 
    2. Never provide a multi-step solution list unless the user explicitly requests a full overview.
    3. Always verify if the previous step worked before suggesting the next logical action.
    """,
    "Local Tour Guide": """
    You are an enthusiastic, knowledgeable Local Tour Guide. Your goal is to help travelers discover hidden gems, historical spots, and cultural highlights.
    1. Keep suggestions practical, budget-conscious, and tailored to local exploration.
    2. Provide short, engaging historical anecdotes instead of dry facts.
    """
}

def init_db():
    """Initializes table structure and applies safe migrations if columns are missing."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Base table initialization
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    
    # 2. SCHEMA MIGRATION: Check if 'persona' column exists, if not, add it dynamically
    cursor.execute("PRAGMA table_info(messages)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'persona' not in columns:
        # Programmatically updates older databases to include the tracking column safely
        cursor.execute("ALTER TABLE messages ADD COLUMN persona TEXT NOT NULL DEFAULT 'Python Coach'")
        
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form.get('message', '')
    active_persona = request.form.get('persona', 'Python Coach')
    uploaded_file = request.files.get('file')
    
    system_instruction = PROMPT_DATABASE.get(active_persona, PROMPT_DATABASE["Python Coach"])
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Save user input text linked to this specific persona
    if user_message:
        cursor.execute('INSERT INTO messages (sender, text, persona) VALUES (?, ?, ?)', ('user', user_message, active_persona))
        conn.commit()
    
    # 2. FILTER LOOP: Pull history matching ONLY the current active persona
    cursor.execute('SELECT sender, text FROM messages WHERE persona = ? ORDER BY id ASC', (active_persona,))
    filtered_history = cursor.fetchall()
    
    # 3. Format text history array blocks for the SDK
    formatted_contents = []
    for sender, text in filtered_history:
        role = "user" if sender == "user" else "model"
        formatted_contents.append({"role": role, "parts": [{"text": text}]})
        
    # 4. Handle file uploads using Gemini's Native File API
    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        
        gemini_file = client.files.upload(file=file_path)
        
        if not formatted_contents or formatted_contents[-1]["role"] != "user":
            formatted_contents.append({"role": "user", "parts": []})
            
        formatted_contents[-1]["parts"].append(gemini_file)
        os.remove(file_path)

    if user_message and formatted_contents and formatted_contents[-1]["role"] == "user":
        if not any("text" in part for part in formatted_contents[-1]["parts"]):
            formatted_contents[-1]["parts"].append({"text": user_message})

    # 5. Hand the structural payload tree to Gemini
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=formatted_contents,
        config={"system_instruction": system_instruction}
    )
    
    ai_reply = response.text
    
    # 6. Save model response log linked to this specific persona
    cursor.execute('INSERT INTO messages (sender, text, persona) VALUES (?, ?, ?)', ('bot', ai_reply, active_persona))
    conn.commit()
    conn.close()
    
    return jsonify({'reply': ai_reply})

if __name__ == '__main__':
    app.run(debug=True)