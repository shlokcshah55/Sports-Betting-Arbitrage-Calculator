# controller.py
from model import Model
from view import View

#Allows GUI to interact with the model
class Controller:
    def __init__(self, root):
        self.model = Model()  # Create Model instance
        self.view = View(root)  # Create View instance
        sports = self.model.get_sports()
        if not sports:
            self.view.show_popup('API Down')
        else:
            self.view.set_sports(self.model.get_sports())  # Set sports in the view
        self._bind()

    def _bind(self):
        #Setting abstract method in view to the ones in the class
        self.view.set_get_events_clicked(self.load_events)
        self.view.set_submit_clicked(self.calculate_arbitrage)

    def load_events(self):
        selected_sport = self.view.sport_var.get()
        mapping = self.view.sport_map
        events = self.model.get_events(mapping[selected_sport])
        if not events:
            self.view.show_popup('API Down')
        else:
            self.view.set_events(events)

    def calculate_arbitrage(self):
        selected_event = self.view.event_var.get()
        riskType = self.view.get_type_of_bet()
        max_bet = self.view.get_max_to_spend()
        try:
            #Validation to ensure positive number always entered
            max_bet = int(max_bet)
            if max_bet <= 0:
                self.view.show_popup('Please put in a number bigger than 0')
            else:
                result = self.model.calculate_arbitrage(selected_event, riskType, int(max_bet))
                if not result:
                    self.view.show_popup('Arbitrage not possible')
                else:
                    self.view.create_large_popup(result)
                    print(result)
        except ValueError:
            self.view.show_popup('Please enter a valid number for the amount')


