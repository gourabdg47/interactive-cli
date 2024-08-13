from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal
import questionary
from datetime import datetime

console = Console()

def main_menu():
    console.print(Panel(Text("Welcome to the Modern CLI", justify="center", style="bold magenta")))

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
        console.print(Panel("Settings: Configure your preferences", title="Settings", style="bold yellow"))
    elif choice == options[2]:
        console.print(Panel("Process: The process has started", title="Process", style="bold blue"))
    elif choice == options[3]:
        console.print(Panel("Donate $$$ for this app development!", title="Exit", style="bold red"))
    elif choice == options[4]:
        console.print(Panel("Exiting the application. Goodbye!", title="Exit", style="bold red"))
        exit()

def write_journal():
    console.print(Panel("Journal Entry", title="Write Your Journal", style="bold green"))

    session = PromptSession()
    bindings = KeyBindings()

    journal_entry = []

    @bindings.add('c-s') # TODO: This 'ctrl + s' shit is not working 
    def save_journal(event):
        run_in_terminal(lambda: save_and_ask(journal_entry))
        event.app.exit()


    console.print("[bold yellow]Type your journal entry below. Press Ctrl + S or type 'save-me' to save.[/bold yellow]")
    console.print("[bold red]Press Ctrl + C to cancel and return to the main menu.[/bold red]")

    while True:
        try:
            line = session.prompt("> ", key_bindings=bindings)

            if line and line.lower() == "save-me":
                save_and_ask(journal_entry)
                ask_return_to_menu()
                break
            journal_entry.append(line)

        except KeyboardInterrupt:
            console.print(Panel("Exiting journal entry mode.", style="bold red"))
            ask_return_to_menu()
            break
        except Exception as e:
            console.print(Panel(f"ERROR:  {e}", style="bold red"))
            ask_return_to_menu()
            break

def save_and_ask(journal_entry):
    entry = '\n'.join(journal_entry)
    if entry:
        save_journal_to_file(entry)
        console.print(Panel("Your journal entry has been saved.", style="bold green"))
        ask_return_to_menu()
    else:
        console.print(Panel("No entry was written.", style="bold red"))

def save_journal_to_file(entry):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"journal_{timestamp}.txt"
    with open(filename, "w") as file:
        file.write(entry)
    console.print(f"Journal saved as [bold yellow]{filename}[/bold yellow]")

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
