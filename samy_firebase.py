# samy_firebase.py

import os

import firebase_admin
from firebase_admin import auth as firebase_admin_auth
from firebase_admin import db as firebase_admin_db
from firebase_admin import _user_mgt as admin_user_mgt
from firebase_admin import credentials

home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '/home/harpangell/PycharmProjects/samy/')
credential_path = os.path.join(credential_dir, 'firebase-adminsdk.json')
FIREBASE_CRED = credentials.Certificate(credential_path)

mainApp = firebase_admin.initialize_app(FIREBASE_CRED, options={
    'databaseURL': 'https://samy-c1136.firebaseio.com'
})

admin_db = firebase_admin_db.reference('/', app=mainApp)
admin_auth = firebase_admin_auth