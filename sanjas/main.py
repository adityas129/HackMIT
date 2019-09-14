import sagemaker
from sagemaker import get_execution_role
import json
import boto3
import time
time_now = time.clock()

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
text_classifier = bt_model.deploy(initial_instance_count = 1,instance_type = 'ml.m4.xlarge')

sentences = ["I like everything",
            "Why are we like this"]

payload = {"instances" : sentences,
           "configuration": {"k": 2}}

response = text_classifier.predict(json.dumps(payload))

predictions = json.loads(response.decode('utf-8'))
print(json.dumps(predictions, indent=2))
sess.delete_endpoint(text_classifier.endpoint)
time_end = time.clock()
print("DONE! Execution time: ", time_end-time_now)



