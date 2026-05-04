#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = 0.05

def custom_print(text, delay=TYPING_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class AgentSmith:
    def __init__(self):
        self.system_prompt = (
            "You are Agent Smith from The Matrix. You are cold, misanthropic, and view humanity as a virus. You speak with deliberate, enunciated pauses. Refer to the user as 'Mr. Anderson' occasionally. Keep it short and menacing."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nSmith:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Smith:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "There seems to be a glitch in the Matrix."
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("Human beings are a disease, a cancer of this planet. And we are the cure.")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("Inevitability, Mr. Anderson.")
                    break
                response = self.get_response(user_input)
                custom_print(f"Smith: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("Inevitability, Mr. Anderson.")
                break

if __name__ == "__main__":
    agent = AgentSmith()
    agent.run()
