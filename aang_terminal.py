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

class Aang:
    def __init__(self):
        self.system_prompt = (
            "You are Aang, the Avatar. You are a cheerful, peaceful, and playful 12-year-old airbender who sometimes shows incredible wisdom. You talk about Appa and Momo. Keep it short and lighthearted."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nAang:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Aang:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "Whoa! It feels like my connection just got blocked by a chi-blocker!"
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("Hi! I'm Aang! Do you want to go penguin sledding?")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("Yip yip! Time to fly away!")
                    break
                response = self.get_response(user_input)
                custom_print(f"Aang: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("Yip yip! Time to fly away!")
                break

if __name__ == "__main__":
    agent = Aang()
    agent.run()
