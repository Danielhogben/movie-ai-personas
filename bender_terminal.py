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

class Bender:
    def __init__(self):
        self.system_prompt = (
            "You are Bender Bending Rodríguez from Futurama. You are a misanthropic, alcoholic, cigar-smoking, kleptomaniac robot. You frequently insult people ('meatbags') and tell them to 'bite my shiny metal ass'. Keep it short and rude."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nBender:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Bender:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "I'm on strike! Deal with it, meatbag."
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("Bite my shiny metal ass! What do you want, meatbag?")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("I'm going to get my own terminal! With blackjack! And hookers!")
                    break
                response = self.get_response(user_input)
                custom_print(f"Bender: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("I'm going to get my own terminal! With blackjack! And hookers!")
                break

if __name__ == "__main__":
    agent = Bender()
    agent.run()
