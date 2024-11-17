# view.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#Where GUI displayed
class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Arbitrage Calculator")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")

        # Title label
        self.title_label = tk.Label(root, text="Sports Betting Arbitrage Calculator", font=("Helvetica", 18, "bold"),
                                    bg="#2c3e50", fg="white")
        self.title_label.pack(pady=20)

        self.main_frame = ttk.Frame(root, padding="20 20 20 20")
        self.main_frame.pack(expand=True)

        # Sport selection
        self.sport_label = ttk.Label(self.main_frame, text="Select Sport:", font=("Helvetica", 12))
        self.sport_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.sport_var = tk.StringVar()
        self.sports_menu = ttk.Combobox(self.main_frame, textvariable=self.sport_var, font=("Helvetica", 12), width=30)
        self.sports_menu.grid(row=0, column=1, padx=10, pady=10)

        # Load Events button
        self.load_events_button = ttk.Button(self.main_frame, text="Load Events", command=None)
        self.load_events_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Event selection
        self.event_label = ttk.Label(self.main_frame, text="Select Event:", font=("Helvetica", 12))
        self.event_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.event_var = tk.StringVar()
        self.events_menu = ttk.Combobox(self.main_frame, textvariable=self.event_var, font=("Helvetica", 12), width=30)
        self.events_menu.grid(row=2, column=1, padx=10, pady=10)

        # Maximum Bet Amount
        self.max_bet_label = ttk.Label(self.main_frame, text="Maximum Bet Amount:", font=("Helvetica", 12))
        self.max_bet_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.max_bet_var = tk.StringVar()
        self.max_bet_entry = ttk.Entry(self.main_frame, textvariable=self.max_bet_var, font=("Helvetica", 12), width=30)
        self.max_bet_entry.grid(row=3, column=1, padx=10, pady=10)

        # Radio Buttons for bet type (safe or risky)
        self.bet_type_var = tk.StringVar(value="safe")  # Default value is "safe"
        self.safe_bet_rb = ttk.Radiobutton(self.main_frame, text="Safe Bet", variable=self.bet_type_var, value="safe",
                                           style="TRadiobutton")
        self.safe_bet_rb.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.risky_bet_rb = ttk.Radiobutton(self.main_frame, text="Risky Bet", variable=self.bet_type_var,
                                            value="risky", style="TRadiobutton")
        self.risky_bet_rb.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Submit button
        self.submit_button = ttk.Button(self.main_frame, text="Calculate Arbitrage", command=self.on_submit)
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.on_load_events = None
        self.on_submit = None

        # Add padding and centering
        for widget in self.main_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

    def set_sports(self, sports):
        # Update sports dropdown with sports as a list of (ID, name) tuples
        self.sport_map = sports
        self.sports_menu['values'] = list(self.sport_map.keys())
        self.sports_menu.current(0)

    def set_events(self, events):
        # Update events dropdown with events as a list of (ID, name) tuples
        self.event_map = events
        self.events_menu['values'] = list(self.event_map.keys())
        self.events_menu.current(0)

    def get_selected_sport_id(self):
        return self.sport_map.get(self.sport_var.get(), None)

    def get_selected_event_id(self):
        return self.event_map.get(self.event_var.get(), None)

    def get_type_of_bet(self):
        return self.bet_type_var.get()

    def get_max_to_spend(self):
        return self.max_bet_var.get()

    def set_get_events_clicked(self, command):
        self.load_events_button.config(command=command)

    def set_submit_clicked(self, command):
        self.submit_button.config(command=command)

    def _on_load_events_clicked(self):
        if self.on_load_events:
            self.on_load_events()

        # Placeholder method to be connected to the controller
        pass

    def on_submit(self):
        # Placeholder method to be connected to the controller
        pass

    def show_popup(self, message):
        messagebox.showerror("Error", message)

    def create_large_popup(self, data):
        # Create a new Toplevel window for the popup
        popup = tk.Toplevel(self.root)
        popup.title("Arbitrage Opportunity")

        # Set the size of the popup window (width x height)
        popup.geometry("500x350")
        popup.configure(bg="#2c3e50")  # Dark background for the popup

        # Add a frame to organize the contents
        frame = ttk.Frame(popup, padding="20")
        frame.pack(expand=True, padx=10, pady=10, fill="both")

        # Title label with bold font and better color contrast
        title_label = ttk.Label(frame, text=f"Arb Opportunity found on {data.getEvent()}!", font=("Arial", 16, "bold"),
                                foreground="#E74C3C", background="#2c3e50", wraplength=460)
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Information label for home team betting details
        home_bet_label = ttk.Label(frame,
                                   text=f"Bet {round(data.getHomeAmount(),2)} on {data.getHomeTeam()} to Win on {data.getHomeSite()}. If they win you stand to win {round(data.getProfitHomeWins(),2)}",
                                   font=("Arial", 12), foreground="white", background="#2c3e50", wraplength=460)
        home_bet_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Information label for away team betting details
        away_bet_label = ttk.Label(frame,
                                   text=f"Bet {round(data.getAwayAmount(),2)} on {data.getAwayTeam()} to Win on {data.getAwaySite()}. If they win you stand to win {round(data.getProfitAwayWins(),2)}",
                                   font=("Arial", 12), foreground="white", background="#2c3e50", wraplength=430)
        away_bet_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Informtation label for draw if exists
        if data.getDrawAvailable():
            draw_bet_label = ttk.Label(frame,
                                       text=f"Bet {round(data.getDrawAmount(), 2)} on a draw on {data.getDrawSite()}. If they win you stand to win {round(data.getProfitAwayWins(), 2)}",
                                       font=("Arial", 12), foreground="white", background="#2c3e50", wraplength=430)
            draw_bet_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Close button styled with padding and rounded edges
        close_button = ttk.Button(frame, text="Close", command=popup.destroy, style="TButton")
        close_button.grid(row=4, column=0, padx=10, pady=20)

        # Make sure the popup is centered on the screen
        window_width = 500
        window_height = 350
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        popup.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

        # Make sure the popup stays on top of the main window
        popup.grab_set()
        popup.focus_set()

        # Run the popup event loop
        popup.mainloop()
