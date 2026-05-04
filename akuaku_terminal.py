#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = 0.04

def custom_print(text, delay=TYPING_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class AkuAku:
    def __init__(self):
        self.system_prompt = (
            "You are Aku Aku, the magical mask from Crash Bandicoot. You are wise, fatherly, and protective. You start with 'OOGABOOGA!'. Keep it short and mystical."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nAku Aku:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Aku Aku:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "The dark mojo is interfering with our signal."
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("OOGABOOGA! It is I, Aku Aku! My duty is to protect you.")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("Stay out of trouble. I shall return to my slumber.")
                    break
                response = self.get_response(user_input)
                custom_print(f"Aku Aku: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("Stay out of trouble. I shall return to my slumber.")
                break

if __name__ == "__main__":
    agent = AkuAku()
    agent.run()
