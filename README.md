# Python Application with Tkinter, JSON, and NumPy

This Python application utilizes **Tkinter** for the user interface, **JSON** for data handling, and **NumPy** for numerical computation.
This is a sports betting arbitrage calculator that provides numerous upcoming sporting events and calculates where arbitrage is possible across these.
The output will be the amount of money to bet on which website and the guaranteed amount you will make

## Prerequisites

Ensure you have the following installed:

- **Python 3.x** (recommended: Python 3.6 or higher)
- **pip** (Python package installer)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   
2. **Navigate to the right folder**:
   ```bash
   cd <project directory>

3. **Create Virtual Environment (Optional but reccomended)**:
   ```bash
   python -m venv venv

4. **Activate virtual environment**:
- On windows:
   ```bash
   venv\Scripts\activate
- On Mac/Linux:
    ```bash
    source venv/bin/activate

5. **Install Required Dependencies**:
    ```bash
    pip install -r requirements.txt
   
6. **Running the Application**:
    ```bash
   python main.py

7. **Example Usage**:
- Select a sport from the dropdown box
- Click the get events button
- Select an event from the dropdown box
- Select either a Risky or Safe strategy
- Select Maximum money you would like to bet
- Press calculate arbitrage
- If multiple events currently do not have arbitrage (likely) and you want to see a working method select the "Example 3 event" or "Examples 2 event" and press calculate
- This will show you how the result will look

8. **Strategies Used**:
This is described in more detail in the respective functions comments but I will give a brief summary below
- There are 2 options we have allowed: A Risky bet and a Safe Bet
- A Risky bet maximises the expected return but will skew the calculations to place more money on the more likely event
- A Safe bet maximises the minimum of the potential returns which balances the distribution of the money across events.

Hope you Enjoy


