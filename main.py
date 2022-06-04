import pandas as pd
import datetime as dt
import smtplib
import os
from random import randint

# Email data

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")

# Actual time data

now = dt.datetime.now()
now_year = now.year
now_month = now.month
now_day = now.day

# Pandas reader

data = pd.read_csv("birthdays.csv")
data = data.to_dict(orient="records")

birthday_data = {}
for item in data:
    if item["month"] == now_month and item["day"] == now_day:
        birthday_data = {"name": item['name'], "email": item["email"]}
        files = []
        file_path = f"letter_templates/letter_{randint(1, 3)}.txt"

        with open(file_path) as letter_file:
            msg = letter_file.read()
            msg = msg.replace("[NAME]", birthday_data["name"])

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=birthday_data['email'],
                                msg=f"Subject: Happy Birthday\n\n{msg}")
