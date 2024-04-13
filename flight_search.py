import os
from datetime import datetime, timedelta
import requests
from flight_data import FlightData

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.base_url = "https://api.tequila.kiwi.com"
        self.api_key = os.environ['TEQUILA_API_KEY']
    def get_iata(self,city_code):
        self.params = {
            "term":city_code,
            "location_types":"city",
            "limit":1
        }

        headers = {
            "apikey":self.api_key
        }
       # print(f"Searching IATA Code for city {city_code}")
        response = requests.get(url=f"{self.base_url}/locations/query",params=self.params,headers=headers)
        json = response.json()
        iata_code = json["locations"][0]["code"]
       # print(f"IATA Code for city {city_code} is {iata_code}")
        return iata_code
        #['locations']['city']['code']

    def get_flight_data(self, origin_city_code, destination_city_code, from_time, to_time):

        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        headers = {
            "apikey": self.api_key
        }
        url = f"{self.base_url}/v2/search"



        response = requests.get(url=url, params=params, headers=headers)



        try:
            data = response.json()['data'][0]
        except IndexError:
            print(f"No  flights found for {destination_city_code}")
            return None
        except KeyError:
            print(f"No  flights found for {destination_city_code}")
            return None


        flight_data = FlightData(
            price=data['price'],
            origin_city=data['route'][0]['cityFrom'],
            origin_airport=data['route'][0]['flyFrom'],
            destination_city=data['route'][0]['cityTo'],
            destination_airport=data['route'][0]['flyTo'],
            out_date=data['route'][0]['local_departure'].split("T")[0],
            return_date=data['route'][1]['local_departure'].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £ {flight_data.price} ")

        return  flight_data

