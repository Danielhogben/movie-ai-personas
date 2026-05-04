# Movie AI Personas

A collection of interactive terminal simulators based on famous movie and TV Artificial Intelligences.
Each script provides a unique, in-character experience powered by a local LLM.

## Included Personas:
*   **W.O.P.R. / JOSHUA** (`wargames_terminal.py`): The Cold War supercomputer from *WarGames*.
*   **HAL 9000** (`hal9000_terminal.py`): The unnervingly calm and logical computer from *2001: A Space Odyssey*.
*   **GLaDOS** (`glados_terminal.py`): The passive-aggressive, sarcastic testing AI from *Portal*.
*   **JARVIS** (`jarvis_terminal.py`): The sophisticated, British AI assistant from *Iron Man*.
*   **T-800** (`terminator_terminal.py`): The blunt, aggressive Cyberdyne Systems Model 101 from *The Terminator*.
*   **BMO** (`bmo_terminal.py`): The cheerful living video game console from *Adventure Time*.

## ⚔️ AI Colloquium (Battle Mode)
Want to see two AIs talk to each other? Use the battle script to witness legendary roasts and debates.

```bash
# Example: GLaDOS vs. HAL 9000
./ai_colloquium.py glados hal
```

## Usage
Ensure you have a local Ollama instance running with the `llama-3-2-1b-instruct-q4_k_m:latest` model (or update the configuration in each file).

```bash
# Run an AI persona
./glados_terminal.py
```