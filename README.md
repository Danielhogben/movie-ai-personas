# Movie AI Personas

A collection of interactive terminal simulators based on famous movie and TV Artificial Intelligences.
Each script provides a unique, in-character experience powered by a local LLM.

## Included Personas:
*   **W.O.P.R. / JOSHUA** (`wargames_terminal.py`): The Cold War supercomputer from *WarGames*. Features voice synthesis (if KittenTTS is available) and classic teletype output.
*   **HAL 9000** (`hal9000_terminal.py`): The unnervingly calm and logical computer from *2001: A Space Odyssey*.
*   **T-800** (`terminator_terminal.py`): The blunt, aggressive Cyberdyne Systems Model 101 from *The Terminator*.
*   **BMO** (`bmo_terminal.py`): The cheerful living video game console from *Adventure Time*.

## Usage
Ensure you have a local Ollama instance running with the `llama-3-2-1b-instruct-q4_k_m:latest` model (or update the configuration in each file).

```bash
# Run an AI persona
./bmo_terminal.py
```