from idlelib.debugobj import dispatch
#i think here in this case i donnot use the tools of telegram directly
import telegram
#telegram.ext is a submodule of telegram
from telegram.ext import Updater,MessageHandler,Filters
import configparser
#a python standard lib for log
import logging


def main():
    config=configparser.ConfigParser()
    config.read('config.ini')
#Updater : continuously fetch new updates from telegram and pass them on to Dispatcher class
#create an instance of Updater class
#use_context=True : my handler will recieve the Context object as a argument
    updater=Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']),use_context=True)
    dispatcher=updater.dispatcher
#config the format or others for the output log
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#Filters.text is a filter,~Filters.command is a deny filter to exclude commands text,
# here combine these 2 filters
#echo is a function we defined to deal with the messages
    echo_handler=MessageHandler(Filters.text & (~Filters.command),echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()


#define the function echo to process the updated messages
def echo(update,context):
    reply_message=update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id,text=reply_message)
    #context.bot.send_message(chat_id=update.effective_chat.id, text="hi~ i'm here.")

if __name__=='__main__':
    main()

