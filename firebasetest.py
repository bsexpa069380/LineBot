import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("serviceAccountKey.json")


firebase_admin.initialize_app(cred)

db= firestore.client()
# db.collection("Teacher").add({'Name':"James", "Number": "0901455687", 'Subject':["Math", "English", "Physic"],"Photo" : "https://i.imgur.com/CeoGOfQ.jpeg"})
# db.collection("Teacher").add({'Name':"Kevin", "Number": "0555432123", 'Subject':["Math", "English", "Physic"],"Photo" : "https://i.imgur.com/j59UPHV.jpeg"})
# db.collection("Teacher").add({'Name':"Sharon", "Number": "0907789878", 'Subject':["Math", "Chinese", "Chemistry"],"Photo" : "https://i.imgur.com/MZ04TkZ.png"})
# db.collection("Teacher").add({'Name':"Selina", "Number": "0966122345", 'Subject':["Programming", "English" ],"Photo" : "https://i.imgur.com/9ky5VEy.png"})

# print("Done")

Teachers = db.collection("Teacher").get()
SubjectSet =set()
for teacher in Teachers:
    teacher = teacher.to_dict()
    print(teacher)
    for sub in teacher["Subject"]:
        SubjectSet.add(sub)

Sublist = [subject for subject in SubjectSet]

print(Sublist)