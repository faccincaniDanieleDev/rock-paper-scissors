"""main.py — Entry point for the Rock Paper Scissors game."""

from src import GUI


def main() -> None:
    """Creates the window and starts the game loop."""
    window = GUI()
    window.mainloop()


if __name__ == "__main__":
    main()