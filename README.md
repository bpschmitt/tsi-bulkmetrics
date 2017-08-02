# tsi-bulkmetrics

#### Description

This script assists in loading metric data into TrueSight Intelligence.

- app.py - this is the main script
- param.json - this is the configuration file

#### Pre-requisites
- Python 3.x
- json
- pandas
- time
- requests

#### Known Issues

- The measurement limit does not work properly yet.  I believe there is a limit to the number of measurements
you can send at one time (1250 maybe?) so keep an eye on the response codes.

#### To-Do

- Move metric create json into configuration file.
- Fix bulk measurement limit/chunk size