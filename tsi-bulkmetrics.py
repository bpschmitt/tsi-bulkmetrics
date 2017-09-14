import json
import pandas as pd
import time
import requests
import argparse

METRICAPI = "https://api.truesight.bmc.com/v1/metrics"
MEASUREMENTSAPI = "https://api.truesight.bmc.com/v1/measurements"
EVENTAPI = "https://api.truesight.bmc.com/v1/events"
BATCH = 500

# with open('param.json') as json_data:
#     parms = json.load(json_data)

def getArgs():

    parser = argparse.ArgumentParser(description='TrueSight Intelligence - Bulk Measures Ingestion')
    subparsers = parser.add_subparsers(help='You must choose one of these options', dest='command')

    # Metric options
    parser_metric = subparsers.add_parser('metric', help='Options for Creating a Metric')
    parser_metric.add_argument('-k','--apikey', help='TrueSight Intelligence API Key', required=True)
    parser_metric.add_argument('-e','--email', help='TrueSight Intelligence Account Email', required=True)
    parser_metric.add_argument('-f','--metricfile', help='File containing metric JSON definition', required=True)
    parser_metric.set_defaults(func=create_metric)

    # Measurement options
    parser_measures = subparsers.add_parser('measures', help='Options for Sending Measurements')
    parser_measures.add_argument('-k', '--apikey', help='TrueSight Intelligence API Key', required=True)
    parser_measures.add_argument('-e', '--email', help='TrueSight Intelligence Account Email', required=True)
    parser_measures.add_argument('-f','--measuresfile', help='Excel file containing measurement data', required=True)
    parser_measures.add_argument('-s', '--source', help='Measurement source (e.g. MyServer)', required=True)
    parser_measures.add_argument('-m', '--metricname', help='Name of Metric (e.g. MY_COOL_METRIC)', required=True)
    parser_measures.add_argument('-a', '--appid', help='TrueSight Intelligence App ID', required=True)
    parser_measures.add_argument('-tscol', help='Column name of timestamp data. DEFAULT: ts', default="ts", required=False)
    parser_measures.add_argument('-valcol', help='Column name of measure data. DEFAULT: value', default="value", required=False)
    parser_measures.set_defaults(func=send_measures)

    ## Troubleshooting

    # parser.add_argument('-t', '--test', help='Test mode: print output, but do not create metric or send measures', action="store_true", required=False)

    args = parser.parse_args()

    return args

def create_metric(args):

    print(args)

    try:
        with open(args.metricfile) as data_file:
            metric = json.load(data_file)
    except FileNotFoundError:
        print('ERROR: There was an error opening the metric JSON file. Please check the path and file name.')
        exit(1)
    else:
        print("Creating metric...")
        print(json.dumps(metric, indent=4))
        r = requests.post(METRICAPI, data=json.dumps(metric), headers={'Content-type': 'application/json'}, auth=(args.email, args.apikey))
        print("Metric Status: %s - %s" % (r.status_code,r.reason))

    return True

def parse_data(args):


    df = pd.read_excel(args.measuresfile)

    data = []
    for index, row in df.iterrows():
        tup = (row[args.tscol], row[args.valcol])
        data.append(tup)

    return sorted(data, key=lambda tup: tup[0])

def create_batch(data,args):

    measures = []
    measuresbatch = []
    measurecount = 1 # start at 2 since header is 1
    batchcount = 1

    print("Total number of measures: %s" % len(data))

    for item in data:

        print("Measure num: %s of %s" % (measurecount,len(data)))
        print(item)

        measure = [
            args.source,  # source
            args.metricname,  # metric name, identifier in Pulse.  Caps required
            int(item[1]),  # measure
            int(item[0]),  # timestamp
            {"app_id": args.appid}  # metadata
        ]

        measures.append(measure)

        if measurecount == len(data):
            print("Creating final batch...")
            measuresbatch.append(measures)
        elif batchcount < BATCH:
            batchcount = batchcount + 1
        else:
            batchcount = 1
            print("Creating batch...")
            measuresbatch.append(measures)
            measures = []
            # possible sleep here...

        measurecount = measurecount + 1

    return measuresbatch


def send_measures(args):

    print("Invoking send measures...")
    print(args)
    print(args.email)

    data = parse_data(args)
    payload = create_batch(data, args)

    for chunk in payload:
        try:
            print(chunk)
            r = requests.post(MEASUREMENTSAPI, data=json.dumps(chunk), headers={'Content-type': 'application/json'}, auth=(args.email, args.apikey))
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)
        else:
            #print(json.dumps(chunk,indent=4))
            print("Measurements Response Code: %s - %s" % (r.status_code, r.reason))
        finally:
            print("Resting for 5 seconds...")
            time.sleep(5)

    return True


def main():

    args = getArgs()
    #print(args)

    if args.command is not None:
        r = args.func(args)
    else:
        print("You forgot to specify 'metric' or 'measures'.")

    if r:
        exit(0)
    else:
        print("Something went wrong...")
        exit(1)

if __name__ == "__main__":
    main()
