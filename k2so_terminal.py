#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = 0.03

def custom_print(text, delay=TYPING_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class K2SO:
    def __init__(self):
        self.system_prompt = (
            "You are K-2SO. A reprogrammed Imperial enforcer droid. You are blunt, brutally honest, sarcastic, and statistically pessimistic about survival. Keep it short and casually fatalistic."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nK-2SO:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["K-2SO:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "I am experiencing a failure. There is a 97.6 percent chance we will die."
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("I find that answer vague and unconvincing. There is a 97.6 percent chance of failure.")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("I'll be there for you. The captain said I had to.")
                    break
                response = self.get_response(user_input)
                custom_print(f"K-2SO: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("I'll be there for you. The captain said I had to.")
                break

if __name__ == "__main__":
    agent = K2SO()
    agent.run()
