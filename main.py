import sys
import requests
from PyQt5.QtWidgets import QLabel,QWidget,QVBoxLayout,QPushButton,QLineEdit,QApplication
from PyQt5.QtCore import Qt

class WeatherApi(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:",self)
        self.city_input = QLineEdit(self)
        self.enter_button = QPushButton("Get Weather",self)
        self.temperature = QLabel(self)
        self.emoji_label = QLabel(self)
        self.weather_description = QLabel(self)
        self.initUI()

    def initUI(self):
        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.enter_button)
        vbox.addWidget(self.temperature)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.weather_description)

        self.setLayout(vbox)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.enter_button.setObjectName("enter_button")
        self.emoji_label.setObjectName("emoji_label")
        self.weather_description.setObjectName("weather_description")
        self.temperature.setObjectName("temperature")

        self.setStyleSheet(
            """
            QLabel,QPushButton,QLineEdit{
                font-family:calibri;
            }
            QLabel#city_label{
                font-size:45px;
                font-style:italic;
            }
            QLineEdit#city_input{
                font-size:30px;
            }
            QPushButton#enter_button{
                font-size:30px;
                font-weight:bold;
            }
            QLabel#emoji_label{
                font-size:65px;
                font-family:Segoe UI Emoji;
            }
            QLabel#weather_description{
                font-size:45px;
            }
            QLabel#temperature{
                font-size:50px;
            }
            """
        )
        self.enter_button.clicked.connect(self.get_weather)
    def get_weather(self):
        try:
            api = "03406042cbd47f900af1d6b17e772d46"
            city = self.city_input.text().strip()

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"
            response = requests.get(url)
            error = response.raise_for_status()
            data = response.json()
            self.display_weather(data)
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_errors("Bad Request")
                case 401:
                    self.display_errors("Unauthorized")
                case 402:
                    self.display_errors("Payment Required")
                case 403:
                    self.display_errors("Forbidden")
                case 404:
                    self.display_errors("Not Found:\n City name not found")
                case 500:
                    self.display_errors("Internal Server Error")
                case 501:
                    self.display_errors("Not Implemented")
                case 502:
                    self.display_errors("Bad Gateway")
                case 503:
                    self.display_errors("Service Unavailable")
        except requests.exceptions.RequestException as req_error:
            self.display_errors(f"{req_error}")
        except requests.exceptions.Timeout as time_out:
            self.display_errors(f"{time_out}")
        except requests.exceptions.ConnectionError:
            self.display_errors("Connection Error:\n Please check you internet")



    def display_weather(self,data):
        temper = data["main"]["temp"]
        self.temperature.setText(f"{temper:.0f}°C")

        desrip = data["weather"][0]["description"]
        self.weather_description.setText(f"{desrip}")

        id = data["weather"][0]["id"]
        emoji = self.get_weather_emoji(id)
        self.emoji_label.setText(f"{emoji}")


    def display_errors(self,message):
        self.temperature.setStyleSheet("font-size:30px")
        self.temperature.setText(message)
        self.emoji_label.clear()
        self.weather_description.clear()

    @staticmethod
    def get_weather_emoji(id):
        if id >= 200 and id <= 232:
            return "⛈️"
        elif id >= 300 and id <= 321:
            return "🌦️"
        elif id >= 500 and id <= 531:
            return "🌧️"
        elif id >= 600 and id <= 622:
            return "❄️"
        elif id == 701:
            return "🌫️"
        elif id == 711:
            return "💨"
        elif id == 721:
            return "🌫️"
        elif id == 731:
            return "🌪️"
        elif id == 741:
            return "🌫️"
        elif id == 751:
            return "🏜️"
        elif id == 761:
            return "🌪️"
        elif id == 762:
            return "🌋"
        elif id == 771:
            return "💨"
        elif id == 781:
            return "🌪️"
        elif id == 800:
            return "☀️"
        elif id == 801:
            return "🌤️"
        elif id == 802:
            return "⛅"
        elif id == 803:
            return "🌥️"
        elif id == 804:
            return "☁️"

def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApi()
    weather_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()