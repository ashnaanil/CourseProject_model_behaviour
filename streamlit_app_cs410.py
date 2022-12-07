import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import nltk
from rank_bm25 import *
import string #library that contains punctuation


st.set_page_config(layout="wide")

def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

def tokenization(text):
    tokens = text.split()
    return tokens

def remove_stopwords(text):
    output= [i for i in text if i not in stopwords]
    return output

def preprocess(filepath):
    # Load combined dataset
           
    #applying function to the column
    combined_df['clean_doc_text']= combined_df['clean_doc_text'].apply(lambda x: tokenization(x))

    #applying the function
    combined_df['clean_doc_text']= combined_df['clean_doc_text'].apply(lambda x:remove_stopwords(x))
 
    preprocessed_corpus = combined_df["clean_doc_text"].tolist()

    return preprocessed_corpus


def ranked_list(query, df, preprocessed_corpus):
    bm25 = BM25Okapi(preprocessed_corpus,k1=1.2, b=0.5, epsilon=500 )
   
    # Preprocessing query
    punc_free_query = remove_punctuation(query)
    lower_query = punc_free_query.lower()
    tokenized_query = tokenization(lower_query)
    preprocessed_query = remove_stopwords(tokenized_query)
    # print(preprocessed_query)

    #getting scores for each document
    doc_scores = bm25.get_scores(preprocessed_query)

    df["doc_scores"] = doc_scores
    df = df.sort_values(by=['doc_scores'], ascending=False)

    return df


#main
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

filepath = "./combined_dataset.csv"
combined_df = pd.read_csv(filepath)
ranked_df = combined_df


preprocessed_corpus = preprocess(combined_df)


# -- Create three columns
col1, col2, col3 = st.columns([10, 25, 10])
# -- Put the image in the middle column
# - Commented out here so that the file will run without having the image downloaded
with col1:
    st.image("eventbrite.jpg", width=350)
# -- Put the title in the last column
with col2:
    st.title("Event Search Engine - CS 410 Final Project")
with col3:
    st.image("Twitter.jpg", width=350)
# -- Put the title in the last column

# -- Get the user input
query_col, city_col = st.columns([5, 5])

with city_col:
    city_choice = st.selectbox(
        "Which city are you looking at?",
        ("All", "champaign", "chicago", "seattle", "arlington"),
    )

with query_col:
    text_input = st.text_input(
        "Enter your query here 👇",
    )
    if text_input:
        st.write("You entered this query: ", text_input)
        #use ranker code to retrieve ranked list
        ranked_df =  ranked_list(text_input, combined_df, preprocessed_corpus)

    #st.subheader("Look at the below table for the results of your query:")


# -- Apply the continent filter
if city_choice != "All":
    ranked_df = ranked_df[ranked_df.city == city_choice]

ranked_table = st.container()
with ranked_table:
    st.title("Ranked List of Events:")
    table = go.Figure(data=go.Table(columnorder = [1,2,3,4,5], columnwidth = [50,40,40,50,40],
    header=dict(values=list(ranked_df[['title','time','venue','URL','user']].columns), height=60,
    font=dict(color='black'), fill_color='#546e9c', align='center',line_color='black',font_size = 30), 
    cells=dict(values=[ranked_df.title,ranked_df.time,ranked_df.venue,ranked_df.URL,ranked_df.user],
    font=dict(color='black'), fill_color = "#8ca5d1", align='left',line_color='black',font_size = 20)))
    
    table.update_layout(width=1800, height=800)
    st.write(table)







