import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from random import randrange

cred = credentials.Certificate("minerva-7ae74-firebase-adminsdk-judw4-1dad1c53d1.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://minerva-7ae74.firebaseio.com/'})
client = firestore.client()

enumeration = client.collection("meta_data1").document("s2i").get().to_dict()
users = ["Arjun", "Sanja", "Adi", "Sanzeed"]
labels = list(enumeration.keys())
num_labels = len(labels)

data1 = client.collection("data1")
docs = data1.where("is_labeled", "==", False).stream()
count = 0
for doc in docs:
	if count > 20:
		break
	count += 1
	doc_id = doc.id
	doc_dict = doc.to_dict()
	doc_dict["is_labeled"] = True
	label = labels[randrange(num_labels)]

	doc_dict["label_distribution"][label] += 1
	user = users[randrange(len(users))]
	doc_dict["user_labels"] = {}
	doc_dict["user_labels"][user] = label
	client.collection("data1").document(doc_id).set(doc_dict)







