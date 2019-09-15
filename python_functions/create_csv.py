# from firebase import firebase
import pandas as pd
import os

classes = ["Neutral", "Positive", "Negative"]

df = pd.read_csv("test.csv", sep=",")
df.drop(df.columns.difference(['sentiment','text']), 1, inplace=True)

csv = df.to_csv(index=False)

with open("clean.csv", "w") as f:
	f.write(csv)




