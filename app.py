import json
import pandas as pd
import time
import requests
import argparse

with open('param.json') as json_data:
    parms = json.load(json_data)

def getArgs():
    parser = argparse.ArgumentParser(description='TrueSight Intelligence - Bulk Metrics Ingestion')
    parser.add_argument('-f', help='Filename - enter full file path to metric XLS file', required=False)
    parser.add_argument('-m', help='Metric Name', required=False)
    parser.add_argument('-l', help='Limit - number of rows to process in each batch.  DEFAULT: 1000', required=False)
    parser.add_argument('-t', help='Test mode - print output, but do not send measures', action="store_true", required=False)
    args = parser.parse_args()

    return args

def create_metric():

    metric = {
            "name": "Total_Ticket_Count",
            "description": "Total Ticket Count",
            "displayName": "Total Ticket Count",
            "displayNameShort": "TotalTicketCount",
            "unit": "number",
            "defaultAggregate": "sum",
            "type": "Remedy"
        }

    r = requests.post(parms['metricapi'], data=json.dumps(metric), headers=parms['headers'], auth=(parms['email'], parms['apikey']))
    print("Metric Status: %s - %s" % (r.status_code,r.reason))

def parse_data(file):

    df = pd.read_excel(file)

    data = []
    for index, row in df.iterrows():
        tup = (row['ts'], row['incident_count'])
        data.append(tup)

    return sorted(data, key=lambda tup: tup[0])

def create_batch(data,limit):

    measures = []
    measuresbatch = []
    measurecount = 1 # start at 2 since header is 1
    batchcount = 1

    print("Total number of measures: %s" % len(data))

    for item in data:

        print("Measure num: %s of %s" % (measurecount,len(data)))
        print(item)

        measure = [
            "Remedy",  # source
            "Total_Ticket_Count",  # display name
            int(item[1]),  # measure
            int(item[0]),  # timestamp
            {"app_id": parms['app_id']}  # metadata
        ]

        measures.append(measure)

        if measurecount == len(data):
            print("creating final batch...")
            measuresbatch.append(measures)
        elif batchcount < limit:
            batchcount = batchcount + 1
        else:
            batchcount = 1
            print("creating batch...")
            measuresbatch.append(measures)
            measures = []
            time.sleep(5)

        measurecount = measurecount + 1

    return measuresbatch


def send_measures(payload):

    for chunk in payload:
        try:
            r = requests.post(parms['measurementsapi'], data=json.dumps(chunk), headers=parms['headers'], auth=(parms['email'], parms['apikey']))
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        else:
            print("Measurements Response Code: %s" % r.status_code)
        finally:
            time.sleep(5)


def main():
    args = getArgs()

    if args.l:
        limit = args.l
    else:
        limit = 1000

    print("Limit: %s" % limit)

    # Create metric
    #create_metric()

    # Extract and Parse data
    data = parse_data(parms['file'])

    # Create payload
    payload = create_batch(data,limit)

    if args.t == True:
        print("Test mode enabled - no data sent.")
    else:
        send_measures(payload)

if __name__ == "__main__":
    main()
