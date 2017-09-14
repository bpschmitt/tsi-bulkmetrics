# tsi-bulkmetrics

#### Description

This script assists in creating metrics and loading measurement data into TrueSight Intelligence.

- tsi-bulkmetrics.py - main script
- metric.json - metric configuration file

```
usage: tsi-bulkmetrics.py [-h] {metric,measures} ...

TrueSight Intelligence - Bulk Measures Ingestion

positional arguments:
  {metric,measures}  sub_command help
    metric           Options for Creating a Metric
    measures         Options for Sending Measurements

optional arguments:
  -h, --help         show this help message and exit
```

#### Examples
```
python tsi-bulkmetrics.py metric -f metric.json -e myemail@email.com -k my-api-key-goes-here
```

```
python tsi-bulkmetrics.py measures -s Remedy -m MY_COOL_METRIC -a MyApp -e myemail@email.com -k my-api-key-goes-here -tscol myts -valcol metric_name -f /path/to/measurements.xlsx
```

#### Pre-requisites
- Python 3.x
- json
- pandas
- time
- requests
- argparse

#### What the Script Does

- Creates TSI metrics from the command line by parsing the metric.json file
- Loads measurement data in bulk (DEFAULT: 500 measures at once) from an Excel file

#### There are some limitations, however

- Currently, it only reads a single timestamp and metric value