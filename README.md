# tsi-bulkmetrics

### Description

This script assists in creating metrics and loading measurement data into TrueSight Intelligence.

- tsi-bulkmetrics.py - main script
- metric.json - metric configuration file

### Pre-requisites
- Python 3.x
- json
- pandas
- time
- requests
- argparse

### What the script does

- Creates TSI metrics from the command line by parsing the metric.json file
- Loads measurement data in bulk (DEFAULT: 500 measures at once) from an Excel file

### There are some limitations, however

- Currently, it only reads a single timestamp and metric value

#### Options for Creating a Metric
```
usage: tsi-bulkmetrics.py metric [-h] -k APIKEY -e EMAIL -f METRICFILE

optional arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --apikey APIKEY
                        TrueSight Intelligence API Key
  -e EMAIL, --email EMAIL
                        TrueSight Intelligence Account Email
  -f METRICFILE, --metricfile METRICFILE
                        File containing metric JSON definition
```

#### Options for Sending Measurements
```
usage: tsi-bulkmetrics.py measures [-h] -k APIKEY -e EMAIL -f MEASURESFILE -s
                                   SOURCE -m METRICNAME -a APPID
                                   [-tscol TSCOL] [-valcol VALCOL]

optional arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --apikey APIKEY
                        TrueSight Intelligence API Key
  -e EMAIL, --email EMAIL
                        TrueSight Intelligence Account Email
  -f MEASURESFILE, --measuresfile MEASURESFILE
                        Excel file containing measurement data
  -s SOURCE, --source SOURCE
                        Measurement source (e.g. MyServer)
  -m METRICNAME, --metricname METRICNAME
                        Name of Metric (e.g. MY_COOL_METRIC)
  -a APPID, --appid APPID
                        TrueSight Intelligence App ID
  -tscol TSCOL          Column name of timestamp data. DEFAULT: ts
  -valcol VALCOL        Column name of measure data. DEFAULT: value
```

### Examples
#### Create a Metric
```
python tsi-bulkmetrics.py metric -f metric.json -e myemail@email.com -k my-api-key-goes-here
```
#### Send Measurements
```
python tsi-bulkmetrics.py measures -s Remedy -m MY_COOL_METRIC -a MyApp -e myemail@email.com -k my-api-key-goes-here -tscol myts -valcol metric_name -f /path/to/measurements.xlsx
```

