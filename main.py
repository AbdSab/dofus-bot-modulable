import sniffer
import bot
import traject_parse
import event
import messages
import hunt
import chat
import threading
import combat
import pyautogui
import time

def fight():
    cac = combat.enemy_is_cac()
    if cac:
        pyautogui.press('2')
        bot.click_on_cell(cac)
        time.sleep(.3)
    else:
        combat.go_to_nearest_entity()
        time.sleep(.5)
    if combat.enemy_is_cac():
        pyautogui.press('2')
        bot.click_on_cell(cac)
        time.sleep(.3)
        pyautogui.press('2')
        bot.click_on_cell(cac)
        time.sleep(.3)
        pyautogui.press('3')
        bot.click_on_cell(cac)
        time.sleep(.3)
        pyautogui.press('3')
        bot.click_on_cell(cac)

combat.fight_script(fight)


# hunt.start()
while True:
    hunt.go_to_next_step()