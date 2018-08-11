import uuid
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("aibs-e5783-firebase-adminsdk-n2422-86cbb19d43.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://aibs-e5783.firebaseio.com'
})


def add_log(username, business, log):
    data = db.reference('/'+username+'/'+business+'/logs').push()
    data.set(log)


def get_user(username):
    data = db.reference('/'+username)
    return data.get()
