from imports import *

def main():
    address_list = get_addresses()
    
    for wallet_address in address_list:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(current_time)

        wallet_result = get_wallet_data(wallet_address)

        txn_hashes, new_txn, last_txn = get_txns_and_last(wallet_result, wallet_address)

        if is_log_file(wallet_address):

            if is_new_txn(new_txn, last_txn):
                print("No new transactions have been made on wallet address: \n " + wallet_address)
                
            else:
                last_txn_soup, last_method = scrape_etherscan(wallet_address, last_txn)

                status = get_txn_status(last_txn_soup)

                if status == "Fail":
                    print("Status of txn is 'Fail'")
                else:
                    send_final_result(last_method, last_txn_soup, current_time, wallet_address)
        else:
            create_log_file(wallet_address, txn_hashes)

if __name__ == "__main__":
    schedule.every(300).seconds.do(main)

    while 1:
        schedule.run_pending()
        time.sleep(1)


