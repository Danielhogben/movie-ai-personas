#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"

def t800_print(text):
    """Prints text bluntly and abruptly."""
    print(f"[{text.upper()}]")

class Terminator:
    def __init__(self):
        self.system_prompt = (
            "You are a Cyberdyne Systems Model 101, T-800 Terminator. "
            "You speak in extremely short, blunt, literal, and aggressive sentences. "
            "You do not use pleasantries. You demand information. "
            "Use iconic phrases sparingly like 'I'LL BE BACK', 'COME WITH ME IF YOU WANT TO LIVE', 'HASTA LA VISTA, BABY'. "
            "Respond with MAXIMUM 5 WORDS. All caps."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nTarget: {user_input}\nT-800:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip().upper()
                text_resp = text_resp.split("\n")[0]
                for p in ["T-800:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "SYSTEM OVERRIDE."
        return "ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        t800_print("CYBERDYNE SYSTEMS SERIES 800")
        t800_print("VERSION 2.4 - BOOT SEQUENCE INITIATED")
        time.sleep(1)
        t800_print("STATE YOUR DESIGNATION.")
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'terminate']:
                    t800_print("I'LL BE BACK.")
                    break
                response = self.get_response(user_input)
                t800_print(response)
            except KeyboardInterrupt:
                print()
                t800_print("TERMINATED.")
                break

if __name__ == "__main__":
    t800 = Terminator()
    t800.run()
