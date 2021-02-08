import json, requests, itertools
from time import gmtime

class Weather(object):
	
	api_key = "YOUR_API_KEY"
	base_url = "https://api.openweathermap.org/data/2.5/"
	city_name = "Charlotte"
	degree_sign= u'\N{DEGREE SIGN}'
	
	def __init__ (self):
		pass
	
	def getCurrentWeather(self):

		complete_url = self.base_url + "weather?q=" + self.city_name + "&units=imperial&appid=" + self.api_key
		
		try:
			response = requests.get(complete_url)
			x = response.json()
		
			if x["cod"] != "404":

				y = x["main"]
				current_temperature = y["temp"]

				z = x["weather"]
				weather_description = z[0]["description"]

			img_data = self.getIconImage(x["weather"][0]["icon"])
			current_weather = [str(int(current_temperature)) + self.degree_sign, str(weather_description), img_data]
			
		except ConnectionError:
			print("No Internet Connection")
			
		return current_weather
	
	def getDayForecast(self):

		complete_url = self.base_url + "forecast?q=" + self.city_name + "&units=imperial&appid=" + self.api_key
		
		try:
			response = requests.get(complete_url)
			x = response.json()
			
			current_forecast = []
			
			if x["cod"] != "404":
				
				y = x["list"]
				
				for i in itertools.islice(y, 3):
					current_forecast.append(i)
		except ConnectionError:
			print("No Internet Connection")
				
		return current_forecast
		
	def getWeekForecast(self):
	
		complete_url = self.base_url + "forecast?q=" + self.city_name + "&units=imperial&appid=" + self.api_key
		
		try:
			response = requests.get(complete_url)
			x = response.json()
			
			week_forecast = []
			
			if x["cod"] != "404":
				
				y = x["list"]
				
				for i in y:
					if gmtime(i["dt"]).tm_hour == gmtime(y[-1]["dt"]).tm_hour and gmtime(i["dt"]).tm_mday != gmtime().tm_mday:
						week_forecast.append(i)
		except ConnectionError:
			print("No Internet Connection")
					
		return week_forecast
				
	def getIconImage(self, icon):
		img_response = requests.get("http://openweathermap.org/img/wn/" + icon + "@2x.png")
		return img_response.content