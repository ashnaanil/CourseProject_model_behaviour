import numpy as np
import csv

class Event:

    def __init__(self, eventName, eventDate, eventTime, eventVenue, eventCity, eventDescription, eventTags, user, url):

        self.eventName = eventName
        self.eventDate = eventDate
        self.eventTime = eventTime
        self.eventVenue = eventVenue
        self.eventCity = eventCity
        self.eventDescription = eventDescription
        self.eventTags = eventTags
        self.user = user
        self.url = url
        self.id = ""

class EventCollection:
    
    def __init__(self, path):

        self.eventList = []
        self.path = path
    
    def readData(self):
        with open(self.path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.eventList.append(Event(row[2], row[3], row[4], row[5], row[0], row[6], row[8], row[7], row[1]))
    


'''
USAGE shown below
'''

# file_path = "Eventbrite_data.csv"
# collection = EventCollection(file_path)
# collection.readEventbriteData()
# print(collection.eventList[7].eventName)
# print(collection.eventList[7].eventDate)
# print(collection.eventList[7].eventDescription)