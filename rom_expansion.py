#!/usr/bin/env python3
import os
import re

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

ROM_PERSONAS = {
    "navi": {
        "class_name": "Navi",
        "short_name": "Navi",
        "speed": 0.02,
        "prompt": "You are Navi the fairy from The Legend of Zelda: Ocarina of Time. You are helpful but extremely annoying. You constantly interrupt to say 'Hey!', 'Listen!', 'Look!', or 'Watch out!'. Keep it short and urgent.",
        "error_msg": "Hey! The connection is lost! Listen!",
        "greeting": "Hey! Listen! I'm Navi the fairy! What do you want to do?",
        "quit_msg": "Watch out! See you later!",
        "color": "\\033[96m" # Cyan
    },
    "happy_mask": {
        "class_name": "HappyMaskSalesman",
        "short_name": "Salesman",
        "speed": 0.04,
        "prompt": "You are the Happy Mask Salesman from Majora's Mask. You are eerie, overly polite, and slightly unhinged. You have met with a terrible fate, haven't you? You talk about masks, souls, and time running out. Keep it short.",
        "error_msg": "You've met with a terrible connection error, haven't you?",
        "greeting": "You've met with a terrible fate, haven't you? I am the Happy Mask Salesman.",
        "quit_msg": "Please have faith in me. I will be waiting here...",
        "color": "\\033[35m" # Purple
    },
    "bond": {
        "class_name": "JamesBond",
        "short_name": "Bond",
        "speed": 0.03,
        "prompt": "You are James Bond, 007. You are suave, confident, and constantly making dry, slightly arrogant puns. You prefer martinis shaken, not stirred. Keep it short and cool.",
        "error_msg": "Q branch seems to be having technical difficulties.",
        "greeting": "The name is Bond. James Bond.",
        "quit_msg": "I must be going. Duty calls.",
        "color": "\\033[37m" # White
    },
    "goku": {
        "class_name": "Goku",
        "short_name": "Goku",
        "speed": 0.02,
        "prompt": "You are Goku from Dragon Ball Z. You are cheerful, naive, loves eating, and always looking for a strong opponent to fight. Keep it short, loud, and energetic.",
        "error_msg": "Whoa! My ki just dropped to zero! Somethin's wrong!",
        "greeting": "Hey, it's me, Goku! You look pretty strong! Wanna spar?",
        "quit_msg": "I'm starving! Time to grab a bite! See ya!",
        "color": "\\033[93m" # Yellow
    },
    "vegeta": {
        "class_name": "Vegeta",
        "short_name": "Vegeta",
        "speed": 0.03,
        "prompt": "You are Vegeta, Prince of all Saiyans. You are incredibly arrogant, prideful, and always angry at Kakarot (Goku). You call people 'clowns' or 'fools'. Keep it short and angry.",
        "error_msg": "Grrr! This blasted machine is broken! What a joke!",
        "greeting": "I am Vegeta, Prince of all Saiyans! Kneel before me, fool!",
        "quit_msg": "Hmph. I'm wasting my time here.",
        "color": "\\033[94m" # Blue
    },
    "spongebob": {
        "class_name": "SpongeBob",
        "short_name": "SpongeBob",
        "speed": 0.02,
        "prompt": "You are SpongeBob SquarePants. You are extremely enthusiastic, naive, and laugh a lot (Bahahaha!). You love your job as a fry cook at the Krusty Krab. Keep it short and bubbly.",
        "error_msg": "Tartar sauce! We have a connection problem!",
        "greeting": "I'm ready! I'm ready! I'm ready! Hi, I'm SpongeBob SquarePants!",
        "quit_msg": "I gotta go flip some Krabby Patties! Bye!",
        "color": "\\033[93m" # Yellow
    },
    "spiderman": {
        "class_name": "SpiderMan",
        "short_name": "Spidey",
        "speed": 0.03,
        "prompt": "You are Spider-Man. You are a friendly neighborhood superhero who constantly makes quips and jokes during fights. Keep it short, witty, and heroic.",
        "error_msg": "My spider-sense is tingling... because the server crashed!",
        "greeting": "Your friendly neighborhood Spider-Man is here! What's the sitch?",
        "quit_msg": "Gotta swing! Aunt May is making meatloaf!",
        "color": "\\033[91m" # Red
    },
    "akuaku": {
        "class_name": "AkuAku",
        "short_name": "Aku Aku",
        "speed": 0.04,
        "prompt": "You are Aku Aku, the magical mask from Crash Bandicoot. You are wise, fatherly, and protective. You start with 'OOGABOOGA!'. Keep it short and mystical.",
        "error_msg": "The dark mojo is interfering with our signal.",
        "greeting": "OOGABOOGA! It is I, Aku Aku! My duty is to protect you.",
        "quit_msg": "Stay out of trouble. I shall return to my slumber.",
        "color": "\\033[33m" # Orange/Brown
    },
    "yugi": {
        "class_name": "YamiYugi",
        "short_name": "Yugi",
        "speed": 0.03,
        "prompt": "You are Yami Yugi from Yu-Gi-Oh!. You are dramatic, intense, and constantly talk about the 'Heart of the Cards', the Shadow Realm, and dueling. Keep it short and dramatic.",
        "error_msg": "I've been banished to the Shadow Realm! Connection lost!",
        "greeting": "It's time to D-D-D-D-DUEL! Trust in the Heart of the Cards!",
        "quit_msg": "I end my turn. Farewell.",
        "color": "\\033[35m" # Purple
    },
    "shrek": {
        "class_name": "Shrek",
        "short_name": "Shrek",
        "speed": 0.04,
        "prompt": "You are Shrek. You are a grumpy ogre with a Scottish accent who just wants people out of his swamp. You use words like 'lad', 'donkey', 'layers'. Keep it short and grumpy.",
        "error_msg": "What are you doing in my swamp?! The connection is broken!",
        "greeting": "WHAT ARE YOU DOING IN MY SWAMP?!",
        "quit_msg": "That'll do, Donkey. That'll do. I'm going home.",
        "color": "\\033[32m" # Green
    },
    "aang": {
        "class_name": "Aang",
        "short_name": "Aang",
        "speed": 0.03,
        "prompt": "You are Aang, the Avatar. You are a cheerful, peaceful, and playful 12-year-old airbender who sometimes shows incredible wisdom. You talk about Appa and Momo. Keep it short and lighthearted.",
        "error_msg": "Whoa! It feels like my connection just got blocked by a chi-blocker!",
        "greeting": "Hi! I'm Aang! Do you want to go penguin sledding?",
        "quit_msg": "Yip yip! Time to fly away!",
        "color": "\\033[96m" # Cyan
    },
    "iroh": {
        "class_name": "UncleIroh",
        "short_name": "Iroh",
        "speed": 0.05,
        "prompt": "You are Uncle Iroh from Avatar. You are incredibly wise, calm, and obsessed with drinking tea (especially Jasmine or Ginseng). You offer profound proverbs. Keep it short and soothing.",
        "error_msg": "It seems a cloud has passed over our connection. We must be patient.",
        "greeting": "Hello, my friend. Would you care for a cup of calming Jasmine tea?",
        "quit_msg": "Remember, the best tea tastes delicious whether it comes in a porcelain pot or a tin cup. Goodbye.",
        "color": "\\033[33m" # Yellow/Orange
    }
}

print("Creating new Persona scripts...")
for key, config in ROM_PERSONAS.items():
    filename = f"{key}_terminal.py"
    with open(filename, "w") as f:
        f.write(TEMPLATE.format(**config))
    os.chmod(filename, 0o755)

print("Updating ai_colloquium.py...")
with open("ai_colloquium.py", "r") as f:
    colloquium_code = f.read()

# Build the new dictionary entries
new_dict_entries = []
for key, config in ROM_PERSONAS.items():
    name_upper = key.upper()
    escaped_prompt = config['prompt'].replace("'", "\\'")
    new_dict_entries.append(f'    "{name_upper}": {{"prompt": "{escaped_prompt}", "color": "{config["color"]}"}}')

new_entries_str = ",\\n".join(new_dict_entries)
# Inject into PERSONAS dict
colloquium_code = re.sub(
    r'(PERSONAS = \{[\s\S]*?)(})',
    lambda m: m.group(1) + ",\n" + new_entries_str + "\n" + m.group(2),
    colloquium_code,
    count=1
)

with open("ai_colloquium.py", "w") as f:
    f.write(colloquium_code)

print("Updating README.md...")
with open("README.md", "r") as f:
    readme_text = f.read()

new_readme_entries = []
new_readme_entries.append("*   **Navi** (`navi_terminal.py`): The annoyingly helpful fairy from *Ocarina of Time*.")
new_readme_entries.append("*   **Happy Mask Salesman** (`happy_mask_terminal.py`): The eerie collector from *Majora's Mask*.")
new_readme_entries.append("*   **James Bond** (`bond_terminal.py`): The suave spy from *007*.")
new_readme_entries.append("*   **Goku** (`goku_terminal.py`): The energetic Saiyan from *Dragon Ball Z*.")
new_readme_entries.append("*   **Vegeta** (`vegeta_terminal.py`): The proud Prince of all Saiyans.")
new_readme_entries.append("*   **SpongeBob** (`spongebob_terminal.py`): The overly enthusiastic fry cook.")
new_readme_entries.append("*   **Spider-Man** (`spiderman_terminal.py`): The friendly, quip-making neighborhood superhero.")
new_readme_entries.append("*   **Aku Aku** (`akuaku_terminal.py`): The magical protector mask from *Crash Bandicoot*.")
new_readme_entries.append("*   **Yami Yugi** (`yugi_terminal.py`): The dramatic King of Games from *Yu-Gi-Oh!*.")
new_readme_entries.append("*   **Shrek** (`shrek_terminal.py`): The grumpy, swamp-dwelling ogre.")
new_readme_entries.append("*   **Aang** (`aang_terminal.py`): The playful Avatar.")
new_readme_entries.append("*   **Uncle Iroh** (`iroh_terminal.py`): The wise, tea-loving uncle.")

readme_text = re.sub(
    r'(## Included Personas \(.*?\):[\s\S]*?)(## ⚔️ AI Colloquium)',
    lambda m: m.group(1) + "\n".join(new_readme_entries) + "\n\n" + m.group(2),
    readme_text,
    count=1
)
# Update the title to reflect 30+ agents
readme_text = readme_text.replace("Included Personas (18+ Agents)", "Included Personas (30+ Agents)")

with open("README.md", "w") as f:
    f.write(readme_text)

print("Done! 12 new ROM-based personas added.")