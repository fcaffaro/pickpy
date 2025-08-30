from pickpy.menu import TerminalMenu
from pickpy.terminal import BColors

menu = TerminalMenu()

# Interactive menu with custom colors
choice = menu.select_option(
    ["Start", "Options", "Exit"],
    header="Custom Colors Demo",
    header_color=BColors.OKBLUE,
    selected_color=BColors.WARNING,
    unselected_color=BColors.OKGREEN,
)

# Fallback (non-TTY) also supports custom colors via get_choice
choice = menu.get_choice(
    ["Red", "Green", "Blue"],
    header="Pick a color:",
    header_color=BColors.WARNING,
    option_color=BColors.OKGREEN,
)

# Customize input prompt color
match choice:
    case "Red":
        menu.terminal.safe_print("You picked Red!", color=BColors.FAIL)
    case "Green":
        menu.terminal.safe_print("You picked Green!", color=BColors.OKGREEN)
    case "Blue":
        menu.terminal.safe_print("You picked Blue!", color=BColors.OKBLUE)
