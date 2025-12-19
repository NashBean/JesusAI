# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, Response
import json

app = Flask(__name__)

# Jesus-style response (static for now)
JESUS_RESPONSE = {
    "response": "My child, the Kingdom of Heaven is like a mustard seed. "
                "Though small, it grows into the greatest of trees. "
                "What parable shall I teach you today?",
    "verse": "Matthew 13:31-32"
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower()
    
    # Simple keyword responses
    if 'love' in user_message:
        reply = "Love your neighbor as yourself. This is the greatest commandment."
        verse = "Matthew 22:39"
    elif 'forgive' in user_message:
        reply = "Forgive, and you will be forgiven. As far as the east is from the west, so far has He removed our sins."
        verse = "Luke 6:37, Psalm 103:12"
    else:
        reply = JESUS_RESPONSE["response"]
        verse = JESUS_RESPONSE["verse"]
    
    return jsonify({
        "reply": reply,
        "verse": verse,
        "speaker": "Jesus"
    })

@app.route('/')
def home():
    return '''
    <h1>JesusAI is Alive!</h1>
    <p>Send POST to /chat with JSON: {"message": "your question"}</p>
    <textarea id="msg" style="width:100%;height:100px;"></textarea><br>
    <button onclick="send()">Ask Jesus</button>
    <pre id="out"></pre>
    <script>
    function send() {
        fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: document.getElementById('msg').value})
        })
        .then(r => r.json())
        .then(d => document.getElementById('out').textContent = JSON.stringify(d, null, 2));
    }
    </script>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
