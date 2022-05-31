from imports import *

# function to send message to telegram bot
def telegram_bot_sendtext(bot_message):

    bot_token = ''
    bot_chatID = '1908664243'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()