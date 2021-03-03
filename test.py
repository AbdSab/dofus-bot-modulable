import combat_utils
import pyautogui
import bot
import combat
import time

# def fight():
#     cac = combat.enemy_is_cac()
#     combat.go_to_nearest_entity()
#     if cac:
#         pyautogui.press('2')
#         pyautogui.click(bot.click_on_cell(cac))
#
#
# combat.fight_script(fight)


print(combat_utils.get_cac_cells(380))
