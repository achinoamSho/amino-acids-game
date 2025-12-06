# Amino Acid Classification Quiz

This is a small Python project for practicing basic amino acid properties.

You can play it in two ways:

- A **terminal quiz game** (`amino_acids_game.py`)
- A simple **GUI app** using Tkinter (`amino_acids_gui.py`)

The quiz helps you practice:

- **Charge** - `positive` / `negative` / `neutral`
- **Polarity** - `polar` / `nonpolar`
- **Aromaticity** - `aromatic` / `non-aromatic`
- **Hydrophobicity** - `hydrophobic` / `hydrophilic`

Under the hood, the data and logic are kept in a separate module so both the CLI and GUI use the same core code.

## Project structure

```text
.
├── amino_acids_logic.py   # Core logic and amino acid data (no input/print)
├── amino_acids_game.py    # Terminal (CLI) quiz game + persistent stats
├── amino_acids_gui.py     # Tkinter GUI front-end
├── test_game.py           # Tests for the logic module
├── quiz_stats.json        # Generated at runtime: stored statistics (ignored by git)
├── README.md              # This file
└── .gitignore             # Git ignore rules for the project
```

## Requirements

- **Python 3.10+**
- Standard library only for the game and GUI.
- (Optional) [`pytest`](https://pytest.org/) if you want to run the tests.

To install `pytest`:

```bash
pip install pytest
```

## How to play (terminal version)

Run the CLI game:
```bash
python amino_acids_game.py
```
**1.** Choose a **game mode**:

- `1` Single category (amino acid → property)
- `2` Mixed categories (each question can use a different category)
- `3` Reverse questions (property → amino acid)

**2.** If you chose single category, pick which category to practice (charge / polarity / aromaticity / hydrophobicity).

**3.** Choose how many questions you want (e.g. 5 or 10).

**4.** For each question:

- Read the prompt (e.g. “What is the polarity of Serine (S)?” or “Which amino acid is positively charged?”).
- Answer by typing the **number** of your choice, e.g. 1 or 2.
- Type `q` at any time to quit.

At the end, the game shows:
- Your score for this run.
- Your accuracy for this game.
- Your overall stats (games played, total questions, overall accuracy, best run).

Stats are stored in `quiz_stats.json` in the project folder.

## How to play (GUI version)
Run :
```bash
python amino_acids_gui.py
```
In the window:
**1.** Choose a **mode** at the top:

- Single category
- Mixed categories
- Reverse (property → amino acid)

**2.** For single-category mode, choose the **category** from the dropdown.

**3.** Click **“New question”** to start.

**4.** Answer by clicking one of the numbered buttons.

Your current score and streak are shown at the bottom of the window.

## Running the tests
```bash
pytest
```
The tests focus on the logic in `amino_acids_logic.py`:

- correct properties for specific amino acids
- hydrophobic vs hydrophilic sets
- case-insensitive answer checking

<img src="https://github.com/user-attachments/assets/a2c4619f-ade2-431c-99bf-58ecf90b8961" alt="Amino Acids" width="800">
