import json
import math
from urllib import request, parse
from geopy.distance import geodesic
import requests


def flight_data():
    res = requests.get("https://argiedel:Argie101!@opensky-network.org/api/states/all").json()
    return res


def meters_to_latitude(m):
    return m / 111111


def meters_to_longitude(m, lat):
    return (m * math.cos(lat)) / 111111


def within_area(usr_lat, usr_lon, plane_lat, plane_lon, seeing_distance):
    try:
        user = (usr_lat/2, usr_lon)
        plane = (plane_lat/2, plane_lon)
    except TypeError:
        return False
    return geodesic(user, plane).kilometers < seeing_distance


def only_within(plane_data, vis_range, lat, lon):
    plane_list = []
    for plane in plane_data['states']:
        if within_area(lat, lon, plane[6], plane[5], vis_range):
            plane_list.append(plane)
    return plane_list


def weather_within(lat, lon):
    q = (('lat', lat), ('lon', lon), ('key', '035b6785ed234522b2c9dcb513611690'))
    q_parse = parse.urlencode(q)
    res = request.urlopen('http://api.weatherbit.io/v2.0/current' + '?' + q_parse)
    content = res.read().decode()
    data = json.loads(content)['data']
    return data


def cloud_obstruction(data, percent):
    return data[0]['clouds'] > percent


def visible_within_cloud(plane_data, weather_data, obstruction_percent):
    if not cloud_obstruction(weather_data, obstruction_percent):
        for plane in plane_data:
            if plane[7] and plane[7] > 1981.2:
                del plane
    return plane_data


def remove_grounded(plane_data):
    for plane in plane_data:
        if plane[8]:
            del plane
    return plane_data


def map_planes(plane_data, lat, lon):
    weather_data = weather_within(lon, lat)
    plane_data = only_within(plane_data, 20, lat, lon)
    plane_data = remove_grounded(plane_data)
    plane_data = visible_within_cloud(plane_data, weather_data, 40)
    return json.dumps(plane_data)