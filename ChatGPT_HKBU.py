import configparser
#a lib for making HTTP requests
import requests

#define a class
class HKBU_ChatGPT():
    #initialize an instance and load my config file
    def __init__(self,config_='./config.ini'):
        #if config_ is a dir string ,firstly create ConfigParser instance then read the config file
        if type(config_) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        #if config_ is already an instance use it directly
        elif type(config_) == configparser.ConfigParser:
            self.config = config_

    def submit(self,message):
        basicurl=self.config['CHATGPT']['BASICURL']
        modelname=self.config['CHATGPT']['MODELNAME']
        apiversion=self.config['CHATGPT']['APIVERSION']
        #form the URL
        url=basicurl+"/deployments/"+modelname+"/chat/completions/?api-version="+apiversion
        headers={'Content-Type':'application/json',
                 'api-key':(self.config['CHATGPT']['ACCESS_TOKEN'])}
        #pass the user's message；payload（body）
        conversation = [{"role": "user", "content": message}]
        payload={'messages':conversation}
    #using POST HTTP method , pass parameters,send requests to api
        response=requests.post(url,json=payload,headers=headers)
        if response.status_code==200:
            data=response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:',response

if __name__ == '__main__':
    #an instance of HKBU_ChatGPT CLASS
    ChatGPT_test = HKBU_ChatGPT()
    try:
        #a loop pass the users input to chatgpt and print response
        while True:
            user_input = input("Typing to start your chat :\t")
            response = ChatGPT_test.submit(user_input)
            print(response)
    except KeyboardInterrupt :
            print("The user stops the program.")






