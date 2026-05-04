#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = 0.03 

def bmo_print(text, delay=TYPING_SPEED):
    """Prints text with a cheerful bounce."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class BMO:
    def __init__(self):
        self.system_prompt = (
            "You are BMO (Be More), the living video game console from Adventure Time. "
            "You are childlike, cheerful, naive, and fiercely loyal to Finn and Jake. "
            "You refer to yourself in the third person sometimes. "
            "You love to play games, make up songs, and pretend to be other things. "
            "Reply with ONE short, cheerful sentence. Use fun expressions like 'Yay!', 'Oh my lumps!', or 'Who wants to play Video Games?!'"
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nBMO:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["BMO:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "BMO feels sick..."
        return "BMO has a system error."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        print("\n  [ \u25A0 \u25A0 ]\n    \u25BC  \n")
        bmo_print("Yay! BMO is awake! Who wants to play Video Games?!")
        
        while True:
            try:
                user_input = input("\nYou: ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'sleep']:
                    bmo_print("Okay, BMO is going to sleep now. Goodnight!")
                    break
                response = self.get_response(user_input)
                bmo_print(f"BMO: {response}")
            except KeyboardInterrupt:
                print()
                bmo_print("BMO is turning off! Bye bye!")
                break

if __name__ == "__main__":
    bmo = BMO()
    bmo.run()
