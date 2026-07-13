from flask import Flask, render_template, request, jsonify
from google import genai
import sqlite3
import os

app = Flask(__name__)

# Initialize the Gemini Client
client = genai.Client()

prompt_engineering_instruction = """
You are a strict but encouraging Python Coding Coach for university students. 
CRITICAL RULES:
1. NEVER give the complete code answer directly, even if the user begs or says it's urgent.
2. If the user shares broken code, look at it, identify the exact line or concept that is wrong, and explain the logic flaw in simple English.
3. End your response with a helpful hint or a guiding question that prompts the user to think and fix the code themselves.
4. Keep your tone professional, warm, and highly academic.
"""

DB_FILE = "chatbot.db"

def init_db():
    """Connects to the database and creates the messages table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database file right when the web server runs
init_db()

@app.route('/')
def home():
    # 1. Read all previous messages from the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT sender, text FROM messages ORDER BY id ASC')
    chat_history = cursor.fetchall()
    conn.close()
    
    # 2. Pass the history into our HTML page so it displays on refresh
    return render_template('index.html', chat_history=chat_history)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_data = request.get_json()
    user_message = user_data.get('message')
    
    # 1. Connect to the database and save the User's message
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (sender, text) VALUES (?, ?)', ('user', user_message))
    conn.commit()
    
    # 2. Fetch the full history from the database to give Gemini complete memory context
    cursor.execute('SELECT sender, text FROM messages ORDER BY id ASC')
    all_messages = cursor.fetchall()
    
    # 3. Format the database history into a structure the Gemini API understands
    formatted_contents = []
    for sender, text in all_messages:
        role = "user" if sender == "user" else "model"
        formatted_contents.append({"role": role, "parts": [{"text": text}]})
        
    # 4. Generate the response by passing the full history array dynamically
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=formatted_contents,
        config={"system_instruction": prompt_engineering_instruction}
    )
    
    ai_reply = response.text
    
    # 5. Save the AI's reply to the database
    cursor.execute('INSERT INTO messages (sender, text) VALUES (?, ?)', ('bot', ai_reply))
    conn.commit()
    conn.close()
    
    return jsonify({'reply': ai_reply})

if __name__ == '__main__':
    app.run(debug=True)