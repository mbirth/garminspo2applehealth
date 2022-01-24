Garmin SpO2 to Apple Health
===========================

For some reason, Garmin Connect on iOS doesn't sync Blood Oxygen (SpO2) data into Apple Health
despite syncing various other metrics perfectly fine already.

There's a [feature request](https://forums.garmin.com/apps-software/mobile-apps-web/f/garmin-connect-mobile-ios/254977/request-for-spo2-vo2-max-and-respiration-data-to-be-shared-to-apple-health-app)
in their forums from February 2021, but apart from "We've added this to our feature request list"
nothing came of it in the past 11 months. And I found similar requests as old as [over 4 years (June 2018)](https://forums.garmin.com/outdoor-recreation/outdoor-recreation/f/fenix-5-plus-series/147239/spo2-measurements).

Until Garmin finds the 5 minutes to implement this feature, I've resorted to use the wonderful
[garminconnect](https://github.com/cyberjunky/python-garminconnect) Python-library to download
my SpO2 data, a PHP script to serve the data from the last 2 days as JSON and an iOS Shortcut to
sync that to Apple Health.

While it's not the most elegant solution, it works.


Usage
-----

1. Copy `auth.py.example` to `auth.py` and edit it to specify your Garmin Connect credentials
2. Copy `spo2_empty.db3` to `spo2.db3`
3. Run `pipenv install` to install dependencies
4. Make a cronjob running `pipenv run ./fetch.py` regularly
5. Copy the script from the `php` folder to a webserver and edit the file to point to the SQLite
   database file.
6. Install the [SpO2 Inserter Shortcut](https://www.icloud.com/shortcuts/7f6f94eb536e4fb1857993bfbc181ccb)
   on your iPhone and point it to the PHP script.
7. Optional: Create an Automation in Shortcuts to run this automatically.
