from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.key_binding import KeyBindings
import questionary
from datetime import datetime
import logging
import os

'''
%Y-%m-%d: Year-Month-Day (e.g., 2024-08-15).
%H:%M:%S: Hour:Minute
(e.g., 14:30:45).
%A: Full weekday name (e.g., Thursday).
'''

###### folder init:
# Check and create required folders
init_folders = [
    'logs', 
    'journals'
]

# Ensure required directories exist
LOG_DIRECTORY = 'logs'
JOURNAL_DIRECTORY = 'journals'

for directory in [LOG_DIRECTORY, JOURNAL_DIRECTORY]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Initialize logging with different handlers for INFO and ERROR levels
info_handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, 'app_info.log'))
error_handler = logging.FileHandler(os.path.join(LOG_DIRECTORY, 'app_error.log'))

info_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
    datefmt='%Y-%m-%d %H:%M:%S %A'
)

info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all logs

logger.addHandler(info_handler)
logger.addHandler(error_handler)

console = Console()
bindings = KeyBindings()

PROMPT_FLAG = False

def time_info():
    from datetime import datetime

    # Get the current date, day, and time
    now = datetime.now()

    date_str = now.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
    day_str = now.strftime("%A")          # Full weekday name (e.g., Monday)
    time_str = now.strftime("%H-%M-%S")   # Format: HH-MM-SS

    return date_str, day_str, time_str

def app_init():
    
    os.system('cls' if os.name == 'nt' else 'clear') # Clearing screen
    console.print(Panel(Text("Welcome to the Modern CLI", justify="center", style="bold magenta"))) # Welcome message



def main_menu():
    
    app_init()

    options = [
        "Option 1: Write Journal",
        "Option 2: Configure Settings",
        "Option 3: Start Process",
        "Option 4: Donate to the dev",
        "Option 5: Exit"
    ]

    choice = questionary.select(
        "Choose an action:",
        choices=options,
        style=questionary.Style([
            ('qmark', 'fg:#E91E63 bold'),
            ('question', 'fg:#673AB7 bold'),
            ('answer', 'fg:#2196F3 bold'),
            ('pointer', 'fg:#03A9F4 bold'),
            ('highlighted', 'fg:#03A9F4 bold'),
            ('selected', 'fg:#4CAF50 bold'),
            ('separator', 'fg:#E0E0E0'),
            ('instruction', 'fg:#9E9E9E'),
            ('text', 'fg:#FFFFFF'),
            ('disabled', 'fg:#757575 italic')
        ])
    ).ask()

    if choice == options[0]:
        write_journal()
    elif choice == options[1]:
        configure_settings()
    elif choice == options[2]:
        start_process()
    elif choice == options[3]:
        donate()
    elif choice == options[4]:
        exit_app()

def configure_settings():
    console.print(Panel("Settings: Configure your preferences", title="Settings", style="bold yellow"))
    # Implement settings logic

def start_process():
    console.print(Panel("Process: The process has started", title="Process", style="bold blue"))
    # Implement process logic

def donate():
    console.print(Panel("Donate $$$ for this app development!", title="Donate", style="bold red"))
    # Implement donation logic

def exit_app():
    console.print(Panel("Exiting the application. Goodbye!", title="Exit", style="bold red"))
    os.system('cls' if os.name == 'nt' else 'clear')
    exit()

def write_journal():
    console.print(Panel("Journal Entry", title="Write Your Journal", style="bold green"))

    session = PromptSession()

    journal_entry = []
    line_number = 1
    global PROMPT_FLAG
    PROMPT_FLAG = False

    console.print("[bold yellow]Type your journal entry below. Press Ctrl + S to save automatically.[/bold yellow]")
    console.print("[bold red]Press Ctrl + C to cancel and return to the main menu.[/bold red]")

    @bindings.add('c-s')
    def save_journal(event):
        global PROMPT_FLAG
        save_and_ask(journal_entry)
        console.print("[bold green]Press ENTER to return to main menu.[/bold green]")
        # event.app.exit()
        PROMPT_FLAG = True

    while not PROMPT_FLAG:
        try:
            prompt_text = f"{line_number}: "
            line = session.prompt(prompt_text, key_bindings=bindings)

            if line and line.lower() == "save-me":
                logging.info("User requested to save journal entry.")
                save_and_ask(journal_entry)
                ask_return_to_menu()
                break

            if line:
                journal_entry.append(line)
                logging.debug(f"Appended line {line_number} to journal entry: {line}")
                line_number += 1

        except KeyboardInterrupt:
            console.print(Panel("Exiting journal entry mode.", style="bold red"))
            logging.warning("User exited journal entry mode with KeyboardInterrupt.")
            ask_return_to_menu()
            break

        except Exception as e:
            console.print(Panel(f"ERROR: {e}", style="bold red"))
            logging.error(f"An error occurred: {e}", exc_info=True)
            ask_return_to_menu()
            break

def save_and_ask(journal_entry):
    try:
        sanitized_entries = [entry if entry is not None else '' for entry in journal_entry]
        entry = '\n'.join(sanitized_entries)

        save_journal_to_file(entry)
        # console.print("Journal entry saved.", style="bold green")
        logging.info("Journal entry successfully saved.")

    except Exception as e:
        console.print(Panel(f"ERROR saving journal: {e}", style="bold red"))
        logging.error(f"An error occurred while saving the journal: {e}", exc_info=True)

def save_journal_to_file(entry):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"journals/journal_{timestamp}.txt"

    with open(filename, "w") as file:
        file.write(entry)
        file.close()

    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(f"Journal saved as [bold yellow]{filename}[/bold yellow]")
    logging.info(f"Journal saved as {filename}")

def ask_return_to_menu():
    
    return_to_menu = questionary.confirm("Would you like to return to the main menu?").ask()
    if return_to_menu:
        main_menu()
    else:
        new_entry = questionary.confirm("Would you like to enter a new journal entry?").ask()
        if new_entry:
            write_journal()
        else:
            ask_return_to_menu()

if __name__ == "__main__":
    while True:
        main_menu()
