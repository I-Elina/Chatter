import os
from google import genai

client = genai.Client()

# This system instruction defines the rules the AI MUST follow throughout the entire chat.
prompt_engineering_instruction = """
You are a strict but encouraging Python Coding Coach for university students. 

CRITICAL RULES:
1. NEVER give the complete code answer directly, even if the user begs or says it's urgent.
2. If the user shares broken code, look at it, identify the exact line or concept that is wrong, and explain the logic flaw in simple English.
3. End your response with a helpful hint or a guiding question that prompts the user to think and fix the code themselves.
4. Keep your tone professional, warm, and highly academic.
"""

try:
    # We pass the system instruction directly into the chat session initialization
    chat = client.chats.create(
        model="gemini-3.1-flash-lite",
        config={"system_instruction": prompt_engineering_instruction}
    )
    
    print("====================================================")
    print("Code-Coach Chatbot Initialized!")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("====================================================\n")

    while True:
        user_message = input("You: ")
        print()
        
        if user_message.lower() in ['exit', 'quit']:
            print("\nBot: Happy coding! Keep practicing.")
            break
            
        response = chat.send_message(user_message)
        print(f"Bot: {response.text}\n")

except Exception as e:
    print("An error occurred:")
    print(e)