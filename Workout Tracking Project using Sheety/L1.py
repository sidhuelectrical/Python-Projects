from dotenv import load_dotenv
import os
from input_validation import get_input
import requests as web

import datetime as dt
from zoneinfo import ZoneInfo
load_dotenv("api.env")  # Loading the env variables from this file

APP_ID = os.getenv("WORKOUT_API_ID")
API_KEY = os.getenv("WORKOUT_API_KEY")
BASE_URL = os.getenv("BASE_URL")
SHEETY_URL_ENDPOINT = os.getenv("SHEETY_URL_ENDPOINT")
date_formatted = dt.datetime.now(
    tz=ZoneInfo("Asia/Kolkata")).strftime("%d/%m/%Y")
time_formatted = dt.datetime.now(
    tz=ZoneInfo("Asia/Kolkata")).strftime("%H:%M:%S")


# Nutrition API Parameters
# Using a get_input function to ensure that the inputs are passed reliably

nutrition_headers = {"Content-Type": "application/json",
                     "x-app-id": APP_ID, "x-app-key": API_KEY}

query = get_input("What activity did you perform in gym today")
weight = get_input("what is your current weight in Kilograms",

                   # pyright: ignore[reportArgumentType]
                   cast=float, min_val=30, max_val=500)
height = get_input("What is your height in cm",

                   # pyright: ignore[reportArgumentType]
                   cast=float, min_val=100, max_val=300)
age = get_input("What is your age(in years)",

                # pyright: ignore[reportArgumentType]
                cast=float, min_val=15, max_val=150)
gender = get_input("What is your gender", choices=["male", "female"])
nutrition_param = {
    "query": query,
    "weight_kg": weight,
    "height_cm": height,
    "age": age,
    "gender": gender
}
nutrition_response = web.post(
    url=BASE_URL, json=nutrition_param, headers=nutrition_headers, timeout=10)
"""Using POST to sent the data to Sheety and using timeout function to stop and raise the exception requests.Timeout in case the response takes  more than 10 second"""
nutrition_response.raise_for_status()

# Parsing the provided response to json format
nutrition_response_json = nutrition_response.json()

if "exercises" not in nutrition_response_json:
    raise ValueError(f"Invalid API Response format{nutrition_response_json}")
"""Checking whether the response is valid or not"""


# Sheety application implementation

authentication_headers = {
    "Authorization": os.getenv("BEARER_TOKEN"),
}  # Using Bearer method for Authentication
for item in nutrition_response_json["exercises"]:
    data_to_be_passed = {"sheet1":
                         {
                             "date": date_formatted,
                             "time": time_formatted,
                             "exercise": item["name"].title(),
                             "duration": f"{item['duration_min']} min",
                             "calories": item["nf_calories"]

                         }}
    """ Here Sheety expects the duration to be passed as a string as "{duration_min} min " instead of int or float"""

    post_response = web.post(
        url=SHEETY_URL_ENDPOINT, json=data_to_be_passed, headers=authentication_headers)
    post_response.raise_for_status()
