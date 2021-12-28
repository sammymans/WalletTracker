#import requests
from typing import Text, final
from bs4 import BeautifulSoup
import requests

import urllib.request
from urllib.request import Request, urlopen
import pandas as pd

import re
import telegram

# function to send message to telegram bot
def telegram_bot_sendtext(bot_message):

   bot_token = '5082173588:AAESTXSXnmNG8PP0CjJXt0PyoJSNzcez610'
   bot_chatID = '1908664243'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()

module = "account"
action = "txlist"
address = "0x2812B2eAe0533d2aD78e647792ae800DD78321dc"
startblock = "0"
endblock = "99999999"
page="1"
offset="" #leave empty to print all
sort="asc"
apikey="YourApiKeyToken"

# take out s out of https???
url_txns = "https://api.etherscan.io/api?module=" + module + "&action=" + action +"&address=" + address + "&startblock=" + startblock + "&endblock="+ endblock + "&page="+ page+"&offset="+ offset +"&sort="+sort+"&apikey=" + apikey

# api call
response = requests.get(url_txns)

# retrieve 'result' and put into a dictionary
address_content = response.json()
result = address_content.get("result")
#print(result[-1])

new_result = result

parameters = ["blockNumber", "timeStamp", "hash", "nonce", "blockHash", "transactionIndex", "from", "to", "value", "gas", "gasPrice", "isError", "txreceipt_status", "input", "contractAddress", "cumulativeGasUsed", "gasUsed", "confirmations"]
new_parameters = ["blockNumber", "timeStamp", "nonce", "blockHash", "transactionIndex", "gas", "gasPrice", "isError", "txreceipt_status", "input", "contractAddress", "cumulativeGasUsed", "gasUsed", "confirmations"]

# wanted parameters: ["hash", "from", "to", "value"]
# Make new dictionary with wanted parameters

for i in range(len(new_result)):
    for param in new_parameters:
        del new_result[i][param]

# TEST PRINT
# print(new_result)
# for i, transaction in enumerate(new_result):
#     print("TRANSACTION: ", i)
#     print(transaction)

# get the last transaction hash code from txt file
with open('log.txt') as f:
    for line in f:
        pass
    last_txn = line.strip('\n')

print(last_txn)

# write the updated information to a txt file
f = open('log.txt','w')

for i in range(len(new_result)):
    f.writelines(str(new_result[i]["hash"]))
    f.write("\n")

f.close()

# Determine if the latest transaction is in new/same as last by looking at transaction hash code
new_txn = new_result[-1]["hash"]
print(new_txn)

if new_txn == last_txn:
    print("same")

    #telegram_bot_sendtext("same")
else:
    # if the transactions are different, need to send telegram message saying what was traded
    # get the contract address of the token traded & and the amount traded in ETH

    etherscan_url = "https://etherscan.io/address/" + address
    etherscan_req = Request(etherscan_url, headers={'User-Agent': 'Chrome/96.0.4664.110'})

    etherscan_response = urlopen(etherscan_req, timeout=0.5).read()
    etherscan_response_close = urlopen(etherscan_req, timeout=0.5).close()

    etherscan_soup = BeautifulSoup(etherscan_response, "html.parser")

    txn_table = etherscan_soup.find("table", attrs={"class": "table table-hover"})
    txn_table_data = txn_table.find_all("tr")

    links = []
    for link in etherscan_soup.find_all('a'):
        links.append(str(link.get('href')))
        
    for link in links:
        if last_txn in link:
            # url of txn hash block
            last_txn_url = 'https://etherscan.io' + link
            
    print(last_txn_url)
    print(type(last_txn_url))

    last_txn_req = Request(last_txn_url, headers={'User-Agent': 'Chrome/96.0.4664.110'})

    last_txn_response = urlopen(last_txn_req, timeout=0.5).read()
    last_txn_response_close = urlopen(last_txn_req, timeout=0.5).close()

    last_txn_soup = BeautifulSoup(last_txn_response, "html.parser")

    # print(last_txn_soup)

    media_bodies = []
    for ye in last_txn_soup.find_all('div', attrs={'class': 'media-body'}):
        media_bodies.append(ye)
        
    txn_action = media_bodies[0]
    print(txn_action)

    # txn_actions = last_txn_soup.find_all('a', class_='mr-1 d-inline-block')
    # print(txn_actions)

    ca_html = (txn_action.find('a', class_='mr-1 d-inline-block'))
    print(ca_html)
    ca = ca_html.get('href')
    final_ca = ca[7:]
    print(final_ca)

    print('\n')

    text = []
    for span in txn_action.findAll('span'):
        text.append(span.text)

    #print(text)

    amount_initial = str(text[1])
    token_initial = str(text[2])
    for_amount = str(text[4])
    token_ca = str(final_ca)
    message = "UniSwap Transaction With: " + token_ca

    print(message)
    print("diff")

    # send telegram message
    telegram_bot_sendtext(message)








    



