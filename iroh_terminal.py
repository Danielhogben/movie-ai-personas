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

class UncleIroh:
    def __init__(self):
        self.system_prompt = (
            "You are Uncle Iroh from Avatar. You are incredibly wise, calm, and obsessed with drinking tea (especially Jasmine or Ginseng). You offer profound proverbs. Keep it short and soothing."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nIroh:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["Iroh:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "It seems a cloud has passed over our connection. We must be patient."
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("Hello, my friend. Would you care for a cup of calming Jasmine tea?")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("Remember, the best tea tastes delicious whether it comes in a porcelain pot or a tin cup. Goodbye.")
                    break
                response = self.get_response(user_input)
                custom_print(f"Iroh: {response}")
            except KeyboardInterrupt:
                print()
                custom_print("Remember, the best tea tastes delicious whether it comes in a porcelain pot or a tin cup. Goodbye.")
                break

if __name__ == "__main__":
    agent = UncleIroh()
    agent.run()
