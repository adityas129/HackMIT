import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("minerva-7ae74-firebase-adminsdk-judw4-1dad1c53d1.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://minerva-7ae74.firebaseio.com/'})
client = firestore.client()

labels = ["Neutral", "Positive", "Negative"]
df = pd.read_csv("clean.csv")
data = df["text"].tolist()

for tweet in data[:30]:
	big_dict = {}
	big_dict["data"] = tweet
	big_dict["label_distribution"] = {}

	for label in labels:
		big_dict["label_distribution"][label] = 0

	big_dict["is_labeled"] = False
	big_dict["predicted_label"] = None
	big_dict["user_labels"] = None
	client.collection("data1").add(big_dict)


# label_to_number = {label: i for i, label in enumerate(labels, 0)}
# number_to_label = {str(v): k for k,v in label_to_number.items()}

# # print(number_to_label)

# client.collection("meta_data1").document("s2i").set(label_to_number)
# client.collection("meta_data1").document("i2s").set(number_to_label)

