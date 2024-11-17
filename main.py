# main.py
import tkinter as tk
from controller import Controller

def main():
    root = tk.Tk()
    app = Controller(root)  # Instantiate the Controller which initializes the View and Model
    root.mainloop()

if __name__ == "__main__":
    main()
