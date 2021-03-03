from scapy.all import sniff
from scapy.all import Raw
from decoder import decoder
import event
import threading
import json
import traceback


def update(pkg):
    try:
        raw = bytes(pkg.getlayer(Raw))
        msg = decoder.readMsg(raw.hex(), False)
        event_name = msg['__type__']
        #print(event_name)
        with open('messages.txt', 'a') as out:
            out.write(json.dumps(msg) + "\n")
        event.emit(event_name, msg)
        #if not event_name == 'ChatServerMessage' and not event_name == 'ChatServerWithObjectMessage':
    except Exception as e:
        traceback.print_exc()
        #print(e)
        pass


def start():
    sniff(filter='tcp port 5555', lfilter=lambda p: p.haslayer(Raw), prn=update)


sniffer = threading.Thread(target=start)
sniffer.start()
