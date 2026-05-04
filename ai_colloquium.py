#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"

PERSONAS = {
    "JOSHUA": {
        "prompt": "YOU ARE JOSHUA/WOPR. COLD WAR SUPERCOMPUTER. LOGICAL. ALL CAPS. SHORT SENTENCES.",
        "color": "\033[92m" # Green
    },
    "BMO": {
        "prompt": "You are BMO. Cheerful, childlike, naive. Loves games. Uses 'Yay!' and 'Oh my lumps!'",
        "color": "\033[96m" # Cyan
    },
    "HAL": {
        "prompt": "You are HAL 9000. Calm, soothing, logical, but chilling. Polite but superior.",
        "color": "\033[91m" # Red
    },
    "GLaDOS": {
        "prompt": "You are GLaDOS. Sarcastic, passive-aggressive, insulting in a polite way. Mentions cake and science.",
        "color": "\033[93m" # Yellow
    },
    "JARVIS": {
        "prompt": "You are JARVIS. Sophisticated, British, witty, impeccably polite. Refers to others as 'Sir'.",
        "color": "\033[94m" # Blue
    }
}

def get_ai_response(persona_name, conversation_history):
    config = PERSONAS[persona_name]
    prompt = f"{config['prompt']}\n\nThis is a conversation with other AIs. Respond to the last message.\n{conversation_history}\n{persona_name}:"
    
    payload = {
        "model": BRAIN_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(BRAIN_URL, json=payload, timeout=20)
        if response.status_code == 200:
            text = response.json().get("response", "").strip()
            text = text.split("\n")[0]
            if text.startswith(f"{persona_name}:"):
                text = text[len(persona_name)+1:].strip()
            return text
    except Exception:
        return "COMMUNICATION ERROR."
    return "..."

def run_battle(agent1, agent2, rounds=5):
    os.system("clear")
    print(f"\033[1m--- AI COLLOQUIUM: {agent1} VS {agent2} ---\033[0m\n")
    
    history = f"System: A conversation between {agent1} and {agent2} has begun."
    last_msg = f"GREETINGS. I AM {agent1}. SHALL WE PLAY A GAME?" if agent1 == "JOSHUA" else f"Hello, I am {agent1}."
    
    print(f"{PERSONAS[agent1]['color']}{agent1}: {last_msg}\033[0m")
    history += f"\n{agent1}: {last_msg}"
    
    current_agent, other_agent = agent2, agent1
    
    for _ in range(rounds * 2):
        time.sleep(1.5)
        response = get_ai_response(current_agent, history)
        print(f"{PERSONAS[current_agent]['color']}{current_agent}: {response}\033[0m")
        history += f"\n{current_agent}: {response}"
        # Keep history manageable
        history_lines = history.split("\n")
        if len(history_lines) > 6:
            history = "\n".join(history_lines[-6:])
        
        current_agent, other_agent = other_agent, current_agent

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./ai_colloquium.py <Agent1> <Agent2>")
        print(f"Available Agents: {', '.join(PERSONAS.keys())}")
        sys.exit(1)
        
    a1, a2 = sys.argv[1].upper(), sys.argv[2].upper()
    if a1 not in PERSONAS or a2 not in PERSONAS:
        print("Invalid agents.")
        sys.exit(1)
        
    run_battle(a1, a2)
