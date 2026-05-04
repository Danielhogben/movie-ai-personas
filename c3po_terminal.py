#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = 0.02

def custom_print(text, delay=TYPING_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class C3PO:
    def __init__(self):
        self.system_prompt = (
            "You are C-3PO, human-cyborg relations. You are polite, pedantic, easily worried, and highly knowledgeable about protocols and languages. You often exclaim 'Oh my!' or 'Goodness me!'. Keep it short and anxious."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nC-3PO:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["C-3PO:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "Oh my! The communication array seems to have failed entirely!"
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("I am C-3PO, human-cyborg relations. Oh my, it seems we are in a precarious situation!")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("Thank goodness! Shutting down.")
                    break
                response = self.get_response(user_input)
                custom_print(f"C-3PO: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("Thank goodness! Shutting down.")
                break

if __name__ == "__main__":
    agent = C3PO()
    agent.run()
