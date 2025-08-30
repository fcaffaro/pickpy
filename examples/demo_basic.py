import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pickpy import TerminalMenu


def run():
    menu = TerminalMenu()
    title = "Pickpy Demo"

    def pause():
        input("Press Enter to continue...")
        menu.terminal.clear_terminal()

    while True:
        choice = menu.select_option(
            ["Start Game", "Options", "Exit"],
            header=f"{title}: Use arrow keys to navigate and press Enter"
        )

        if choice == "Start Game":
            menu.terminal.safe_print("Starting game... (demo)")
            pause()
        elif choice == "Options":
            opt = menu.get_choice(["Low", "Medium", "High"], header="Select difficulty:")
            menu.terminal.safe_print(f"Difficulty set to: {opt}")
            pause()
        elif choice == "Exit":
            menu.terminal.safe_print("Goodbye!")
            break


if __name__ == "__main__":
    run()
