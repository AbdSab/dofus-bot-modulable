import labot.sniffer.network as sniffer
import event
import json
import traceback

def update(msg):
    try:
        msg_data = msg.json()
        event_name = msg_data['__type__']
        event.emit(event_name, msg_data)
        # with open('messages.txt', 'a') as out:
        #      out.write(json.dumps(msg_data) + "\n")
    except Exception as e:
        traceback.print_exc()
        #print(e)
        pass


sniffer.launch_in_thread(update)