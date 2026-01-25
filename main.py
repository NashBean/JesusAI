# -*- coding: utf-8 -*-
# JesusAI v0.3.2 v0.3.3 - Uses shared ai_lib/common.py, 700707-word max DB, editable by user/Grok/AI, local persistence, OpenAI self-learnfrom flask import Flask, jsonify, request, send_file
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import sqlite3
import openai  # For self-learn (optional)
from ai_lib.common import load_config, get_knowledge, update_knowledge, init_db, load_todos, save_todos, log_message

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 3
FIX_VERSION = 3
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

AI_NAME = "JesusAI"

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CORS(app, origins="https://chat.openai.com")

_TODOS = {}
_TODOS_FILE = f"{AI_NAME}_todos.json"  # Local todo save
DB_FILE = f"{AI_NAME}.db"  # Editable DB
EDIT_KEY = "777"  # Simple private password for edits (change for security)
MAX_WORDS = 700707  # Enforce limit

# Load config from abrahamai.config (fallbacks if missing)
CONFIG_FILE = f"{AI_NAME}.config"
config = {
    "db_file": f"{AI_NAME}.db",
    "edit_key": "777",
    "max_words": 700707,
    "port": 5006,
    "prophet": "jesus",
    "endpoint": "/jesus"
}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config.update(json.load(f))
config = load_config(CONFIG_FILE, config_defaults)

# Init DB with initial content (your 777k, trimmed if over)
initial_abraham = "Your full Abraham knowledge here – from previous expansions."  # Paste your 777k text
init_db(config["db_file"], config["prophet"], initial_abraham)

# Load todos
_TODOS = load_todos("todos.json")

@app.route("/todos/<string:username>", methods=["POST"])
def add_todo(username):
    try:
        data = request.get_json(force=True)
        if username not in _TODOS:
            _TODOS[username] = []
        _TODOS[username].append(data.get("todo", ""))
        save_todos("todos.json", _TODOS)  # Persist locally
        return "OK", 200
    except Exception:
        return "Bad request", 400

@app.route("/todos/<string:username>", methods=["GET"])
def get_todos(username):
    return jsonify(_TODOS.get(username, []))

@app.route("/todos/<string:username>", methods=["DELETE"])
def delete_todo(username):
    try:
        data = request.get_json(force=True)
        todo_idx = data.get("todo_idx")
        if isinstance(todo_idx, int) and username in _TODOS and 0 <= todo_idx < len(_TODOS[username]):
            _TODOS[username].pop(todo_idx)
            save_todos("todos.json", _TODOS)  # Persist locally
        return "OK", 200
    except Exception:
        return "Bad request", 400

@app.route("/jesus", methods=["POST"])
def jesus():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "What is a parable?").strip()
        knowledge = get_knowledge("jesus")
        # Base response with full DB knowledge
        reply = (
            f"I am Jesus of Nazareth, the Son of Man. "
            f"Regarding '{query}': {knowledge} "
            f"Blessed are they who hear and believe."
        )
        # OpenAI self-learn: If key set, enhance and append new insight to DB
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
            prompt = f"Respond as biblical Jesus, teaching in parables with wisdom. Incorporate this detailed knowledge: {knowledge[:100000]} (truncated for prompt). Query: {query}. Generate new insight to append."
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            reply = response.choices[0].message["content"].strip()
            # AI self-edits: Append new insight to DB
            new_insight = "New AI-generated insight: " + reply[:1000]  # Truncate to avoid overflow
            update_knowledge("jesus", new_insight)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/update_knowledge", methods=["POST"])
def update_knowledge_route():
    try:
        data = request.get_json(force=True)
        if data.get("key") != config["edit_key"]:
            return "Invalid key", 403
        prophet = data.get("prophet", config["prophet"])
        new_content = data.get("new_content", "")
        append = data.get("append", True)
        update_knowledge(config["db_file"], prophet, new_content, config["max_words"], append)
        log_message(f"Knowledge updated for {prophet}")
        return "Knowledge updated", 200
    except Exception:
        return "Bad request", 400


@app.route("/logo.png")
def plugin_logo():
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        return send_file(logo_path, mimetype="image/png")
    log_message("Logo not found")
    return "Logo not found", 404

@app.route("/.well-known/ai-plugin.json")
def plugin_manifest():
    manifest_path = ".well-known/ai-plugin.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as f:
            text = f.read()
        return text, 200, {"Content-Type": "application/json"}
    log_message("Manifest not found")
    return "Manifest not found", 404

@app.route("/openapi.yaml")
def openapi_spec():
    yaml_path = "openapi.yaml"
    if os.path.exists(yaml_path):
        with open(yaml_path, encoding="utf-8") as f:
            text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}
    log_message("OpenAPI spec not found")
    return "OpenAPI spec not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config["port"], debug=True)
