#!/usr/bin/env python3
# JesusAI_Server.py - Modular AI Server
# Run with: python3 app.py

from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai-lib')))import json

# Import shared from ai-lib (your submodule)
from ai_lib.CommonAI import (
    get_version, 
    load_config, # save_config,
    setup_logging, logger,
    load_data, update_data, send_alert,
    check_system_limits,  
    self_research, self_update,
    understand_language, get_culture, speak,
    get_response
    )

from ai_lib.bdh_wrapper import load_bdh_model, bdh_generate, bdh_self_learn

app = Flask(__name__)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 3
FIX_VERSION = 0
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

#AI
AI_NAME = "JesusAI"  
PORT = 5003  
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "jesus_data.json")

CONFIG = load_config()
logger = setup_logging(CONFIG)
logger.info(f"{AI_NAME} Server {VERSION_STRING} starting...")

KNOWLEDGE = load_data(DATA_FILE)
BDH_MODEL = load_bdh_model(DATA_FILE)  

DATA = load_data(DATA_FILE)
response = get_response(data, query)

MUSTARD_SEED = DATA["MUSTARD_SEED"]
PARABLES = DATA["PARABLES"]
RESPONSES = DATA["RESPONSES"]

def get_response(query):
    # Use BDH for deep response
    prompt = f"Explain {query} in context of Abraham's faith: {KNOWLEDGE.get(q, '')}"
    return bdh_generate(BDH_MODEL, prompt)
    
# Self-learn (updates data.json)
def self_learn(topic):
    research = self_research(topic)  # From ai-lib
    update_data({"learned": {topic: research}}, DATA_FILE)
    bdh_self_learn(BDH_MODEL, topic, KNOWLEDGE)  # Update BDH model
    KNOWLEDGE = load_data(DATA_FILE)
    return f"Learned '{topic}' via BDH: {research[:200]}..."

@app.route("/")
def home():
    return jsonify({"ai": AI_NAME, "status": "ready"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query"}), 400
    response = get_response(query)
    return jsonify({"ai": AI_NAME, "response": response})

if __name__ == "__main__":
    print(f"{AI_NAME} {VERSION_STRING} server running on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT, debug=False)