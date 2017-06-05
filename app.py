import json
import pandas as pd
import dateutil.parser
import time
import requests

with open('param.json') as json_data:
    parms = json.load(json_data)

def create_metric():

    metric = {
            "name": "Metric_Name",
            "description": "Metric Description",
            "displayName": "Metric Display Name",
            "displayNameShort": "Metric Display Name Short",
            "unit": "number",
            "defaultAggregate": "avg",
            "type": "Metric"
        }

    r = requests.post(parms['metricapi'], data=json.dumps(metric), headers=parms['headers'], auth=(parms['email'], parms['apikey']))
    print("Metric Status: %s" % r.status_code)

def parse_data(file):

    df = pd.read_excel(file)

    data = []
    for index, row in df.iterrows():
        dt = dateutil.parser.parse(str(row['ts']))
        ts = int(time.mktime(dt.timetuple()))
        tup = (ts, row['value'])
        data.append(tup)

    return sorted(data, key=lambda tup: tup[0])

def create_batch(data):

    measures = []
    for item in data:
        measure = [
            "ServerName", #source
            "MetricName", #metric
            item[1], #measure
            item[0], #timestamp
            { "app_id": parms['app_id'] } #metadata
        ]
        measures.append(measure)

    return json.dumps(measures)


def send_measures(batch):
    r = requests.post(parms['measurementsapi'], data=batch, headers=parms['headers'], auth=(parms['email'], parms['apikey']))
    print("Measurements Status: %s" % r.status_code)



# Create metric
create_metric()

# Extract and Parse data
data = parse_data(parms['file'])
print(data)

# Create batch of measurements
batch = create_batch(data)
print(batch)

# Send measurements
send_measures(batch)
