from bottle import run, static_file, route


import flights


@route('/')
def root():
    return static_file('file.html', root='')


@route('/flight_map.js')
def static():
    return static_file('flight_map.js', root='')


@route('/flights/<lat>/<lon>')
def get_flights(lat, lon):
    return flights.map_planes(flights.flight_data(), float(lat), float(lon))


run(debug=True, port=8090, host='0.0.0.0')
