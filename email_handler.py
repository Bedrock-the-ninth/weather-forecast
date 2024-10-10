import os
import smtplib
import pandas as pd
from dotenv import load_dotenv

load_dotenv(".env")

EMAIL = os.getenv(EMAIL)
PASS = os.getenv(PASS)


def file_handler():
    df = pd.read_csv('email_list.csv')
    return [(row['name'], row['email']) for _, row in df.iterrows()]


class EmailDelivery:
    def __init__(self, message):
        self.message = message
        self.name_tuple, self.email_tuple = zip(*file_handler())
        self.delivery_agent()

    def delivery_agent(self):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASS)
            for name, email in zip(self.name_tuple, self.email_tuple):
                connection.sendmail(from_addr=EMAIL, to_addrs=email,
                                    msg=f"Subject:Your Favorite Weather Forecast is Back"
                                        f"\n\nDear {name},"
                                        f"\n{self.message}")
