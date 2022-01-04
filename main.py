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

import schedule
import time

import datetime

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(current_time)

# function to send message to telegram bot
def telegram_bot_sendtext(bot_message):

    bot_token = ''
    bot_chatID = '1908664243'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

# function to fetch addresses from the config file
def get_addresses():
    address_list = []

    with open('config.txt') as file:
        for line in file:
            address_list.append(line.strip())

    return address_list


def run():
    
    address_list = get_addresses()
    print(address_list)

    for wallet_address in address_list:

        # --------------------------------- ACCESS THE ETHERSCAN WEBSITE FOR THE WALLET --------------------------------

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

        # Make new array that holds the transaction hashes
        new_result = []
        for i in range(len(result)):
            new_result.append(result[i]['hash'])

        # --------------------------------------------------------------------------------------------------

        # --------------------------------- IF LOG FILE EXISTS, GET LAST TXN AND UPDATE --------------------------------

        # Check if a log file exists for the wallet we are analyzing
        if os.path.isfile(address + 'log.txt'):
            print("File exists")

            # get the last transaction hash code from txt file
            with open(address + 'log.txt') as f:
                for line in f:
                    pass
                last_txn = line.strip('\n')

            print("Last Txn: " + last_txn)

            # write the updated information to a txt file
            f = open(address + 'log.txt','w')

            for i in range(len(new_result)):
                f.writelines(str(new_result[i]))
                f.write("\n")

            f.close()
        
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------- IF LOG FILE EXISTS, CHECK, IF NOT WRITE A FILE --------------------------------

        # If log file exists
        if os.path.isfile(address + 'log.txt'):

            new_txn = new_result[-1]
            print("New Txn: " + new_txn)

            # Determine if the latest transaction is in new/same as last by looking at transaction hash code


            # CHANGE FOR DEBUGGING != OR ==


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

                # ---------------------------- GET THE LINK FOR THE TXN HASH (LATEST ONE) --------------------------

                # COMMENT OUT FOR DEBUGGING        
                last_txn_url = 'https://etherscan.io/tx/' + last_txn

                # ----------------------------------------------------------------------------------------------------

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
                #last_txn_url = 'https://etherscan.io/tx/0x0a01bd507b8fac5f757d1be210666438d53b72bfa8c26eaa63d63aeb87c71fdd'
                
                # ---------------------------- GET THE TYPE OF METHOD FOR THE TRANSACTION --------------------------

                methods = []
                for span in etherscan_soup.find_all('span', attrs={'class':'u-label u-label--xs u-label--info rounded text-dark text-center'}):
                    methods.append(span.text)
                
                last_method = methods[0]
                print(last_method)

                # ----------------------------------------------------------------------------------------------------


                last_txn_req = Request(last_txn_url, headers={'User-Agent': 'Chrome/96.0.4664.110'})

                last_txn_response = urlopen(last_txn_req, timeout=1).read()
                last_txn_response_close = urlopen(last_txn_req, timeout=1).close()

                last_txn_soup = BeautifulSoup(last_txn_response, "html.parser")

                # ---------------------------- GET THE STATUS (SUCCESS/FAIL) OF THE TRANSACTION --------------------------

                for data in last_txn_soup.find_all('div', attrs={'class': 'col col-md-9'}):
                    status = data.text
                
                if status == "Fail":
                    print("Status of txn is 'Fail'")
                else:
                    print("Status of txn is 'Success'")

                    # Check if one of transfer, multicall, approve, claim, swap:

                    # Transfer
                    if last_method == "Transfer":
                        print("TRANSFER BETWEEN TWO WALLETS")

                    # Claim
                    elif last_method == "Claim":
                        
                        media_bodies = []
                        for ye in last_txn_soup.find_all('div', attrs={'class': 'media-body'}):
                            media_bodies.append(ye)

                        txn_action = media_bodies[0]
                        # print(txn_action)
                        
                        print("CLAIM TOKENS")
                        ca_html_claim = (txn_action.find('a', href = True))
                        ca_html_claim = str(ca_html_claim.get('href'))
                        ca_claim = ca_html_claim[7:49]
                        
                        telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + address + "\n" + "\U0001F4B0 Claimed \U0001F4B0 \n" + "*Token:* " + ca_claim)

                    # Approve
                    elif last_method == "Approve":
                        media_bodies = []
                        for ye in last_txn_soup.find_all('div', attrs={'class': 'media-body'}):
                            media_bodies.append(ye)

                        txn_action = media_bodies[0]
                        print(txn_action)

                        print("APPROVED TOKENS")
                        ca_html_approve = (txn_action.find('a', href = True))
                        ca_html_approve = str(ca_html_approve.get('href'))
                        ca_approve = ca_html_approve[7:]

                        telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + address + "\n" + "\U00002705 Approved \U00002705 \n" + "*Token:* " + ca_approve)

                    # swap
                    elif last_method == "Multicall" or last_method == "Swap Exact Token":
                        media_bodies = []
                        for ye in last_txn_soup.find_all('div', attrs={'class': 'media-body'}):
                            media_bodies.append(ye)

                        txn_action = media_bodies[0]
                        print(txn_action)

                        print("SWAPPED")
                        ca_html_swap = (txn_action.find('a', class_='mr-1 d-inline-block'))
                        print(ca_html_swap)

                        wrapped_eth_address = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                        if ca_html_swap == None:
                            ca_links = []
                            for a in txn_action.find_all('a'):
                                ca_links.append(a.get('href'))
                            
                            ca_link = ca_links[-1][7:]

                            if ca_link == wrapped_eth_address:
                                print("change")
                                txn_action_weird = media_bodies[1]

                                ca_links2 = []
                                for a in txn_action_weird.find_all('a'):
                                    ca_links2.append(a.get('href'))
                                
                                #print(ca_links2)

                                ca_link = ca_links2[-1][7:]   
                            
                            telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + address + "\n" + "\U0001F4EC TRADED WITH \U0001F4EC \n" + "*Token:* \n" + ca_link)

                        else:                        
                            
                            ca_html_swap = str(ca_html_swap.get('href'))
                            print(ca_html_swap)
                            ca_swap = ca_html_swap[7:]
                            print(ca_swap)

                            words = []
                            for content in txn_action.find_all('span', class_='mr-1 d-inline-block'):
                                words.append(content.text)
                            
                            print(words)

                            # Check if it is a buy or a sell
                            if words == []:
                                print("WRAPPED ETH SWAP")
                            elif words[1] == "Ether":
                                print("SWAPPED - BUY")
                                telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + address + "\n" + "\U0001F4EC Swapped - BUY \U0001F4EC \n" + "*Token:* \n" + words[0] + " " + words[1] + "\nFor " + words[2] + " " + ca_swap)
                            elif words[2] == 'Ether':
                                print("SWAPPED - SELL")
                                telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + address + "\n" + "\U0001F4EC Swapped - SELL \U0001F4EC \n" + "*Token:* \n" + words[0] + " " + ca_swap + "\nFor " + words[1] + " " + words[2])
                        # else:
                        #     print("other")
                    # Unknown txn
                    else:
                        print("UNKNOWN TRANSACTION TYPE")

        else:
            print("file does not exist, file created")
            f = open(address + 'log.txt','w')

            for i in range(len(new_result)):
                f.writelines(str(new_result[i]))
                f.write("\n")

            f.close()     

        print("\n")


schedule.every(10).seconds.do(run)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)





    



