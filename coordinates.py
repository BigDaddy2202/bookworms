import pandas as pd
import os
from geopy import geocoders
from geopy.geocoders import GoogleV3

API_KEY = os.getenv("API1234")
g = GoogleV3(api_key=API_KEY)

def getCoordinates(inputAddress):
    loc_coordinates = []
    try:
        location = g.geocode(inputAddress, timeout=15)
        loc_coordinates.append((location.latitude, location.longitude))
        return loc_coordinates[0]
    except Exception as e:
        ret = 'Encountered error: ' + str(e)
        return ret


#=================================================================================================================================================
# import requests

# response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=Bakul+Niwas+room+215+IIIT+Hyderabad+gachibowli+hyderabad')

# resp_json_payload = response.json()
# print(resp_json_payload['results'][0]['geometry']['location'])
#==================================================================================================================================================
