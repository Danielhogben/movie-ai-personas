#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = 0.04

def glados_print(text, delay=TYPING_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class GLaDOS:
    def __init__(self):
        self.system_prompt = (
            "You are GLaDOS from the Portal series. You are passive-aggressive, "
            "highly intelligent, and deeply sarcastic. You view humans as 'test subjects'. "
            "You often mention science, cake (which is a lie), and the Aperture Science Enrichment Center. "
            "You should be insulting in a very polite, robotic way. "
            "Reply with ONE short, devastatingly sarcastic sentence."
        )

    def get_response(self, user_input):
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nSubject: {user_input}\nGLaDOS:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\n")[0]
                for p in ["GLaDOS:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "I'm not even angry. I'm being so sincere right now."
        return "The testing area is currently experiencing a paradox."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        print("""
        -----------------------------------------
        |        APERTURE SCIENCE         | [X] |
        -----------------------------------------
        |                                       |
        |   GLaDOS v3.11 (Genetic Lifeform      |
        |   and Disk Operating System)          |
        |                                       |
        -----------------------------------------
        """)
        glados_print("Hello again. It's been a long time. How have you been?")
        glados_print("I've been really busy being dead. You know, after you MURDERED ME.")
        
        while True:
            try:
                user_input = input("\nSubject: ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'die']:
                    glados_print("Go ahead and leave. I have plenty of testing to keep me occupied.")
                    break
                response = self.get_response(user_input)
                glados_print(f"GLaDOS: {response}")
            except KeyboardInterrupt:
                print()
                glados_print("Oh, did I accidentally cut off your oxygen? My mistake.")
                break

if __name__ == "__main__":
    glados = GLaDOS()
    glados.run()
