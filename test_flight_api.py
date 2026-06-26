import http.client

conn = http.client.HTTPSConnection("sky-scrapper.p.rapidapi.com")


headers = {
    'x-rapidapi-key': "ad8d8e335emsh58018338e80b978p1d27bbjsne704fbdd5a5a",
    'x-rapidapi-host': "sky-scrapper.p.rapidapi.com",
    'Content-Type': "application/json"
}

conn.request("GET", "/api/v1/flights/searchAirport?query=Chennai&locale=en-US", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))