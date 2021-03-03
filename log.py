import event


def log(text):
    print(text)
    event.emit('Log', text)
