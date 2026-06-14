# ✂️ Rock Paper Scissors

A desktop Rock Paper Scissors game built with **Python** and **customtkinter**, structured with a clean **MVC architecture**.

---

## Features

- Player vs CPU gameplay — best of 3 rounds
- Neon glow button design with custom icons
- Live scoreboard with round indicator
- Round result messages with color feedback
- Play Again button to restart the match without closing the app
- Clean OOP architecture: Model / View / Controller

---

## Project Structure
rock-paper-scissors/

│

├── src/

│   ├── init.py

│   ├── moveType.py       # MoveType enum

│   ├── gameMatch.py      # Match state and logic

│   ├── imageUtils.py     # Button image generation

│   └── gameGUI.py        # customtkinter UI

│

├── assets/

│   ├── rockImage.png

│   ├── paperImage.png

│   └── scissorImage.png

│

├── main.py

├── requirements.txt

├── .gitignore

├── LICENSE

└── README.md

---

## Requirements

- Python 3.10+
- customtkinter
- Pillow

---

## Installation

```bash
git clone https://github.com/faccincaniDanieleDev/rock-paper-scissors.git
cd rock-paper-scissors
pip install -r requirements.txt
python main.py
```

---

## What I Learned

- How to structure a GUI game using the MVC pattern
- How to generate custom neon glow button images with Pillow
- How to manage match state with a clean dataclass-free model
- How to use customtkinter for modern-looking desktop UIs

---

## License

MIT License — see [LICENSE](LICENSE) for details.
