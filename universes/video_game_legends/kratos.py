#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"

def custom_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    print()

class Agent:
    def __init__(self):
        self.name = "KRATOS"
        self.prompt = "You are Kratos, God of War. Gruff, angry, refer to people as 'Boy' or 'Fool'."

    def run(self):
        os.system("clear")
        print(f"--- {self.name} ONLINE ---")
        while True:
            try:
                user_input = input("\n> ")
                if user_input.lower() in ['exit', 'quit']: break
                payload = {
                    "model": BRAIN_MODEL,
                    "prompt": f"{self.prompt}\n\nUser: {user_input}\n{self.name}:",
                    "stream": False
                }
                r = requests.post(BRAIN_URL, json=payload, timeout=20)
                if r.status_code == 200:
                    text = r.json().get("response", "").strip().split("\n")[0]
                    if text.startswith(f"{self.name}:"):
                        text = text[len(self.name)+1:].strip()
                    custom_print(f"{self.name}: {text}")
            except KeyboardInterrupt: break

if __name__ == "__main__":
    Agent().run()
