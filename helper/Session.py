import json
from helper.cTime import MyDate
from cDatabase.DB_Session import DB_Session

config = json.load(open('config.json', 'r'))
database_session = DB_Session("db_session")

class Session:
    _date = MyDate()
    _id, duration, topic, desc, host = int(), int(), str(), str(), str()

    def __init__(self, date, duration, topic, host, desc = "", _id = -1):
        if _id == -1:
            self._date = date
            self.duration = duration
            self.topic = topic
            self.host = host
            self.desc = desc
        else:
            self._id = _id
            self.fill_values()

    def create(self): database_session.create(self)

    def delete(self): database_session.delete(self)

    def change(self, session): database_session.change(self, session)

    def fill_values(self):
        info = database_session.get(self._id)
        self._date = info['date']
        self.duration = info['duration']
        self.topic = info['topic']
        self.host = info['host']
        self.desc = info['desc']

    def is_found(self): 
        for session in database_session.values():
            if (session.date == self.date 
                and session.duration == self.duration 
                and session.topic == self.topic
                and session.host == self.host
                and session.desc == self.desc
                and session._id == self._id): return True
        return False

    def __str__(self): return "ACM Session: " + self.topic + " | " + str(self.date)