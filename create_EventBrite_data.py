
"""
# Crawler for fetching data from eventbrite Website and creating a dataset

https://www.eventbrite.com/
"""

from bs4 import BeautifulSoup
import requests

# Function to extract Event Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("h1", attrs={"class":'event-title'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Event Date
def get_date(soup):
  try:
    time_tag = soup.select_one("time")
    date_attr = time_tag.attrs
    date_string = date_attr["datetime"]
  except AttributeError:
    date_string = ""	

  return date_string


# Function to extract Event time
def get_time(soup):
  try:
    time_tag = soup.find("span", attrs={"class":'date-and-time__line-break'})
    time_attr = time_tag.string
    time_string = time_attr.strip()
  except AttributeError:
    time_string = ""	

  return time_string


# Function to extract Event location
def get_location(soup):
  try:
    location_tag = soup.select_one("section[aria-labelledby='location-heading'] p")
    location_string = location_tag.text

  except AttributeError:
    location_string = ""	

  return location_string


# Function to extract Event Info
def get_details(soup):
  try:
    info_tag = soup.select("div[class='eds-l-mar-bot-8 structured-content'] p")
    info_string = ""
    for p in info_tag:
      info_string = info_string + p.text + "\n"
    # info_string = info_tag

  except AttributeError:
    info_string = ""	

  return info_string


# Function to extract Event User (ie the event is posted by which user)
def get_user(soup):
  try:
    user_tag = soup.select_one("div[class='organizer-info__name'] a")
    user_string = user_tag.text

  except AttributeError:
    user_string = ""	

  return user_string

# Function to extract Event Tags
def get_tags(soup):
  try:
    tags_tag = soup.select("section[aria-labelledby='tags-heading'] a")
    
    tags_list = []
    for a in tags_tag:
      tags_list.append(a.text)

  except AttributeError:
    tags_list = []

  return tags_list

"""# Fetching links from the search result webpage


URL for Events in Champaign -- https://www.eventbrite.com/d/il--champaign/all-events/?page=1

URL for Events in Chicago -- https://www.eventbrite.com/d/il--chicago/all-events/?page=1

URL for Events in Seattle -- https://www.eventbrite.com/d/wa--seattle/all-events/?page=1

URL for Events in Arlington -- https://www.eventbrite.com/d/tx--arlington/all-events/?page=1



"""

import tqdm.notebook as tq
import pandas as pd

# Initialize dataframe
df_cols = ['city', 'URL', 'title' , 'date', 'time', 'venue', 'details', 'user', 'tags']

#with column names
df = pd.DataFrame(columns=df_cols)
# df.head()

#Initialize Location
locations = ["il--champaign", "il-chicago", "wa--seattle", "tx--arlington" ]

#Initialize Page no
pages = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

for location in tq.tqdm(locations):
  for page in tq.tqdm(pages):

    #Fetch all links on that page
    URL = "https://www.eventbrite.com/d/" + location + "/all-events/?page=" + page
    # print(URL)

    # HTTP Request
    webpage = requests.get(URL)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    links = soup.select("a[class='eds-event-card-content__action-link']")

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
      links_list.append(link['href'])

    links_list = list(set(links_list))
    # print(links_list)
    # print(len(links_list))

    #Fetch details for each link

    # Loop for extracting product details from each link 
    for link in tq.tqdm(links_list):

      new_webpage = requests.get(link)

      new_soup = BeautifulSoup(new_webpage.content, "lxml")

      # Function calls to fetch all necessary event information

      Event_URL = link
      Event_Title = get_title(new_soup)    
      Event_Date = get_date(new_soup)
      Event_Time = get_time(new_soup)
      Event_Location = get_location(new_soup)
      Event_Details = get_details(new_soup)
      Event_User = get_user(new_soup)
      Event_Tags = get_tags(new_soup)

      #add row to end of DataFrame

      city=""
      if(location == "il--champaign"):
        city = "champaign"
      elif(location == "il-chicago"):
        city = "chicago"
      elif(location == "wa--seattle"):
        city = "seattle"
      elif(location == "tx--arlington"):
        city = "arlington"
      df.loc[len(df.index)] = [city, Event_URL, Event_Title, Event_Date, Event_Time, Event_Location, Event_Details, Event_User, Event_Tags]

      # print()
      # print()

# df

# print(len(df))

df.to_csv('Eventbrite_data.csv', index=False)

