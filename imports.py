# import libraries

import requests
import urllib.request

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

import os
import re

import telegram
import emoji

import schedule
import time
import datetime

# other files

from telegram_bot import telegram_bot_sendtext
from log_data import get_addresses, is_log_file, create_log_file, get_txns_and_last
from scrape import get_wallet_data, get_txns_and_last, get_addresses, get_txn_status, is_new_txn, scrape_etherscan, send_final_result