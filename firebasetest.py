import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("serviceAccountKey.json")


firebase_admin.initialize_app(cred)

db= firestore.client()
db.collection("Teacher").add({'Name':"James", "Number": "0901455687", 'Subject':"Math"})