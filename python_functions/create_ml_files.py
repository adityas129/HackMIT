import json
import re
from sklearn.model_selection import StratifiedShuffleSplit
import pickle
import os



def split_data(data, n=1):
	"""
	Specifications:
	    Splits data into n stratified samples (1 by default)
	
	Args:
	    data (dict): {data:label}
	    n (int, optional): number of splits
	
	Yields:
	    tuple of 2 dicts: train and test dictionary 
	"""

	
	data_points, labels = zip(*data.items())
	label_to_number = {label: i for i, label in enumerate(set(labels), 0)}

	#Save dictionary to resolve labels later on 
	with open(".resolve_labels.pickle", "wb") as f:
		pickle.dump(label_to_number, f, protocol=pickle.HIGHEST_PROTOCOL)

	labels = [label_to_number[label] for label in labels]
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

		line = "__label__{0} {1}".format(str(label), clean_data_point)
		append_file(filepath, line)

	return filepath

if __name__ == "__main__":
	data = {"cat": "good", "dog": "bad", "fish": "good", "moose": "bad"}
	for x,y in split_data(data):
		train_file = create_file(x, "train.txt")
		test_file = create_file(y, "test.txt")
		print("Training File:",train_file)
		print("Testing File:",test_file)





