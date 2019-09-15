# HackMIT


## Inspiration

With the ubiquitous and readily available ML/AI turnkey solutions, the major bottlenecks of data anlytics lay in the consistency and usability of datasets. This project aims to help a labeller to be consistent with both his fellow labellers and his past self while seeing the live class distribution of the dataset.


## What it does

The UI allows a user to annotate datapoints from a predefined list of labels while seeing the distribution of labels this particular datapoint has been previously assigned. The project also leverages AWS' BlazingText service to suggest labels of incoming datapoints from models that are being retrained and redeployed as it collects more labelled information. Furthermore, the user will also see the top N similar data-points (using Overlap Coefficient Similarity) and their corresponding labels. 

In theory, this added information will motivate the annotator to remain consistent when labelling data points and also to be aware of the labels that other annotators have assigned to a datapoint.


## How we built it 

The project utilises Google's Firestore realtime database with AWS Sagemaker to streamline the creation and deployment of text classification models.


## Challenges we faced

The initial set-up of SageMaker was a major timesink, the constant permission erros when trying to create instances and assign roles were very frustrating. The process of listening to changes in Firebase to trigger a streamlined process in SageMaker was also very intricate.

## Accomplishments that we're proud of

We actually got the ML models to be deployed and predict our unlaballed data in a pretty timely fashion using a fixed number of triggers from Firebase.


## What we learnt 

Clear and effective communication is super important when desgning the architecture of technical projects. There were numerous times where two team members were vouching for the same structure but the lack of clarity lead to an apparent disprarity.






