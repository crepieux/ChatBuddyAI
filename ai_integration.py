from openai_chat_completion.chat_request import send_openai_request

def generate_ai_response(user_message):
    prompt = f"User: {user_message}\nAI:"
    try:
        response = send_openai_request(prompt)
        return response.strip()
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "I'm sorry, I couldn't generate a response at this time."
