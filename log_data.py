from imports import *

# function to fetch addresses from the config file
def get_addresses():

        address_list = []

        with open('config.txt') as file:
            for line in file:
                address_list.append(line.strip())

        return address_list

# does log file exist
def is_log_file(wallet_address):
    return os.path.isfile(wallet_address + 'log.txt')

# create log file
def create_log_file(wallet_address, txn_hashes):
    print("file does not exist, file created")
    f = open(wallet_address + 'log.txt','w')

    for i in range(len(txn_hashes)):
        f.writelines(str(txn_hashes[i]))
        f.write("\n")

    f.close()      

# get last txn
def get_txns_and_last(wallet_result, wallet_address):

    new_result = []
    for i in range(len(wallet_result)):
        new_result.append(wallet_result[i]['hash'])
    
    if os.path.isfile(wallet_address + 'log.txt'):
        print("File exists")

        with open(wallet_address + 'log.txt') as f:
            for line in f:
                pass
            last_txn = line.strip('\n')

        print("Last Txn: " + last_txn)

        f = open(wallet_address + 'log.txt','w')

        for i in range(len(new_result)):
            f.writelines(str(new_result[i]))
            f.write("\n")

        f.close()
    
    return new_result, new_result[-1], last_txn

