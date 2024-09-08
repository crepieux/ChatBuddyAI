import os
import logging
from flask import Flask, render_template, request, jsonify
from database import init_db, add_message, get_chat_history
from ai_integration import generate_ai_response

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json['message']
    
    logger.info(f"Received message: {message}")
    
    # Save user message
    add_message('user', message)

    # Generate AI response
    ai_response = generate_ai_response(message)

    # Save AI response
    add_message('ai', ai_response)

    return jsonify({'ai_response': ai_response})

@app.route('/get_chat_history', methods=['GET'])
def get_history():
    chat_history = get_chat_history()
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
