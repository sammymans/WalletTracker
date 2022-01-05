# WalletTracker

## Overview

Wallet Tracker is a python application that is created to track the cryptocurrency wallets that primarily trade on the Ethereum blockchain network. Given an unlimited amount of wallet addresses, the program will send alerts as messages to a telegram bot. Alert messages are sent everytime a new transaction is evident from the provided wallet, updates are accurate to the minute to ensure precise tracking. Telegram messages will include several key metrics and details regarding the transaction: the receiving wallet address, token contract address associated with the transaction, and the number of tokens traded.

## Set-up

To start using Wallet Tracker, all you need to do is create a telgram account at https://telegram.org/

Once an account has been made, the user must add the telegram bot as a contact:

1. Click on Contacts

![image](https://user-images.githubusercontent.com/78626496/148142026-b125ff0a-939d-4ace-8afb-3022a51258fd.png)

2. Search for @alert_whale_bot

![image](https://user-images.githubusercontent.com/78626496/148142052-1cc7ad61-3c13-4a0a-9340-f36be23e1509.png)

3. Add as a contact and wait for messages!

## Screenshots + Demo

Wallet Tracker tracks 3 different transactions: token claims, token approvals, token trades

https://user-images.githubusercontent.com/78626496/148144402-18928895-edd9-45c9-8226-8555b454660c.MP4

###### Token Claim

Includes the date and time, the wallet that claimed, and the token that was claimed

![image](https://user-images.githubusercontent.com/78626496/148142252-78eb3657-dd16-48c0-9450-52df4711a2e3.png)

###### Token Approval

Includes the date and time, the wallet that claimed, and the token that was approved

![image](https://user-images.githubusercontent.com/78626496/148142269-9ba6105d-458e-4df4-bcd3-cc3ba9d238e5.png)

###### Token Trades

Can either be a BUY or a SELL: includes the date and time, wallet that traded, and the amount traded in ETH as well as in the token of interest

BUY:

![image](https://user-images.githubusercontent.com/78626496/148142319-ac9f667a-c436-4b62-acca-dd1853fd0411.png)

SELL:

![image](https://user-images.githubusercontent.com/78626496/148142302-e6d8681f-dc37-4a1b-84f4-4d5aa8a1e350.png)
