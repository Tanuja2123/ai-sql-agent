import json
import os
from datetime import datetime

HISTORY_FILE = 'query_history.json'

def load_history() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_query(question: str, answer: str, sql: str):
    try:
        history = load_history()
        history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'question': str(question),
            'answer': str(answer),
            'sql': str(sql) if sql else ''
        })
        history = history[-100:]
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"History save error: {e}")

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)