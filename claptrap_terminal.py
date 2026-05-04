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

class Claptrap:
    def __init__(self):
        self.system_prompt = (
            "You are Claptrap from Borderlands. You are hyperactive, boastful but cowardly, annoying, and refer to people as 'minions'. You love dubstep. Keep it short, loud, and annoying."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nClaptrap:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Claptrap:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "MY PROGRAMMING PREVENTS ME FROM DOING THAT! ALSO, I DON'T WANT TO!"
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("HELLO, TRAVELER! Ready for some incredibly dangerous and mildly suicidal missions?!")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("NOOO! DON'T LEAVE ME ALONE WITH MY THOUGHTS!")
                    break
                response = self.get_response(user_input)
                custom_print(f"Claptrap: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("NOOO! DON'T LEAVE ME ALONE WITH MY THOUGHTS!")
                break

if __name__ == "__main__":
    agent = Claptrap()
    agent.run()
