import json
import re
from sklearn.model_selection import StratifiedShuffleSplit
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from gensim.utils import simple_preprocess
import spacy
nlp = spacy.load('en')


def get_data(client):

	data1 = client.collection("data1")
	docs = data1.where("is_labeled", "==", True).stream()

	big_data_dict = {}
	for doc in docs:
		data_dict = doc.to_dict()
		label_dist = data_dict["label_distribution"] 
		label_max = None
		freq = -1
		for k in label_dist.keys():
			if label_dist[k] > freq:
				freq = label_dist[k]
				label_max = k

		big_data_dict[data_dict["data"]] = label_max			


	#print(big_data_dict)
	return big_data_dict


def split_data(client, data, n=1):
	"""
	Specifications:
	    Splits data into n stratified samples (1 by default)
	
	Args:
	    client (TYPE): ...
	    data (dict): {data:label}
	    n (int, optional): number of splits
	
	Yields:
	    tuple of 2 dicts: train and test dictionary 
	"""

	
	data_points, labels = zip(*data.items())

	#Dict to enumerate labels
	enumeration = client.collection("meta_data1").document("s2i").get().to_dict()


	labels = [enumeration[label] for label in labels]
	sss = StratifiedShuffleSplit(n_splits=n, test_size=0.3, random_state=0)
	sss.get_n_splits(data_points, labels)

	for train_index, test_index in sss.split(data_points, labels):
		train_data = []
		train_labels = []
		test_data = []
		test_labels = []
	
		for x in train_index:
			train_data.append(data_points[x])
			train_labels.append(labels[x])

		for y in test_index:
			test_data.append(data_points[y])
			test_labels.append(labels[y])

		data_train = dict(zip(train_data, train_labels))
		data_test = dict(zip(test_data, test_labels))

		yield data_train, data_test


def append_file(filepath, line):
	"""
	Specifications:
	Adds single entry to file
	
	Args:
	    filepath (str): training file
	    train_line (TYPE): labelled data to add
	"""
	#TODO: add error checks to see if file was written to properly

	#if file exists and it has content, add a newline 
	if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
		with open(filepath, "a") as f:
			f.write("".join(("\n", line)))

	else:
		with open(filepath, "a") as f:
			f.write(line)



	return 

def create_file(data, filepath):
	"""
	Specifications:
		Creates training/testing file from Data from Firebase
	
	Args:
	    data (dict): dict of each label and majority label
	    labels (list): list of all labels
	    filepath (str): name of file to be created
	
	Returns:
	    str: filepath of training file created 
	"""
	
	for data_point in data:
		
		#Get label
		label = data[data_point]
		#Data points cannot have new lines for BlazingText input
		clean_data_point = re.sub(r'\n', " ", data_point)
		clean_data_point = lemmatizer(clean_data_point)
		clean_data_point = " ".join(simple_preprocess(clean_data_point, deacc=True, min_len=2, max_len=17))
		line = "__label__{0} {1}".format(str(label), clean_data_point)
		append_file(filepath, line)

	return filepath


# def enumerate_labels(all_labels):

# 	label_to_number = {label: i for i, label in enumerate(set(all_labels), 0)}
# 	#Save dictionary to resolve labels later on 
# 	with open(".resolve_labels.pickle", "wb") as f:
# 		pickle.dump(label_to_number, f, protocol=pickle.HIGHEST_PROTOCOL)

# 	return 

def lemmatizer(text):        
    sent = []
    doc = nlp(text)
    for word in doc:
        sent.append(word.lemma_)
    return " ".join(sent)

def run_all(client):
    """Specifications:
    Get all labeled docs and create train and test files from them. 
    Will throw an error if not enough labels in each class.
    """

    data = get_data(client)
    for train_data, test_data in split_data(client, data, 1):
	    train_file = create_file(train_data, "../sanjas/dummy.train")
	    test_file = create_file(test_data, "../sanjas/dummy.test")
	    print(train_file)
	    print(test_file)

    return train_file, test_file



if __name__ == "__main__":
	# labels = ["Positive", "Negative", "Neutral"]
	# enumerate_labels(labels)
	# data = {"cat": "Positive", "dog": "Neutral", "fish": "Negative", 
	# 	"moose": "Positive", "sanja": "Negative", "arjun": "Neutral",
	# 	"aditya": "Negative", "sanzeed": "Neutral", "arjunisa": "Positive"}

	# for x,y in split_data(data):
	# 	train_file = create_file(x, "train.txt")
	# 	test_file = create_file(y, "test.txt")
	# 	print("Training File:",train_file)
	# 	print("Testing File:",test_file)
	cred = credentials.Certificate("minerva-7ae74-firebase-adminsdk-judw4-1dad1c53d1.json")
	firebase_admin.initialize_app(cred, {'databaseURL': 'https://minerva-7ae74.firebaseio.com/'})
	client = firestore.client()

	run_all(client)





