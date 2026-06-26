import requests

url = "https://irctc-api2.p.rapidapi.com/trainAvailability"

querystring = {
    "source": "KYN",
    "destination": "TPJ",
    "date": "25-06-2026"
}

headers = {
    "x-rapidapi-key": "80901fa0f0msh69c96d2ee12d9e8p1e6ac2jsn60e70defa338",
    "x-rapidapi-host": "irctc-api2.p.rapidapi.com"
}

response = requests.get(
    url,
    headers=headers,
    params=querystring
)

print(response.status_code)
print(response.json())