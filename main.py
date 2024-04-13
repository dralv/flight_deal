from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime,timedelta
from notification_manager import NotificationManager


data_manager= DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_data()
notification_manager =  NotificationManager()

ORIGIN_CITY_IATA = "LON"
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


for data in sheet_data:
    if data['iataCode'] == '':
        iata_code = flight_search.get_iata(data['city'])
        data['iataCode'] = iata_code
        data_manager.update_sheet(data['id'],'iataCode',iata_code)


for data in sheet_data:
    flight = flight_search.get_flight_data(
        ORIGIN_CITY_IATA,
        data['iataCode'],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight.price < data['lowestPrice']:
        notification_manager.send_email(flight.price,ORIGIN_CITY_IATA,flight.destination_city,flight.out_date,flight.return_date)
        data_manager.update_sheet(data['id'],"lowestPrice",flight.price)


