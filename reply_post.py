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
final_message = 'Hi there! This is the BetterNewsForToronto bot!\n\nI heard you guys don\'t like the Toronto Sun, so I\'m here to provide you some better options! Below are five related links that have nothing to do with the Toronto Sun! (Links are not guaranteed to be news articles...sorry!)'
subreddit = r.get_subreddit('pythonforengineers')
for submission in subreddit.get_new(limit=20):
    # print submission.title

    # If we haven't replied to this post before
    if submission.id not in posts_replied_to:

        # Do a case insensitive search
        if re.search("torontosun", submission.url, re.IGNORECASE):
            # Reply to the post   
            g = pygoogle(submission.title)
            g.pages = 5
            gDict = g.search()
            gTitles = gDict.keys()
            linkCount = 0;
            index = 0;
            excludeTorontoSun = 'torontosun'
            while (linkCount < 5):
                compURL = gDict[gTitles[index]]
                if excludeTorontoSun not in compURL:
                    final_message += '\n\n'+gTitles[index]+'\n'+gDict[gTitles[index]] 
                    linkCount+=1
                    index+=1
                else:
                    index+=1

            submission.add_comment(final_message)
            print "Bot replying to : ", submission.title

            # Store the current id into our list
            posts_replied_to.append(submission.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")