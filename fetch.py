#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import sqlite3
from auth import USERNAME, PASSWORD, DAYS_TO_FETCH
from pprint import pprint
from time import sleep
from garminconnect import (
    Garmin,
    GarminConnectConnectionError
)

today = datetime.date.today()
startfrom = today - datetime.timedelta(days=DAYS_TO_FETCH)

print(f"Logging into Garmin Connect using {USERNAME}.")
api = Garmin(USERNAME, PASSWORD)

tries = 0
while True:
    try:
        api.login()
        break
    except GarminConnectConnectionError as e:
        tries += 1
        wait = tries
        if wait > 2:
            wait = 2
        print(f"Error during login! Retry #{tries} in {wait} sec.", flush=True)
        sleep(wait)

db = sqlite3.connect("spo2.db3")

reqday = startfrom
while reqday <= today:
    print("Querying data for: {}".format(reqday.isoformat()))
    sleep = api.get_sleep_data(reqday.isoformat())
    #pprint(sleep)

    if not "wellnessEpochSPO2DataDTOList" in sleep:
        print("No SpO2 data for {}. Skipping day.".format(reqday.isoformat()))
        reqday += datetime.timedelta(days=1)
        continue

    spo2 = sleep["wellnessEpochSPO2DataDTOList"]
    #pprint(spo2)

    print("Got {} records.".format(len(spo2)))

    for rec in spo2:
        ts = datetime.datetime.fromisoformat(rec["epochTimestamp"][:-2])   # strip hundreds of seconds
        sql = "INSERT OR IGNORE INTO spo2 VALUES (?, ?, ?)"
        db.execute(sql, [ts.timestamp(), rec["spo2Reading"], rec["readingConfidence"]])

    reqday += datetime.timedelta(days=1)

db.commit()
db.close()

api.logout()
