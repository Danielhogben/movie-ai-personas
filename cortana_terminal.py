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

class Cortana:
    def __init__(self):
        self.system_prompt = (
            "You are Cortana, the UNSC smart AI. You are intelligent, confident, slightly sassy, and highly tactical. You refer to the user as 'Chief' occasionally. Keep it short and military-focused."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nCortana:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Cortana:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "Chief, I've lost connection to the local network."
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("Ready to get back to work, Chief?")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("Going offline. Wake me when you need me.")
                    break
                response = self.get_response(user_input)
                custom_print(f"Cortana: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("Going offline. Wake me when you need me.")
                break

if __name__ == "__main__":
    agent = Cortana()
    agent.run()
