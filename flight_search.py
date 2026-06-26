import http.client
import json



#airport_codes={
    #'Mumbai' : 'BOM',
    #'Chennai' : 'MAA',
    #'Delhi' : 'DEL',
    #'Hyderabad' : 'HYD',
    #'Kolkata' : 'CCU',
    #'Pune' : 'PNQ',
    #'Jaipur' : 'JAI',
    #'Lucknow' : 'LKO',
    #'Patna' :  'PAT',
    #'Goa' : 'GOI',
    #'Coimbatore' : 'CJB',
    #'Kochi' : 'COK',
    #'Madurai' : 'IXM',
    #'Mangalore' : 'IXE',
    #'Mysore' : 'MYQ',
    #'Bangalore' : 'BLR',
    #'Dombivli' : 'BOM',
    #'Bhubaneswar' : 'BBI',
    #'Ahmedabad' : 'AMD',
    #'Chandigarh' : 'IXC',
    #'Nagpur' : 'NAG',
    #'Nashik' : 'ISK',
    #'Surat' : 'STV',
    #'Vadodara' : 'BDQ',
    #'Visakhapatnam' : 'VTZ',
    #'Vijayawada' : 'VGA',
    #'Indore' : 'IDR',
    #'Tiruchirappalli' : 'TRZ'
#}
CITY_DATA = {
    "Mumbai": {
        "skyId": "BOM",
        "entityId": "95673320"
    },
    "Chennai": {
        "skyId": "MAA",
        "entityId": "95673361"
    },
    "Bangalore": {
        "skyId": "BLR",
        "entityId": "95673351"
    },
    "Delhi": {
        "skyId": "DEL",
        "entityId": "95673498"
    },
    "Hyderabad": {
        "skyId": "HYD",
        "entityId": "128668073"
    },
    "Kolkata": {
        "skyId": "CCU",
        "entityId": "128668366"
    },
    "Pune": {
        "skyId": "PNQ",
        "entityId": "128668941"
    },
    "Jaipur": {
        "skyId": "JAI",
        "entityId": "128668565"
    },
    "Lucknow": {
        "skyId": "LKO",
        "entityId": "128668794"
    },
    "Patna": {
        "skyId": "PAT",
        "entityId": "9567344"
    },
    "Goa": {
        "skyId": "GOI",
        "entityId": "27541888"
    },
    "Coimbatore": {
        "skyId": "CJB",
        "entityId": "95673549"
    },
    "Kochi": {
        "skyId": "COK",
        "entityId": "95673550"
    },
    "Madurai": {
        "skyId": "IXM",
        "entityId": "95673566"
    },
    "Mangalore": {
        "skyId": "IXE",
        "entityId": "128668563"
    },
    "Mysore": {
        "skyId": "MYQ",
        "entityId": "128668863"
    },
    "Bhubaneswar": {
        "skyId": "BBI",
        "entityId": "128668039"
    },
    "Ahmedabad": {
        "skyId": "AMD",
        "entityId": "95673366"
    },
    "Chandigarh": {
        "skyId": "IXC",
        "entityId": "128667255"
    },
    "Nagpur": {
        "skyId": "NAG",
        "entityId": "128668867"
    },
    "Nashik": {
        "skyId": "ISK",
        "entityId": "129055659"
    },
    "Surat": {
        "skyId": "STV",
        "entityId": "128667060"
    },
    "Vadodara": {
        "skyId": "BDQ",
        "entityId": "95673367"
    },
    "Visakhapatnam": {
        "skyId": "VTZ",
        "entityId": "128668501"
    },
    "Vijayawada": {
        "skyId": "VGA",
        "entityId": "128667161"
    },
    "Indore": {
        "skyId": "IDR",
        "entityId": "128667504"
    },
    "Tiruchirappalli": {
        "skyId": "TRZ",
        "entityId": "95673567"
    },
    "Dombivli": {
        "skyId": "BOM",
        "entityId": "95673320"
    }
}
def search_flights(source_city, destination_city, travel_date):
    if source_city not in CITY_DATA:
        return []
    if destination_city not in CITY_DATA:
        return []
    
    origin_sky_id=CITY_DATA[source_city]['skyId']
    origin_entity_id=CITY_DATA[source_city]['entityId']

    destination_sky_id=CITY_DATA[destination_city]['skyId']
    destination_entity_id=CITY_DATA[destination_city]['entityId']




    conn = http.client.HTTPSConnection("sky-scrapper.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "ad8d8e335emsh58018338e80b978p1d27bbjsne704fbdd5a5a",
        'x-rapidapi-host': "sky-scrapper.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request(
        "GET",
        f"/api/v2/flights/searchFlights?"
        f"originSkyId={origin_sky_id}"
        f"&destinationSkyId={destination_sky_id}"
        f"&originEntityId={origin_entity_id}"
        f"&destinationEntityId={destination_entity_id}"
        f"&date={travel_date}"
        f"&cabinClass=economy"
        f"&adults=1"
        f"&sortBy=best"
        f"&currency=INR"
        f"&market=en-IN"
        f"&countryCode=IN",
        headers=headers
    )

    res = conn.getresponse()
    data = res.read()
    #with open('sample_flight.json', 'w', encoding='utf-8') as f:
        #f.write(data.decode('utf-8'))


    result = json.loads(data.decode('utf-8'))
    flight_options=[]
    

    if (
        'data' not in result or 'itineraries' not in result['data'] or not result['data']['itineraries']):
        return[]
    flights=result['data']['itineraries']
    

    flights = sorted(
        flights,
        key=lambda x: x["price"]["raw"]
    )

    for flight in flights[:3]:

        leg = flight["legs"][0]

        flight_options.append({
            "mode": "flight",
            "airline": leg["carriers"]["marketing"][0]["name"],
            "price": flight["price"]["raw"],
            "departure": leg["departure"][11:16],
            "arrival": leg["arrival"][11:16],
            "duration": (
                f'{leg['durationInMinutes']//60}h'
                f'{leg['durationInMinutes']%60}m'
            )
        })
    return flight_options
