import pyautogui
import messages
import event
import tinydb

CHAT_COMMERCE = '5'
CHAT_RECRUTEMENT = '6'


CHANNEL = {
    CHAT_COMMERCE: '/b',
    CHAT_RECRUTEMENT: '/r'
}

db = tinydb.TinyDB('chat_data.json')


def general(text):
    pyautogui.press('space')
    pyautogui.write(text)
    pyautogui.press('enter')


def process_chat(msg):
    db.insert({
        'channel': msg['channel'],
        'content': msg['content'],
    })


event.on(messages.ChatServerMessage, process_chat)
