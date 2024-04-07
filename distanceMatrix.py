import googlemaps as gmaps
import matrixkey
import datetime
from datetime import datetime
class distanceMatrix():
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = gmaps.Client(api_key)

    def get_traffic_time(self, dest, mode=0):
        modes = ["driving", "transit"]
        return self.client.distance_matrix(
            origins = self.client.geolocate()['location'],
            destinations = dest,
            mode = modes[mode]
        )
    
if __name__ == '__main__':
    test = distanceMatrix(matrixkey.API_KEY)
    print(test.get_traffic_time('Skyline College')['rows'][0]['elements'][0]['duration']['value'])
    #print(gmaps.Client(matrixkey.API_KEY).geolocate())