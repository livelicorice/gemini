#!/usr/bin/env python3.9

import argparse
from re import S
import sys
import datetime
import logging
import math
from unittest import result
import requests
import json
import statistics as stat
import numpy as np

logging.basicConfig(filename='gemini.log', level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


parser = argparse.ArgumentParser(description='Gemini Currency Alerting Tool')
parser.add_argument("--pair", default=None, type=str, required=True, help="Enter a currency pair. ie. btcusd")
parser.add_argument("--dev", default=1, type=int, help="Enter the maximum deviation allowed")
args = parser.parse_args()
pair = args.pair
dev = args.dev

base_url = "https://api.gemini.com/v1"
response = requests.get(base_url + "/symbols")
symbols = response.json()

def search(list, pair):
    for i in range(len(list)):
        if list[i] == pair:
            return True
    return False
if search(symbols, pair):
    logger.info("Currency Pair is valid.")
else:
    logger.error("Currency Pair does not exist! Choose a currency pair from the following...")
    #logger.error()
    logger.error(symbols)
    sys.exit()
    
price_base_url = "https://api.gemini.com/v1"
price_response = requests.get(price_base_url + "/pricefeed/" + pair)
pdata = price_response.json()
cprice = pdata[0]['price']
current_price = float(cprice)

base_url = "https://api.gemini.com/v2"
response = requests.get(base_url + "/ticker/" + pair)
all_data = response.json()
data = all_data["changes"]
ndata = list(map(float, data))

ct = datetime.datetime.now().isoformat()

# Finding the variance is essential before calculating the standard deviation
def varinc(val, ddof=0):
    n = len(val)
    m = sum(val) / n
    return sum((x - m) ** 2 for x in val) / (n - ddof)
# finding the standard deviation
def stddev(val):
    vari = varinc(val)
    stdev = math.sqrt(vari)
    return stdev

avg = stat.mean(ndata)
avg = (round(avg, 2))
std_dev = stat.pstdev(ndata)
std_dev = abs(round(std_dev, 3))

def magnitude(current_price, avg, std_dev):
    try:
        result = ( current_price - avg ) / std_dev
    except ZeroDivisionError:
        logger.error("tsk, tsk, Divide by Zero error. Increase precision of Standard Deviation")
    else:
        return result

mag = magnitude(current_price, avg, std_dev)
mag = abs(round(mag, 2))
bool = mag > dev

payload = json.dumps({"timestamp": ct,
                      "level": logging.getLevelName(20),
                      "trading_pair": pair,
                      "deviation_alert": bool,
                      "data": {
                        "list_price": current_price,
                        "average": avg,
                        "change": std_dev,
                        "sdev": mag
                    }}, indent=4)
print(payload)
