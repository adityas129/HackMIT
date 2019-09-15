import sagemaker
from sagemaker import get_execution_role
import json
import boto3
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

modified = 0
can_train = False
train_if_greater_than = 3

def run_sagemaker(client):

    assert can_train == True
    can_train = False
    modified = 0
    sess = sagemaker.Session()

    # role = get_execution_role()
    role = "arn:aws:iam::091903783005:role/sanjasage"
    print(role) # This is the role that SageMaker would use to leverage AWS resources (S3, CloudWatch) on your behalf

    bucket = "sanjasage-1"
    print(bucket)
    prefix = 'blazingtext/supervised' #Replace with the prefix under which you want to store the data if needed

    s3_output_location = 's3://{}/{}/output'.format(bucket, prefix)
    region_name = boto3.Session().region_name

    print("Here 0")

    container = sagemaker.amazon.amazon_estimator.get_image_uri(region_name, "blazingtext", "latest")
    print('Using SageMaker BlazingText container: {} ({})'.format(container, region_name))


    train_channel = prefix + '/train'
    validation_channel = prefix + '/validation'

    sess.upload_data(path='dummy.train', bucket=bucket, key_prefix=train_channel)
    sess.upload_data(path='dummy.test', bucket=bucket, key_prefix=validation_channel)

    s3_train_data = 's3://{}/{}'.format(bucket, train_channel)
    s3_validation_data = 's3://{}/{}'.format(bucket, validation_channel)


    train_data = sagemaker.session.s3_input(s3_train_data, distribution='FullyReplicated', 
                            content_type='text/plain', s3_data_type='S3Prefix')
    validation_data = sagemaker.session.s3_input(s3_validation_data, distribution='FullyReplicated', 
                                 content_type='text/plain', s3_data_type='S3Prefix')
    data_channels = {'train': train_data, 'validation': validation_data}
    print("HERE 0.5")

    bt_model = sagemaker.estimator.Estimator(container,
                                             role, 
                                             train_instance_count=1, 
                                             train_instance_type='ml.c4.4xlarge',
                                             train_volume_size = 30,
                                             train_max_run = 360000,
                                             input_mode= 'File',
                                             output_path=s3_output_location,
                                             sagemaker_session=sess)

    bt_model.set_hyperparameters(mode="supervised",
                                epochs=10,
                                min_count=2,
                                learning_rate=0.05,
                                vector_dim=10,
                                early_stopping=True,
                                patience=4,
                                min_epochs=5,
                                word_ngrams=2)


    bt_model.fit(inputs=data_channels, logs=True)

    print("here 1")
    text_classifier = bt_model.deploy(initial_instance_count = 1, instance_type = 'ml.m4.xlarge')

    sentences = ["I like everything",
                "Why are we like this"]

    payload = {"instances" : sentences,
               "configuration": {"k": 2}}

    response = text_classifier.predict(json.dumps(payload))

    predictions = json.loads(response.decode('utf-8'))
    print(json.dumps(predictions, indent=2))
    sess.delete_endpoint(text_classifier.endpoint)
    can_train = True
    print("DONE with sagemaker! ")


def get_unlabeled(client):
    collection = client.collection('data1')
    result_unlabeled = list(collection.get({"is_labeled":"false"}))
    print("Unlabeled: ", result_unlabeled)
    return result_unlabeled


def update_dataset(client):
    # TODO: Use Arjun's code
    pass  

def action_modified(client):
    modified += 1
    if modified >= train_if_greater_than and train == True:
        print("Will train! Modified is ", modified)
        update_dataset(client)
        run_sagemaker(client)



def listen_for_changes(client):
    collection = client.collection('data1')
    # Create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):

        for change in changes:
            if change.type.name == 'ADDED':
                print(u'New : {}'.format(change.document.id))
                print("collection has these elements: ", list(collection.get()))
            elif change.type.name == 'MODIFIED':
                print(u'Modified : {}'.format(change.document.id))
                action_modified(client)
                
            elif change.type.name == 'REMOVED':
                print(u'Removed : {}'.format(change.document.id))

    col_query = client.collection(u'data1')

    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

if __name__ == "__main__":

    cred = credentials.Certificate("minerva-7ae74-firebase-adminsdk-judw4-1dad1c53d1.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://minerva-7ae74.firebaseio.com/'})
    client = firestore.client()
    print("database work till here")
    listen_for_changes(client)
    while True:
        time.sleep(1)

