import queue


class Messenger:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        print(F"the listeners is {self.listeners.__str__()}")
        self.listeners.append(q)
        print(F"the listeners is {self.listeners.__str__()}")
        return q

    def publish(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                print(F"the is is {i} and listeners is {self.listeners[i]}")
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]
