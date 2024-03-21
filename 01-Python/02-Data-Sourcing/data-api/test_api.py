# pylint: disable=missing-docstring,invalid-name
import requests

baseurl = "https://api.openweathermap.org"
endpoint = "/geo/1.0/direct?q=Barcelona&appid=bbf75210a9732d35aa79bc0477dd4fcf"
response = requests.get(baseurl+endpoint).json()
city = response[0]
print(f"{city['name']}: ({city['lat']}, {city['lon']})")
