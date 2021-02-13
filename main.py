import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime
import re
import matplotlib.pyplot as plt

load_dotenv()

# Setting up environment variable from your twitter account
api_key = os.getenv('api_key')
api_key_secret = os.getenv('api_key_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print("Performing...")

# Getting date of the day to perform search
date_since = datetime.today().strftime('%Y-%m-%d')

# Filter to get ride of retweets
query = 'CVE -filter:retweets'

cve_counts = dict()

# Finding each tweet in english to avoid some bad one
for tweet in tweepy.Cursor(api.search, lang='en', q=query, since=date_since, tweet_mode="extended").items(100):
    print("TWEET FETCHED FROM USER ", tweet.user.name, "\nValue : \n", tweet.full_text, "\n\n")
    pattern = "(?i)(CVE-(1999|2\d{3})-(\d{3,}))"
    x = re.search(pattern, tweet.full_text)
    print(x, "\n\n\n")
    if x:
        value = x.group(0)
        if value:
            if value in cve_counts:
                cve_counts[value] += 1
            else:
                cve_counts[value] = 1

print("CVE count : ", cve_counts)

# Creating graph

# Converting dictionary to list

# x axis values
x = list(cve_counts.keys())

# y axis value
y = list(cve_counts.values())

# Plotting the points
plt.plot(x, y)

# Naming x and y axis
plt.xlabel('CVE')
plt.ylabel('Today occurrences')

# Title to graph
plt.title('Occurrences of CVE on Twitter today')

# show the plot
plt.show()
