"""# Loading the dataset"""

import pandas as pd
import numpy as np
import string #library that contains punctuation

EventBrite_df = pd.read_csv("EventBrite_data.csv", encoding='windows-1252')
Twitter_df = pd.read_csv("twitter_data.csv")

# Replace nan values by ""
EventBrite_df = EventBrite_df.replace(np.nan, "")
Twitter_df = Twitter_df.replace(np.nan, "")

# Creating a tags strings column -- if tags value is ["A", "B", "C"] -- creating a new column with value "A B C"

# Using apply function single column
def combine_tags(x):
  x = x.replace('[','')
  x = x.replace(']','')
  x = x.replace('\'','')
  x = x.split(',')
  
  combine_str = " ".join(x)
  
  return combine_str

EventBrite_df["tags_combined"] = EventBrite_df["tags"].apply(combine_tags)
Twitter_df["tags_combined"] = Twitter_df["tags"].apply(combine_tags)


EventBrite_df["Doc_text"] = EventBrite_df[["title", "details", "city", "venue", "tags_combined"]].apply(" ".join, axis=1)
Twitter_df["Doc_text"] = Twitter_df[["title", "details", "city", "venue", "tags_combined"]].apply(" ".join, axis=1)


# First concatenating both dataset to form single dataset
combined_df = pd.concat([EventBrite_df, Twitter_df], axis=0)
combined_df = combined_df.drop(columns=['Rank', 'Unnamed: 0'])

#Punctuation removal

#defining the function to remove punctuation
def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

#storing the puntuation free text
combined_df['clean_doc_text']= combined_df['Doc_text'].apply(lambda x:remove_punctuation(x))
combined_df['clean_doc_text']= combined_df['clean_doc_text'].apply(lambda x: x.lower())


combined_df.to_csv('combined_dataset.csv', index=False)