import requests
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # create widgets
        self.label = QtWidgets.QLabel("Enter sell and buy volume thresholds:")
        self.sell_threshold = QtWidgets.QLineEdit()
        self.sell_threshold.setPlaceholderText("Sell threshold")
        self.buy_threshold = QtWidgets.QLineEdit()
        self.buy_threshold.setPlaceholderText("Buy threshold")
        self.calculate_button = QtWidgets.QPushButton("Calculate")
        self.result_label = QtWidgets.QLabel()

        # create layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.sell_threshold)
        layout.addWidget(self.buy_threshold)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        # create widget to hold layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # connect calculate_button to calculate function
        self.calculate_button.clicked.connect(self.calculate)

    def calculate(self):
        # get sell and buy thresholds from user input
        sell_threshold = int(self.sell_threshold.text())
        buy_threshold = int(self.buy_threshold.text())

        # get data from API
        response = requests.get("https://api.hypixel.net/skyblock/bazaar")
        data = response.json()

        # initialize variables to store the best item and its difference
        best_item = ""
        max_difference = 0

        # iterate through all items
        for item in data["products"]:
            # get sell and buy prices for current item
            sell_summary = data["products"][item]["sell_summary"]
            buy_summary = data["products"][item]["buy_summary"]

            # check if sell_summary or buy_summary is empty
            if not sell_summary or not buy_summary:
                continue

            sell_price = sell_summary[0]["pricePerUnit"]
            buy_price = buy_summary[0]["pricePerUnit"]

            # calculate difference between sell and buy prices
            difference = buy_price - sell_price

            # get volume of buy and sell orders
            sell_volume = data["products"][item]["quick_status"]["sellVolume"]
            buy_volume = data["products"][item]["quick_status"]["buyVolume"]

            # only consider items with high volume and a high margin
            if difference > max_difference and sell_volume > sell_threshold and buy_volume > buy_threshold:
                max_difference = difference
                best_item = item

        # display result
        self.result_label.setText(
            f"The best item to flip is: {best_item} with a difference of {max_difference} coins.")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
