from tkinter import Tk
from graph import Graph
from train import Train
from snake_game import Game
import tkinter as tk


class StartMenu:
    def __init__(self):
        self.conf_file = "conf.txt"
        self.parameters = {
            "No_Borders": True,
            "Machine_Learning": True
        }
        self.checkboxes = {}
        self.load_config()

    def load_config(self):
        """Load parameters from conf.txt if it exists."""
        try:
            with open(self.conf_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if key in self.parameters:
                        self.parameters[key] = value == "True"
        except FileNotFoundError:
            # Default values are already set
            pass

    def save_config(self):
        """Save parameters to conf.txt."""
        with open(self.conf_file, "w") as f:
            for key, value in self.parameters.items():
                f.write(f"{key}={value}\n")

    def update_parameters(self):
        """Update parameters based on checkbox states."""
        for key, checkbox in self.checkboxes.items():
            self.parameters[key] = checkbox.var.get()  # Retrieve state directly from custom variable

    def start_game(self):
        """Start the game with selected parameters."""
        self.save_config()

        # Retrieve selected parameters
        free_borders = self.parameters["No_Borders"]
        is_ml = self.parameters["Machine_Learning"]

        # Initialize the game components
        root = Tk()
        root.title("Snake Game")
        graph = Graph()
        train = Train()
        game = Game(root, graph, train, is_ml, free_borders)
        game.play()
        root.mainloop()

    def show(self):
        """Display the start menu."""
        root = tk.Tk()
        root.title("Snake Game Start Menu")
        root.geometry("400x300")

        # Add checkboxes for each parameter
        for i, (key, value) in enumerate(self.parameters.items()):
            checkbox_var = tk.BooleanVar(value=value)  # Custom variable to track state
            checkbox = tk.Checkbutton(
                root, text=key.replace("_", " ").title(), variable=checkbox_var
            )
            checkbox.var = checkbox_var  # Attach variable to the checkbox
            checkbox.grid(row=i, column=0, sticky="w")
            self.checkboxes[key] = checkbox

        # Add start button
        tk.Button(root, text="Start Game", command=lambda: self.start_and_close(root)).grid(
            row=len(self.parameters), column=0, pady=10
        )

        root.mainloop()

    def start_and_close(self, menu_root):
        """Close the start menu and start the game."""
        self.update_parameters()  # Update parameters from checkboxes
        menu_root.destroy()  # Close the start menu
        self.start_game()  # Start the game


menu = StartMenu()
menu.show()
