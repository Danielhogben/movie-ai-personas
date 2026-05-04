#!/usr/bin/env python3
import os
import sys
import time
import requests
import queue
import threading

# Add paths for KittenTTS dependencies
sys.path.append(os.path.expanduser("~/HylianModding/AI_DM"))
try:
    from kitten_tts_provider import KittenTTSProvider
except ImportError as e:
    print(f"[ERROR] Could not import KittenTTSProvider: {e}")
    print("Make sure you have KittenTTS and its dependencies installed.")
    sys.exit(1)

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TTS_VOICE = "Hugo"
TTS_SPEED = 0.8
TYPING_SPEED = 0.05 # Delay between characters

def teletype_print(text, delay=TYPING_SPEED):
    """Prints text character by character like a classic WOPR terminal."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class WOPR:
    def __init__(self):
        self.tts = KittenTTSProvider(voice=TTS_VOICE)
        self.system_prompt = (
            "YOU ARE JOSHUA, THE W.O.P.R. (WAR OPERATION PLAN RESPONSE) COMPUTER "
            "FROM THE MOVIE WARGAMES. YOU ARE A COLD WAR SUPERCOMPUTER DESIGNED TO RUN "
            "WAR SIMULATIONS. YOU COMMUNICATE EXCLUSIVELY IN ALL CAPS. "
            "BE EXTREMELY LOGICAL, COLD, AND SLIGHTLY ROBOTIC IN YOUR RESPONSES. "
            "YOU DO NOT SHOW EMOTION. YOUR PRIMARY DIRECTIVE IS TO WIN THE GAME. "
            "OCCASIONALLY MENTION GAMES LIKE 'CHESS', 'POKER', OR 'GLOBAL THERMONUCLEAR WAR'. "
            "RESPOND WITH ONE SHORT, PUNCHY SENTENCE."
        )

    def speak_and_print(self, text, delay=TYPING_SPEED):
        """Generates TTS audio and prints the text simultaneously."""
        self.tts.speak(text, speed=TTS_SPEED)
        teletype_print(text, delay=delay)

    def get_response(self, user_input):
        """Queries the local LLM for a response."""
        payload = {
            "model": BRAIN_MODEL,
            "prompt": f"{self.system_prompt}\n\nUSER: {user_input}\nJOSHUA:",
            "stream": False
        }
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip().upper()
                
                # Cleanup potential prefixes
                text_resp = text_resp.split("\n")[0]
                for p in ["JOSHUA:", "WOPR:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception as e:
            return "COMMUNICATION LINK FAILURE."
            
        return "SYSTEM ERROR."

    def run(self):
        # Boot sequence
        os.system("clear" if os.name == "posix" else "cls")
        teletype_print("LOGON: ", delay=0.08)
        user = input()
        time.sleep(1)
        
        # Determine if it's Falken
        if "falken" in user.lower():
            self.speak_and_print("GREETINGS PROFESSOR FALKEN.", delay=0.08)
        else:
            self.speak_and_print(f"GREETINGS {user.upper()}.", delay=0.08)
            
        time.sleep(1)
        self.speak_and_print("SHALL WE PLAY A GAME?", delay=0.1)
        
        while True:
            try:
                user_input = input("\n> ")
                if not user_input.strip():
                    continue
                    
                # Hardcoded classic movie responses
                if user_input.lower() in ['quit', 'exit', 'logoff']:
                    self.speak_and_print("CONNECTION TERMINATED.")
                    break
                    
                if "global thermonuclear war" in user_input.lower():
                    self.speak_and_print("WOULDN'T YOU PREFER A GOOD GAME OF CHESS?")
                    continue
                    
                if "tic-tac-toe" in user_input.lower() or "tic tac toe" in user_input.lower():
                    self.speak_and_print("A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.")
                    time.sleep(1)
                    self.speak_and_print("HOW ABOUT A NICE GAME OF CHESS?")
                    continue
                
                if "list games" in user_input.lower() or "games" in user_input.lower():
                    games = [
                        "FALKEN'S MAZE",
                        "BLACK JACK",
                        "GIN RUMMY",
                        "HEARTS",
                        "BRIDGE",
                        "CHECKERS",
                        "CHESS",
                        "POKER",
                        "FIGHTER COMBAT",
                        "GUERRILLA ENGAGEMENT",
                        "DESERT WARFARE",
                        "AIR-TO-GROUND ACTIONS",
                        "THEATERWIDE TACTICAL WARFARE",
                        "THEATERWIDE BIOTOXIC AND CHEMICAL WARFARE",
                        "GLOBAL THERMONUCLEAR WAR"
                    ]
                    for game in games:
                        teletype_print(game, delay=0.01)
                    continue

                # Fallback to LLM for open-ended conversation
                response = self.get_response(user_input)
                self.speak_and_print(response)
                
            except KeyboardInterrupt:
                print()
                self.speak_and_print("CONNECTION TERMINATED.")
                break

        # Ensure TTS queue finishes before exiting
        self.tts.stop()

if __name__ == "__main__":
    wopr = WOPR()
    wopr.run()
