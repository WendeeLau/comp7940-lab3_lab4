#i think here in this case i donnot use the tools of telegram directly
#import telegram
from telegram import update, Update
#telegram.ext is a submodule of telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import configparser
#a python standard lib for log
import logging
import redis
#update chatbot with chatgpt api
from ChatGPT_HKBU import HKBU_ChatGPT

#global variable redis1
#redis client
#global redis1

def main():
    config=configparser.ConfigParser()
    config.read('config.ini')
#Updater : continuously fetch new updates from telegram and pass them on to Dispatcher class
#create an instance of Updater class
#use_context=True : my handler will recieve the Context object as a argument
    updater=Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']),use_context=True)
    dispatcher=updater.dispatcher

#a redis client
    global redis1
#create an instance of Redis
    redis1=redis.Redis(host=(config['REDIS']['HOST']),
                       password=(config['REDIS']['PASSWORD']),
                       port=(config['REDIS']['REDISPORT']),
                       decode_responses=(config['REDIS']['DECODE_RESPONSE']),
                       username=(config['REDIS']['USER_NAME']))

#config the format or others for the output log
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#diapater for echo function
#Filters.text is a filter,~Filters.command is a deny filter to exclude commands text,
# here combine these 2 filters
#echo is a callback function (i defined it) to deal with the messages
    #echo_handler=MessageHandler(Filters.text & (~Filters.command),echo)
    #dispatcher.add_handler(echo_handler)

#dispater for chatgpt
    global chatgpt
    chatgpt=HKBU_ChatGPT(config)
    chatgpt_handler=MessageHandler(Filters.text & (~Filters.command),equipped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

#add self-defined funcs as handlers to the dispatcher for handling cmd
    dispatcher.add_handler(CommandHandler("add",add_cmd))
    dispatcher.add_handler(CommandHandler("help",help_cmd))
    dispatcher.add_handler(CommandHandler("hello",hello_cmd))
    
#start my chatbot
#my chatbot periodically sends requests to the Telegram server to check for new messages
#getUpdates methods
    updater.start_polling()
#idle() enters an infinite loop,
#ensuring my chatbot remains active until manually terminated
    updater.idle()


#define the function echo to process the updated messages
def echo(update,context):
    reply_message=update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id,text=reply_message)

# no return value
#Send a message when the command /help is issue.
def help_cmd(update:Update,context:CallbackContext):
    logging.info("help_cmd")
    update.message.reply_text("Helping you.")


#no return value
#Send a message when the command /add is issue
def add_cmd(update:Update,context:CallbackContext):
    try:
        global redis1
        # memory the user's input keyword
        logging.info("add_cmd_keyword:"+context.args[0])
        # usr_msg local varieble in this func
        usr_msg = context.args[0]
        redis1.incr(usr_msg)
# get(usr_msg) may not need decode  because decode_responses=True
        #key in redis is the keywords input by usr
        #value is the frequency
        update.message.reply_text('You have said ' + usr_msg + ' for ' + redis1.get(usr_msg) + ' times.')
    except(IndexError,ValueError):
        update.message.reply_text('Usage: /add <keyword>')

#define /hello <name> , no return value
def hello_cmd(update:Update,context:CallbackContext):
    try:
        #here no need redis
        #memory the user's input name
        logging.info("hello_cmd_name:"+context.args[0])
        #usr_msg local varieble in this func
        usr_msg = context.args[0]
        update.message.reply_text('Good day , '+usr_msg+' !')
    except(IndexError,ValueError):
        update.message.reply_text('Usage: /hello <your name>')

#use ChatGPT API
def equipped_chatgpt(update,context):
    global chatgpt
    reply_message=chatgpt.submit(update.message.text)
    logging.info("Update:"+str(update))
    logging.info("context:"+str(context))
    context.bot.send_message(chat_id=update.effective_chat.id,text=reply_message)


if __name__=='__main__':
    main()

