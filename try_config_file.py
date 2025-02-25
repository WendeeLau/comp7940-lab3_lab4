#configparser is a python standard module
import configparser
#create a ConfigParser object , config is an instance
config = configparser.ConfigParser()
config.read('config.ini')
print(config['TELEGRAM']['ACCESS_TOKEN'])
#here TELEGRAM is a section of config.ini,ACCESS_TOKEN is a key of that section

