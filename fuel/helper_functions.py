import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException as WebDriverException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException

from . import driver


def getMsgMetaInfo(webdriver_element):
    """
    Returns webdriver_element's sender and message text.
    Message Text is a blank string, if it is a non-text message
    TODO: Identify msg type and print accordingly
    """
    # check for non-text message
    try:
        msg = webdriver_element.find_element(
            By.XPATH, './/div[contains(@class, "copyable-text")]')
        msg_sender = msg.get_attribute('data-pre-plain-text')
        msg_text = msg.find_elements(
            By.XPATH, './/span[contains(@class, "selectable-text")]')[-1].text
    except IndexError:
        msg_text = ""
    except Exception:
        msg_sender = ""
        msg_text = ""

    return msg_sender, msg_text


"""
Simple Commands
"""


def say_hi():
    print("Saying hi")
    return "Hello i am the intelli bot developed by the good young team at Intelli-Africa"


"""
Helper Methods
"""

def get_unread():
    chats = driver.find_elements_by_class_name("_2EXPL")
    return chats

def get_last_message():
    text_bubbles = driver.find_elements_by_class_name(
        "vW7d1")  # message-in = receiver, message-out = sender
    # print(text_bubbles)
    return text_bubbles[-1]


def chat_history():
    text_bubbles = driver.find_elements_by_class_name(
        "message-in")  # message-in = receiver, message-out = sender
    # print(text_bubbles)
    tmp_queue = []

    try:
        for bubble in text_bubbles:
            msg_texts = bubble.find_elements_by_class_name("copyable-text")
            for msg in msg_texts:
                #raw_msg_text = msg.find_element_by_class_name("selectable-text.invisible-space.copyable-text").text.lower()
                # raw_msg_time = msg.find_element_by_class_name("bubble-text-meta").text        # time message sent
                tmp_queue.append(msg.text.lower())

        if len(tmp_queue) > 0:
            test = driver.find_element(By.XPATH, './/span[contains(@class, "_2_LEW")]')
            loc = test.get_attribute('title')
            if "Location" in loc:
                return "location"
            else:
                return tmp_queue[-1]  # Send last message in list

    except StaleElementReferenceException as e:
        print(str(e))
        # Something went wrong, either keep polling until it comes back or figure out alternative

    return False


def send_message(msg):
    # a = "Choose any one of the below options: \n1.See my account balance\n2.See my recent transactions\n3.Make a payment\n4.Buy data\n6.Pay biller"
    # input_box = driver.find_element_by_class_name('_2S1VP')

    # select correct input box to type msg
    input_box = driver.find_element(
        By.XPATH, '//*[@id="main"]//footer//div[contains(@contenteditable, "true")]')
    # input_box.clear()
    input_box.click()

    # print(msg)

    # print(type(msg))

    if '\n' in msg:
        msgresult = msg.splitlines()
        # logging.warning("-------------------------------------{}------------------------".format(msgresult))

        for n in msgresult:
            # print(n)
            action = ActionChains(driver)
            action.send_keys(n)
            action.send_keys(Keys.SHIFT).send_keys(
                Keys.ENTER).send_keys(Keys.SHIFT)
            # action.send_keys(Keys.RETURN)
            action.perform()
        action.send_keys(Keys.ENTER)
        action.perform()
    else:
        action = ActionChains(driver)
        action.send_keys(msg)
        action.send_keys(Keys.ENTER)
        action.perform()

# Get all the contacts


def whatsapp_contacts():
    contacts = driver.find_elements_by_class_name("chat-title")

    return [contact.text for contact in contacts]


def is_action_message(last_msg):
    if last_msg[0] == "/":
        return True

    time.sleep(0.1)
    return False
