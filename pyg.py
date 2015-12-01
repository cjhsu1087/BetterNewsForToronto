#!/usr/bin/python
import praw
import pdb
import re
import os
from config_bot import *
from pygoogle import pygoogle

# Check that the file that contains our username exists
if not os.path.isfile("config_bot.py"):
    print "You must create a config file with your username and password."
    print "Please see config_skel.py"
    exit(1)

# Create the Reddit instance
user_agent = ("BetterNewsForToronto 0.1")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)

# Get the top 5 values from our subreddit

whitelist = ['thestar', 'theglobeandmail', 'nationalpost', 'torontosun', 'macleans', 'metronews', 'nowtoronto', 'torontoist', 'blogto', 'cbc', '680news', 'citynews']
subreddit = r.get_subreddit('toronto')
for submission in subreddit.get_new(limit=5):
    # print submission.title
    print ('start submissions')
    # If we haven't replied to this post before
    if (submission.id not in posts_replied_to) and ('reddit' not in submission.url) and ('imgur' not in submission.url):
        print('gathered submission')
        # Reply to the post 
        final_message = 'Hi there! This is the BetterNewsForToronto bot!\n\nI\'m here to provide some information related to this post. Below are a few relevant links from other news sources. (Links are not guaranteed to be news articles...sorry! Bot results depend on the post\'s title.)' 
        g = pygoogle(submission.title)
        g.pages = 2
        gDict = g.search()
        gTitles = gDict.keys()
        linkCount = 0;
        index = 0;
        
        while (linkCount < 5):
            if (index >= len(gTitles)):
                break
            compURL = gDict[gTitles[index]]
            if (submission.url not in compURL) and ('reddit' not in compURL) and any(sub in compURL for sub in whitelist):
                final_message += '\n\n'+gTitles[index]+'\n'+gDict[gTitles[index]] 
                linkCount+=1
                index+=1
            else:
                index+=1
            

        
        print "Bot replying to : ", submission.title
        if (linkCount > 0):
            print (final_message)
        else:
            print ("no results found")


# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")