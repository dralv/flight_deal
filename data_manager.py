import requests
import os


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.url = "https://api.sheety.co/028889e3f0eb8904732d082a6fb699e9/flightDeals/prices"
        self.auth = os.environ['SHEETY_AUTH']
        self.headers = {
            "Authorization": self.auth
        }

    def get_data(self):
        response = requests.get(url=self.url, headers=self.headers)
        json = response.json()
        data = json['prices']
        return data

    def update_sheet(self,id,field,value):
        body = {
            "price":{
                field:value
            }
        }
        requests.put(url=f"{self.url}/{id}",json=body,headers=self.headers)

