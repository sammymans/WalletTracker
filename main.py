#import requests
from typing import Text, final
from bs4 import BeautifulSoup
import requests

import urllib.request
from urllib.request import Request, urlopen
import pandas as pd

import re
import telegram

import os

import emoji


# function to send message to telegram bot
def telegram_bot_sendtext(bot_message):

   bot_token = ''
   bot_chatID = '1908664243'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()

address_list = ['0x2812B2eAe0533d2aD78e647792ae800DD78321dc', 
                '0x8FDA3f6b19dF2091bead80E35E8a5d6Cb1E4a0c0', 
                '0xD3057d9c2315EbAB53b84659D4cAc71fEf7031Ee',
                '0x15A7DAF8a04942cA22d14B2e431578d939C5b2C0',
                '0xa78AA318431A86b77a9621C357c4a7D9eBb46827',
                '0x01AbA45695FD77EB95A6C194873cf3617aAe4798']

print("\nNew: ")
for wallet_address in address_list:

    module = "account"
    action = "txlist"
    address = wallet_address              # <------ WALLET ADDRESS
    startblock = "0"
    endblock = "99999999"
    page="1"
    offset="" # leave empty to print all
    sort="asc"
    apikey=""

    # take out s out of https???
    url_txns = "https://api.etherscan.io/api?module=" + module + "&action=" + action +"&address=" + address + "&startblock=" + startblock + "&endblock="+ endblock + "&page="+ page+"&offset="+ offset +"&sort="+sort+"&apikey=" + apikey

    # api call
    response = requests.get(url_txns)

    # retrieve 'result' and put into a dictionary
    address_content = response.json()
    result = address_content.get("result")
    #print(result)
    #print(result[-1])
    #print(type(result))

    new_result = []
    #print(type(new_result))

    parameters = ["blockNumber", "timeStamp", "hash", "nonce", "blockHash", "transactionIndex", "from", "to", "value", "gas", "gasPrice", "isError", "txreceipt_status", "input", "contractAddress", "cumulativeGasUsed", "gasUsed", "confirmations"]
    new_parameters = ["blockNumber", "timeStamp", "nonce", "blockHash", "transactionIndex", "gas", "gasPrice", "isError", "txreceipt_status", "input", "contractAddress", "cumulativeGasUsed", "gasUsed", "confirmations"]

    # wanted parameters: ["hash", "from", "to", "value"]
    # Make new array with wanted parameters

    for i in range(len(result)):
        new_result.append(result[i]['hash'])

    # print(new_result)

    # TEST PRINT
    # print(new_result)
    # for i, transaction in enumerate(new_result):
    #     print("TRANSACTION: ", i)
    #     print(transaction)

    # Check if a log file exists for the wallet we are analyzing
    if os.path.isfile(address + 'log.txt'):
        print("File exists")

        # get the last transaction hash code from txt file
        with open(address + 'log.txt') as f:
            for line in f:
                pass
            last_txn = line.strip('\n')

        print(last_txn)

        # write the updated information to a txt file
        f = open(address + 'log.txt','w')

        for i in range(len(new_result)):
            f.writelines(str(new_result[i]))
            f.write("\n")

        f.close()

    # If log file exists
    if os.path.isfile(address + 'log.txt'):

        # Determine if the latest transaction is in new/same as last by looking at transaction hash code <-------------------------------
        new_txn = new_result[-1]
        print(new_txn)

        if new_txn == last_txn:
            print("No new transactions have been made on wallet address: \n " + address)
            # telegram_bot_sendtext("same")
        else:
            # if the transactions are different, need to send telegram message saying what was traded
            # get the contract address of the token traded & and the amount traded in ETH

            etherscan_url = "https://etherscan.io/address/" + address
            etherscan_req = Request(etherscan_url, headers={'User-Agent': 'Chrome/96.0.4664.110'})

            # add code for timeout?

            etherscan_response = urlopen(etherscan_req, timeout=1).read()
            etherscan_response_close = urlopen(etherscan_req, timeout=1).close()

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
                    #pass # COMMENT OUT LATER

            #test cases:

            # transfer
            #last_txn_url = 'https://etherscan.io/tx/0x4ba8c56b0ec48d217032304b5c676de144d80d52825a67300afca157303cb3f9'
            # multicall
            #last_txn_url = 'https://etherscan.io/tx/0x433d8e08e23339d047479253aaf7f0edb8190a66d9eedc03ba537d6cb7adc746'
            # approve
            #last_txn_url = 'https://etherscan.io/tx/0xd4c216586e2a43a5b90729606617a70e75b04bb6beb7cc8cf9ec26641df907a4'
            # claim
            #last_txn_url = 'https://etherscan.io/tx/0xf302d087828d507c4cfd7c33d0ea7cc9377f57d3b6372ce52a33ea094222af5d'
            # swap (buy)
            #last_txn_url = 'https://etherscan.io/tx/0xa0cf45db93e2e436e3810a9f1664ee8b6305afd35956881286c949ceb0574b45'
            # swap (sell)
            #last_txn_url = 'https://etherscan.io/tx/0x433d8e08e23339d047479253aaf7f0edb8190a66d9eedc03ba537d6cb7adc746'
            # warning
            #last_txn_url = 'https://etherscan.io/tx/0x2b0b58fbe52f272889097b74c3ae9b238c6001a8efdbf16cf45bdc4c38a54c4f'

            #random
            #last_txn_url = 'https://etherscan.io/tx/0x4ac2bc3109906e8765313648847f0c54236fd6fd1393725e1fb3f213c7492620'
            

            # print(last_txn_url)
            # print(type(last_txn_url))

            last_txn_req = Request(last_txn_url, headers={'User-Agent': 'Chrome/96.0.4664.110'})

            last_txn_response = urlopen(last_txn_req, timeout=1).read()
            last_txn_response_close = urlopen(last_txn_req, timeout=1).close()

            last_txn_soup = BeautifulSoup(last_txn_response, "html.parser")

            # print(last_txn_soup)

            # If status of the transaction is a fail, exit
            for data in last_txn_soup.find_all('div', attrs={'class': 'col col-md-9'}):
                status = data.text
            
            if status == "Fail":
                print("Status is 'Fail'")
            else:
                print("Status is 'Success'")

                # need function to wait while transaction is pending
                # while(status == "Pending"):
                #     print("waiting")

                # Check if one of transfer, multicall, approve, claim, swap:

                media_bodies = []
                for ye in last_txn_soup.find_all('div', attrs={'class': 'media-body'}):
                    media_bodies.append(ye)

                # if media_bodies is empty --> transfer between wallets
                if media_bodies == []:
                    print("Transfer between two wallets")
                else:
                    txn_action = media_bodies[0]
                    #print(txn_action)

                    txn_detail = []
                    for ye in txn_action.find_all('span', attrs={'class': 'text-secondary mr-1 d-inline-block'}):
                        txn_detail.append(ye)

                    # if txn_detail is empty --> claim tokens
                    if txn_detail == []:
                        print("CLAIM TOKENS")
                        ca_html_claim = (txn_action.find('a', href = True))
                        ca_html_claim = str(ca_html_claim.get('href'))
                        ca_claim = ca_html_claim[7:49]
                        
                        telegram_bot_sendtext("*Wallet:* " + address + "\n" + "\U0001F4B0 Claimed \U0001F4B0 \n" + "*Token:* " + ca_claim)

                    # else must be either an approval or a swap of tokens
                    else:
                        # If message says "Approved" --> approved
                        if txn_detail[0].text == "Approved":
                            print("APPROVED TOKENS")
                            ca_html_approve = (txn_action.find('a', href = True))
                            ca_html_approve = str(ca_html_approve.get('href'))
                            ca_approve = ca_html_approve[7:]

                            telegram_bot_sendtext("*Wallet:* " + address + "\n" + "\U00002705 Approved \U00002705 \n" + "*Token:* " + ca_approve)

                        # Else, must be a swap
                        else:
                            # txn_actions = last_txn_soup.find_all('a', class_='mr-1 d-inline-block')
                            # print(txn_actions)

                            print("SWAPPED")
                            ca_html_swap = (txn_action.find('a', class_='mr-1 d-inline-block'))
                            ca_html_swap = str(ca_html_swap.get('href'))
                            ca_swap = ca_html_swap[7:]
                            #print(ca_swap)

                            words = []
                            for content in txn_action.find_all('span', class_='mr-1 d-inline-block'):
                                words.append(content.text)
                            
                            print(words)

                            # Check if it is a buy or a sell
                            if words[1] == "Ether":
                                telegram_bot_sendtext("*Wallet:* " + address + "\n" + "\U0001F4EC Swapped - BUY \U0001F4EC \n" + "*Token:* \n" + words[0] + " " + words[1] + "\nFor " + words[2] + " " + ca_swap)
                            else:
                                telegram_bot_sendtext("*Wallet:* " + address + "\n" + "\U0001F4EC Swapped - SELL \U0001F4EC \n" + "*Token:* \n" + words[0] + " " + ca_swap + "\nFor " + words[1] + " " + words[2])

    else:
        print("file does not exist, file created")
        f = open(address + 'log.txt','w')

        for i in range(len(new_result)):
            f.writelines(str(new_result[i]))
            f.write("\n")

        f.close()     

    print("\n")








    



