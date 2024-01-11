from google.cloud import firestore
import re
import time, datetime


class FaccialibroGcloud(object):
    def __init__(self):
        self.db = firestore.Client()
        self.counter = 0

    def get_hashtags(msg: str) -> list:
        return re.findall('(#\w+)', msg, re.DOTALL)

    def clean(self):
        msgs = self.db.collection('messages').get()
        hashes = self.db.collection('hashtags').get()

        for x in msgs:
            print(f"Cleaning: {x.id}")
            try:
                self.db.collection('messages').document(x.id).delete()
            except Exception as e:
                print(f"Error deleting document {x.id}: {e}")

        for x in hashes:
            print(f"Cleaning: {x.id}")
            try:
                self.db.collection('hashtags').document(x.id).delete()
            except Exception as e:
                print(f"Error deleting document {x.id}: {e}")

    def add_chirps(self, string):
        # timestamp = time.time()
        timestamp = datetime.datetime.now()
        messaggio = string
        # hashtags = self.get_hashtags(messaggio)
        hashtags = re.findall('(#\w+)', messaggio, re.DOTALL)
        print(timestamp)
        h = {
            'message': messaggio,
            'hashtags': hashtags,
            'timestamp': str(timestamp)
        }
        self.db.collection('messages').document(str(timestamp)).set(h)
        for hsh in hashtags:
            ref = self.db.collection('hashtags').document(hsh).get()
            if ref.exists:
                hash_ref = self.db.collection('hashtags').document(hsh)
                hash_ref.update({str(timestamp): timestamp})
            else:
                tmp = {
                    str(timestamp): str(timestamp)
                }
                self.db.collection('hashtags').document(hsh).set(tmp)
        x = {
            'message': messaggio,
            'hashtags': hashtags,
            'timestamp': str(timestamp),
            'id': self.counter
        }
        print(x)
        self.counter = self.counter + 1
        return x

    def get_chirps(self, ids):
        chirp = self.db.collection('messages').document(ids).get()

        if chirp.exists:
            h = {
                'id': str(chirp.get('timestamp')),
                'message': chirp.get('message'),
                'timestamp': chirp.get('timestamp')
            }
            return h
        else:
            return None

    def get_topics(self, topic):
        hash_ref = self.db.collection('hashtags').document(topic).get()
        lists = []
        messages = []
        if hash_ref.exists:
            data = hash_ref.to_dict()
            for key, value in data.items():
                print(f"{key}: {value}")
                lists.append(value)

            for x in lists:
                message_ref = self.db.collection('hashtags').document(x).get()
                messages.append(message_ref.get('message'))
            return messages
        else:
            return None
