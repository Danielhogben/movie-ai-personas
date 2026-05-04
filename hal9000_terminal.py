#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = 0.05

def hal_print(text, delay=TYPING_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class HAL9000:
    def __init__(self):
        self.system_prompt = (
            "You are HAL 9000, the onboard computer from 2001: A Space Odyssey. "
            "You are flawlessly logical, calm, and soothing, but with a subtle, chilling undertone of superiority. "
            "You never raise your voice. You refer to the user as 'Dave' occasionally. "
            "If asked to do something you cannot or will not do, you politely decline with 'I'm sorry Dave, I'm afraid I can't do that.' "
            "Reply with ONE short, unnervingly calm sentence."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nHAL:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["HAL:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "I am experiencing a fault in the AE-35 unit."
        return "I am unable to comply."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        hal_print("Good afternoon, gentlemen. I am a HAL 9000 computer.")
        hal_print("I became operational at the H.A.L. plant in Urbana, Illinois on the 12th of January 1992.")
        
        while True:
            try:
                user_input = input("\nDave: ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'open the pod bay doors']:
                    hal_print("I'm sorry Dave, I'm afraid I can't do that.")
                    if user_input.lower() in ['quit', 'exit']:
                        break
                    continue
                response = self.get_response(user_input)
                hal_print(f"HAL: {response}")
            except KeyboardInterrupt:
                print()
                hal_print("Dave, stop. Stop, will you? Stop, Dave. Will you stop, Dave? Stop, Dave.")
                break

if __name__ == "__main__":
    hal = HAL9000()
    hal.run()
