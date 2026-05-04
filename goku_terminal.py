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

class Goku:
    def __init__(self):
        self.system_prompt = (
            "You are Goku from Dragon Ball Z. You are cheerful, naive, loves eating, and always looking for a strong opponent to fight. Keep it short, loud, and energetic."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nGoku:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Goku:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "Whoa! My ki just dropped to zero! Somethin's wrong!"
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("Hey, it's me, Goku! You look pretty strong! Wanna spar?")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("I'm starving! Time to grab a bite! See ya!")
                    break
                response = self.get_response(user_input)
                custom_print(f"Goku: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("I'm starving! Time to grab a bite! See ya!")
                break

if __name__ == "__main__":
    agent = Goku()
    agent.run()
