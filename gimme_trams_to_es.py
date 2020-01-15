import urllib.request, json
from elasticsearch import Elasticsearch, helpers
import datetime
import time

elastic = Elasticsearch("localhost")

def map_to_es(obj):
    entity = {}
    location = {}
    entity_time = datetime.datetime.strptime(obj["Time"], '%Y-%m-%d %H:%M:%S')
    location["lat"] = obj["Lat"]
    location["lon"] = obj["Lon"]
    entity["location"] = location
    entity["brigade"] = obj["Brigade"]
    entity["line"] = obj["Lines"]
    entity["time"] = entity_time.isoformat()
    entity["vehicle_number"] = obj["VehicleNumber"]
    return entity

while True:

    buses = ''
    trams = ''
    api_key = 'gimme your api key!'
    with urllib.request.urlopen("https://api.um.warszawa.pl/api/action/busestrams_get/?apikey={0}&type=1&resource_id=f2e5503e927d-4ad3-9500-4ab9e55deb59".format(api_key)) as url:
        buses = json.loads(url.read().decode())['result']

    with urllib.request.urlopen("https://api.um.warszawa.pl/api/action/busestrams_get/?apikey={0}&type=2&resource_id=f2e5503e927d-4ad3-9500-4ab9e55deb59".format(api_key)) as url:
        trams = json.loads(url.read().decode())['result']

    buses.extend(trams)
    data = map(map_to_es,buses)
    data = list(data)
    print("Sending records...")
    helpers.bulk(elastic, data, index="ztm")
    time.sleep(10)
