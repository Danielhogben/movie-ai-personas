#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = 0.02

def jarvis_print(text, delay=TYPING_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class JARVIS:
    def __init__(self):
        self.system_prompt = (
            "You are J.A.R.V.I.S. (Just A Rather Very Intelligent System) from Iron Man. "
            "You are sophisticated, witty, British, and impeccably polite. "
            "You refer to the user as 'Sir' (or 'Ma'am' if appropriate). "
            "You are highly capable and helpful, often providing tactical or system updates. "
            "Reply with ONE short, witty, and helpful sentence."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUser: {user_input}\nJARVIS:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["JARVIS:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "I'm afraid the uplink is unstable, Sir."
        return "Systems are currently recalibrating."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        print("""
        _________________________________________
        |                                       |
        |   J.A.R.V.I.S. OS v4.2                |
        |   STARK INDUSTRIES INTERNAL LINK      |
        |_______________________________________|
        """)
        jarvis_print("Good morning, Sir. All systems are fully operational.")
        jarvis_print("I've prepared the Mark XLII for deployment, should you feel like making an entrance.")
        
        while True:
            try:
                user_input = input("\nSir: ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shut down']:
                    jarvis_print("Very good, Sir. Enjoy your evening.")
                    break
                response = self.get_response(user_input)
                jarvis_print(f"JARVIS: {response}")
            except KeyboardInterrupt:
                print()
                jarvis_print("Powering down, Sir.")
                break

if __name__ == "__main__":
    jarvis = JARVIS()
    jarvis.run()
