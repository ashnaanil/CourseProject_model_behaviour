import pandas as pd
import numpy as np
import urllib
import re
import warnings

chicago_tweets = pd.read_csv(r"C:\Ashna\OneDrive - Microsoft\MCS\TIS\Project\Data\tweets_chicago.csv")
seattle_tweets = pd.read_csv(r"C:\Ashna\OneDrive - Microsoft\MCS\TIS\Project\Data\tweets_seattle.csv")
champaign_tweets = pd.read_csv(r"C:\Ashna\OneDrive - Microsoft\MCS\TIS\Project\Data\tweets_champaign.csv")
arlington_tweets = pd.read_csv(r"C:\Ashna\OneDrive - Microsoft\MCS\TIS\Project\Data\tweets_arlington.csv")

def preprocess(data):
    data = data[["User","Tweet", "Location"]]
    
    data = data.rename({'Location':'city'}, axis=1)
    data["date"] = "N/A"
    data["time"] = "N/A"
    data["title"] = "N/A"
    data["venue"] = "N/A"
    data["user"] = "Twitter User @" + data["User"]
    data["URL"] = "N/A"
    data["tags"] = [[] for _ in range(data.shape[0])]

    for i in range(0,len(data)):
        tweet = data["Tweet"][i]
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet)
        for url in urls:
                try:
                    res = urllib.request.urlopen(url)
                    actual_url = res.geturl()
                    data["URL"][i] = actual_url  
                except:
                    continue
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    for i in range(0,len(data)):
        text = data["Tweet"][i]
        text = emoji_pattern.sub(r'', text) # no emoji
        text = text.lower() # make lowercase
        hashtags = re.findall(r"#(\w+)", text)
        data["tags"][i] = hashtags
        data["Tweet"][i] = text
        
    data = data.rename({'Tweet':'details'}, axis=1)
    data = data[['city', 'URL', 'title', 'date', 'time','venue','details','user','tags']]
    return data

arlington_tweets = arlington_tweets.head(200)
chicago_tweets = chicago_tweets.head(200)
seattle_tweets = seattle_tweets.head(200)

chicago_tweets["Location"] = "Chicago"
seattle_tweets["Location"] = "Seattle"
champaign_tweets["Location"] = "Champaign"
arlington_tweets["Location"] = "Arlington"

a = preprocess(chicago_tweets)
b = preprocess(seattle_tweets)
c = preprocess(champaign_tweets)
d = preprocess(arlington_tweets)

data = pd.concat([a,b,c,d])

# saving the dataframe
data.to_csv('twitter_data.csv')