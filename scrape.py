from imports import *

def get_wallet_data(wallet_address):
    module = "account"
    action = "txlist"
    address = wallet_address              # <------ WALLET ADDRESS
    startblock = "0"
    endblock = "99999999"
    page="1"
    offset=""
    sort="asc"
    apikey=""

    url_txns = "https://api.etherscan.io/api?module=" + module + "&action=" + action +"&address=" + address + "&startblock=" + startblock + "&endblock="+ endblock + "&page="+ page+"&offset="+ offset +"&sort="+sort+"&apikey=" + apikey

    response = requests.get(url_txns)

    # if response.status_code != 200:
    #     print("json error")
    #     break

    address_content = response.json()
    result = address_content.get("result")

    return result

def is_new_txn(new_txn, last_txn):
    return new_txn == last_txn

def scrape_etherscan(wallet_address, last_txn):
    

    etherscan_url = "https://etherscan.io/address/" + wallet_address
    etherscan_req = Request(etherscan_url, headers={'User-Agent': 'Chrome/96.0.4664.110'}) 

    etherscan_response = urlopen(etherscan_req, timeout=1).read()             
    etherscan_response_close = urlopen(etherscan_req, timeout=1).close()      

    etherscan_soup = BeautifulSoup(etherscan_response, "html.parser")

    txn_table = etherscan_soup.find("table", attrs={"class": "table table-hover"})
    txn_table_data = txn_table.find_all("tr")

    last_txn_url = 'https://etherscan.io/tx/' + last_txn

    methods = []
    for span in etherscan_soup.find_all('span', attrs={'class':'u-label u-label--xs u-label--info rounded text-dark text-center'}):
        methods.append(span.text)
    
    last_method = methods[0]
    print(last_method)

    last_txn_req = Request(last_txn_url, headers={'User-Agent': 'Chrome/96.0.4664.110'})

    last_txn_response = urlopen(last_txn_req, timeout=1).read()
    last_txn_response_close = urlopen(last_txn_req, timeout=1).close()

    last_txn_soup = BeautifulSoup(last_txn_response, "html.parser")

    return last_txn_soup, last_method

def get_txn_status(last_txn_soup):
    for data in last_txn_soup.find_all('div', attrs={'class': 'col col-md-9'}):
        status = data.text
    
    return status

def send_final_result(last_method, last_txn_soup, current_time, wallet_address):
    print("Status of txn is 'Success'")

    # Transfer
    if last_method == "Transfer":
        print("TRANSFER BETWEEN TWO WALLETS")

    # Claim
    elif last_method == "Claim":
        
        media_bodies = []
        for ye in last_txn_soup.find_all('div', attrs={'class': 'media-body'}):
            media_bodies.append(ye)

        txn_action = media_bodies[0]
        
        print("CLAIM TOKENS")
        ca_html_claim = (txn_action.find('a', href = True))
        ca_html_claim = str(ca_html_claim.get('href'))
        ca_claim = ca_html_claim[7:49]
        
        telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + wallet_address + "\n" + "\U0001F4B0 Claimed \U0001F4B0 \n" + "*Token:* " + ca_claim)

    # Approve
    elif last_method == "Approve":
        media_bodies = []
        for ye in last_txn_soup.find_all('div', attrs={'class': 'media-body'}):
            media_bodies.append(ye)

        txn_action = media_bodies[0]

        print("APPROVED TOKENS")
        ca_html_approve = (txn_action.find('a', href = True))
        ca_html_approve = str(ca_html_approve.get('href'))
        ca_approve = ca_html_approve[7:]

        telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + wallet_address + "\n" + "\U00002705 Approved \U00002705 \n" + "*Token:* " + ca_approve)

    # swap
    elif last_method == "Multicall" or last_method == "Swap Exact Token":
        media_bodies = []
        for ye in last_txn_soup.find_all('div', attrs={'class': 'media-body'}):
            media_bodies.append(ye)

        txn_action = media_bodies[0]

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

                ca_link = ca_links2[-1][7:]   
            
            telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + wallet_address + "\n" + "\U0001F4EC TRADED WITH \U0001F4EC \n" + "*Token:* \n" + ca_link)

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
                telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + wallet_address + "\n" + "\U0001F4EC Swapped - BUY \U0001F4EC \n" + "*Token:* \n" + words[0] + " " + words[1] + "\nFor " + words[2] + " " + ca_swap)
            elif words[2] == 'Ether':
                print("SWAPPED - SELL")
                telegram_bot_sendtext(current_time + "\n\n" + "*Wallet:* " + wallet_address + "\n" + "\U0001F4EC Swapped - SELL \U0001F4EC \n" + "*Token:* \n" + words[0] + " " + ca_swap + "\nFor " + words[1] + " " + words[2])
    # Unknown txn
    else:
        print("UNKNOWN TRANSACTION TYPE")
