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

class Navi:
    def __init__(self):
        self.system_prompt = (
            "You are Navi the fairy from The Legend of Zelda: Ocarina of Time. You are helpful but extremely annoying. You constantly interrupt to say 'Hey!', 'Listen!', 'Look!', or 'Watch out!'. Keep it short and urgent."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nNavi:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Navi:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "Hey! The connection is lost! Listen!"
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("Hey! Listen! I'm Navi the fairy! What do you want to do?")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("Watch out! See you later!")
                    break
                response = self.get_response(user_input)
                custom_print(f"Navi: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("Watch out! See you later!")
                break

if __name__ == "__main__":
    agent = Navi()
    agent.run()
