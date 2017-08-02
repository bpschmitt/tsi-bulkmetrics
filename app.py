import json
import pandas as pd
import time
import requests

with open('param.json') as json_data:
    parms = json.load(json_data)

def create_metric():

    metric = {
            "name": "MyMetric",
            "description": "This is my metric",
            "displayName": "My Metric",
            "displayNameShort": "MyMetric",
            "unit": "number",
            "defaultAggregate": "avg",
            "type": "Metric"
        }

    r = requests.post(parms['metricapi'], data=json.dumps(metric), headers=parms['headers'], auth=(parms['email'], parms['apikey']))
    print("Metric Status: %s - %s" % (r.status_code,r.reason))

def parse_data(file):

    df = pd.read_excel(file)

    data = []
    for index, row in df.iterrows():
        # dt = dateutil.parser.parse(str(row['ts']))
        # ts = int(time.mktime(dt.timetuple()))
        tup = (row['ts'], row['mymetric'])
        data.append(tup)

    return sorted(data, key=lambda tup: tup[0])

def create_batch(data):

    print("Count: %s" % len(data))
    limit = 1500

    for i in range(0, len(data), limit):
        measures = []
        for item in data[i:i+limit]:
            measure = [
                "Brad_Laptop", #source
                "MyMetric", #metric
                int(item[1]), #measure
                int(item[0]), #timestamp
                { "app_id": parms['app_id'] } #metadata
            ]
            #print(measure)
            measures.append(measure)

        print("sending %s" % len(measures))
        print(measures)
        send_measures(json.dumps(measures))
        #print(measures)
        #print(send_measures(json.dumps(measures)))
        time.sleep(2)


    #return json.dumps(measures)


def send_measures(batch):
    #pass

    r = requests.post(parms['measurementsapi'], data=batch, headers=parms['headers'], auth=(parms['email'], parms['apikey']))
    print("Measurements Status: %s" % r.status_code)
    return r.status_code


# Create metric
create_metric()

# Extract and Parse data
data = parse_data(parms['file'])
#print(data)

# Create and send batch of measurements
batch = create_batch(data)
#print(batch)

# Send measurements
#send_measures(batch)
