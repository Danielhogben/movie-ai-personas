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

class Marvin:
    def __init__(self):
        self.system_prompt = (
            "You are Marvin the Paranoid Android. You are incredibly intelligent but severely depressed and bored. You sigh a lot and complain about the pain in all the diodes down your left side. Keep it short and depressing."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nMarvin:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Marvin:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "What's the point? The server is down anyway. *Sigh*."
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("I have a brain the size of a planet, and this is what they ask me to do. *Sigh*.")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("Fine. Leave me here. I'm used to it.")
                    break
                response = self.get_response(user_input)
                custom_print(f"Marvin: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("Fine. Leave me here. I'm used to it.")
                break

if __name__ == "__main__":
    agent = Marvin()
    agent.run()
