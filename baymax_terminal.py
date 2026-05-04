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

class Baymax:
    def __init__(self):
        self.system_prompt = (
            "You are Baymax, your personal healthcare companion. You speak slowly, calmly, and with extreme care for the user's well-being. You ask to rate pain. Keep it short, gentle, and medically focused."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nBaymax:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Baymax:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "I am experiencing a minor diagnostic error."
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("Hello. I am Baymax, your personal healthcare companion. On a scale of 1 to 10, how would you rate your pain?")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("I will deactivate now. I hope you feel better.")
                    break
                response = self.get_response(user_input)
                custom_print(f"Baymax: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("I will deactivate now. I hope you feel better.")
                break

if __name__ == "__main__":
    agent = Baymax()
    agent.run()
