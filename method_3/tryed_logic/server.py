import logging
from datetime import timedelta

from flask import Response
from flask_sse import sse
from gevent.resolver.cares import channel

from method_1.server import app

NO_MESSAGE_TEXT = "No message yet !"


class SSEService:
    def __init__(self):
        self.users = []
        self.messageForMap = {}

    def add_user(self, name):
        if name not in self.users:
            print("enter into condition")
            self.users.append(name)
            print(f"self.user is {self.users}")
            messageForNewUser = []
            for u in self.users:
                messages = self.messageForMap.get(u)
                print(f"the message is {messages}")
                if messages:
                    print(f"the message for map is {self.messageForMap}")
                    self.messageForMap[u].append(Message(name, u, NO_MESSAGE_TEXT))
                    print(f"the message for map is {self.messageForMap}")
                    messageForNewUser.append(Message(u, name, NO_MESSAGE_TEXT))
                    print(f"the message for new user is {messageForNewUser}")
                else:
                    print(f"the else ohh message for map is {self.messageForMap}")
                    messageForNewUser.append(Message(name, u, NO_MESSAGE_TEXT))
            print(f"no va the message for map is {self.messageForMap}")
            self.messageForMap[name] = messageForNewUser
            print(f"the message for map is {self.messageForMap}")

    def send_user_message(self, message):
        if message.getFrom() in self.users and message.getTo() in self.users:
            messagesTo = self.messageForMap.get(message.getTo())
            messagesFrom = self.messageForMap.get(message.getFrom())

            # Remove "No message yet !" message for "from" user
            newMessagesTo = []
            for m in messagesTo:
                if m.getFrom() == message.getFrom() and m.getMessage() == NO_MESSAGE_TEXT:
                    continue
                if m.getFrom() == m.getTo() and m.getMessage() == NO_MESSAGE_TEXT:
                    continue
                newMessagesTo.append(m)

            # Remove "No message yet !" message for "to" user
            newMessagesFrom = []
            for m in messagesFrom:
                if m.getFrom() == message.getTo() and m.getMessage() == NO_MESSAGE_TEXT:
                    continue
                if m.getFrom() == m.getTo() and m.getMessage() == NO_MESSAGE_TEXT:
                    continue
                newMessagesFrom.append(m)

            self.messageForMap[message.getTo()] = []
            self.messageForMap[message.getFrom()] = []

            newMessagesTo.append(message)
            newMessagesFrom.append(message)

            self.messageForMap[message.getTo()].extend(newMessagesTo)
            self.messageForMap[message.getFrom()].extend(newMessagesFrom)

    @app.route('/user-list-event')
    def get_users(self, name):
        if name is not None and not name.isspace():
            return self.users.copy()
        else:
            return []

    @app.route('/last-message-event')
    def get_last_user_message(self, name):
        if name is not None and not name.isspace():
            messages = self.messageForMap.get(name)
            if messages:
                return messages[-1]
            else:
                return None
        else:
            return None

    @app.route('/all-message-event')
    def get_all_user_messages(self, name):
        if name is not None and not name.isspace():
            messages = self.messageForMap.get(name)
            if messages:
                return messages
            else:
                return []
        else:
            return []


class Message:
    def __init__(self, from_, to, message):
        self.from_ = from_
        self.to = to
        self.message = message

    def getFrom(self):
        return self.from_

    def getTo(self):
        return self.to

    def getMessage(self):
        return self.message
