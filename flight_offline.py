import json

with open("sample_flight.json", "r", encoding="utf-8") as f:
    result = json.load(f)

flights=result['data']['itineraries']
flights=sorted(flights, key=lambda x:x['price']['raw'])
flight_options=[]

def get_flight_options():
    flight_options=[]
    for flight in flights[:3]:
        leg=flight['legs'][0]
        flight_options.append({
            'mode' : 'flight',
            'airline' : leg['carriers']['marketing'][0]['name'],
            'price' : flight['price']['raw'],
            'departure' : leg['departure'][11:16],
            'arrival' : leg['arrival'][11:16],
            'duration' : leg['durationInMinutes']
        })
    return flight_options


def display_flights(flight_options):
    for i, flight in enumerate(flights[:3], start=1):
        leg=flight['legs'][0]
        flight_options.append({
            'mode' : 'flight',
            'airline' : leg['carriers']['marketing'][0]['name'],
            'price' : flight['price']['raw'],
            'departure' : leg['departure'][11:16],
            'arrival' : leg['arrival'][11:16],
            'duration' : leg['durationInMinutes']
        })
        print('='*50)
        print('Flight', i)
        print("Airline:", leg['carriers']['marketing'][0]['name'])
        print("Price:", flight['price']['formatted'])
        print("From:", leg['origin']['name'])
        print("To:", leg['destination']['name'])
        print("Departure:", leg['departure'][11:16])
        print("Arrival:", leg['arrival'][11:16])
        duration=leg['durationInMinutes']

        hours=duration // 60
        minutes=duration % 60
        print('Duration:', f'{hours}h {minutes}m')
flight_options=get_flight_options()
print('\n FLIGHT OPTIONS')
print(flight_options)