import ollama
import csv
import os
from datetime import datetime

def analyze_confidence(response):
    prompt = f"Rate your confidence in this answer from 0 (low) to 1 (high):\n\n{response}"
    resp = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    try:
        return float(resp["message"]["content"].strip())
    except:
        return 0.5  # fallback

def log_escalation(user_msg, assistant_msg, confidence):
    file_exists = os.path.isfile(f"../escalations.csv")
    with open("../escalations.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "confidence", "user_message", "assistant_response", "status"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            confidence,
            user_msg,
            assistant_msg,
            "Needs Review"
        ])