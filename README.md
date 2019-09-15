# HackMIT


## Inspiration

With the ubiquitous and readily available ML/AI turnkey solutions, the major bottlenecks of data analytics lay in the consistency and validity of datasets. 
**This project aims to enable a labeller to be consistent with both his fellow labellers and his past self while seeing the live class distribution of the dataset.**

## What it does

The UI allows a user to annotate datapoints from a predefined list of labels while seeing the distribution of labels this particular datapoint has been previously assigned by another annotator. The project also leverages AWS' BlazingText service to suggest labels of incoming datapoints from models that are being retrained and redeployed as it collects more labelled information. Furthermore, the user will also see the top N similar data-points (using Overlap Coefficient Similarity) and their corresponding labels. 

In theory, this added information will motivate the annotator to remain consistent when labelling data points and also to be aware of the labels that other annotators have assigned to a datapoint.

## How we built it

The project utilises Google's Firestore realtime database with AWS Sagemaker to streamline the creation and deployment of text classification models.
For the front-end we used Express.js, Node.js and CanvasJS to create the dynamic graphs. For the backend we used Python, AWS Sagemaker, Google's Firestore and several NLP libraries such as SpaCy and Gensim. We leveraged the realtime functionality of Firestore to trigger functions (via listeners) in both the front-end and back-end. After K detected changes in the database, a new BlazingText model is trained, deployed and used for inference for the current unlabeled datapoints.

## Challenges we ran into

The initial set-up of SageMaker was a major timesink, the constant permission errors when trying to create instances and assign roles were very frustrating. Additionally, our limited knowledge of front-end tools made the process of creating dynamic content challenging and time-consuming.


## Accomplishments that we're proud of

We actually got the ML models to be deployed and predict our unlabelled data in a pretty timely fashion using a fixed number of triggers from Firebase.

## What we learned

Clear and effective communication is super important when designing the architecture of technical projects. There were numerous times where two team members were vouching for the same structure but the lack of clarity lead to an apparent disparity.
We also realized Firebase is pretty cool.

## What's next for LabelLearn
Creating more interactive UI, optimizing the performance, have more sophisticated text similarity measures. 

## What we learnt 

Clear and effective communication is super important when desgning the architecture of technical projects. There were numerous times where two team members were vouching for the same structure but the lack of clarity lead to an apparent disprarity.






