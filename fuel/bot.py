import os
import time
import requests
import logging
import csv

from time import sleep

from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from . import driver
from .helper_functions import send_message, chat_history, whatsapp_contacts, is_action_message, get_unread, get_last_message

def find_fuel(location, data):
    reader = csv.reader(open(data, 'r'))
    result = list()
    for data in reader:
        if location.lower() in data[0].lower():
            result.append(["Location: "+data[0] + " " + data[2] + "\n " + "Payment:" + data[3] + "\n " + "Fuel Type: " + data[4] + "\n" + "Queue: " + data[5]])

    return result


class BotConfig(object):
    last_msg = False
    last_msg_id = False

    command_history = []
    last_command = ""

    def __init__(self, contact_list):
        self.contacts = contact_list

    def get_contacts(self):
        return self.contacts

    def set_last_chat_message(self, msg, time_id):
        self.last_msg = msg
        self.last_msg_id = time_id

    def get_last_chat_message(self):
        return self.last_msg, self.last_msg_id

    def set_last_command(self, command):
        self.last_command = command
        self.command_history.append(command)

    def get_unread(self):
        script = open(
            "unread.js", "r").read()
        chats = driver.execute_script(script)
        return chats

    def get_last_msg(self):
        script = open(
            "last.js", "r").read()
        last_message = driver.execute_script(script)
        return last_message

    def get_command_history(self):
        return "You have asked the following commands: " + ", ".join(self.command_history)


class Bot(object):
    def __init__(self):
        print("hello m bout to intilise")
        self.config = BotConfig(contact_list=whatsapp_contacts())
        print("Bot config was success")
        self.init_bot()
        print("bot has been created with chat list {}".format(whatsapp_contacts()))

    def do_the_loop(self):
        chats = get_unread()
        for chat in chats:
            try:
                chat.click()
                print("---------i clicked----------")
                last_chat = get_last_message()
                if last_chat.find_elements_by_class_name("message-in"):
                    self.poll_chat()
                elif last_chat.find_elements_by_class_name("message-out"):
                    print("nove on")
                # self.poll_chat()
                # sleep(2)
                print("---------on to the next------")
            except Exception as e:
                self.do_the_loop()


    def init_bot(self):
        # sleep(10)
        while True:
            # self.poll_chat()
            try:
                self.do_the_loop()
            except Exception as e:
                self.do_the_loop()
            

    def poll_chat(self):
        last_msg = chat_history()

        if last_msg:
            time_id = time.strftime('%H-%M-%S', time.gmtime())
            if last_msg == "location":
                print("------------------location process starts-------------")
                try:
                    exp = driver.find_element(By.XPATH, './/div[contains(@class, "invisible-space")]')
                    location = exp.get_attribute('data-plain-text')
                    phone = driver.find_element(By.XPATH, '//*[@id="main"]/header//span[contains(@dir, "auto")]').text
                    send_message(send_location(location, phone))
                except NoSuchElementException as e:
                    logging.error(e)
            else:
                last_saved_msg, last_saved_msg_id = self.config.get_last_chat_message()
                if last_saved_msg != last_msg and last_saved_msg_id != time_id:
                    self.config.set_last_chat_message(
                        msg=last_msg, time_id=time_id)

                    logging.debug("------------------------------{}------------------------".format(
                        self.config.get_last_chat_message()))

                    # is_action = is_action_message(last_msg=last_msg)
                    # if is_action:
                    self.config.set_last_command(last_msg)
                    self.bot_options(action=last_msg, location="none")    
        # print(last_msg)

    def bot_options(self, action, location):
        simple_menu = {                                 # function requires no extra arguments
            # "code": say_hi,
            "help": self._help_commands,
            "all_commands": self.config.get_command_history,
        }
        simple_menu_keys = simple_menu.keys()
    
        try:
            print("-------------------Input Type-----------------------", type(action))
            print("-------------------Input Type-----------------------", action)
            phone = driver.find_element(By.XPATH, '//*[@id="main"]/header//span[contains(@dir, "auto")]').text
            print("-------------------before all we had {}-----------------------".format(action))

            command_args = [action]
            logging.debug("Command args: {cmd}".format(cmd=command_args))
            print("**************************{}************************".format(command_args))

            if command_args[0] == "pakaipa":
                message = """
<<<<<<< HEAD
                    Usatye! Intelli Africa Solutions has created me to help you find the closest fuel station to your current location over the weekend. 
                    Please TEXT your current neighbourhood or suburb and i will get back to you shortly....
=======
                    Usatye!

                    Intelli Africa Solutions has created me to help you find the closest fuel station to your current location over the weekend. 
                    
                    Please TEXT your current neighbourhood or surburb and i will get back to you shortly....
>>>>>>> 30f6a7c55d0368a8fc29df44f6099fc2bd442aaf
                    """
                send_message(message)

            elif command_args[0] in ["thank you", "maita basa", "tatenda", "siyabonga", "thanx", "thanks", "merci"]:
                message = "No problem, I hope I was useful. For all your software needs, kindly contact us at info@intelliafrica.solutions"
                send_message(message)

            else:
                print("i got in here")
                message = find_fuel(command_args[0], "data.csv")
                if len(message) == 0:
                    message = "Sorry i ddn't quite catch that, may you send me your current suburb or neighbourhood..."
                    send_message(message)
                else:
                    print("**********************************{}*************************".format(message))
                    for item in message:
                        message = item[0]
                        send_message(str(message))
                    send_message("Thank you for using our service. Contact Intelli Africa Solutions for your any software needs at www.intelliafricasolutions.com")

                   

                    # elif command_args[0] == "hi":
                    #     cur_phone = driver.find_element(By.XPATH, '//*[@id="main"]/header//span[contains(@dir, "auto")]').text
                    #     register = Registration(command=command_args[0])
                    #     decision, phone = register.extract_vars()

                    #     if decision == 'yes':
                    #         r = requests.get(url='http://localhost:5000/api/whatsapp_banking/is_account_linked?mobile_number={0}'.format(phone))
                    #         data = r.json()
                    #         send_message(data['message'])

                    # elif command_args[0] == "images":
                    #     query = "".join(command_args[1])
                    #     g_images = GoogleResults(images=True)
                    #     g_images.images(qry=query)
                    #     g_images.execute_search()

                    # elif command_args[0] == "maps":     # Anything to do with maps create the object
                    #     maps_parser = GoogleMapsParser(command=command_args[0])
                    #     origin, destination, mode = maps_parser.extract_vars()

                    #     if origin and destination and mode:
                    #         g_maps = GoogleResults(maps=True)
                    #         g_maps.maps(origin=origin, destination=destination, travel_mode=mode)
                    #         g_maps.execute_search()
                    #     else:
                    #         send_message("Google Maps search has been cancelled")

        except KeyError as e:
            print("Key Error Exception: {err}".format(err=str(e)))
            send_message(
                "Wrong command. Send me /help to see a list of valid commands")

    @staticmethod
    def _help_commands():
        print("Asking for help")
        return "Commands: /hi, /all_commands, /google {query}, /images {query}, /maps"
