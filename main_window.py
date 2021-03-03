import tkinter as tk
import sniffer
import bot
import event
import messages
import hunt
import tkinter.scrolledtext as tkscrolled
import threading

win = tk.Tk()
win.title('Bot haha')

current_pos_label = tk.Label(win, text=str(bot.map_pos))
current_pos_label.pack()


def update_map(msg):
    current_pos_label['text'] = "Map {}".format(str(bot.map_pos))
def loop_hunt():
    while True:
        hunt.go_to_next_step()

th = threading.Thread(target=loop_hunt)
def start():
    th.start()


button = tk.Button(win, text='Start', width=25, command=start)
button.pack()

logTextWidget = tkscrolled.ScrolledText(win)
logTextWidget.pack(expand=True, fill='both')

def update_log(text):
    logTextWidget.insert(tk.INSERT, "{}\n".format(text))


event.on(messages.MapComplementaryInformationsDataMessage, update_map)
event.on('Log', update_log)

win.mainloop()
