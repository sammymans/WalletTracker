#import requests
import pip._vendor.requests as requests
import telegram

from bs4 import BeautifulSoup

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
    telegram_bot_sendtext("same")
else:
    # if the transactions are different, need to send telegram message saying what was traded
    # get the contract address of the token traded & and the amount traded in ETH

    





    print("diff")
    # send telegram message
    telegram_bot_sendtext("diff")


etherscan_url = 'https://etherscan.io/address/' + address
page = requests.get(etherscan_url)
soup = BeautifulSoup(page.content, 'html.parser')
page.close()

#print(soup.prettify())
recent_txn = soup.find_all('span', style=True)
print(recent_txn)

#u-label u-label--xs u-label--info rounded text-dark text-center

# print all of the transactions with select data
# for i,transaction in enumerate(result):
#     time = transaction.get("timeStamp")
#     hash = transaction.get("hash")
#     tx_from = transaction.get("from")
#     tx_to = transaction.get("to")
#     tx_value = transaction.get("value")

#     print("Transaction # ", i)
#     print("time: ", time)
#     print("hash: ", hash)
#     print("from address: ", tx_from)
#     print("to address: ", tx_to)
#     print("value: ", float(tx_value)*0.000000000000000001)
#     print("\n")


    



