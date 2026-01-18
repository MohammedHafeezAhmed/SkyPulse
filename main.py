import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,
                             QLabel,QLineEdit,QVBoxLayout,QPushButton)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
      super().__init__()
      self.city_label=QLabel("Enter City: ",self)
      self.city_input=QLineEdit(self)
      self.get_weather_button=QPushButton("Get Weather",self)
      self.temperature_label=QLabel(self)
      self.emoji_label=QLabel(self)
      self.description_label=QLabel(self)
      self.initUI()

    def initUI(self):
       
       self.setWindowTitle("SkyPulse")

       vbox=QVBoxLayout()

       vbox.addWidget(self.city_label)
       vbox.addWidget(self.city_input)
       vbox.addWidget(self.get_weather_button)
       vbox.addWidget(self.temperature_label)
       vbox.addWidget(self.emoji_label)
       vbox.addWidget(self.description_label)

       self.setLayout(vbox)

       self.city_label.setAlignment(Qt.AlignCenter)
       self.city_input.setAlignment(Qt.AlignCenter)
       self.temperature_label.setAlignment(Qt.AlignCenter)
       self.emoji_label.setAlignment(Qt.AlignCenter)
       self.description_label.setAlignment(Qt.AlignCenter)

       self.city_label.setObjectName("citylabel")
       self.city_input.setObjectName("cityinput")
       self.temperature_label.setObjectName("temperaturelabel")
       self.get_weather_button.setObjectName("weatherbtn")
       self.emoji_label.setObjectName("emojilabel")
       self.description_label.setObjectName("desc")

       self.setStyleSheet("""
                          QLabel,QPushButton{
                            font-family:Arial;
                          }
                          QLabel#citylabel{
                            font-size:50px;font-style:italic;
                          }
                          QLineEdit#cityinput{
                            font-size:25px;
                          }
                          QPushButton#weatherbtn{
                            font-size:15px;font-weight:bold;
                          }
                          
                          QLabel#emojilabel
                          {font-size:35px;
                           font-family:Segoe UI emoji;
                          }
                         
                          """)
       self.get_weather_button.clicked.connect(self.get_weather)
      

    def get_weather(self):
       api_key = "dbfb526bf3ea5f273f9caaa8081b0a24"
       city=self.city_input.text()
       url= f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

       try:
          request=requests.get(url)
          request.raise_for_status()
          data = request.json()
       
          if data["cod"] == 200:
           self.display_weather(data)
       except requests.exceptions.HTTPError as http_error:
          match request.status_code:
             case 400:
                self.display_error("Bad request\n please check your input")
             case 401:
                self.display_error("Unauthorised\n Invalid api key")
             case 403:
                self.display_error("Forbidden\n Access is denied")
             case 404:
                self.display_error("not found\n city not found") 
             case 500:
                self.display_error("Internal server error\n please try again later")
             case 502:
                self.display_error("bad gateway\n Invalid response from server")
             case 503:
                self.display_error("service unavailable\n Server is down")                  
             case 504:
                self.display_error("Gateway timeout\n no response from server")
             case _:
                self.display_error(f"http error occured\n no {http_error}") 
       except requests.exceptions.ConnectionError:
          self.display_error("connection error check ur internet connection")
       except requests.exceptions.ConnectTimeout:
          self.display_error("timeout error the request timed out")
       except requests.exceptions.TooManyRedirects:
          self.display_error("too many redirects . check the url")
       except requests.exceptions.RequestException as req_error:
          self.display_error(f"request error \n too {req_error}")
          pass
       


    def display_error(self,message):
       
       self.temperature_label.setStyleSheet("font-size:20px;")
       self.temperature_label.setText(message)
       self.emoji_label.clear()       
       self.description_label.clear()


    def display_weather(self,data):
       
       self.temperature_label.setStyleSheet("font-size:40px;")
       self.description_label.setStyleSheet("font-size:40px;")
       temp_k = data["main"]["temp"]
       temp_c = temp_k - 273.15 
       temp_f = (temp_k*9/5) - 459.67
       jonny=(f"{temp_k:.2f}F")

       w_id = data["weather"][0]["id"]      
       weather_disc = data["weather"][0]["description"]

       self.temperature_label.setText(jonny)
       self.emoji_label.setText(self.get_weather_emoji(w_id))       
       self.description_label.setText(weather_disc)

    @staticmethod
    def get_weather_emoji(w_id):
       
       if 200 <= w_id <= 232:
          return "🌩"
       elif 300 <= w_id <= 321:
          return "⛅"
       elif 500 <= w_id <= 531:
          return "⛈"
       elif 600 <= w_id <= 622:
          return "❄"
       elif 701 <= w_id <= 741:
          return "🌫"
       elif w_id == 762:
          return "🌋"
       elif w_id == 771:
          return "💨"
       elif w_id == 781:
          return "🌪" 
       elif w_id == 800:
          return "☀"
       elif 800 <= w_id <= 804:
          return "🌪"    
       else:
          return ""
          

if __name__ == "__main__":
   app=QApplication(sys.argv)
   weather_app=WeatherApp()
   weather_app.show()
   sys.exit(app.exec_())
