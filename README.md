# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

# Team Name: Model Behavior
Team Members: Gautam Putcha, Ashna Anil, Kunal Samant, Parth Maheshkumar Patel


We will be building a search engine that ranks events/activities in your location based on events on websites such as Eventbrite, tweets or Facebook events based on a combination of user preferences/history. This is a text retrieval and ranking task after parsing information from different sources. This uses content based filtering while ranking the events to match the users preferences. 

We found this to be an important and interesting task and in today's world there are a lot of events occurring and it is hard to keep track or try to find the right events on social media. Searching on any one source alone typically does not allow users to find the events they are looking for. This search engine will combine and rank the data and make it easier for users to find all of the events they are interested in from a single source of truth.

Our approach is to pull data from a variety of sources containing data about events near any given user’s location. This would include Eventbrite, AllEvents.in, Facebook events, and even tweets related to nearby events. We would be using BM25 or similar ranking systems from the Metapy Library that we have used during the 410 Coursework.

Our expected outcome is to develop a centralized system for finding events in a users area by searching for relevant events from several sources of data. We expect to have a well-functioning frontend to accompany our text retrieval and ranking system. We hope to leverage the text retrieval techniques learnt in this course to optimize our ranking process and find the most relevant results for users.

We will get user feedback through relevant or not relevant ratings and improve on our performance with higher success rates. Lastly, we intend to use Python for the Backend and React/Flask for the Frontend of the project.

# Software Documentation

# 1. Functional Overview
The basic idea of the application we have built is to accept a query from the user and return a ranked list of the most relevant events in a given city. The user can choose from a drop-down menu of cities where events are taking place. A user's workflow on our application would look as follows:
1. Open the event ranking engine application.
2. Type in a query for the events that the user desires to search for. Press "Enter". The ranked list of results is shown.
3. The user may optionally filter the results for the desired city/location. The ranked list is then updated to include only events in the user's desired city.

For any individual seeking a specific event or type of event near them, our application could be used to find a list of the most relevant events from multiple sources (i.e. Eventbrite and Twitter)

# 2. How the software is implemented
The functionality of our application is primarily implemented using the following files:
1. create_EventBrite_data.py
2. create_twitter_data.py
3. preprocess.py
4. streamlit_app_cs410.py

create_EventBrite_data.py contains a crawler implementation that is used to retrieve data from the eventbrite website and create a dataset. The "BeautifulSoup" library was used to scrape information about events from the website, and the collected data was saved in a csv file (EventBrite_data.csv)

preprocess.py is not run during the usage of our application. We created this file to process the raw data we gathered from both Eventbrite as well as Twitter. This file carries out the following tasks:
1. Replaces any of the "NaN" values in the dataset with empty strings.
2. For the "tags" field of our data (hashtags/eventbrite search tags) remove the square bracket and backslash characters.
3. Concatenate the two datasets from Twitter and Eventbrite.
4. Remove the punctuation in the words of the dataset.
5. Stores the cleaned up data into a new CSV file.

The streamlit_app_cs410.py file contains all of the functionality that runs when the user starts the application. In this file, we leverage the "Streamlit" framework to support our frontend. The connection between the streamlit frontend and our backend with the Event ranking engine is stored in this file as well. This file contains the following functions:
1. remove_punctuation(text): This function is used for the pre-processing of the query. Similar to the code in preprocess.py, it removes any punctuation from the query terms entered by the user.
2. tokenization(text): This function is used for the pre-processing of both the query as well as the event data. This takes in a string and splits it into single tokens/words. A list of all the tokens in the string is returned. This function leverages the string split() function.
3. remove_stopwords(text): This function is used for the pre-processing of both the query as well as the event data. This takes in a string and removes all of the stopwords such as "the", "and", etc. This is done by using the pre-defined list of stopwords provided by the nltk library in python.
4. preprocess(filepath): This function takes in the filepath of the output of the preprocess.py file and completes the remaining steps of preprocessing on the combined dataset. This includes utilizing the above functions to remove stopwords and tokenize the documents to formulate a final corpus to be used by our ranker. The function returns the preprocessed_corpus variable which provides a list of lists. Each list represents a document and contains the words in the document after pre-processing.
5. ranked_list(query, df, preprocessed_corpus): This is our ranking engine. This takes in the inputs of the user's query, the resultant csv of preprocess.py (after local pre-processing too) and the pre-processed corpus returned by the preprocess method above. A BM25 ranker is initialized using the rank_bm25 library. We initialize the Okapi BM25 ranker with the pre-processed corpus, and parameters k1 = 1.2, b = 0.5 and epsilon = 500. After initializing the ranker, the remove puncuation method, tokenization method, and remove stopwords method are used to preprocess the query entered by the user. We then use the get_scores method on the BM25 ranker to get the corresponding document scores and sort them. The final ranked list of events is returned.

The main code calls the preprocess and ranked_list functions. The ranked_list function is called every time a new query is entered by the user.

# 3. Documentation of the Sotware Usage
To run the application, the user must follow the following steps:
1. Ensure that all of the files in this repository are stored on a single folder locally.
2. Open up a terminal and perform the following commands:
```
pip install streamlit
pip install plotly
pip install rank-bm25
```
Also make sure that the python string library is available for use.

3. To start the application, enter the following into the terminal:
```
streamlit run streamlit_app_cs410.py
```
4. You should now see the following output on the terminal window:
```
	  You can now view your Streamlit app in your browser.
	
	  Local URL: http://localhost:8501
	  Network URL: http://xx.xxx.xx.xx:xxxx
```
5. Copy the "Local URL" and paste it into a browser.
6. This should launch the ranking application on your browser.
7. Now, the user may type in any query and press the "Enter" key to see the results of the relevant events.
8. Optionally, the user may choose a location filter using the provided drop-down menu to list only the events in a given city.
9. As new queries and entered or a new filter is applied, the results of the ranking engine will update and present themselves on the table shown below the search box UI.
