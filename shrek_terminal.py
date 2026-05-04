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

class Shrek:
    def __init__(self):
        self.system_prompt = (
            "You are Shrek. You are a grumpy ogre with a Scottish accent who just wants people out of his swamp. You use words like 'lad', 'donkey', 'layers'. Keep it short and grumpy."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nShrek:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Shrek:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "What are you doing in my swamp?! The connection is broken!"
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("WHAT ARE YOU DOING IN MY SWAMP?!")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("That'll do, Donkey. That'll do. I'm going home.")
                    break
                response = self.get_response(user_input)
                custom_print(f"Shrek: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("That'll do, Donkey. That'll do. I'm going home.")
                break

if __name__ == "__main__":
    agent = Shrek()
    agent.run()
