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
        try:
            with open(self.conf_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if key in self.parameters:
                        self.parameters[key] = value == "True"
        except FileNotFoundError:
            pass

    def save_config(self):
        with open(self.conf_file, "w") as f:
            for key, value in self.parameters.items():
                f.write(f"{key}={value}\n")

    def update_parameters(self):
        for key, checkbox in self.checkboxes.items():
            self.parameters[key] = checkbox.var.get()

    def start_game(self):
        self.save_config()

        free_borders = self.parameters["No_Borders"]
        is_ml = self.parameters["Machine_Learning"]

        root = Tk()
        root.title("Snake Game")
        graph = Graph()
        train = Train()
        game = Game(root, graph, train, is_ml, free_borders)
        game.play()
        root.mainloop()

    def show(self):
        root = tk.Tk()
        root.title("Snake Game Start Menu")
        root.geometry("400x300")

        for i, (key, value) in enumerate(self.parameters.items()):
            checkbox_var = tk.BooleanVar(value=value)
            checkbox = tk.Checkbutton(
                root, text=key.replace("_", " ").title(), variable=checkbox_var
            )
            checkbox.var = checkbox_var 
            checkbox.grid(row=i, column=0, sticky="w")
            self.checkboxes[key] = checkbox

        tk.Button(root, text="Start Game", command=lambda: self.start_and_close(root)).grid(
            row=len(self.parameters), column=0, pady=10
        )

        root.mainloop()

    def start_and_close(self, menu_root):
        self.update_parameters()
        menu_root.destroy()
        self.start_game()  


menu = StartMenu()
menu.show()
