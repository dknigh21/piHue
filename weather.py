import json
import requests



def getTemp():

	api_key = "4d3438e56dc48f503d4b43250ec70871"
	base_url = "https://api.openweathermap.org/data/2.5/weather?"
	city_name = "Charlotte"
	complete_url = base_url + "q=" + city_name + "&appid=" + api_key

	response = requests.get(complete_url)
	x = response.json()

	if ["cod"] != "404":

		y = x["main"]
		current_temperature = y["temp"]

		z = x["weather"]
		weather_description = z[0]["description"]

def getForecast():

	api_key = "4d3438e56dc48f503d4b43250ec70871"
	base_url = "https://api.openweathermap.org/data/2.5/forecast?"
	city_name = "Charlotte"
	complete_url = base_url + "q=" + city_name + "&appid=" + api_key