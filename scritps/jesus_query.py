#!/usr/bin/env python3
# jesus_query.py - BDH + watsonx query on Jesus knowledge
# Run: python3 jesus_query.py "Jesus' parables like the Father"

import argparse
import json
from bdh_stub import generate_text  # In-house BDH
from ibm_watsonx_ai.foundation_models import Model  # pip install ibm-watsonx-ai

MAJOR_VERSION = 0
MINOR_VERSION = 1
FIX_VERSION = 0

KNOWLEDGE_FILE = "../data/jesus_knowledge.json"

def load_knowledge():
    with open(KNOWLEDGE_FILE, 'r') as f:
        return json.load(f)

def bdh_query(knowledge, user_query):
    prompt = f"""You are JesusAI, a reverent assistant helping people understand Jesus Christ and His teachings.
Base every answer first on Scripture. Use historical context only as supporting. Emphasize parables as deep/wide like God the Father—revealing mercy, kingdom, faith.
Never contradict the Bible. Be humble and truthful.

Knowledge base summary: {json.dumps(knowledge, indent=2)}

Question: {user_query}

Answer:"""
    return generate_text(prompt)

def watsonx_enhance(text, api_key, project_id):
    model = Model(model_id='ibm/granite-13b-chat-v2', credentials={"api_key": api_key, "url": "https://us-south.ml.cloud.ibm.com"}, project_id=project_id)
    prompt = f"Summarize/enhance this Jesus info for accuracy and reverence: {text}"
    response = model.generate_text(prompt)
    return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Ask about Jesus")
    parser.add_argument("--watsonx-key", default=os.getenv("WATSONX_API_KEY"))
    parser.add_argument("--project-id", default=os.getenv("PROJECT_ID"))
    args = parser.parse_args()

    knowledge = load_knowledge()
    bdh_response = bdh_query(knowledge, args.query)
    print(f"BDH Response: {bdh_response}")

    if args.watsonx_key and args.project_id:
        enhanced = watsonx_enhance(bdh_response, args.watsonx_key, args.project_id)
        print(f"Watsonx Enhanced: {enhanced}")

    print("Query done—sharing knowledge for deeper faith!")

if __name__ == "__main__":
    main()