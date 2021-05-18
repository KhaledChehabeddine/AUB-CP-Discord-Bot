import json
from cDatabase.KV_Database import KV_Database

config = json.load(open('config.json', 'r'))

class DB_Session(KV_Database):
    """[summary]

    Args:
        KV_Database ([type]): [description]
    """
    def __init__(self, path): 
        """[summary]

        Args:
            path ([type]): [description]
        """
        super().__init__(path)

    def create(self, session):
        """[summary]

        Args:
            session ([type]): [description]

        Returns:
            [type]: [description]
        """
        session_id = max(list(self.db.keys()) + [0]) + 1
        self.db[session_id] = {
            'date': str(session._date), 
            'duration': session.duration,
            'topic': session.topic,
            'host': session.host,
            'desc': session.desc,
        }
        self.save()
        return session_id

    def delete(self, session):
        """[summary]

        Args:
            session ([type]): [description]

        Returns:
            [type]: [description]
        """
        del(self.db[session._id])
        self.save()
        return True

    def change(self, session1, session2):
        """[summary]

        Args:
            session1 ([type]): [description]
            session2 ([type]): [description]
        """
        info = self.get(self._id)
        session1._date = session2._date
        session1.duration = session2.duration
        session1.topic = session2.topic
        session1.desc = session2.desc
        session1.host = session2.host