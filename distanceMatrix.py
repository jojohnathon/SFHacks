import googlemaps as gmaps
class distanceMatrix:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = gmaps.Client(api_key)

    def get_traffic_time(self, dest, mode=0, model=0):
        modes = ["driving", "transit"]
        models = ['best_guess', 'optimistic', 'pessimistic']

        return gmaps.distance_matrix(
            origin = self.client.geolocate(), 
            destinations = dest, 
            mode=modes[mode],
            traffic_model = models[model]
        )['location']