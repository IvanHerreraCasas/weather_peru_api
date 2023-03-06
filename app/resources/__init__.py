from flask import jsonify

def get_available_stations(city):
    # TODO: Implement logic to get list of available stations
    stations = [
        {'name': 'Station A', 'location': 'Lima', 'lat': -12.0464, 'lon': -77.0428},
        {'name': 'Station B', 'location': 'Cusco', 'lat': -13.5319, 'lon': -71.9675},
        {'name': 'Station C', 'location': 'Arequipa', 'lat': -16.409, 'lon': -71.5375}
    ]
    return jsonify(stations)
