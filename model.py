# model.py
import requests
import numpy as np

#Where all data is managed and logic of application occurs
class Model:
    def __init__(self):
        #Initalise private attributes to access API
        self.__base_url = 'https://api.the-odds-api.com'
        self.__apiKey = '6ebc0d5da4dc608ac306bf5a99dbe8cf'

    #Get all upcoming sports with an event
    def get_sports(self):
        url = f'{self.__base_url}/v4/sports/?apiKey={self.__apiKey}'
        data = self.sendRequest(url)
        if not data:
            return False
        else:
            sports = {f"{item['group']}: {item['title']}" : item['key'] for item in data}
            return sports

    #Get all corresponding events for a sport
    def get_events(self, sport):
        url = f'{self.__base_url}/v4/sports/{sport}/odds/?apiKey={self.__apiKey}&regions=uk&markets=h2h'
        data = self.sendRequest(url)
        if not data:
            return False
        else:
            events_for_view = {f"{item['sport_title']}: {item['home_team']} vs {item['away_team']}": item['id'] for item in data}
            self.events_data = {f"{item['sport_title']}: {item['home_team']} vs {item['away_team']}": item for item in data}
            events_for_view['Example 3 event'] = 'example 1'
            events_for_view['Example 2 event'] = 'example 2'
            return events_for_view

    def calculate_arbitrage(self, event, type, amount):
        # If there are no real-time odds where arb is possible and checking 3-event works
        if event == 'Example 3 event':
            self.set_values_for_3_event_example(event, type, amount)

        # If there are no real-time odds where arb is possible and checking 2-event works
        elif event == 'Example 2 event':
            self.set_values_for_2_event_example(event, type, amount)
        else:
            self.amount = amount
            # Use API to get all odds with associated betting site for this event
            self.getOddsWithBettingSite(event)
            #Checking if Arb is even possible
            if not self.checkArbitragePossible():
                return False
            #Choosing Simplex Tableu set up according to which strategy and number of possible outcomes
            else:
                if type == 'safe':
                    if self.noPossibleResults == 2:
                        self.initial_tableu_safe_two_outcome()
                    elif self.noPossibleResults == 3:
                        self.initial_tableu_safe_three_outcome()
                elif type == 'risky':
                    if self.noPossibleResults == 2:
                        self.initial_tableu_risky_two_outcome()
                    elif self.noPossibleResults == 3:
                        self.initial_tableu_risky_three_outcome()

        #Initalising the Result depending on if 3 outcome or not
        drawAvailable = True
        if self.noPossibleResults == 2:
            self.drawBetOdds = None
            self.moneyOnDraw = None
            self.drawBetSite = None
            drawAvailable = False
        result = Result(self.event_name, drawAvailable,
                        self.homeTeam, self.homeBetOdds, self.moneyOnHome, self.homeBetSite,
                        self.awayTeam, self.awayBetOdds, self.moneyOnAway, self.awayBetSite,
                        self.drawBetOdds, self.moneyOnDraw, self.drawBetSite)

        return result

    #Setting all attributes required for arb calculation manually (3-event)
    def set_values_for_3_event_example(self, event, type, amount):
        self.event_name = event
        self.homeTeam = 'Chelsea'
        self.homeBetOdds = 2.8
        self.homeBetSite = 'PaddyPower'
        self.awayTeam = 'Arsenal'
        self.awayBetOdds = 3.2
        self.awayBetSite = 'William Hill'
        self.drawBetOdds = 3.4
        self.drawBetSite = 'Coral'
        self.noPossibleResults = 3
        self.amount = amount
        if type == 'safe':
            self.initial_tableu_safe_three_outcome()
        elif type == 'risky':
            self.meanHomeProbability = 0.33
            self.meanAwayProbability = 0.33
            self.meanDrawProbability = 0.33
            self.initial_tableu_risky_three_outcome()

    #Setting all attributes required for arb calculation manually (2-event)
    def set_values_for_2_event_example(self, event, type, amount):
        self.event_name = event
        self.homeTeam = 'Cheslea'
        self.homeBetOdds = 2
        self.homeBetSite = 'PaddyPower'
        self.awayTeam = 'Arsenal'
        self.awayBetOdds = 2.5
        self.awayBetSite = 'William Hill'
        self.amount = amount
        self.noPossibleResults = 2
        if type == 'safe':
            self.initial_tableu_safe_two_outcome()
        elif type == 'risky':
            self.meanHomeProbability = 0.35
            self.meanAwayProbability = 0.65
            self.initial_tableu_risky_two_outcome()


    def initial_tableu_risky_two_outcome(self):
        """
        Risky Maximization Function for Arbitrage Betting

        The maximization function in the simplex method is designed to optimize the expected return,
        which is calculated as the product of the calculated probabilities of each event
        (using the scaled mean probability from all the betting sites scraped) and the respective return.

        Why it is Risky Explanation:
        - The maximization skews towards the more likely event, resulting in higher amounts being placed on it.
        - If the less likely event occurs, the profit will be smaller due to this bias.

        It is Setup as below

        Maximization Function:
            (Pw * Ow) * x1 + (Pl * Ol) * x2

        Where:
        - Pw, Pl: Calculated probabilities of win and loss, respectively
        - Ow, Ol: Odds for win and loss, respectively
        - x1, x2: Amounts bet on win and loss, respectively

        ## Inequality Constraints:
        1. (x1 * Ow) + x1 <= x1 + x2
        2. (x2 * Ol) + x2 <= x1 + x2
        3. x1 + x2 <= A

        Here, A represents the total available amount for betting.

        The tableu below shows the linear program in standard form
        """

        maximisationFunctionX1, maximisationFunctionX2 = (self.meanHomeProbability * self.homeBetOdds) + self.meanHomeProbability - 1,\
                                                         (self.meanAwayProbability * self.awayBetOdds) + self.meanAwayProbability - 1
        tableu = np.array([
            [-self.homeBetOdds, 1, 1, 0, 0, 0],
            [1, -self.awayBetOdds, 0, 1, 0, 0],
            [1, 1, 0, 0, 1, self.amount],
            [-maximisationFunctionX1, -maximisationFunctionX2, 0, 0, 0, 0]]
        )
        solution = self.simplex(tableu,
                                ['x1','x2','s1','s2','s3'],
                                [0,1])

        self.moneyOnHome = solution[0]
        self.moneyOnAway = solution[1]

    def initial_tableu_risky_three_outcome(self):
        """
        We do the same thing as above but now with 3 events

        Maximization Function:
            (Pw * Ow) * x1 + (Pd * Od) * x2 + (Pl * Ol) * x3

        Where:
        - Pw, Pd, Pl: Calculated probabilities of win, draw, and loss, respectively
        - Ow, Od, Ol: Odds for win, draw, and loss, respectively
        - x1, x2, x3: Amounts bet on win, draw, and loss, respectively

        Inequality Constraints:
        1. (x1 * Ow) + x1 <= x1 + x2 + x3
        2. (x2 * Od) + x2 <= x1 + x2 + x3
        3. (x3 * Ol) + x3 <= x1 + x2 + x3
        4. x1 + x2 + x3 <= A

        The tableu below represents this linear program in standard form
        """

        maximisationFunctionX1, maximisationFunctionX2, maximisationFunctionX3 = \
            (self.meanHomeProbability * self.homeBetOdds) + self.meanHomeProbability - 1, \
            (self.meanDrawProbability * self.drawBetOdds) + self.meanDrawProbability - 1, \
            (self.meanAwayProbability * self.awayBetOdds) + self.meanAwayProbability - 1,
        tableu = np.array([
            [-self.homeBetOdds, 1,1, 1, 0, 0,0, 0],
            [1, -self.drawBetOdds,1, 0, 1, 0,0, 0],
            [1, 1, -self.awayBetOdds, 0, 0, 1,0, 0],
            [1, 1, 1, 0, 0, 0,1, self.amount],
            [-maximisationFunctionX1, -maximisationFunctionX2, -maximisationFunctionX3, 0, 0, 0, 0,0]]
        )
        solution = self.simplex(tableu,
                                ['x1', 'x2', 'x3', 'S1', 'S2', 'S3', 'S4'],
                                [0,1,2])
        self.moneyOnHome = solution[0]
        self.moneyOnDraw = solution[1]
        self.moneyOnAway = solution[2]

    def initial_tableu_safe_three_outcome(self):
        """
        # Less Risky Function for Arbitrage (Three-Outcome Event)

        In this method, the maximization function focuses on minimizing the risk by optimizing the
        minimum possible return, rather than skewing towards the more likely outcome. This ensures
        a more balanced distribution of bets across the three possible outcomes.

        ## Risk Explanation:
        - The maximization function aims to minimize the impact of the least likely event, ensuring that
          the potential loss is capped, but possibly at the expense of maximizing overall profit.

        ## Maximization Function:
            min((Pw * Ow) * x1, (Pd * Od) * x2, (Pl * Ol) * x3)

        Where:
        - Pw, Pd, Pl: Calculated probabilities of win, draw, and loss, respectively
        - Ow, Od, Ol: Odds for win, draw, and loss, respectively
        - x1, x2, x3: Amounts bet on win, draw, and loss, respectively

        ## Inequality Constraints:
        1. (x1 * Ow) + x1 <= x1 + x2 + x3
        2. (x2 * Od) + x2 <= x1 + x2 + x3
        3. (x3 * Ol) + x3 <= x1 + x2 + x3
        4. x1 + x2 + x3 <= A

        The tableu below represents this in standard form on which simplex can be done

        Here, A represents the total available amount for betting.
        """

        tableu = np.array([
            [-1, self.homeBetOdds + 1, -1 - self.drawBetOdds, 0, 1, 0, 0, 0, 0, 0, 0],
            [-1, self.homeBetOdds + 1, 0, -1 - self.awayBetOdds, 0, 1, 0, 0, 0, 0, 0],
            [0, -self.homeBetOdds, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, -self.drawBetOdds, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, -self.awayBetOdds, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 1, self.amount],
            [1, -self.homeBetOdds, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        ])
        solution = self.simplex(tableu,
                                ['s1', 'x1', 'x2', 'x3', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
                                [1,2,3])
        self.moneyOnHome = solution[0]
        self.moneyOnDraw = solution[1]
        self.moneyOnAway = solution[2]

    def initial_tableu_safe_two_outcome(self):
        """
        Same as above but with 2 events

        Maximization Function:
            min((Pw * Ow) * x1, (Pl * Ol) * x2)

        Where:
        - Pw, Pl: Calculated probabilities of win and loss, respectively
        - Ow, Ol: Odds for win and loss, respectively
        - x1, x2: Amounts bet on win and loss, respectively

        ## Inequality Constraints:
        1. (x1 * Ow) + x1 <= x1 + x2
        2. (x2 * Ol) + x2 <= x1 + x2
        3. x1 + x2 <= A

        A is the total amount betted and the tableu below represents this linear program in standard from """

        tableu = np.array([
            [-1, self.homeBetOdds+1, -1-self.awayBetOdds,1, 0,0,0,0],
            [0,-self.homeBetOdds, 1,0,1,0,0,0],
            [0,1,-self.awayBetOdds,0,0,1,0,0],
            [0,1,1,0,0,0,1,self.amount],
            [1,-self.homeBetOdds, 1,0,0,0,0,0]
            ])

        solution = self.simplex(tableu,
                                ['s1', 'x1', 'x2', 'S1', 'S2', 'S3', 'S4'],
                                [1,2])

        self.moneyOnHome = solution[0]
        self.moneyOnAway = solution[1]

    # Simplex Method Implementation
    def simplex(self, tableau, variables, desired):
        # Loop until we reach an optimal solution
        num_rows, num_cols = tableau.shape
        count = 0
        while True:
            # Step 1: Check for optimality (all coefficients in the objective row are <= 0)
            objective_row = tableau[-1, :-1]
            if all(obj >= 0 for obj in objective_row):
                break  # Optimal solution found

            # Step 2: Find pivot column (most negative coefficient in the objective row)
            pivot_col = np.argmin(objective_row)
            # Step 3: Determine the pivot row using the minimum ratio test
            ratios = []
            for i in range(num_rows - 1):
                if tableau[i, pivot_col] > 0:
                    ratios.append(tableau[i, -1] / tableau[i, pivot_col])
                else:
                    ratios.append(np.inf)

            pivot_row = np.argmin(ratios)
            if ratios[pivot_row] == np.inf:
                raise ValueError("Problem is unbounded.")

            # Step 4: Perform pivoting (Gauss-Jordan elimination)
            pivot_value = tableau[pivot_row, pivot_col]
            tableau[pivot_row, :] /= pivot_value

            for i in range(num_rows):
                if i != pivot_row:
                    row_factor = tableau[i, pivot_col]
                    tableau[i, :] -= row_factor * tableau[pivot_row, :]

        # Extract solution
        solution = np.zeros(num_cols - 1)
        for i in range(num_rows - 1):
            col = tableau[:-1, i]
            if np.sum(col == 1) == 1 and np.sum(col) == 1:  # Basic variable
                basic_var_index = np.argmax(col)
                solution[i] = tableau[basic_var_index, -1]

        result = []
        for i in desired:
            result.append(solution[i])
        return result

    def checkArbitragePossible(self):
        suppliers = list(self.oddsAndSupplier.keys())

        # In a 2 outcome event
        if self.noPossibleResults == 2:
            homeOdds, awayOdds = zip(*self.oddsAndSupplier.values())

            # Calculate the probabilities using the odds for both a win and a loss
            homeProbability, meanHomeProbability = self.calculate_probabilities(homeOdds)
            awayProbability, meanAwayProbability = self.calculate_probabilities(awayOdds)
            self.meanHomeProbability, self.meanAwayProbability = self.normalize_probabilities(
                meanHomeProbability, meanAwayProbability)

            #Get the site and probability in which is most likely for arbitrage for both a win and loss (the smallest one)
            self.homeBetSite, homeBestProbability = self.get_best_site(homeProbability, suppliers)
            self.awayBetSite, awayBestProbability = self.get_best_site(awayProbability, suppliers)

            #Check if possible
            if homeBestProbability + awayBestProbability >= 1:
                return False
            else:
                self.homeBetOdds = 1 / homeBestProbability
                self.awayBetOdds = 1 / awayBestProbability
                self.discrepency = 1 - (homeBestProbability + awayBestProbability)
                return True
        else:
            #Repeat same thing for 3 event
            homeOdds, awayOdds, drawOdds = zip(*self.oddsAndSupplier.values())

            homeProbability, meanHomeProbability = self.calculate_probabilities(homeOdds)
            awayProbability, meanAwayProbability = self.calculate_probabilities(awayOdds)
            drawProbability, meanDrawProbability = self.calculate_probabilities(drawOdds)
            self.meanHomeProbability, self.meanAwayProbability, self.meanDrawProbability = self.normalize_probabilities(
                meanHomeProbability, meanAwayProbability, meanDrawProbability
            )

            self.homeBetSite, homeBestProbability = self.get_best_site(homeProbability, suppliers)
            self.awayBetSite, awayBestProbability = self.get_best_site(awayProbability, suppliers)
            self.drawBetSite, drawBestProbability = self.get_best_site(drawProbability, suppliers)

            if homeBestProbability + awayBestProbability + drawBestProbability >= 1:
                return False
            else:
                self.homeBetOdds = 1 / homeBestProbability
                self.awayBetOdds = 1 / awayBestProbability
                self.drawBetOdds = 1 / drawBestProbability
                self.discrepency = 1 - (homeBestProbability + awayBestProbability + drawBestProbability)
                return True

    #Helper function to convert from odds to probabilities
    def calculate_probabilities(self, odds):
        probabilities = [1 / odd for odd in odds]
        mean_probability = sum(probabilities) / len(probabilities)
        return probabilities, mean_probability

    #Helper function to normalising proabilities so add to 100% to be used later
    def normalize_probabilities(self, *mean_probabilities):
        total_probability = sum(mean_probabilities)
        return [mean / total_probability for mean in mean_probabilities]

    #Helper function to get site with largest odds
    def get_best_site(self, probabilities, suppliers):
        sorted_probabilities = sorted(enumerate(probabilities), key=lambda x: x[1])
        best_index, best_probability = sorted_probabilities[0]
        return suppliers[best_index], best_probability

    #Using JSON to get data required
    def getOddsWithBettingSite(self, event):
        actualData = self.events_data[event]
        self.homeTeam = actualData['home_team']
        self.awayTeam = actualData['away_team']
        self.event_name = f'{self.homeTeam} V {self.awayTeam}'
        self.noPossibleResults = (len(actualData['bookmakers'][0]["markets"][0]["outcomes"]))

        if self.noPossibleResults == 2:
            order = (self.homeTeam, self.awayTeam)
            self.oddsAndSupplier = {bookie['title']: (
                self.get_in_order(bookie['markets'][0]['outcomes'], order[0]),
                self.get_in_order(bookie['markets'][0]['outcomes'], order[1])) for bookie in actualData['bookmakers']}
        else:
            order = (self.homeTeam, self.awayTeam, 'Draw')
            self.oddsAndSupplier = {bookie['title']: (
                self.get_in_order(bookie['markets'][0]['outcomes'], order[0]),
                self.get_in_order(bookie['markets'][0]['outcomes'], order[1]),
                self.get_in_order(bookie['markets'][0]['outcomes'], order[2])) for bookie in actualData['bookmakers']}

    #Helper function to get results in order required if dosent naturally occur in API
    def get_in_order(self, jsonOdds, teamName):
        for odds in jsonOdds:
            if odds['name'] == teamName:
                return odds['price']

    def sendRequest(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return False
        else:
            data = response.json()
            return data


#Class to put the results of arbitrage into
class Result:
    def __init__(self, event, drawAvailable, homeTeam, homeOdds, homeAmount, homeSite, awayTeam, awayOdds, awayAmount, awaySite, drawOdds, drawAmount, drawSite):
        self.__event = event
        self.__drawAvailable = drawAvailable
        self.__homeTeam = homeTeam
        self.__homeOdds = homeOdds
        self.__homeAmount = homeAmount
        self.__homeSite = homeSite
        self.__awayTeam = awayTeam
        self.__awayOdds = awayOdds
        self.__awayAmount = awayAmount
        self.__awaySite = awaySite

        self.__drawOdds = drawOdds
        self.__drawAmount = drawAmount
        self.__drawSite = drawSite
        self.__ifHomeWinsProfit = homeOdds * homeAmount + homeAmount
        self.__ifAwayWinsProfit = awayOdds*awayAmount + awayAmount

        if drawAvailable:
            self.__ifDrawProfit = drawOdds * drawAmount + drawAmount
        else:
            self.__ifDrawProfit = None
    def getEvent(self):
        return self.__event

    def getDrawAvailable(self):
        return self.__drawAvailable

    def getHomeTeam(self):
        return self.__homeTeam

    def getHomeOdds(self):
        return self.__homeOdds

    def getHomeAmount(self):
        return self.__homeAmount

    def getHomeSite(self):
        return self.__homeSite

    def getAwayTeam(self):
        return self.__awayTeam

    def getAwayOdds(self):
        return self.__awayOdds

    def getAwayAmount(self):
        return self.__awayAmount

    def getAwaySite(self):
        return self.__awaySite

    def getDrawOdds(self):
        return self.__drawOdds

    def getDrawAmount(self):
        return self.__drawAmount

    def getDrawSite(self):
        return self.__drawSite

    def getProfitHomeWins(self):
        return self.__ifHomeWinsProfit

    def getProfitAwayWins(self):
        return self.__ifAwayWinsProfit

    def getProfitDraw(self):
        return self.__ifDrawProfit
