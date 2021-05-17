import datetime
import json
from copy import deepcopy
from fake_useragent import UserAgent
import requests
import numpy as np
import pandas as pd
import sched, time

s = sched.scheduler(time.time, time.sleep)
min_age = 1
while min_age != 18 or min_age != 45:
    min_age = int(input("Enter minimum age 18 or 45: "))
    if min_age == 18 or min_age == 45:
        break
district_id = int(input("Enter district id, You can find district with there id in district_mapping.csv file: "))


def filter_column(df, col, value):
    df_temp = deepcopy(df.loc[df[col] == value, :])
    return df_temp


today = datetime.datetime.today()
fmt_today = today.strftime("%d-%m-%Y")

temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}


def runner(sc):
    print("NOTE: HIT Ctrl + C Multiple times if required to close Application")
    print(
        "Running at maximum speed of 3 seconds per request per IP, "
        "response could be stale by 30 min as per cowin API. Cowin APIs are geofenced")
    print("Default to BBMP District with District ID: 294 and Today's Date: {}".format(fmt_today))
    print("For other districts with there respective id check districts.csv file")
    print("Showing data for age: {}+ and district id: {}".format(min_age, district_id))
    print()
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
        district_id, fmt_today)

    response = requests.get(URL, headers=browser_header)

    if (response.ok):
        resp_json = json.loads(response.text)['centers']
        final_df = None
        if resp_json is not None:
            df = pd.DataFrame(resp_json)
            if len(df):
                df = df.explode("sessions")
                df['min_age_limit'] = df.sessions.apply(lambda x: x['min_age_limit'])
                df['vaccine'] = df.sessions.apply(lambda x: x['vaccine'])
                df['available_capacity'] = df.sessions.apply(lambda x: x['available_capacity'])
                df['date'] = df.sessions.apply(lambda x: x['date'])
                df = df[["date", "available_capacity", "vaccine", "min_age_limit", "pincode", "name", "state_name",
                         "district_name", "block_name", "fee_type"]]
                if final_df is not None:
                    final_df = pd.concat([final_df, df])
                else:
                    final_df = deepcopy(df)
                final_df = filter_column(final_df, "min_age_limit", min_age)
                print(final_df)
            else:
                print("No rows in the data Extracted from the API")
    print()
    print(
        "=============================================================================================================")
    print()
    s.enter(3, 1, runner, (sc,))


s.enter(3, 1, runner, (s,))
s.run()
