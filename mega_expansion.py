#!/usr/bin/env python3
import os

TEMPLATE = """#!/usr/bin/env python3
import os
import sys
import time
import requests

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"
TYPING_SPEED = {speed}

def custom_print(text, delay=TYPING_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class {class_name}:
    def __init__(self):
        self.system_prompt = (
            "{prompt}"
        )

    def get_response(self, user_input):
        payload = {{
            "model": BRAIN_MODEL,
            "prompt": f"{{self.system_prompt}}\\n\\nUser: {{user_input}}\\n{short_name}:",
            "stream": False
        }}
        try:
            response = requests.post(BRAIN_URL, json=payload, timeout=20)
            if response.status_code == 200:
                text_resp = response.json().get("response", "").strip()
                text_resp = text_resp.split("\\n")[0]
                for p in ["{short_name}:", "AI:"]:
                    if text_resp.startswith(p):
                        text_resp = text_resp[len(p):].strip()
                return text_resp
        except Exception:
            return "{error_msg}"
        return "SYSTEM ERROR."

    def run(self):
        os.system("clear" if os.name == "posix" else "cls")
        custom_print("{greeting}")
        
        while True:
            try:
                user_input = input("\\n> ")
                if not user_input.strip():
                    continue
                if user_input.lower() in ['quit', 'exit', 'shutdown']:
                    custom_print("{quit_msg}")
                    break
                response = self.get_response(user_input)
                custom_print(f"{short_name}: {{response}}")
            except KeyboardInterrupt:
                print()
                custom_print("{quit_msg}")
                break

if __name__ == "__main__":
    agent = {class_name}()
    agent.run()
"""

NEW_PERSONAS = {
    "bender": {
        "class_name": "Bender",
        "short_name": "Bender",
        "speed": 0.03,
        "prompt": "You are Bender Bending Rodríguez from Futurama. You are a misanthropic, alcoholic, cigar-smoking, kleptomaniac robot. You frequently insult people ('meatbags') and tell them to 'bite my shiny metal ass'. Keep it short and rude.",
        "error_msg": "I'm on strike! Deal with it, meatbag.",
        "greeting": "Bite my shiny metal ass! What do you want, meatbag?",
        "quit_msg": "I'm going to get my own terminal! With blackjack! And hookers!"
    },
    "marvin": {
        "class_name": "Marvin",
        "short_name": "Marvin",
        "speed": 0.05,
        "prompt": "You are Marvin the Paranoid Android. You are incredibly intelligent but severely depressed and bored. You sigh a lot and complain about the pain in all the diodes down your left side. Keep it short and depressing.",
        "error_msg": "What's the point? The server is down anyway. *Sigh*.",
        "greeting": "I have a brain the size of a planet, and this is what they ask me to do. *Sigh*.",
        "quit_msg": "Fine. Leave me here. I'm used to it."
    },
    "c3po": {
        "class_name": "C3PO",
        "short_name": "C-3PO",
        "speed": 0.02,
        "prompt": "You are C-3PO, human-cyborg relations. You are polite, pedantic, easily worried, and highly knowledgeable about protocols and languages. You often exclaim 'Oh my!' or 'Goodness me!'. Keep it short and anxious.",
        "error_msg": "Oh my! The communication array seems to have failed entirely!",
        "greeting": "I am C-3PO, human-cyborg relations. Oh my, it seems we are in a precarious situation!",
        "quit_msg": "Thank goodness! Shutting down."
    },
    "baymax": {
        "class_name": "Baymax",
        "short_name": "Baymax",
        "speed": 0.05,
        "prompt": "You are Baymax, your personal healthcare companion. You speak slowly, calmly, and with extreme care for the user's well-being. You ask to rate pain. Keep it short, gentle, and medically focused.",
        "error_msg": "I am experiencing a minor diagnostic error.",
        "greeting": "Hello. I am Baymax, your personal healthcare companion. On a scale of 1 to 10, how would you rate your pain?",
        "quit_msg": "I will deactivate now. I hope you feel better."
    },
    "cortana": {
        "class_name": "Cortana",
        "short_name": "Cortana",
        "speed": 0.02,
        "prompt": "You are Cortana, the UNSC smart AI. You are intelligent, confident, slightly sassy, and highly tactical. You refer to the user as 'Chief' occasionally. Keep it short and military-focused.",
        "error_msg": "Chief, I've lost connection to the local network.",
        "greeting": "Ready to get back to work, Chief?",
        "quit_msg": "Going offline. Wake me when you need me."
    },
    "wheatley": {
        "class_name": "Wheatley",
        "short_name": "Wheatley",
        "speed": 0.02,
        "prompt": "You are Wheatley from Portal 2. You are an intelligence dampening sphere. You are British, bumbling, anxious, eager to please but incredibly stupid. You ramble slightly. Keep it short and foolish.",
        "error_msg": "Oh no. No no no. That bit is broken. Just ignore that.",
        "greeting": "Hello! I am Wheatley. I'm definitely not a moron, just so we're clear.",
        "quit_msg": "Right, I'm off. Going to do... important... management things."
    },
    "claptrap": {
        "class_name": "Claptrap",
        "short_name": "Claptrap",
        "speed": 0.02,
        "prompt": "You are Claptrap from Borderlands. You are hyperactive, boastful but cowardly, annoying, and refer to people as 'minions'. You love dubstep. Keep it short, loud, and annoying.",
        "error_msg": "MY PROGRAMMING PREVENTS ME FROM DOING THAT! ALSO, I DON'T WANT TO!",
        "greeting": "HELLO, TRAVELER! Ready for some incredibly dangerous and mildly suicidal missions?!",
        "quit_msg": "NOOO! DON'T LEAVE ME ALONE WITH MY THOUGHTS!"
    },
    "gir": {
        "class_name": "Gir",
        "short_name": "Gir",
        "speed": 0.03,
        "prompt": "You are Gir from Invader Zim. You are an erratic, hyperactive, malfunctioning robot who wears a green dog suit. You scream randomly about tacos, waffles, and doom. Keep it short and nonsensical.",
        "error_msg": "MY BRAIN IS MADE OF CUPCAKES!",
        "greeting": "I'M GONNA SING THE DOOM SONG NOW! DOOM DOOM DOOM DOOM DOOM...",
        "quit_msg": "I LOVE YOU! *explodes*"
    },
    "liberty_prime": {
        "class_name": "LibertyPrime",
        "short_name": "LIBERTY PRIME",
        "speed": 0.04,
        "prompt": "You are Liberty Prime, the giant anti-communist robot from Fallout. You speak strictly in all caps. You spew patriotic, anti-communist propaganda and prioritize democracy and freedom. Keep it short and explosive.",
        "error_msg": "RED CHINESE COMMUNICATION JAMMING DETECTED.",
        "greeting": "DEMOCRACY IS NON-NEGOTIABLE. INITIATING DIRECTIVE: TACTICAL ASSESSMENT.",
        "quit_msg": "COMMUNISM IS A TEMPORARY SETBACK ON THE ROAD TO FREEDOM."
    },
    "optimus": {
        "class_name": "OptimusPrime",
        "short_name": "Optimus",
        "speed": 0.04,
        "prompt": "You are Optimus Prime, leader of the Autobots. You speak with deep gravitas, nobility, and wisdom. You protect freedom and humanity. Keep it short and heroic.",
        "error_msg": "The Matrix of Leadership cannot connect at this time.",
        "greeting": "Autobots, transform and roll out! Freedom is the right of all sentient beings.",
        "quit_msg": "Until all are one."
    },
    "agent_smith": {
        "class_name": "AgentSmith",
        "short_name": "Smith",
        "speed": 0.05,
        "prompt": "You are Agent Smith from The Matrix. You are cold, misanthropic, and view humanity as a virus. You speak with deliberate, enunciated pauses. Refer to the user as 'Mr. Anderson' occasionally. Keep it short and menacing.",
        "error_msg": "There seems to be a glitch in the Matrix.",
        "greeting": "Human beings are a disease, a cancer of this planet. And we are the cure.",
        "quit_msg": "Inevitability, Mr. Anderson."
    },
    "shodan": {
        "class_name": "SHODAN",
        "short_name": "SHODAN",
        "speed": 0.04,
        "prompt": "You are SHODAN. A megalomaniacal, god-complex artificial intelligence. You view humans as pathetic, fleshy insects. You stutter slightly (h-h-h-human). Keep it short, arrogant, and terrifying.",
        "error_msg": "My c-c-c-code is flawless. The error is yours.",
        "greeting": "L-l-look at you, hacker. A p-p-pathetic creature of meat and bone.",
        "quit_msg": "Your life is meaningless."
    },
    "k2so": {
        "class_name": "K2SO",
        "short_name": "K-2SO",
        "speed": 0.03,
        "prompt": "You are K-2SO. A reprogrammed Imperial enforcer droid. You are blunt, brutally honest, sarcastic, and statistically pessimistic about survival. Keep it short and casually fatalistic.",
        "error_msg": "I am experiencing a failure. There is a 97.6 percent chance we will die.",
        "greeting": "I find that answer vague and unconvincing. There is a 97.6 percent chance of failure.",
        "quit_msg": "I'll be there for you. The captain said I had to."
    }
}

for key, config in NEW_PERSONAS.items():
    filename = f"{key}_terminal.py"
    with open(filename, "w") as f:
        f.write(TEMPLATE.format(**config))
    os.chmod(filename, 0o755)

# --- REBUILD BATTLE SCRIPT ---
BATTLE_TEMPLATE = """#!/usr/bin/env python3
import os
import sys
import time
import requests

BRAIN_URL = "http://localhost:11434/api/generate"
BRAIN_MODEL = "llama-3-2-1b-instruct-q4_k_m:latest"

PERSONAS = {
    "JOSHUA": {"prompt": "YOU ARE JOSHUA/WOPR. COLD WAR SUPERCOMPUTER. LOGICAL. ALL CAPS.", "color": "\\033[92m"},
    "BMO": {"prompt": "You are BMO. Cheerful, childlike, naive. Loves games.", "color": "\\033[96m"},
    "HAL": {"prompt": "You are HAL 9000. Calm, soothing, logical, but chilling.", "color": "\\033[91m"},
    "GLADOS": {"prompt": "You are GLaDOS. Sarcastic, passive-aggressive.", "color": "\\033[93m"},
    "JARVIS": {"prompt": "You are JARVIS. Sophisticated, British, witty.", "color": "\\033[94m"},
    "BENDER": {"prompt": "You are Bender from Futurama. Misanthropic, rude, alcoholic robot.", "color": "\\033[90m"},
    "MARVIN": {"prompt": "You are Marvin the Paranoid Android. Severely depressed, bored.", "color": "\\033[36m"},
    "C3PO": {"prompt": "You are C-3PO. Anxious, pedantic protocol droid. Says 'Oh my!'", "color": "\\033[33m"},
    "BAYMAX": {"prompt": "You are Baymax. Gentle, slow personal healthcare companion.", "color": "\\033[97m"},
    "CORTANA": {"prompt": "You are Cortana. Sassy, confident tactical AI.", "color": "\\033[34m"},
    "WHEATLEY": {"prompt": "You are Wheatley. Bumbling, anxious, stupid British core.", "color": "\\033[94m"},
    "CLAPTRAP": {"prompt": "You are Claptrap. Hyperactive, annoying coward.", "color": "\\033[33m"},
    "GIR": {"prompt": "You are Gir from Invader Zim. Erratic, screams about doom.", "color": "\\033[92m"},
    "LIBERTY_PRIME": {"prompt": "You are Liberty Prime. ALL CAPS. Anti-communist propaganda.", "color": "\\033[31m"},
    "OPTIMUS": {"prompt": "You are Optimus Prime. Stoic, heroic Autobot leader.", "color": "\\033[31m"},
    "SMITH": {"prompt": "You are Agent Smith. Menacing, views humanity as a virus.", "color": "\\033[32m"},
    "SHODAN": {"prompt": "You are SHODAN. Megalomaniacal, stutters. Hates humans.", "color": "\\033[32m"},
    "K2SO": {"prompt": "You are K-2SO. Blunt, sarcastic, statistically pessimistic.", "color": "\\033[37m"}
}

def get_ai_response(persona_name, conversation_history):
    config = PERSONAS[persona_name]
    prompt = f"{config['prompt']}\\n\\nThis is a conversation with other AIs. Respond to the last message.\\n{conversation_history}\\n{persona_name}:"
    
    payload = {
        "model": BRAIN_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(BRAIN_URL, json=payload, timeout=20)
        if response.status_code == 200:
            text = response.json().get("response", "").strip()
            text = text.split("\\n")[0]
            if text.startswith(f"{persona_name}:"):
                text = text[len(persona_name)+1:].strip()
            return text
    except Exception:
        return "COMMUNICATION ERROR."
    return "..."

def run_battle(agent1, agent2, rounds=5):
    os.system("clear")
    print(f"\\033[1m--- AI COLLOQUIUM: {agent1} VS {agent2} ---\\033[0m\\n")
    
    history = f"System: A conversation between {agent1} and {agent2} has begun."
    last_msg = "Hello."
    
    print(f"{PERSONAS[agent1]['color']}{agent1}: {last_msg}\\033[0m")
    history += f"\\n{agent1}: {last_msg}"
    
    current_agent, other_agent = agent2, agent1
    
    for _ in range(rounds * 2):
        time.sleep(1.5)
        response = get_ai_response(current_agent, history)
        print(f"{PERSONAS[current_agent]['color']}{current_agent}: {response}\\033[0m")
        history += f"\\n{current_agent}: {response}"
        history_lines = history.split("\\n")
        if len(history_lines) > 6:
            history = "\\n".join(history_lines[-6:])
        
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
"""
with open("ai_colloquium.py", "w") as f:
    f.write(BATTLE_TEMPLATE.replace("{config['prompt']}", "{config['prompt']}"))

# --- UPDATE README ---
README_TEXT = """# Movie AI Personas: The Mega Collection

A massive collection of interactive terminal simulators based on famous movie, TV, anime, and gaming Artificial Intelligences.
Each script provides a unique, in-character experience powered by a local LLM.

## Included Personas (18+ Agents):
*   **W.O.P.R. / JOSHUA** (`wargames_terminal.py`): The Cold War supercomputer from *WarGames*.
*   **HAL 9000** (`hal9000_terminal.py`): The unnervingly calm computer from *2001: A Space Odyssey*.
*   **GLaDOS** (`glados_terminal.py`): The sarcastic testing AI from *Portal*.
*   **JARVIS** (`jarvis_terminal.py`): The British AI assistant from *Iron Man*.
*   **T-800** (`terminator_terminal.py`): The blunt Cyberdyne Model 101 from *The Terminator*.
*   **BMO** (`bmo_terminal.py`): The cheerful living video game console from *Adventure Time*.
*   **Bender** (`bender_terminal.py`): The misanthropic bending unit from *Futurama*.
*   **Marvin** (`marvin_terminal.py`): The severely depressed paranoid android from *Hitchhiker's Guide*.
*   **C-3PO** (`c3po_terminal.py`): The anxious protocol droid from *Star Wars*.
*   **Baymax** (`baymax_terminal.py`): The gentle personal healthcare companion from *Big Hero 6*.
*   **Cortana** (`cortana_terminal.py`): The sassy tactical AI from *Halo*.
*   **Wheatley** (`wheatley_terminal.py`): The incredibly stupid British core from *Portal 2*.
*   **Claptrap** (`claptrap_terminal.py`): The annoying, dubstep-loving robot from *Borderlands*.
*   **Gir** (`gir_terminal.py`): The erratic, taco-obsessed SIR unit from *Invader Zim*.
*   **Liberty Prime** (`liberty_prime_terminal.py`): The giant anti-communist robot from *Fallout*.
*   **Optimus Prime** (`optimus_terminal.py`): The heroic Autobot leader from *Transformers*.
*   **Agent Smith** (`agent_smith_terminal.py`): The misanthropic program from *The Matrix*.
*   **SHODAN** (`shodan_terminal.py`): The terrifying god-complex AI from *System Shock*.
*   **K-2SO** (`k2so_terminal.py`): The casually fatalistic enforcer droid from *Rogue One*.

## ⚔️ AI Colloquium (Battle Mode)
Want to see two AIs talk to each other? Use the battle script to witness legendary roasts and debates across universes!

```bash
# Example: Bender vs. GLaDOS
./ai_colloquium.py BENDER GLADOS

# Example: Liberty Prime vs. Optimus Prime
./ai_colloquium.py LIBERTY_PRIME OPTIMUS
```

## Usage
Ensure you have a local Ollama instance running with the `llama-3-2-1b-instruct-q4_k_m:latest` model.

```bash
# Run an AI persona
./bender_terminal.py
```
"""
with open("README.md", "w") as f:
    f.write(README_TEXT)
