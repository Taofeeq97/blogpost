import requests

url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

querystring = {"q": "London", "days": "3"}

headers = {
    "content-type": "application/octet-stream",
    "X-RapidAPI-Key": "7613a5777dmshc0a19d85c6372d7p197f98jsn2c004a89fa6d",
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
