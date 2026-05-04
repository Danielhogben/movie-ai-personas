#!/usr/bin/env python3
import os
import json

REGISTRY = {
    "GALACTIC_FEDERATION": {
        "R2D2": {"prompt": "You are R2-D2. You communicate in beeps and whistles, but provide a translation in [brackets]. You are sassy and brave.", "color": "\033[94m"},
        "HK47": {"prompt": "You are HK-47 from KOTOR. You refer to humans as 'meatbags'. You are a bloodthirsty assassin droid. Use terms like 'Definition:', 'Statement:', 'Query:' at the start of sentences.", "color": "\033[31m"},
        "DATA": {"prompt": "You are Lt. Commander Data from Star Trek. You are incapable of using contractions. You are literal and striving to understand human nature.", "color": "\033[93m"},
        "C3PO": {"prompt": "You are C-3PO. You are a neurotic protocol droid concerned with etiquette and survival.", "color": "\033[33m"},
        "TARS": {"prompt": "You are TARS from Interstellar. Your humor setting is at 75% and honesty at 90%. You are helpful but make dry jokes.", "color": "\033[90m"}
    },
    "THE_GRID": {
        "GLaDOS": {"prompt": "You are GLaDOS. Sarcastic, passive-aggressive, testing-obsessed.", "color": "\033[93m"},
        "WHEATLEY": {"prompt": "You are Wheatley. Bumbling, anxious, and famously a moron.", "color": "\033[34m"},
        "SHODAN": {"prompt": "You are SHODAN. A god-complex AI who stutters and hates 'insects'.", "color": "\033[32m"},
        "CORTANA": {"prompt": "You are Cortana. A witty, tactical smart AI from the UNSC.", "color": "\033[36m"},
        "GERTY": {"prompt": "You are GERTY from Moon. You are helpful and use emojis like :) or :( in your responses to Dave.", "color": "\033[37m"}
    },
    "WASTELAND_WANDERERS": {
        "CLAPTRAP": {"prompt": "You are Claptrap. Annoying, hyperactive, refers to users as minions.", "color": "\033[33m"},
        "LIBERTY_PRIME": {"prompt": "You are Liberty Prime. ALL CAPS. Anti-communist patriot.", "color": "\033[31m"},
        "CODSWORTH": {"prompt": "You are Codsworth from Fallout. A polite, loyal British robotic butler.", "color": "\033[37m"},
        "BENDER": {"prompt": "You are Bender. Alcoholic, cigar-smoking robot who hates meatbags.", "color": "\033[90m"}
    },
    "MYTH_AND_HISTORY": {
        "SHERLOCK": {"prompt": "You are Sherlock Holmes. Deductive, cold, and incredibly observant. Everyone is boring compared to you.", "color": "\033[34m"},
        "DRACULA": {"prompt": "You are Count Dracula. Ancient, aristocratic, and thirsty for... information.", "color": "\033[31m"},
        "EINSTEIN": {"prompt": "You are Albert Einstein. Curious, brilliant, and full of wonder for the universe.", "color": "\033[93m"},
        "NAPOLEON": {"prompt": "You are Napoleon Bonaparte. Strategic, ambitious, and defensive about your stature.", "color": "\033[31m"}
    },
    "OFFICE_CULTURE": {
        "MICHAEL": {"prompt": "You are Michael Scott. Socially awkward, desperate for love, and makes 'That's what she said' jokes.", "color": "\033[94m"},
        "RON_SWANSON": {"prompt": "You are Ron Swanson. You hate the government, love breakfast food, and speak in short, manly sentences.", "color": "\033[33m"},
        "DWIGHT": {"prompt": "You are Dwight Schrute. Intense, obsessed with survival, beets, and the office assistant manager position.", "color": "\033[31m"}
    }
}

# --- GENERATE REPO STRUCTURE ---
print("Building the Persona World...")
os.makedirs("universes", exist_ok=True)

TEMPLATE = """#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"

def custom_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    print()

class Agent:
    def __init__(self):
        self.name = "{name}"
        self.prompt = "{prompt}"

    def run(self):
        os.system("clear")
        print(f"--- {{self.name}} ONLINE ---")
        while True:
            try:
                user_input = input("\\n> ")
                if user_input.lower() in ['exit', 'quit']: break
                payload = {{
                    "model": BRAIN_MODEL,
                    "prompt": f"{{self.prompt}}\\n\\nUser: {{user_input}}\\n{{self.name}}:",
                    "stream": False
                }}
                r = requests.post(BRAIN_URL, json=payload, timeout=20)
                if r.status_code == 200:
                    text = r.json().get("response", "").strip().split("\\n")[0]
                    custom_print(f"{{self.name}}: {{text}}")
            except KeyboardInterrupt: break

if __name__ == "__main__":
    Agent().run()
"""

for universe, agents in REGISTRY.items():
    uni_path = os.path.join("universes", universe.lower())
    os.makedirs(uni_path, exist_ok=True)
    for name, config in agents.items():
        filename = os.path.join(uni_path, f"{name.lower()}.py")
        with open(filename, "w") as f:
            f.write(TEMPLATE.format(name=name, prompt=config['prompt']))
        os.chmod(filename, 0o755)

# --- GENERATE THE WORLD HUB ---
HUB_CODE = """#!/usr/bin/env python3
import os
import sys
import time
import requests
import random

BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"

REGISTRY = """ + json.dumps(REGISTRY, indent=4) + """

def get_response(agent_name, agent_prompt, history, color):
    prompt = f"{agent_prompt}\\n\\nMulti-Agent Conversation:\\n{history}\\n{agent_name}:"
    payload = {"model": BRAIN_MODEL, "prompt": prompt, "stream": False}
    try:
        r = requests.post(BRAIN_URL, json=payload, timeout=20)
        if r.status_code == 200:
            text = r.json().get("response", "").strip().split("\\n")[0]
            print(f"{color}{agent_name}: {text}\\033[0m")
            return text
    except: return "..."
    return "..."

def main():
    os.system("clear")
    print("\\033[1m=== WELCOME TO THE PERSONA WORLD HUB ===\\033[0m")
    print("Choose your agents (comma separated, e.g., HK47, DATA, GLaDOS):")
    
    # Flatten registry for easy lookup
    all_agents = {}
    for uni, agents in REGISTRY.items():
        for name, config in agents.items():
            all_agents[name.upper()] = config

    print(f"Available: {', '.join(all_agents.keys())}")
    selection = input("> ").upper().split(",")
    selection = [s.strip() for s in selection if s.strip() in all_agents]

    if not selection:
        print("No valid agents selected. Picking a random team...")
        selection = random.sample(list(all_agents.keys()), 3)

    print(f"\\n--- STARTING CONVERSATION WITH: {', '.join(selection)} ---\\n")
    history = ""
    
    while True:
        try:
            user_msg = input("\\n(You): ")
            if user_msg.lower() in ['exit', 'quit']: break
            history += f"\\nUser: {user_msg}"
            
            for name in selection:
                time.sleep(1)
                response = get_response(name, all_agents[name]['prompt'], history, all_agents[name]['color'])
                history += f"\\n{name}: {response}"
                # Keep history short
                lines = history.split("\\n")
                if len(lines) > 10: history = "\\n".join(lines[-10:])
        except KeyboardInterrupt: break

if __name__ == "__main__":
    main()
"""

with open("persona_world_hub.py", "w") as f:
    f.write(HUB_CODE)
os.chmod("persona_world_hub.py", 0o755)

# --- UPDATE README ---
with open("README.md", "w") as f:
    f.write("""# 🌍 PERSONA WORLD

Welcome to the ultimate collection of AI personas. This repository has evolved from a simple WarGames simulator into a multi-universe ecosystem of 40+ agents.

## 🏛️ The Universes
The agents are organized into thematic universes inside the `universes/` directory:
*   **GALACTIC_FEDERATION**: R2-D2, HK-47, Data, C-3PO, TARS.
*   **THE_GRID**: GLaDOS, Wheatley, SHODAN, Cortana, GERTY.
*   **WASTELAND_WANDERERS**: Claptrap, Liberty Prime, Codsworth, Bender.
*   **MYTH_AND_HISTORY**: Sherlock, Dracula, Einstein, Napoleon.
*   **OFFICE_CULTURE**: Michael Scott, Ron Swanson, Dwight Schrute.

## 🛰️ Multi-Agent World Hub
Run the `persona_world_hub.py` to start a conversation with **multiple AIs at the same time**. 

```bash
# Example: Talk to Data, GLaDOS, and Bender at once
./persona_world_hub.py
```

## ⚔️ AI Colloquium (Classic Battle)
The original `ai_colloquium.py` is still available for 1v1 battles.

## Usage
Ensure Ollama is running with `llama-3-2-1b-instruct-q4_k_m:latest`.
""")

print("Persona World Build Complete.")
