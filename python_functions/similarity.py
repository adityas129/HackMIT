import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import py_stringmatching as sm
from gensim.utils import simple_preprocess
import numpy as np

def get_all_docs(client):
	docs = client.collection("data1").stream()
	compare_list = []
	for doc in docs:
		doc_dict = doc.to_dict()
		# print(doc_dict)
		temp_tuple = (doc.id, doc_dict["data"])
		compare_list.append(temp_tuple)


	# print(compare_list)
	return compare_list

def get_similarity(s1, s2):
	#TODO add lematization/stemming and tokenization using (spaCy|nltk|gensim)
	oc = sm.OverlapCoefficient()
	list1 = simple_preprocess(s1, deacc=True, min_len=1, max_len=25)
	list2 = simple_preprocess(s2, deacc=True,min_len=1, max_len=25)
	# print(list1)
	# print(list2)
	return oc.get_raw_score(list1, list2)


def create_similar(compare_list, client):
	#TODO change to len
	for i in range(len(compare_list)):
		scores = [0] * len(compare_list)
		top_scores = {}
		for j in range(len(compare_list)):
			if j == i:
				scores[j] = 0
				continue

			similarity_score = get_similarity(compare_list[i][1], compare_list[j][1])
			scores[j] = similarity_score

		np_array = np.array(scores)
		ind = np.argpartition(np_array, -5)[-5:]
		for index in ind:
			doc_id = compare_list[index][0]
			top_scores[doc_id] = scores[index]
		

		client.collection("data1").document(compare_list[i][0]).update({"similar_docs": top_scores})

	return





if __name__ == "__main__":
	cred = credentials.Certificate("minerva-7ae74-firebase-adminsdk-judw4-1dad1c53d1.json")
	firebase_admin.initialize_app(cred, {'databaseURL': 'https://minerva-7ae74.firebaseio.com/'})
	client = firestore.client()

	compare_list = get_all_docs(client)
	create_similar(compare_list, client)


