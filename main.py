import os
import logging
from flask import Flask, render_template, request, jsonify
from database import init_db, add_message, get_chat_history, create_conversation, get_conversations
from ai_integration import generate_ai_response

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json['message']
    conversation_id = request.json.get('conversation_id')
    
    logger.info(f"Received message: {message}")
    
    if not conversation_id:
        conversation_id = create_conversation()
    
    # Save user message
    add_message(conversation_id, 'user', message)

    # Generate AI response
    ai_response = generate_ai_response(message)

    # Save AI response
    add_message(conversation_id, 'ai', ai_response)

    return jsonify({'ai_response': ai_response, 'conversation_id': conversation_id})

@app.route('/get_chat_history', methods=['GET'])
def get_history():
    conversation_id = request.args.get('conversation_id')
    chat_history = get_chat_history(conversation_id)
    return jsonify(chat_history)

@app.route('/get_conversations', methods=['GET'])
def list_conversations():
    conversations = get_conversations()
    return jsonify(conversations)

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
